import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RUNTIME_HOME = Path(
    os.environ.get("APP_RUNTIME_DIR", PROJECT_ROOT / ".runtime_home")
).resolve()
TEMP_UPLOAD_DIR = PROJECT_ROOT / "temp_uploads"

MAX_UPLOAD_SIZE_BYTES = 20 * 1024 * 1024
ALLOWED_UPLOAD_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}

PADDLE_OCR_VERSION = "PP-OCRv5"
PADDLE_OCR_LANG = "en"
PADDLE_USE_DOC_ORIENTATION_CLASSIFY = False
PADDLE_USE_DOC_UNWARPING = False
PADDLE_USE_TEXTLINE_ORIENTATION = False
PADDLE_OCR_DEVICE = os.environ.get("PADDLE_OCR_DEVICE", "cpu")
PADDLE_TEXT_DETECTION_MODEL = "PP-OCRv5_server_det"
PADDLE_TEXT_RECOGNITION_MODEL = "PP-OCRv5_server_rec"
PADDLE_ENABLE_STRUCTURE = os.environ.get("PADDLE_ENABLE_STRUCTURE", "true").lower() in {
    "1",
    "true",
    "yes",
}
PADDLE_STRUCTURE_TABLE_RECOGNITION = os.environ.get(
    "PADDLE_STRUCTURE_TABLE_RECOGNITION", "false"
).lower() in {"1", "true", "yes"}


def configure_runtime_environment() -> None:
    RUNTIME_HOME.mkdir(parents=True, exist_ok=True)
    (RUNTIME_HOME / ".cache" / "paddle").mkdir(parents=True, exist_ok=True)
    (RUNTIME_HOME / ".paddlex").mkdir(parents=True, exist_ok=True)
    (RUNTIME_HOME / ".cache" / "huggingface").mkdir(parents=True, exist_ok=True)

    # PaddlePaddle 3.0 resolves its dataset and weights caches from the home
    # directory.  PaddleX 3.7 reads PADDLE_PDX_CACHE_HOME at import time.
    # Set these before importing PaddleOCR, rather than preserving a protected
    # Windows user-profile path with ``setdefault``.
    os.environ["HOME"] = str(RUNTIME_HOME)
    os.environ["USERPROFILE"] = str(RUNTIME_HOME)
    os.environ["PADDLE_PDX_CACHE_HOME"] = str(RUNTIME_HOME / ".paddlex")
    os.environ["HF_HOME"] = str(RUNTIME_HOME / ".cache" / "huggingface")
