"""Image OCR used when a faculty uploads a scanned question paper."""

from pathlib import Path

_reader = None


def _get_reader():
    """Create EasyOCR lazily, including a compatibility shim for python-bidi."""
    global _reader
    if _reader is not None:
        return _reader

    # EasyOCR 1.7 imports get_display from ``bidi``. python-bidi 0.4 exposes
    # it from bidi.algorithm instead, so expose the same function before
    # importing EasyOCR. This avoids a server-wide import failure on Python 3.12.
    import bidi
    if not hasattr(bidi, "get_display"):
        from bidi.algorithm import get_display
        bidi.get_display = get_display

    import easyocr
    model_directory = Path(__file__).resolve().parents[1] / ".runtime" / "easyocr"
    model_directory.mkdir(parents=True, exist_ok=True)
    _reader = easyocr.Reader(
        ["en"],
        model_storage_directory=str(model_directory),
        user_network_directory=str(model_directory / "user_network"),
        verbose=False,
    )
    return _reader


def extract_image_text(filepath):
    """Return OCR text from a PNG/JPG question paper."""
    result = _get_reader().readtext(str(filepath), detail=0)
    return "\n".join(result)
