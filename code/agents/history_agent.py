import pandas as pd
from config import USER_HISTORY_CSV


class HistoryAgent:

    def __init__(self):

        self.history = pd.read_csv(
            USER_HISTORY_CSV
        )

    # -------------------------
    # Get User
    # -------------------------

    def get_user(self, user_id):

        user = self.history[

            self.history["user_id"]

            ==

            user_id

        ]

        if user.empty:

            return None

        return user.iloc[0]

    # -------------------------
    # Risk Score
    # -------------------------

    def calculate_risk_score(self, user):

        score = 0

        claims = int(
            user["last_90_days_claim_count"]
        )

        if claims >= 5:

            score += 60

        elif claims >= 3:

            score += 35

        elif claims >= 1:

            score += 15

        history_flags = str(

            user["history_flags"]

        ).lower()

        if history_flags != "none":

            score += 30

        return min(score, 100)

    # -------------------------
    # Risk Level
    # -------------------------

    def risk_level(self, score):

        if score >= 70:

            return "high"

        elif score >= 40:

            return "medium"

        return "low"

    # -------------------------
    # Risk Flags
    # -------------------------

    def build_flags(self, user):

        flags = []

        claims = int(
            user["last_90_days_claim_count"]
        )

        if claims >= 5:

            flags.append(
                "frequent_claimant"
            )

        elif claims >= 3:

            flags.append(
                "multiple_recent_claims"
            )

        history_flags = str(

            user["history_flags"]

        ).lower()

        if history_flags != "none":

            flags.append(
                "user_history_risk"
            )

        if not flags:

            flags.append("none")

        return flags

    # -------------------------
    # Analyze
    # -------------------------

    def analyze(self, user_id):

        user = self.get_user(
            user_id
        )

        if user is None:

            return {

                "risk": "low",

                "risk_score": 0,

                "confidence": 0.5,

                "risk_flags": [

                    "none"

                ]

            }

        score = self.calculate_risk_score(
            user
        )

        risk = self.risk_level(
            score
        )

        flags = self.build_flags(
            user
        )

        confidence = round(

            min(

                1.0,

                0.5 + (score / 100)

            ),

            2

        )

        return {

            "risk": risk,

            "risk_score": score,

            "confidence": confidence,

            "risk_flags": flags

        }