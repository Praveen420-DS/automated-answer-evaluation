from pydantic import BaseModel
from typing import List


# ---------------------------------------
# Existing API Schemas
# ---------------------------------------

class EvaluationRequest(BaseModel):
    expected_answer: str
    student_answer: str
    keywords: List[str]
    concepts: List[str]
    rubric: dict


class AutoEvaluationRequest(BaseModel):
    question: str
    student_answer: str


# ---------------------------------------
# Database Schemas
# ---------------------------------------

class EvaluationCreate(BaseModel):
    question: str
    model_answer: str
    student_answer: str


class EvaluationResponse(BaseModel):
    id: int
    question: str
    model_answer: str
    student_answer: str
    marks: float
    grade: str
    feedback: str

    class Config:
        from_attributes = True