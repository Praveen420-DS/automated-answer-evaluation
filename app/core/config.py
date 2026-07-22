from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RUNTIME_HOME = PROJECT_ROOT / ".runtime_home"
TEMP_UPLOAD_DIR = PROJECT_ROOT / "temp_uploads"

MAX_UPLOAD_SIZE_BYTES = 20 * 1024 * 1024
ALLOWED_UPLOAD_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}

PADDLE_OCR_VERSION = "PP-OCRv5"
PADDLE_OCR_LANG = "en"
PADDLE_USE_DOC_ORIENTATION_CLASSIFY = False
PADDLE_USE_DOC_UNWARPING = False
PADDLE_USE_TEXTLINE_ORIENTATION = False


def configure_runtime_environment() -> None:
    import os

    RUNTIME_HOME.mkdir(parents=True, exist_ok=True)
    (RUNTIME_HOME / ".cache" / "paddle").mkdir(parents=True, exist_ok=True)
    (RUNTIME_HOME / ".paddlex").mkdir(parents=True, exist_ok=True)

    os.environ.setdefault("HOME", str(RUNTIME_HOME))
    os.environ.setdefault("USERPROFILE", str(RUNTIME_HOME))
    os.environ.setdefault("PADDLE_HOME", str(RUNTIME_HOME / ".cache" / "paddle"))
    os.environ.setdefault("PADDLEX_HOME", str(RUNTIME_HOME / ".paddlex"))
