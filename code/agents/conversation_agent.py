import re


class ConversationAgent:

    def __init__(self):

        # -------------------------------
        # Object Keywords
        # -------------------------------

        self.objects = {

            "car": [

                "car","vehicle","automobile","sedan","suv","truck",
                "pickup","van","jeep","taxi",

                "bumper","hood","bonnet","boot","trunk",

                "door","windshield","windscreen","glass",

                "headlight","tail light","taillight",

                "mirror","side mirror",

                "fender","quarter panel",

                "wheel","tyre","tire",

                "rim","roof","grille"

            ],

            "laptop":[

                "laptop","notebook","computer","pc",

                "macbook","screen","display","lcd","led",

                "keyboard","key","keys",

                "trackpad","touchpad",

                "hinge","lid","corner",

                "usb","hdmi",

                "charging port",

                "speaker","camera",

                "webcam","body","base"

            ],

            "package":[

                "package","parcel","shipment","box",

                "carton","delivery","amazon",

                "flipkart","label",

                "barcode","seal",

                "tape","contents",

                "inside","item"

            ]

        }

        # -------------------------------
        # Damage Keywords
        # -------------------------------

        self.damage = {

            "dent":[
                "dent","dented","bent",
                "caved","indented"
            ],

            "scratch":[
                "scratch","scratched",
                "scrape","scraping",
                "scuff","scuffed"
            ],

            "crack":[
                "crack","cracked",
                "fracture","split"
            ],

            "glass_shatter":[
                "shattered",
                "smashed glass",
                "glass broken"
            ],

            "broken_part":[
                "broken","damaged",
                "destroyed","snapped",
                "detached"
            ],

            "missing_part":[
                "missing","lost",
                "removed","gone"
            ],

            "water_damage":[
                "water","wet",
                "rain","coffee",
                "tea","juice",
                "liquid"
            ],

            "stain":[
                "stain","dirty",
                "mud","oil",
                "grease","paint"
            ]

        }

        # -------------------------------
        # Severity
        # -------------------------------

        self.severity = {

            "high":[
                "major","severe",
                "huge","heavy",
                "badly","total loss",
                "completely"
            ],

            "medium":[
                "medium",
                "moderate"
            ],

            "low":[
                "small","minor",
                "little","tiny",
                "light"
            ]

        }

        # -------------------------------
        # Accident Types
        # -------------------------------

        self.accidents = {

            "collision":[
                "hit",
                "crash",
                "collision",
                "rear ended",
                "rear-ended",
                "accident"
            ],

            "fall":[
                "fell",
                "drop",
                "dropped",
                "fall"
            ],

            "shipping":[
                "delivery",
                "courier",
                "shipping"
            ],

            "weather":[
                "rain",
                "storm",
                "hail",
                "flood"
            ]

        }

    # -----------------------------------
    # Generic Keyword Finder
    # -----------------------------------

    def find_keyword(self, text, dictionary):

        for key, values in dictionary.items():

            for word in values:

                if word in text:

                    return key

        return "unknown"

    # -----------------------------------
    # Find Object Part
    # -----------------------------------

    def find_part(self, text):

        PARTS = [

            "front bumper",

            "rear bumper",

            "bumper",

            "hood",

            "bonnet",

            "door",

            "left door",

            "right door",

            "windshield",

            "glass",

            "headlight",

            "taillight",

            "mirror",

            "screen",

            "keyboard",

            "trackpad",

            "hinge",

            "corner",

            "lid",

            "port",

            "box",

            "seal",

            "label"

        ]

        found = []

        for part in PARTS:

            if part in text:

                found.append(part)

        if len(found)==0:

            return "unknown"

        return ",".join(found)

    # -----------------------------------
    # Time Extraction
    # -----------------------------------

    def extract_time(self,text):

        patterns=[

            r"today",

            r"yesterday",

            r"last night",

            r"this morning",

            r"\d+\s+days",

            r"\d+\s+weeks",

            r"\d+\s+months"

        ]

        result=[]

        for p in patterns:

            m=re.findall(p,text)

            result.extend(m)

        if result:

            return ",".join(result)

        return "unknown"

    # -----------------------------------
    # Intent
    # -----------------------------------

    def extract_intent(self,text):

        if any(x in text for x in [

            "claim",

            "insurance",

            "compensation",

            "approve",

            "reimburse"

        ]):

            return "insurance_claim"

        return "unknown"

    # -----------------------------------
    # Analyze
    # -----------------------------------

    def analyze(self,conversation):

        text=conversation.lower()

        claim_object=self.find_keyword(
            text,
            self.objects
        )

        issue=self.find_keyword(
            text,
            self.damage
        )

        severity=self.find_keyword(
            text,
            self.severity
        )

        accident=self.find_keyword(
            text,
            self.accidents
        )

        part=self.find_part(text)

        intent=self.extract_intent(text)

        incident_time=self.extract_time(text)

        confidence=0.50

        if claim_object!="unknown":
            confidence+=0.10

        if issue!="unknown":
            confidence+=0.10

        if part!="unknown":
            confidence+=0.10

        if accident!="unknown":
            confidence+=0.10

        if intent!="unknown":
            confidence+=0.10

        summary=f"""

Claim Object : {claim_object}

Issue : {issue}

Part : {part}

Severity Hint : {severity}

Accident : {accident}

Intent : {intent}

Incident Time : {incident_time}

Original Conversation :

{conversation}

"""

        return{

            "claim_object":claim_object,

            "issue_type":issue,

            "object_part":part,

            "severity_hint":severity,

            "accident_type":accident,

            "intent":intent,

            "incident_time":incident_time,

            "confidence":round(confidence,2),

            "summary":summary

        }