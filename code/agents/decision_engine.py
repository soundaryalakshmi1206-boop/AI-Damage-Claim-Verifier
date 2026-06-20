class DecisionEngine:

    def decide(
        self,
        qwen_result,
        history_result,
        evidence_result,
        image_result
    ):

        # -------------------------
        # Safe Defaults
        # -------------------------

        confidence = float(
            qwen_result.get("confidence", 0.0)
        )

        severity = qwen_result.get(
            "severity",
            "unknown"
        )

        image_quality = qwen_result.get(
            "image_quality",
            "poor"
        )

        camera_angle = qwen_result.get(
            "camera_angle",
            "wrong"
        )

        object_visible = qwen_result.get(
            "object_visible",
            False
        )

        damage_visible = qwen_result.get(
            "damage_visible",
            False
        )

        possible_editing = qwen_result.get(
            "possible_editing",
            False
        )

        evidence_ok = evidence_result.get(
            "evidence_standard_met",
            False
        )

        valid_image = image_result.get(
            "valid_image",
            False
        )

        history_score = history_result.get(
            "risk_score",
            0
        )

        image_score = image_result.get(
            "quality_score",
            0
        )

        # -------------------------
        # Merge Risk Flags
        # -------------------------

        risk_flags = list(set(

            history_result.get("risk_flags", []) +

            image_result.get("risk_flags", [])

        ))

        # -------------------------
        # Weighted Score
        # -------------------------

        score = 0

        if valid_image:
            score += 20

        if evidence_ok:
            score += 20

        if object_visible:
            score += 15

        if damage_visible:
            score += 15

        if image_quality == "good":
            score += 10

        elif image_quality == "fair":
            score += 5

        if camera_angle == "good":
            score += 10

        elif camera_angle == "partial":
            score += 5

        score += confidence * 10

        score += image_score / 10

        # Penalize

        if possible_editing:
            score -= 40
            risk_flags.append(
                "possible_manipulation"
            )

        score -= history_score / 10

        score = max(0, min(score, 100))

        # -------------------------
        # Final Decision
        # -------------------------

        if score >= 75:

            claim_status = "supported"

        elif score >= 45:

            claim_status = "not_enough_information"

        else:

            claim_status = "contradicted"

        # -------------------------
        # Override
        # -------------------------

        if qwen_result.get("claim_status") == "contradicted":

            claim_status = "contradicted"

        if possible_editing:

            claim_status = "not_enough_information"

        risk_flags = list(set(risk_flags))

        if len(risk_flags) == 0:

            risk_flags.append("none")

        return {

            "claim_status": claim_status,

            "severity": severity,

            "confidence": confidence,

            "decision_score": round(score, 2),

            "risk_flags": risk_flags

        }