import cv2
import numpy as np
import os
import imagehash

from PIL import Image, ExifTags


class ImageValidator:

    def __init__(self):
        self.hashes = []

    # -------------------------
    # EXIF Metadata
    # -------------------------

    def get_exif(self, image_path):

        try:

            img = Image.open(image_path)
            exif = img.getexif()

            data = {}

            for tag_id, value in exif.items():

                tag = ExifTags.TAGS.get(tag_id, tag_id)
                data[tag] = value

            return data

        except:
            return {}

    # -------------------------
    # Screenshot Detection
    # -------------------------

    def is_screenshot(self, width, height):

        common = [

            (1080, 2400),
            (1080, 2340),
            (1170, 2532),
            (1125, 2436),
            (828, 1792),
            (1242, 2688),
            (750, 1334),
            (720, 1600),
            (1440, 3200)

        ]

        return (width, height) in common

    # -------------------------
    # Crop Detection
    # -------------------------

    def is_cropped(self, image):

        h, w = image.shape[:2]

        if h < 500 or w < 500:
            return True

        ratio = w / h

        if ratio < 0.4 or ratio > 3:
            return True

        return False

    # -------------------------
    # Duplicate Detection
    # -------------------------

    def duplicate(self, image_path):

        try:

            h = imagehash.phash(
                Image.open(image_path)
            )

        except Exception:

            return False

        for old in self.hashes:

            if h - old <= 3:
                return True

        self.hashes.append(h)

        return False

    
          
    # -------------------------
    # Blur Check
    # -------------------------

    def blur_check(self, gray):

        blur = cv2.Laplacian(
            gray,
            cv2.CV_64F
        ).var()

        if blur < 100:

            return False, blur

        return True, blur


    # -------------------------
    # Brightness Check
    # -------------------------

    def brightness_check(self, gray):

        brightness = np.mean(gray)

        if brightness < 50:

            return False, brightness

        if brightness > 230:

            return False, brightness

        return True, brightness


    # -------------------------
    # Metadata Check
    # -------------------------

    def metadata_check(self, image_path):

        exif = self.get_exif(image_path)

        software = str(
            exif.get(
                "Software",
                ""
            )
        ).lower()

        editors = [

            "photoshop",

            "canva",

            "gimp",

            "lightroom",

            "snapseed"

        ]

        if any(

            editor in software

            for editor in editors

        ):

            return False

        return True


    # -------------------------
    # Quality Score
    # -------------------------

    def quality_score(

        self,

        blur,

        brightness,

        cropped,

        duplicate,

        metadata

    ):

        score = 100

        if blur < 100:

            score -= 25

        if brightness < 50:

            score -= 20

        if brightness > 230:

            score -= 15

        if cropped:

            score -= 20

        if duplicate:

            score -= 20

        if not metadata:

            score -= 25

        return max(score, 0)
        



    # -------------------------
    # Main Validation
    # -------------------------

    def validate(self, image_paths):

        valid_image = True

        risk_flags = []

        usable_images = []

        total_score = 0

        for path in image_paths:

            image = cv2.imread(path)

            if image is None:

                valid_image = False
                risk_flags.append("invalid_image")

                continue

            h, w = image.shape[:2]

            gray = cv2.cvtColor(
                image,
                cv2.COLOR_BGR2GRAY
            )

            # -------------------------
            # Blur
            # -------------------------

            blur_ok, blur = self.blur_check(gray)

            if not blur_ok:

                risk_flags.append(
                    "blurry_image"
                )

            # -------------------------
            # Brightness
            # -------------------------

            brightness_ok, brightness = self.brightness_check(gray)

            if not brightness_ok:

                if brightness < 50:

                    risk_flags.append(
                        "low_light"
                    )

                else:

                    risk_flags.append(
                        "over_exposed"
                    )

            # -------------------------
            # Crop
            # -------------------------

            cropped = self.is_cropped(image)

            if cropped:

                risk_flags.append(
                    "cropped_or_obstructed"
                )

            # -------------------------
            # Screenshot
            # -------------------------

            if self.is_screenshot(w, h):

                risk_flags.append(
                    "non_original_image"
                )

            # -------------------------
            # Duplicate
            # -------------------------

            duplicate = self.duplicate(path)

            if duplicate:

                risk_flags.append(
                    "duplicate_image"
                )

            # -------------------------
            # Metadata
            # -------------------------

            metadata_ok = self.metadata_check(path)

            if not metadata_ok:

                risk_flags.append(
                    "possible_manipulation"
                )

            # -------------------------
            # Quality Score
            # -------------------------

            score = self.quality_score(

                blur,

                brightness,

                cropped,

                duplicate,

                metadata_ok

            )

            total_score += score

            usable_images.append(

                os.path.splitext(

                    os.path.basename(path)

                )[0]

            )

        # -------------------------
        # Remove Duplicates
        # -------------------------

        risk_flags = list(set(risk_flags))

        if len(risk_flags) == 0:

            risk_flags.append("none")

        # -------------------------
        # Average Quality
        # -------------------------

        if len(image_paths) > 0:

            quality_score = round(

                total_score / len(image_paths),

                2

            )

        else:

            quality_score = 0

        return {

            "valid_image": valid_image,

            "quality_score": quality_score,

            "risk_flags": risk_flags,

            "usable_images": usable_images

        }