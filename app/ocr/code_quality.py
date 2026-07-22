import re


PYTHON_KEYWORDS = [
    "def",
    "return",
    "for",
    "while",
    "if",
    "else",
    "elif",
    "in",
    "range",
    "len",
    "print",
    "list",
    "dict",
    "set",
    "min",
    "max",
]


def keyword_score(text: str) -> float:
    """
    Calculate how many programming keywords
    are present in the OCR output.
    """

    if not text:
        return 0.0

    text_lower = text.lower()

    found = 0

    for keyword in PYTHON_KEYWORDS:

        if re.search(
            rf"\b{re.escape(keyword)}\b",
            text_lower
        ):
            found += 1

    return min(
        found / 5,
        1.0
    )


def structure_score(text: str) -> float:
    """
    Check whether OCR text resembles programming code.
    """

    if not text:
        return 0.0

    score = 0.0

    if "def " in text:
        score += 0.2

    if "for " in text:
        score += 0.15

    if "if " in text:
        score += 0.15

    if "return " in text:
        score += 0.15

    if "(" in text and ")" in text:
        score += 0.1

    if "[" in text and "]" in text:
        score += 0.1

    if ":" in text:
        score += 0.1

    if "=" in text:
        score += 0.05

    return min(score, 1.0)


def code_quality_score(text: str) -> float:
    """
    Combined code quality score.
    """

    keyword = keyword_score(text)

    structure = structure_score(text)

    return (
        keyword * 0.5
        + structure * 0.5
    )