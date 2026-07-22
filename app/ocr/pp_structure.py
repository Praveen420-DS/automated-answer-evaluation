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


@lru_cache(maxsize=1)
def get_pp_structure_engine():
    configure_runtime_environment()
    from paddleocr import PPStructureV3

    return PPStructureV3(
        lang=PADDLE_OCR_LANG,
        ocr_version=PADDLE_OCR_VERSION,
        use_doc_orientation_classify=PADDLE_USE_DOC_ORIENTATION_CLASSIFY,
        use_doc_unwarping=PADDLE_USE_DOC_UNWARPING,
        use_textline_orientation=PADDLE_USE_TEXTLINE_ORIENTATION,
        use_table_recognition=False,
        use_formula_recognition=False,
        use_chart_recognition=False,
        use_region_detection=False,
    )


def _extract_blocks(raw_page: Any) -> list[OCRBlock]:
    data = raw_page.json.get("res", {}) if hasattr(raw_page, "json") else {}
    blocks: list[OCRBlock] = []

    for block in data.get("parsing_res_list", []) or []:
        text = str(block.get("block_content", "")).strip()
        if not text:
            continue

        bbox = block.get("block_bbox") or block.get("bbox") or []
        blocks.append(
            OCRBlock(
                text=text,
                bbox=bbox,
                confidence=None,
                type=str(block.get("block_label", "text")),
            )
        )

    return blocks


def analyze_structure(image_paths: list[str | Path]) -> OCRResult:
    engine = get_pp_structure_engine()
    pages: list[OCRPage] = []

    for page_number, image_path in enumerate(image_paths, start=1):
        raw_pages = engine.predict(input=str(image_path))
        blocks = _extract_blocks(raw_pages[0]) if raw_pages else []
        text = "\n".join(block.text for block in blocks)
        pages.append(OCRPage(page_number=page_number, text=text, blocks=blocks))

    full_text = "\n\n".join(page.text for page in pages if page.text)
    return OCRResult(
        pages=pages,
        full_text=full_text,
        metadata={
            "engine": "PaddleOCR",
            "version": PADDLE_OCR_VERSION,
            "model": "PP-StructureV3",
        },
    )
