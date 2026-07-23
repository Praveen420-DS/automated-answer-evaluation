"""Normalize calls from Flask services to the internal evaluation library."""
from __future__ import annotations

import sys
from pathlib import Path

# See backend/app.py: avoid resolving ``app`` to backend/app.py when services
# are imported from the backend working directory.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) in sys.path:
    sys.path.remove(str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT))

from app.evaluation.deterministic_evaluator import evaluate_answers


def evaluate_parsed_answer(
    question_number: str | int | None,
    question_text: str,
    reference_answer: str,
    student_answer: str,
    maximum_score: float,
) -> dict:
    """Evaluate one answer using the maintained deterministic implementation."""
    maximum_score = float(maximum_score or 0)
    raw = evaluate_answers(
        {"answers": [{"answer_text": student_answer or ""}]},
        expected_answer=reference_answer or None,
        maximum_score=maximum_score,
    )
    details = raw.get("details", {})
    return {
        "question_number": question_number,
        "question_text": question_text or "",
        "student_answer": student_answer or "",
        "reference_answer": reference_answer or "",
        "score": raw["score"],
        "maximum_score": raw["maximum_score"],
        "grade": raw["correctness"],
        "confidence": _confidence(details.get("overall_similarity", 0.0)),
        "feedback": _feedback(raw),
        "missing_concepts": raw.get("failed_criteria", []),
        "evaluation_metadata": details,
    }


def _confidence(similarity: float) -> str:
    if similarity >= 0.8:
        return "high"
    if similarity >= 0.4:
        return "medium"
    return "low"


def _feedback(result: dict) -> str:
    failed = result.get("failed_criteria", [])
    return " ".join(failed) if failed else "Answer closely matches the reference answer."
