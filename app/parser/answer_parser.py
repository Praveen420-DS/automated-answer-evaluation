from __future__ import annotations

import re

from app.ocr.models import OCRResult, ParsedAnswer


QUESTION_PATTERN = re.compile(
    r"(?im)^\s*(?:Q(?:uestion)?\s*)?(\d+)[.)]\s*(.*)$"
)


def _extract_code(text: str) -> str | None:
    code_signals = ("def ", "for ", "if ", "return", "#include", "int main", "while ")
    if any(signal in text for signal in code_signals):
        return text.strip()
    return None


def parse_text(text: str, page_numbers: list[int] | None = None) -> list[ParsedAnswer]:
    if not text or not text.strip():
        return []

    matches = list(QUESTION_PATTERN.finditer(text))
    if not matches:
        return [
            ParsedAnswer(
                question_number=None,
                answer_text=text.strip(),
                code=_extract_code(text),
                page_numbers=page_numbers or [],
            )
        ]

    answers: list[ParsedAnswer] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        heading = match.group(2).strip()
        body = text[start:end].strip()
        answer_text = "\n".join(part for part in [heading, body] if part).strip()
        answer_text = re.sub(r"(?im)^\s*(?:Ans|Answer)\s*:\s*", "", answer_text).strip()

        answers.append(
            ParsedAnswer(
                question_number=match.group(1),
                answer_text=answer_text,
                code=_extract_code(answer_text),
                page_numbers=page_numbers or [],
            )
        )

    return answers


def parse_ocr_result(ocr_result: OCRResult) -> dict:
    answers = parse_text(
        ocr_result.full_text,
        page_numbers=[page.page_number for page in ocr_result.pages],
    )
    return {"answers": [answer.model_dump() for answer in answers]}
