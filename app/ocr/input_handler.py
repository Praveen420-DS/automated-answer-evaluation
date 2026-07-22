from __future__ import annotations

import shutil
import uuid
from pathlib import Path

import pypdfium2 as pdfium
from fastapi import UploadFile

from app.core.config import (
    ALLOWED_UPLOAD_EXTENSIONS,
    MAX_UPLOAD_SIZE_BYTES,
    TEMP_UPLOAD_DIR,
)


class InputValidationError(ValueError):
    pass


def validate_upload_name(filename: str | None) -> str:
    if not filename:
        raise InputValidationError("Uploaded file must have a filename.")

    extension = Path(filename).suffix.lower()
    if extension not in ALLOWED_UPLOAD_EXTENSIONS:
        raise InputValidationError("Only PDF, PNG, JPG, and JPEG files are supported.")

    return extension


def save_upload_file(file: UploadFile) -> Path:
    extension = validate_upload_name(file.filename)
    TEMP_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    destination = TEMP_UPLOAD_DIR / f"{uuid.uuid4()}{extension}"
    total = 0

    with destination.open("wb") as buffer:
        while True:
            chunk = file.file.read(1024 * 1024)
            if not chunk:
                break

            total += len(chunk)
            if total > MAX_UPLOAD_SIZE_BYTES:
                destination.unlink(missing_ok=True)
                raise InputValidationError("Uploaded file exceeds the maximum allowed size.")

            buffer.write(chunk)

    if total == 0:
        destination.unlink(missing_ok=True)
        raise InputValidationError("Uploaded file is empty.")

    return destination


def pdf_to_images(pdf_path: str | Path, output_dir: str | Path) -> list[Path]:
    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        document = pdfium.PdfDocument(str(pdf_path))
    except Exception as error:
        raise InputValidationError(f"Invalid PDF file: {error}") from error

    image_paths: list[Path] = []
    try:
        for page_index in range(len(document)):
            page = document[page_index]
            bitmap = page.render(scale=2.0)
            image = bitmap.to_pil()
            image_path = output_dir / f"page_{page_index + 1:04d}.png"
            image.save(image_path)
            image_paths.append(image_path)
    finally:
        document.close()

    if not image_paths:
        raise InputValidationError("PDF did not contain any pages.")

    return image_paths


def input_to_images(input_path: str | Path, workspace: str | Path) -> list[Path]:
    input_path = Path(input_path)
    extension = input_path.suffix.lower()

    if extension == ".pdf":
        return pdf_to_images(input_path, Path(workspace) / "pages")

    if extension in {".png", ".jpg", ".jpeg"}:
        return [input_path]

    raise InputValidationError("Only PDF, PNG, JPG, and JPEG files are supported.")


def cleanup_path(path: str | Path) -> None:
    path = Path(path)
    if path.is_dir():
        shutil.rmtree(path, ignore_errors=True)
    else:
        path.unlink(missing_ok=True)
