from __future__ import annotations

from app.evaluation.scoring import (
    character_similarity,
    overall_similarity,
    score_similarity,
    token_similarity,
)


def evaluate_answers(
    parsed_answers: dict,
    expected_answer: str | None = None,
    maximum_score: float = 10.0,
) -> dict:
    answers = parsed_answers.get("answers", [])
    answer_text = "\n\n".join(answer.get("answer_text", "") for answer in answers)

    if not expected_answer:
        return {
            "score": 0.0,
            "maximum_score": maximum_score,
            "correctness": "not_evaluated",
            "matched_criteria": [],
            "failed_criteria": ["No expected answer was supplied."],
            "details": {
                "answers_detected": len(answers),
            },
        }

    char_score = character_similarity(answer_text, expected_answer)
    token_score = token_similarity(answer_text, expected_answer)
    overall = overall_similarity(answer_text, expected_answer)
    score = score_similarity(answer_text, expected_answer, maximum_score)

    return {
        "score": score,
        "maximum_score": maximum_score,
        "correctness": "correct" if overall >= 0.8 else "partial" if overall >= 0.4 else "incorrect",
        "matched_criteria": ["Text similarity calculated deterministically."],
        "failed_criteria": [] if overall >= 0.8 else ["Answer differs from expected reference."],
        "details": {
            "answers_detected": len(answers),
            "character_similarity": round(char_score, 4),
            "token_similarity": round(token_score, 4),
            "overall_similarity": round(overall, 4),
        },
    }
