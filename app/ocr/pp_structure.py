from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

from app.core.config import (
    PADDLE_OCR_DEVICE,
    PADDLE_OCR_VERSION,
    PADDLE_STRUCTURE_TABLE_RECOGNITION,
    PADDLE_TEXT_DETECTION_MODEL,
    PADDLE_TEXT_RECOGNITION_MODEL,
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
        device=PADDLE_OCR_DEVICE,
        text_detection_model_name=PADDLE_TEXT_DETECTION_MODEL,
        text_recognition_model_name=PADDLE_TEXT_RECOGNITION_MODEL,
        use_doc_orientation_classify=PADDLE_USE_DOC_ORIENTATION_CLASSIFY,
        use_doc_unwarping=PADDLE_USE_DOC_UNWARPING,
        use_textline_orientation=PADDLE_USE_TEXTLINE_ORIENTATION,
        use_table_recognition=PADDLE_STRUCTURE_TABLE_RECOGNITION,
        use_formula_recognition=False,
        use_chart_recognition=False,
        use_region_detection=False,
    )


def _result_data(raw_page: Any) -> dict[str, Any]:
    payload = getattr(raw_page, "json", raw_page)
    if not isinstance(payload, dict):
        raise TypeError("PP-StructureV3 result must provide a dictionary payload")
    data = payload.get("res", payload)
    if not isinstance(data, dict):
        raise TypeError("PP-StructureV3 payload has an invalid 'res' value")
    return data


def _as_list(value: Any) -> list:
    if value is None:
        return []
    if hasattr(value, "tolist"):
        return value.tolist()
    return list(value) if isinstance(value, tuple) else value


def _safe_float(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _table_data(table: Any) -> dict[str, Any]:
    if not isinstance(table, dict):
        return {}
    return {
        key: value
        for key, value in table.items()
        if key in {"block_bbox", "pred_html", "cell_box_list", "table_ocr_pred", "table_structure"}
    }


def _extract_blocks(raw_page: Any) -> list[OCRBlock]:
    data = _result_data(raw_page)
    blocks: list[OCRBlock] = []
    tables = [_table_data(table) for table in data.get("table_res_list", []) or []]

    for index, block in enumerate(data.get("parsing_res_list", []) or []):
        if not isinstance(block, dict):
            continue
        text = str(block.get("block_content", "")).strip()
        block_type = str(block.get("block_label", block.get("label", "text")))
        bbox = _as_list(block.get("block_bbox") or block.get("bbox"))
        matching_table = next(
            (table for table in tables if table.get("block_bbox") == bbox), None
        )
        if not text and not matching_table:
            continue
        blocks.append(
            OCRBlock(
                text=text,
                bbox=bbox,
                confidence=_safe_float(block.get("block_score", block.get("score"))),
                type=block_type,
                order=block.get("block_order", index),
                table=matching_table,
            )
        )

    return blocks


def analyze_structure(image_paths: list[str | Path]) -> OCRResult:
    engine = get_pp_structure_engine()
    pages: list[OCRPage] = []

    for page_number, image_path in enumerate(image_paths, start=1):
        raw_pages = list(engine.predict(input=str(image_path)) or [])
        for result_index, raw_page in enumerate(raw_pages):
            blocks = _extract_blocks(raw_page)
            text = "\n".join(block.text for block in blocks if block.text)
            pages.append(
                OCRPage(
                    page_number=page_number + result_index,
                    text=text,
                    blocks=blocks,
                    structure_blocks=blocks,
                )
            )

    full_text = "\n\n".join(page.text for page in pages if page.text)
    return OCRResult(
        pages=pages,
        full_text=full_text,
        metadata={
            "engine": "PaddleOCR",
            "version": PADDLE_OCR_VERSION,
            "model": "PP-StructureV3",
            "table_recognition": PADDLE_STRUCTURE_TABLE_RECOGNITION,
        },
    )
