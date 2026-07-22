from __future__ import annotations

import tempfile
from pathlib import Path

from app.ocr.input_handler import input_to_images
from app.ocr.models import OCRResult
from app.ocr.paddle_ocr import extract_text_with_paddle
from app.ocr.pp_structure import analyze_structure
from app.core.config import PADDLE_ENABLE_STRUCTURE


def _attach_structure(ocr_result: OCRResult, structure_result: OCRResult) -> None:
    structure_by_page = {page.page_number: page for page in structure_result.pages}
    for page in ocr_result.pages:
        structure_page = structure_by_page.get(page.page_number)
        if structure_page is not None:
            page.structure_blocks = structure_page.structure_blocks or structure_page.blocks


def extract_document(
    file_path: str | Path,
    preprocess: bool = False,
) -> OCRResult:
    with tempfile.TemporaryDirectory() as temp_dir:
        image_paths = input_to_images(file_path, temp_dir)
        result = extract_text_with_paddle(
            image_paths,
            preprocess=preprocess,
            workspace=temp_dir,
        )
        result.metadata["structure_enabled"] = PADDLE_ENABLE_STRUCTURE
        if not PADDLE_ENABLE_STRUCTURE:
            return result

        try:
            structure_result = analyze_structure(image_paths)
        except Exception as error:
            result.metadata["structure_available"] = False
            result.metadata["structure_warning"] = str(error)
        else:
            _attach_structure(result, structure_result)
            result.metadata["structure_available"] = True
            result.metadata["structure_model"] = structure_result.metadata["model"]
        return result


def extract_text_from_image(image_path: str) -> str:
    result = extract_document(image_path)
    return result.full_text
