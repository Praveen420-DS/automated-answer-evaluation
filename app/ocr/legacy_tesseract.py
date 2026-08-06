from __future__ import annotations

from pathlib import Path
import tempfile

import cv2
import pytesseract

from app.ocr.models import OCRBlock, OCRPage, OCRResult
from app.ocr.preprocessing import preprocess_image


TESSERACT_CONFIG = "--oem 3 --psm 11"


def extract_text_with_tesseract(
    image_paths: list[str | Path],
    preprocess: bool = False,
    workspace: str | Path | None = None,
    fallback: bool = False,
    fallback_reason: str | None = None,
) -> OCRResult:
    """
    Fallback OCR using Tesseract.

    Accepts multiple image paths and returns the same OCRResult
    structure used by the PaddleOCR pipeline.
    """

    def process_images(processing_dir: Path | None) -> list[OCRPage]:
        pages: list[OCRPage] = []

        for page_number, image_path in enumerate(image_paths, start=1):
            try:
                prepared_path = preprocess_image(
                    image_path,
                    enabled=preprocess,
                    output_dir=processing_dir,
                )
            except ValueError:
                raise ValueError(
                    f"Unreadable image: {Path(image_path).name}"
                ) from None
            image = cv2.imread(str(prepared_path))
            if image is None:
                raise ValueError(
                    f"Unreadable image: {Path(image_path).name}"
                )

            text = pytesseract.image_to_string(
                image,
                config=TESSERACT_CONFIG,
            ).strip()

            block = OCRBlock(
                text=text,
                type="text",
                confidence=None,
                bbox=[],
            )

            page = OCRPage(
                page_number=page_number,
                text=text,
                blocks=[block] if text else [],
            )
            pages.append(page)

        return pages

    if preprocess and workspace is None:
        with tempfile.TemporaryDirectory() as temporary_workspace:
            pages = process_images(Path(temporary_workspace))
    else:
        processing_dir = Path(workspace) / "preprocessed" if preprocess else None
        pages = process_images(processing_dir)

    full_text = "\n\n".join(
        page.text
        for page in pages
        if page.text
    )

    return OCRResult(
        pages=pages,
        full_text=full_text,
        metadata={
            "engine": "Tesseract",
            "model": f"Tesseract ({TESSERACT_CONFIG})",
            "fallback": fallback,
            "fallback_reason": fallback_reason,
            "structure_enabled": False,
            "preprocessing": preprocess,
        },
    )
