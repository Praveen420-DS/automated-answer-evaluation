"""Tolerant question extraction for text and OCR output."""

import re


# Supports common forms: Q1., Q 1), Question 1:, and 1. at the start of a line.
QUESTION_START = re.compile(
    r"(?:^|\n)\s*(?:(?:q(?:uestion)?\s*)?(\d{1,3}))\s*[.:)\-]\s*",
    re.IGNORECASE,
)
MARKS = re.compile(
    r"(?:\(\s*)?(\d+(?:\.\d+)?)\s*(?:marks?|pts?|points?)(?:\s*\))?",
    re.IGNORECASE,
)


def _clean_question(value: str) -> str:
    """Preserve paragraph breaks but remove OCR's excess whitespace."""
    return re.sub(r"[ \t]+", " ", value).strip(" -:\n\t")


def parse_questions(text):
    """Extract numbered questions even when OCR formatting differs from the template.

    Marks are optional: they are recorded as 0 when absent so faculty can still
    enter reference answers and continue the workflow.
    """
    if not text or not text.strip():
        return []

    matches = list(QUESTION_START.finditer(text))
    questions = []
    seen_numbers = set()

    for index, match in enumerate(matches):
        number = int(match.group(1))
        if number in seen_numbers:
            continue

        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        segment = _clean_question(text[match.end():end])
        mark_match = MARKS.search(segment)
        marks = int(float(mark_match.group(1))) if mark_match else 0
        question = _clean_question(MARKS.sub("", segment, count=1) if mark_match else segment)

        # Avoid creating an item from a page number or a heading with no text.
        if len(question) < 3:
            continue

        seen_numbers.add(number)
        questions.append({"number": number, "question": question, "marks": marks})

    return questions
