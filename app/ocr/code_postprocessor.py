import re


# Common OCR mistakes found in programming code
OCR_REPLACEMENTS = {
    "0f": "of",
    "rn": "m",
    "lisk": "list",
    "Lisk": "List",
    "leng": "len",
    "Lenge": "len",
    "rang": "range",
    "Hange": "range",
    "retum": "return",
    "Retum": "Return",
    "minimun": "minimum",
    "minimus": "minimum",
    "trget": "target",
    "targel": "target",
    "arry": "array",
    "anray": "array",
}


def normalize_ocr_symbols(text: str) -> str:
    """
    Normalize common OCR symbol errors.
    """

    if not text:
        return ""

    replacements = {
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "—": "-",
        "–": "-",
        "−": "-",
        "×": "*",
        "÷": "/",
        "∈": "in",
        "≤": "<=",
        "≥": ">=",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text


def fix_common_ocr_words(text: str) -> str:
    """
    Fix common OCR mistakes in programming text.
    """

    for wrong, correct in OCR_REPLACEMENTS.items():

        text = re.sub(
            rf"\b{re.escape(wrong)}\b",
            correct,
            text,
            flags=re.IGNORECASE
        )

    return text


def clean_code_lines(text: str) -> str:
    """
    Clean unnecessary OCR noise while preserving
    programming structure.
    """

    if not text:
        return ""

    lines = []

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        # Ignore lines that contain only OCR noise
        if len(line) <= 1:
            continue

        lines.append(line)

    return "\n".join(lines)


def postprocess_code(text: str) -> str:
    """
    Complete OCR post-processing pipeline.
    """

    if not text:
        return ""

    text = normalize_ocr_symbols(text)

    text = fix_common_ocr_words(text)

    text = clean_code_lines(text)

    return text