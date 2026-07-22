from pydantic import BaseModel
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