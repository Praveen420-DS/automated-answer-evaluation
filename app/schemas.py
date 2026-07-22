from pydantic import BaseModel, ConfigDict
from typing import Dict, List


class EvaluationRequest(BaseModel):
    expected_answer: str
    student_answer: str
    keywords: List[str]
    concepts: List[str]
    rubric: Dict[str, int]


class AutoEvaluationRequest(BaseModel):
    question: str
    student_answer: str


class EvaluationCreate(BaseModel):
    question: str
    model_answer: str
    student_answer: str


class EvaluationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    question: str
    model_answer: str
    student_answer: str
    marks: float
    grade: str
    feedback: str
