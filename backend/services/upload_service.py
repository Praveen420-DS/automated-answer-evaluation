import os
from pathlib import Path
from uuid import uuid4
from werkzeug.utils import secure_filename

from services.app_ocr_adapter import extract_and_parse

UPLOAD_FOLDER = Path(__file__).resolve().parents[1] / "uploads" / "answer_scripts"

def process_answer_script(file):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    filename = secure_filename(file.filename or "")
    if not filename:
        raise ValueError("Invalid filename")
    suffix = Path(filename).suffix.lower()
    if suffix not in {".pdf", ".png", ".jpg", ".jpeg"}:
        raise ValueError("Only PDF, PNG, JPG, and JPEG files are supported.")
    filepath = UPLOAD_FOLDER / f"{uuid4().hex}{suffix}"

    file.save(filepath)

    result = extract_and_parse(filepath)
    result.update({"success": True, "filename": filename, "path": str(filepath)})
    return result
