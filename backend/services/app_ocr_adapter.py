"""Flask-facing adapter for the internal OCR and answer parsing library.

The functions in :mod:`app.ocr` are deliberately imported inside the request
function.  This keeps Paddle and its model weights out of Flask startup.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) in sys.path:
    sys.path.remove(str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT))


class OCRProcessingError(RuntimeError):
    """Raised when a supported document cannot be processed by OCR."""


def _dump(value: Any) -> dict:
    if hasattr(value, "model_dump"):
        return value.model_dump()
    return value.dict()


def extract_and_parse(file_path: str | Path) -> dict:
    """Extract a PDF/image and return a stable, JSON-ready OCR payload."""
    path = Path(file_path)
    if not path.is_file():
        raise OCRProcessingError("The uploaded file no longer exists.")

    if path.suffix.lower() not in {".pdf", ".png", ".jpg", ".jpeg"}:
        raise OCRProcessingError("Only PDF, PNG, JPG, and JPEG files are supported.")

    try:
        from app.ocr.extractor import extract_document
        from app.parser.answer_parser import parse_ocr_result

        ocr_result = extract_document(path)
        parsed = parse_ocr_result(ocr_result)
    except Exception as error:
        raise OCRProcessingError(f"OCR could not process this document: {error}") from error

    result = _dump(ocr_result)
    return {
        "ocr": {
            "pages": result.get("pages", []),
            "full_text": result.get("full_text", ""),
            "metadata": result.get("metadata", {}),
        },
        "parsed_answers": parsed.get("answers", []),
    }
