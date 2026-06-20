import json
import base64
import time

from openai import OpenAI


class VisionAgent:

    def __init__(self):

        self.client = OpenAI(
            base_url="http://127.0.0.1:1234/v1",
            api_key="lm-studio"
        )

        self.model = "qwen2.5-vl-3b-instruct"

        self.max_retries = 3

        self.max_tokens = 500

        self.temperature = 0

    # -------------------------------------------------------
    # Encode Image
    # -------------------------------------------------------

    def encode_image(self, image_path):

        with open(image_path, "rb") as image:

            return base64.b64encode(
                image.read()
            ).decode("utf-8")

    # -------------------------------------------------------
    # Prompt Builder
    # -------------------------------------------------------

    def build_prompt(self, conversation):

        summary = conversation["summary"]

        prompt = f"""
You are a Senior Insurance Claim Investigator.

Your task is to verify an insurance claim ONLY from the uploaded images.

The conversation below is ONLY background information.

Never trust the user's claim more than the uploaded evidence.

-------------------------------------------------------

Claim Summary

-------------------------------------------------------

{summary}

-------------------------------------------------------

Perform ALL of the following tasks.

1. Detect the object.

Allowed values

car

laptop

package

unknown

-------------------------------------------------------

2. Detect whether damage is visible.

Return

true

false

-------------------------------------------------------

3. Detect the damage type.

Allowed

dent

scratch

crack

glass_shatter

broken_part

missing_part

water_damage

torn_packaging

crushed_packaging

stain

none

unknown

-------------------------------------------------------

4. Detect ALL damaged parts.

Example

front_bumper

front_bumper,hood

screen,hinge

box,label

-------------------------------------------------------

5. Estimate severity.

none

low

medium

high

unknown

-------------------------------------------------------

6. Camera Angle

good

partial

wrong

-------------------------------------------------------

7. Image Quality

good

fair

poor

-------------------------------------------------------

8. Object Visible

true

false

-------------------------------------------------------

9. Possible Editing

true

false

-------------------------------------------------------

10. Supporting Images

Return image names.

Example

Image 1

Image 3

-------------------------------------------------------

11. Confidence

Return value between

0

and

1

-------------------------------------------------------

12. Final Decision

supported

contradicted

not_enough_information

-------------------------------------------------------

13. Reason

Maximum TWO short sentences.

-------------------------------------------------------

Return ONLY valid JSON.

Schema

{{
    "visible_object":"",

    "damage_visible":true,

    "issue_type":"",

    "object_part":"",

    "severity":"",

    "claim_status":"",

    "image_quality":"",

    "camera_angle":"",

    "object_visible":true,

    "possible_editing":false,

    "supporting_images":[],

    "confidence":0.95,

    "reason":""
}}

"""

        return prompt

    # -------------------------------------------------------
    # Build Content
    # -------------------------------------------------------

    def build_content(
        self,
        conversation,
        image_paths
    ):

        prompt = self.build_prompt(
            conversation
        )

        content = [

            {

                "type": "text",

                "text": prompt

            }

        ]

        for i, image in enumerate(image_paths):

            encoded = self.encode_image(image)

            content.append({

                "type": "text",

                "text": f"Image {i+1}"

            })

            content.append({

                "type": "image_url",

                "image_url": {

                    "url": f"data:image/jpeg;base64,{encoded}"

                }

            })

        return content
        # -------------------------------------------------------
    # Call Vision Model
    # -------------------------------------------------------

    def call_model(self, content):

        response = self.client.chat.completions.create(

            model=self.model,

            temperature=self.temperature,

            max_tokens=self.max_tokens,

            messages=[

                {

                    "role": "user",

                    "content": content

                }

            ]

        )

        if response.choices is None:

            raise Exception("No choices returned.")

        if len(response.choices) == 0:

            raise Exception("Empty response.")

        if response.choices[0].message is None:

            raise Exception("Message is empty.")

        text = response.choices[0].message.content

        if text is None:

            raise Exception("Vision model returned empty content.")

        return text


    # -------------------------------------------------------
    # Clean Response
    # -------------------------------------------------------

    def clean_response(self, response_text):

        response_text = response_text.replace(

            "```json",

            ""

        )

        response_text = response_text.replace(

            "```",

            ""

        )

        response_text = response_text.strip()

        return response_text


    # -------------------------------------------------------
    # Validate JSON
    # -------------------------------------------------------

    def validate_json(self, data):

        defaults = {

            "visible_object": "unknown",

            "damage_visible": False,

            "issue_type": "unknown",

            "object_part": "unknown",

            "severity": "unknown",

            "claim_status": "not_enough_information",

            "image_quality": "poor",

            "camera_angle": "wrong",

            "object_visible": False,

            "possible_editing": False,

            "supporting_images": [],

            "confidence": 0.0,

            "reason": "No explanation provided."

        }

        for key, value in defaults.items():

            if key not in data:

                data[key] = value

            elif data[key] is None:

                data[key] = value

            elif isinstance(data[key], str):

                if data[key].strip() == "":

                    data[key] = value

        try:

            data["confidence"] = float(

                data["confidence"]

            )

        except:

            data["confidence"] = 0.0

        if data["confidence"] < 0:

            data["confidence"] = 0.0

        if data["confidence"] > 1:

            data["confidence"] = 1.0

        return data


    # -------------------------------------------------------
    # Analyze
    # -------------------------------------------------------

    def analyze(self, conversation, image_paths):

        content = self.build_content(

            conversation,

            image_paths

        )

        last_error = None

        for attempt in range(

            self.max_retries

        ):

            try:

                response = self.call_model(

                    content

                )

                response = self.clean_response(

                    response

                )

                data = json.loads(

                    response

                )

                return self.validate_json(

                    data

                )

            except Exception as e:

                last_error = e

                print(

                    f"Vision Retry {attempt+1}/{self.max_retries}"

                )

                print(e)

                time.sleep(3)

        raise Exception(

            f"VisionAgent Failed : {last_error}"

        )