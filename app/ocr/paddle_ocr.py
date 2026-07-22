from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import tempfile
from typing import Any

from app.core.config import (
    PADDLE_OCR_DEVICE,
    PADDLE_OCR_VERSION,
    PADDLE_TEXT_DETECTION_MODEL,
    PADDLE_TEXT_RECOGNITION_MODEL,
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


def _as_list(value: Any) -> list:
    if value is None:
        return []

    if hasattr(value, "tolist"):
        return value.tolist()

    return list(value) if isinstance(value, tuple) else value


def _result_data(raw_page: Any) -> dict[str, Any]:
    payload = getattr(raw_page, "json", raw_page)
    if not isinstance(payload, dict):
        raise TypeError("PaddleOCR prediction result must provide a dictionary payload")

    data = payload.get("res", payload)
    if not isinstance(data, dict):
        raise TypeError("PaddleOCR prediction payload has an invalid 'res' value")

    return data


@lru_cache(maxsize=1)
def get_paddle_ocr_engine():
    configure_runtime_environment()
    from paddleocr import PaddleOCR

    return PaddleOCR(
        device=PADDLE_OCR_DEVICE,
        text_detection_model_name=PADDLE_TEXT_DETECTION_MODEL,
        text_recognition_model_name=PADDLE_TEXT_RECOGNITION_MODEL,
        use_doc_orientation_classify=PADDLE_USE_DOC_ORIENTATION_CLASSIFY,
        use_doc_unwarping=PADDLE_USE_DOC_UNWARPING,
        use_textline_orientation=PADDLE_USE_TEXTLINE_ORIENTATION,
    )


def _page_from_paddle_result(raw_page: Any, page_number: int) -> OCRPage:
    data = _result_data(raw_page)
    texts = _as_list(data.get("rec_texts")) or []
    scores = _as_list(data.get("rec_scores")) or []
    boxes = (
        _as_list(data.get("rec_polys"))
        or _as_list(data.get("rec_boxes"))
        or _as_list(data.get("dt_polys"))
        or []
    )

    blocks: list[OCRBlock] = []
    for index, text in enumerate(texts):
        clean_text = str(text).strip()
        if not clean_text:
            continue

        confidence = _safe_float(scores[index] if index < len(scores) else None)
        bbox = _as_list(boxes[index] if index < len(boxes) else None)
        blocks.append(
            OCRBlock(
                text=clean_text,
                bbox=bbox,
                confidence=confidence,
                type="text",
                order=index,
            )
        )

    page_text = "\n".join(block.text for block in blocks)
    return OCRPage(page_number=page_number, text=page_text, blocks=blocks)


def _pages_from_paddle_results(
    raw_pages: Any,
    first_page_number: int,
) -> list[OCRPage]:
    pages = list(raw_pages or [])
    return [
        _page_from_paddle_result(raw_page, first_page_number + index)
        for index, raw_page in enumerate(pages)
    ]


def extract_text_with_paddle(
    image_paths: list[str | Path],
    preprocess: bool = False,
    workspace: str | Path | None = None,
) -> OCRResult:
    engine = get_paddle_ocr_engine()
    pages: list[OCRPage] = []

    def process_images(processing_dir: Path | None) -> None:
        for page_number, image_path in enumerate(image_paths, start=1):
            prepared_path = preprocess_image(
                image_path,
                enabled=preprocess,
                output_dir=processing_dir,
            )
            normalized_pages = _pages_from_paddle_results(
                engine.predict(input=str(prepared_path)),
                first_page_number=page_number,
            )
            pages.extend(normalized_pages or [OCRPage(page_number=page_number, text="")])

    if preprocess and workspace is None:
        with tempfile.TemporaryDirectory() as temporary_workspace:
            process_images(Path(temporary_workspace))
    else:
        process_images(Path(workspace) / "preprocessed" if preprocess else None)

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
