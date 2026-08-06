import sys
from types import ModuleType

import pytest

from backend.services.app_ocr_adapter import (
    OCRProcessingError,
    extract_and_parse,
)

class FakeOCRResult:
    def model_dump(self):
        return {
            "pages": [
                {
                    "page_number": 1,
                    "text": "1. What is AI? Ans: AI simulates intelligence.",
                }
            ],
            "full_text": "1. What is AI? Ans: AI simulates intelligence.",
            "metadata": {
                "engine": "mock-ocr",
                "page_count": 1,
            },
        }


def install_fake_ocr_modules(monkeypatch):
    fake_extractor = ModuleType("app.ocr.extractor")
    fake_parser = ModuleType("app.parser.answer_parser")

    fake_extractor.extract_document = lambda path: FakeOCRResult()

    fake_parser.parse_ocr_result = lambda result: {
        "answers": [
            {
                "question_number": 1,
                "answer": "AI simulates intelligence.",
            }
        ]
    }

    monkeypatch.setitem(
        sys.modules,
        "app.ocr.extractor",
        fake_extractor,
    )
    monkeypatch.setitem(
        sys.modules,
        "app.parser.answer_parser",
        fake_parser,
    )


def test_extract_and_parse_returns_stable_payload(
    tmp_path,
    monkeypatch,
):
    install_fake_ocr_modules(monkeypatch)

    answer_sheet = tmp_path / "answer.jpg"
    answer_sheet.write_bytes(b"mock image")

    result = extract_and_parse(answer_sheet)

    assert result["ocr"]["full_text"]
    assert result["ocr"]["metadata"]["engine"] == "mock-ocr"
    assert len(result["ocr"]["pages"]) == 1

    assert result["parsed_answers"] == [
        {
            "question_number": 1,
            "answer": "AI simulates intelligence.",
        }
    ]


def test_extract_and_parse_rejects_missing_file(tmp_path):
    missing_file = tmp_path / "missing.jpg"

    with pytest.raises(
        OCRProcessingError,
        match="no longer exists",
    ):
        extract_and_parse(missing_file)


def test_extract_and_parse_rejects_unsupported_file(tmp_path):
    unsupported_file = tmp_path / "answer.txt"
    unsupported_file.write_text(
        "not an image",
        encoding="utf-8",
    )

    with pytest.raises(
        OCRProcessingError,
        match="Only PDF, PNG, JPG, and JPEG",
    ):
        extract_and_parse(unsupported_file)