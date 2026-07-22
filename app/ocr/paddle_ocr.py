from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

from app.core.config import (
    PADDLE_OCR_LANG,
    PADDLE_OCR_VERSION,
    PADDLE_USE_DOC_ORIENTATION_CLASSIFY,
    PADDLE_USE_DOC_UNWARPING,
    PADDLE_USE_TEXTLINE_ORIENTATION,
    configure_runtime_environment,
)
from app.ocr.models import OCRBlock, OCRPage, OCRResult
from app.ocr.preprocessing import preprocess_image


def _safe_float(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _as_bbox(value: Any) -> list:
    if value is None:
        return []

    if hasattr(value, "tolist"):
        return value.tolist()

    return value


@lru_cache(maxsize=1)
def get_paddle_ocr_engine():
    configure_runtime_environment()
    from paddleocr import PaddleOCR

    return PaddleOCR(
        lang=PADDLE_OCR_LANG,
        ocr_version=PADDLE_OCR_VERSION,
        use_doc_orientation_classify=PADDLE_USE_DOC_ORIENTATION_CLASSIFY,
        use_doc_unwarping=PADDLE_USE_DOC_UNWARPING,
        use_textline_orientation=PADDLE_USE_TEXTLINE_ORIENTATION,
    )


def _page_from_paddle_result(raw_page: Any, page_number: int) -> OCRPage:
    data = raw_page.json.get("res", {}) if hasattr(raw_page, "json") else {}
    texts = data.get("rec_texts") or []
    scores = data.get("rec_scores") or []
    boxes = data.get("rec_polys") or data.get("dt_polys") or []

    blocks: list[OCRBlock] = []
    for index, text in enumerate(texts):
        clean_text = str(text).strip()
        if not clean_text:
            continue

        confidence = _safe_float(scores[index] if index < len(scores) else None)
        bbox = _as_bbox(boxes[index] if index < len(boxes) else None)
        blocks.append(
            OCRBlock(
                text=clean_text,
                bbox=bbox,
                confidence=confidence,
                type="text",
            )
        )

    page_text = "\n".join(block.text for block in blocks)
    return OCRPage(page_number=page_number, text=page_text, blocks=blocks)


def extract_text_with_paddle(
    image_paths: list[str | Path],
    preprocess: bool = False,
) -> OCRResult:
    engine = get_paddle_ocr_engine()
    pages: list[OCRPage] = []

    for page_number, image_path in enumerate(image_paths, start=1):
        prepared_path = preprocess_image(image_path, enabled=preprocess)
        raw_pages = engine.predict(input=str(prepared_path))

        if not raw_pages:
            pages.append(OCRPage(page_number=page_number, text="", blocks=[]))
            continue

        page = _page_from_paddle_result(raw_pages[0], page_number=page_number)
        pages.append(page)

    full_text = "\n\n".join(page.text for page in pages if page.text)

    return OCRResult(
        pages=pages,
        full_text=full_text,
        metadata={
            "engine": "PaddleOCR",
            "version": PADDLE_OCR_VERSION,
            "model": "PP-OCRv5",
            "preprocessing": preprocess,
        },
    )
