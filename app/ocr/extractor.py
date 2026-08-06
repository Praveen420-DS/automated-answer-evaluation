from __future__ import annotations

import logging
import tempfile
from threading import Lock
from pathlib import Path

from app.ocr.input_handler import input_to_images
from app.ocr.models import OCRResult
from app.ocr.paddle_ocr import extract_text_with_paddle
from app.ocr.legacy_tesseract import extract_text_with_tesseract
from app.ocr.pp_structure import analyze_structure
from app.core.config import OCR_ENGINE, PADDLE_ENABLE_STRUCTURE


logger = logging.getLogger(__name__)
_paddle_circuit_open = False
_paddle_circuit_lock = Lock()


def reset_paddle_circuit_breaker() -> None:
    """Reset the process-level Paddle failure state (primarily for tests)."""
    global _paddle_circuit_open
    with _paddle_circuit_lock:
        _paddle_circuit_open = False


def _paddle_is_available() -> bool:
    with _paddle_circuit_lock:
        return not _paddle_circuit_open


def _open_paddle_circuit() -> None:
    global _paddle_circuit_open
    with _paddle_circuit_lock:
        _paddle_circuit_open = True


def _fallback_reason(error: Exception) -> str:
    # Keep metadata useful without copying exception messages, stack traces,
    # file paths, credentials, or request data into API responses.
    return f"PaddleOCR failed with {type(error).__name__}"


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
        selected_engine = OCR_ENGINE
        paddle_succeeded = False

        if selected_engine == "tesseract":
            logger.info("Using forced Tesseract OCR mode")
            result = extract_text_with_tesseract(
                image_paths,
                preprocess=preprocess,
                workspace=temp_dir,
                fallback=False,
                fallback_reason=None,
            )
        elif selected_engine == "paddle":
            logger.info("Using forced PaddleOCR mode")
            result = extract_text_with_paddle(
                image_paths,
                preprocess=preprocess,
                workspace=temp_dir,
            )
            paddle_succeeded = True
        elif _paddle_is_available():
            try:
                logger.info("Trying PaddleOCR in automatic mode")
                result = extract_text_with_paddle(
                    image_paths,
                    preprocess=preprocess,
                    workspace=temp_dir,
                )
                paddle_succeeded = True
            except Exception as error:
                _open_paddle_circuit()
                reason = _fallback_reason(error)
                logger.warning("%s; opening circuit and using Tesseract", reason)
                result = extract_text_with_tesseract(
                    image_paths,
                    preprocess=preprocess,
                    workspace=temp_dir,
                    fallback=True,
                    fallback_reason=reason,
                )
        else:
            reason = "PaddleOCR skipped because its process circuit breaker is open"
            logger.warning("%s; using Tesseract", reason)
            result = extract_text_with_tesseract(
                image_paths,
                preprocess=preprocess,
                workspace=temp_dir,
                fallback=True,
                fallback_reason=reason,
            )

        result.metadata.setdefault("fallback", False)
        result.metadata.setdefault("fallback_reason", None)
        result.metadata["structure_enabled"] = False

        if not (PADDLE_ENABLE_STRUCTURE and paddle_succeeded):
            return result

        try:
            structure_result = analyze_structure(image_paths)
        except Exception as error:
            warning = f"PP-Structure failed with {type(error).__name__}"
            logger.warning("%s; structure analysis is disabled for this result", warning)
            result.metadata["structure_enabled"] = False
            result.metadata["structure_available"] = False
            result.metadata["structure_warning"] = warning
        else:
            _attach_structure(result, structure_result)
            result.metadata["structure_enabled"] = True
            result.metadata["structure_available"] = True
            result.metadata["structure_model"] = structure_result.metadata["model"]
        return result


def extract_text_from_image(image_path: str) -> str:
    result = extract_document(image_path)
    return result.full_text
