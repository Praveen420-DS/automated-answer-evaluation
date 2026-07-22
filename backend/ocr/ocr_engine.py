import cv2
import easyocr
import os

# Load EasyOCR model once
reader = easyocr.Reader(['en'], gpu=False)


class OCREngine:

    def __init__(self):
        pass

    # ============================
    # Image Preprocessing
    # ============================

    def preprocess(self, image_path):

        image = cv2.imread(image_path)

        if image is None:
            raise Exception("Image not found.")

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        _, threshold = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )

        processed_path = image_path.replace(".", "_processed.")

        cv2.imwrite(processed_path, threshold)

        return processed_path

    # ============================
    # OCR Extraction
    # ============================

    def extract_text(self, image_path):

        processed_image = self.preprocess(image_path)

        result = reader.readtext(processed_image)

        text = ""

        for item in result:
            text += item[1] + "\n"

        return text

    # ============================
    # Confidence Score
    # ============================

    def extract_with_confidence(self, image_path):

        processed_image = self.preprocess(image_path)

        result = reader.readtext(processed_image)

        words = []

        average = 0

        for item in result:

            words.append({

                "text": item[1],
                "confidence": round(item[2], 3)

            })

            average += item[2]

        if len(result) > 0:
            average /= len(result)

        return {

            "text": "\n".join([x["text"] for x in words]),

            "averageConfidence": round(
                average,
                3
            ),

            "words": words

        }


ocr_engine = OCREngine()