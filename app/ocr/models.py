from typing import Any

from pydantic import BaseModel, Field


class OCRBlock(BaseModel):
    text: str
    bbox: list[list[float]] | list[float] = Field(default_factory=list)
    confidence: float | None = None
    type: str = "text"
    order: int | None = None
    table: dict[str, Any] | None = None


class OCRPage(BaseModel):
    page_number: int
    text: str
    blocks: list[OCRBlock] = Field(default_factory=list)
    structure_blocks: list[OCRBlock] = Field(default_factory=list)


class OCRResult(BaseModel):
    pages: list[OCRPage] = Field(default_factory=list)
    full_text: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)


class ParsedAnswer(BaseModel):
    question_number: str | None = None
    answer_text: str
    code: str | None = None
    page_numbers: list[int] = Field(default_factory=list)
