from app.core.feedback import generate_feedback
from app.core.grade import get_grade
from app.core.confidence import confidence_level
from app.core.report import generate_report

from app.core.keyword_matcher import keyword_match
from app.core.concept_matcher import concept_match
from app.core.semantic_similarity import semantic_score
from app.core.rubric_engine import rubric_score
from app.core.completeness import completeness_score


def evaluate_answer(
    expected_answer,
    student_answer,
    keywords,
    concepts,
    rubric
):
    # -----------------------------
    # Module 1 - Keyword Matching
    # -----------------------------
    keyword_result = keyword_match(
        keywords,
        student_answer
    )

    # -----------------------------
    # Module 2 - Concept Matching
    # -----------------------------
    concept_result = concept_match(
        concepts,
        student_answer
    )

    # -----------------------------
    # Module 3 - Semantic Similarity
    # -----------------------------
    semantic = semantic_score(
        expected_answer,
        student_answer
    )

    # -----------------------------
    # Module 4 - Rubric Evaluation
    # -----------------------------
    marks_obtained, total_marks = rubric_score(
        rubric,
        concept_result["covered"]
    )

    # -----------------------------
    # Module 5 - Completeness
    # -----------------------------
    completeness = completeness_score(
        concepts,
        concept_result["covered"]
    )

    # -----------------------------
    # Final Score
    # -----------------------------
    final_score = round((marks_obtained / total_marks) * 10, 2) if total_marks else 0

    # -----------------------------
    # Module 7 - Feedback
    # -----------------------------
    feedback = generate_feedback({

        "semantic_similarity": semantic,

        "keyword_result": keyword_result,

        "concept_result": concept_result,

        "completeness": completeness,

        "final_score": final_score

    })

    # -----------------------------
    # Module 8 - Grade
    # -----------------------------
    grade = get_grade(final_score)

    # -----------------------------
    # Module 9 - Confidence
    # -----------------------------
    confidence = confidence_level(semantic)

    # -----------------------------
    # Prepare Result
    # -----------------------------
    result = {

        "keyword_result": keyword_result,

        "concept_result": concept_result,

        "semantic_similarity": round(semantic, 2),

        "rubric_marks": f"{marks_obtained}/{total_marks}",

        "completeness": completeness,

        "final_score": final_score,

        "feedback": feedback,

        "grade": grade,

        "confidence": confidence

    }

    # -----------------------------
    # Module 10 - Report
    # -----------------------------
    report = generate_report(result)

    # Add report to result
    result["report"] = report

    return result
