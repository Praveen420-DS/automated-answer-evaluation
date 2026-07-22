from __future__ import annotations


def generate_feedback(evaluation: dict) -> dict:
    details = evaluation.get("details", {})
    correctness = evaluation.get("correctness", "not_evaluated")

    strengths: list[str] = []
    missing: list[str] = []
    errors: list[str] = []
    suggestions: list[str] = []

    if details.get("answers_detected", 0) > 0:
        strengths.append("Answer text was detected and parsed.")
    else:
        errors.append("No answer text was detected.")

    if correctness == "correct":
        strengths.append("The answer closely matches the expected reference.")
    elif correctness == "partial":
        missing.append("Some expected content is missing or altered.")
        suggestions.append("Review the missing concepts and improve answer completeness.")
    elif correctness == "incorrect":
        missing.append("The answer does not sufficiently match the expected reference.")
        suggestions.append("Rewrite the answer to include the required logic and key terms.")
    else:
        suggestions.append("Provide an expected answer or rubric to enable deterministic scoring.")

    return {
        "score": evaluation.get("score", 0.0),
        "maximum_score": evaluation.get("maximum_score", 0.0),
        "strengths": strengths,
        "missing_concepts": missing,
        "errors": errors,
        "improvement_suggestions": suggestions,
    }
