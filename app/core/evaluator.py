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
    # ---------------------------------
    # Keyword Matching
    # ---------------------------------
    keyword_result = keyword_match(
        keywords,
        student_answer
    )

    # ---------------------------------
    # Concept Matching
    # ---------------------------------
    concept_result = concept_match(
        concepts,
        student_answer
    )

    # ---------------------------------
    # Semantic Similarity
    # ---------------------------------
    semantic = semantic_score(
        expected_answer,
        student_answer
    )

    # ---------------------------------
    # Rubric Evaluation
    # ---------------------------------
    marks_obtained, total_marks = rubric_score(
        rubric,
        concept_result["covered"]
    )

    # ---------------------------------
    # Completeness
    # ---------------------------------
    completeness = completeness_score(
        concepts,
        concept_result["covered"]
    )

    # ---------------------------------
    # Final Score
    # ---------------------------------
    if total_marks == 0:
        final_score = 0
    else:
        final_score = round((marks_obtained / total_marks) * 10, 2)

    # ---------------------------------
    # Feedback
    # ---------------------------------
    feedback = generate_feedback({
        "semantic_similarity": semantic,
        "keyword_result": keyword_result,
        "concept_result": concept_result,
        "completeness": completeness,
        "final_score": final_score
    })

    # ---------------------------------
    # Grade
    # ---------------------------------
    grade = get_grade(final_score)

    # ---------------------------------
    # Confidence
    # ---------------------------------
    confidence = confidence_level(semantic)

    # ---------------------------------
    # Final Result
    # ---------------------------------
    result = {
        "marks": final_score,                 # <-- Added for database
        "final_score": final_score,

        "grade": grade,
        "feedback": feedback,
        "confidence": confidence,

        "keyword_result": keyword_result,
        "concept_result": concept_result,
        "semantic_similarity": round(semantic, 2),
        "rubric_marks": f"{marks_obtained}/{total_marks}",
        "completeness": completeness
    }

    # ---------------------------------
    # Report
    # ---------------------------------
    result["report"] = generate_report(result)

    return result