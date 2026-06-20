import os
import time
import traceback
from agents.loader import DataLoader
from agents.conversation_agent import ConversationAgent
from agents.vision_agent import VisionAgent
from agents.history_agent import HistoryAgent
from agents.evidence_agent import EvidenceAgent
from agents.decision_engine import DecisionEngine

from utils.image_validator import ImageValidator
from utils.csv_writer import CSVWriter

from config import OUTPUT_CSV, DATASET_DIR


def main():

    print("=" * 70)
    print("            AI DAMAGE CLAIM VERIFIER")
    print("=" * 70)

    # -------------------------------------
    # Load Dataset
    # -------------------------------------

    loader = DataLoader()
    loader.load_all()

    # -------------------------------------
    # Create Agents
    # -------------------------------------

    conversation_agent = ConversationAgent()
    vision = VisionAgent()
    history = HistoryAgent()
    evidence = EvidenceAgent()
    validator = ImageValidator()
    decision = DecisionEngine()

    writer = CSVWriter()

    print("\nStarting Claim Verification...\n")

    # -------------------------------------
    # Process Claims
    # -------------------------------------

    for index, row in loader.claims.iterrows():

        claim_start = time.time()

        print("\n" + "=" * 70)
        print(f"Processing Claim {index + 1}")
        print("=" * 70)

        try:

            user_id = row["user_id"]
            claim_object = row["claim_object"]
            conversation = row["user_claim"]

            image_paths = [
                str(DATASET_DIR / p.strip())
                for p in row["image_paths"].split(";")
            ]

            # -------------------------------------
            # Print Images
            # -------------------------------------

            print("\nIMAGE PATHS")

            for p in image_paths:
                print(p)
                print("Exists :", os.path.exists(p))

            # -------------------------------------
            # Conversation Agent
            # -------------------------------------

            conversation_result = conversation_agent.analyze(
                conversation
            )
            

            print("\nConversation Summary")

            print(conversation_result["summary"])

            # -------------------------------------
            # History
            # -------------------------------------

            history_result = history.analyze(user_id)

            # -------------------------------------
            # Image Validator
            # -------------------------------------

            image_result = validator.validate(image_paths)

            # -------------------------------------
            # Vision Agent
            # -------------------------------------

            if not image_result["valid_image"]:

                qwen_result = {

                    "visible_object": claim_object,

                    "damage_visible": False,

                    "issue_type": "unknown",

                    "object_part": "unknown",

                    "severity": "unknown",

                    "claim_status": "not_enough_information",

                    "image_quality": "poor",

                    "camera_angle": "wrong",

                    "object_visible": False,

                    "possible_editing": False,

                    "confidence": 0.0,

                    "reason": "Image validation failed."

                }

            else:

                try:

                    vision_result = vision.analyze(
                    conversation_result,
                    image_paths
                    )

                    qwen_result = vision_result
                except Exception as e:

                    print("Vision Agent Failed :", e)

                    qwen_result = {

                        "visible_object": claim_object,

                        "damage_visible": False,

                        "issue_type": "unknown",

                        "object_part": "unknown",

                        "severity": "unknown",

                        "claim_status": "not_enough_information",

                        "image_quality": "poor",

                        "camera_angle": "wrong",

                        "object_visible": False,

                        "possible_editing": False,

                        "confidence": 0.0,

                        "reason": "Vision model failed."

                    }

            # -------------------------------------
            # Safety Defaults
            # -------------------------------------

            defaults = {

                "issue_type": "unknown",

                "object_part": "unknown",

                "severity": "unknown",

                "claim_status": "not_enough_information",

                "confidence": 0.0,

                "reason": "No reason available."

            }

            for key, value in defaults.items():

                if key not in qwen_result or qwen_result[key] in [None, ""]:

                    qwen_result[key] = value

            # -------------------------------------
            # Evidence
            # -------------------------------------

            evidence_result = evidence.analyze(

                claim_object,

                qwen_result["object_part"]

            )

            # -------------------------------------
            # Decision
            # -------------------------------------

            decision_result = decision.decide(

                qwen_result,

                history_result,

                evidence_result,

                image_result

            )

            # -------------------------------------
            # Debug Output
            # -------------------------------------

            print("\nFINAL DECISION")

            print("Status      :", decision_result["claim_status"])
            print("Severity    :", decision_result["severity"])
            print("Confidence  :", decision_result["confidence"])
            print("Decision Score :", decision_result["decision_score"])
            print("Risk Score     :", history_result["risk_score"])
            print("Quality Score  :", image_result["quality_score"])
            print("Risk Flags  :", decision_result["risk_flags"])

            # -------------------------------------
            # Save CSV
            # -------------------------------------

            writer.add({

                "user_id":
                user_id,

                "image_paths":
                row["image_paths"],

                "user_claim":
                conversation,

                "claim_object":
                claim_object,

                "evidence_standard_met":
                evidence_result["evidence_standard_met"],

                "evidence_standard_met_reason":
                evidence_result["evidence_standard_met_reason"],

                "risk_flags":
                ";".join(decision_result["risk_flags"]),

                "issue_type":
                qwen_result["issue_type"],

                "object_part":
                qwen_result["object_part"],

                "claim_status":
                decision_result["claim_status"],

                "claim_status_justification":
                qwen_result["reason"],

                "supporting_image_ids":
                ";".join(image_result["usable_images"]),

                "valid_image":
                image_result["valid_image"],

                "severity":
                decision_result["severity"]

            })

            elapsed = round(
                time.time() - claim_start,
                2
            )

            print(f"\n✅ Claim {index + 1} Completed")
            print(f"Time Taken : {elapsed} sec")

        except Exception as e:

            print("\n❌ ERROR")

            print(e)

            traceback.print_exc()

            continue

    # -------------------------------------
    # Save Output
    # -------------------------------------

    writer.save(OUTPUT_CSV)

    print("\n" + "=" * 70)
    print("ALL CLAIMS COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()