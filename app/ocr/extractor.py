from pathlib import Path

import cv2
import pytesseract


def preprocess_image(image_path: str):
    """
    Preprocess handwritten/code image for OCR.
    """

    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(
            f"Could not read image: {image_path}"
        )

    # 1. Convert to grayscale
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    # 2. Upscale
    scaled = cv2.resize(
        gray,
        None,
        fx=3,
        fy=3,
        interpolation=cv2.INTER_CUBIC
    )

    # 3. Denoise
    denoised = cv2.fastNlMeansDenoising(
        scaled,
        None,
        10,
        7,
        21
    )

    # 4. Adaptive threshold
    threshold = cv2.adaptiveThreshold(
        denoised,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        10
    )

    return threshold


def clean_ocr_text(text: str) -> str:
    """
    Clean OCR output while preserving code structure.
    """

    if not text:
        return ""

    lines = []

    for line in text.splitlines():

        line = line.strip()

        if line:
            lines.append(line)

    return "\n".join(lines)


def extract_text_from_image(image_path: str) -> str:
    """
    Extract text using improved preprocessing
    and Tesseract OCR.
    """

    if not Path(image_path).exists():
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    processed_image = preprocess_image(
        image_path
    )

    # Try sparse text layout
    config = "--oem 3 --psm 11"

    text = pytesseract.image_to_string(
        processed_image,
        config=config
    )

    cleaned_text = clean_ocr_text(
        text
    )

    return cleaned_text