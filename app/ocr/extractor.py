from __future__ import annotations

import tempfile
from pathlib import Path

from app.ocr.input_handler import input_to_images
from app.ocr.models import OCRResult
from app.ocr.paddle_ocr import extract_text_with_paddle


def extract_document(
    file_path: str | Path,
    preprocess: bool = False,
) -> OCRResult:
    with tempfile.TemporaryDirectory() as temp_dir:
        image_paths = input_to_images(file_path, temp_dir)
        return extract_text_with_paddle(image_paths, preprocess=preprocess)


def extract_text_from_image(image_path: str) -> str:
    result = extract_document(image_path)
    return result.full_text
