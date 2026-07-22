from pathlib import Path

import cv2
import pytesseract


def extract_text_with_tesseract(image_path: str | Path) -> str:
    image_path = Path(image_path)
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    image = cv2.imread(str(image_path))
    if image is None:
        raise ValueError(f"Invalid or unreadable image: {image_path}")

    return pytesseract.image_to_string(image, config="--oem 3 --psm 11").strip()
