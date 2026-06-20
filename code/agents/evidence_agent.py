import pandas as pd
from config import EVIDENCE_RULES_CSV


class EvidenceAgent:

    def __init__(self):
        self.rules = pd.read_csv(EVIDENCE_RULES_CSV)

        # Synonyms
        self.synonyms = {

            # ---------- Car ----------
            "door": "body panel",
            "door panel": "body panel",
            "hood": "body panel",
            "bonnet": "body panel",
            "trunk": "body panel",
            "boot": "body panel",
            "fender": "body panel",
            "quarter panel": "body panel",

            "front bumper": "bumper",
            "rear bumper": "bumper",
            "bumper": "bumper",

            "front glass": "glass",
            "rear glass": "glass",
            "windshield": "glass",
            "wind shield": "glass",
            "window": "glass",

            "headlight": "light",
            "left headlight": "light",
            "right headlight": "light",
            "taillight": "light",
            "tail light": "light",
            "left taillight": "light",
            "right taillight": "light",
            "fog light": "light",

            "mirror": "mirror",
            "side mirror": "mirror",
            "left mirror": "mirror",
            "right mirror": "mirror",
            "rear view mirror": "mirror",

            # ---------- Laptop ----------
            "screen": "screen",
            "display": "screen",

            "keyboard": "keyboard",
            "keys": "keyboard",

            "trackpad": "trackpad",
            "touchpad": "trackpad",

            "hinge": "hinge",
            "lid": "lid",
            "corner": "corner",
            "port": "port",
            "usb port": "port",
            "charging port": "port",
            "body": "body",
            "base": "body",

            # ---------- Package ----------
            "box": "package",
            "package": "package",
            "parcel": "package",
            "carton": "package",

            "seal": "seal",
            "tape": "seal",

            "label": "label",
            "shipping label": "label",

            "content": "contents",
            "contents": "contents",
            "item": "contents",
            "inside": "contents"
        }

    # -------------------------
    # Normalize Part Name
    # -------------------------

    def normalize(self, part):

        if part is None:
            return ""

        part = str(part).lower().strip()

        part = part.replace("_", " ")
        part = part.replace("-", " ")

        part = " ".join(part.split())

        return self.synonyms.get(part, part)

        # -------------------------
    # Evidence Analysis
    # -------------------------

    def analyze(self, claim_object, object_part):

        claim_object = str(claim_object).lower().strip()

        if pd.isna(object_part):
            object_part = ""

        # Multiple damaged parts
        parts = [

            self.normalize(x)

            for x in str(object_part).split(",")

            if x.strip()

        ]

        matched_rules = []

        rules = self.rules[

            self.rules["claim_object"]

            .str.lower()

            .isin(

                [

                    claim_object,

                    "all"

                ]

            )

        ]

        # -------------------------
        # Rule Matching
        # -------------------------

        for part in parts:

            for _, row in rules.iterrows():

                applies = self.normalize(

                    row["applies_to"]

                )

                if (

                    part == applies

                    or

                    part in applies

                    or

                    applies in part

                ):

                    matched_rules.append(

                        row["minimum_image_evidence"]

                    )

        # -------------------------
        # Return Matched Rule
        # -------------------------

        if len(matched_rules) > 0:

            return {

                "evidence_standard_met": True,

                "confidence": 1.0,

                "matched_parts": parts,

                "missing_parts": [],

                "evidence_standard_met_reason":

                "; ".join(

                    list(

                        set(

                            matched_rules

                        )

                    )

                )

            }

        # -------------------------
        # General Rule
        # -------------------------

        general = rules[

            rules["applies_to"]

            .str.lower()

            ==

            "general claim review"

        ]

        if len(general) > 0:

            return {

                "evidence_standard_met": True,

                "confidence": 0.60,

                "matched_parts": [],

                "missing_parts": parts,

                "evidence_standard_met_reason":

                general.iloc[0][

                    "minimum_image_evidence"

                ]

            }

        # -------------------------
        # No Rule
        # -------------------------

        return {

            "evidence_standard_met": False,

            "confidence": 0.0,

            "matched_parts": [],

            "missing_parts": parts,

            "evidence_standard_met_reason":

            "No matching evidence rule found."

        }