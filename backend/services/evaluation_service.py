from datetime import datetime

from database.mongodb import (
    answer_keys_collection,
    evaluations_collection
)

from ai.evaluator import evaluator


class EvaluationService:

    def __init__(self):
        pass

    # ==========================================
    # Evaluate Student Answer
    # ==========================================

    def evaluate_answer(

        self,
        answer_key_text,
        student_answer_text,
        total_marks,
        student_name,
        exam_name

    ):

        result = evaluator.evaluate(

            answer_key=answer_key_text,
            student_answer=student_answer_text,
            total_marks=total_marks

        )

        evaluation = {

            "studentName": student_name,

            "examName": exam_name,

            "answerKey": answer_key_text,

            "studentAnswer": student_answer_text,

            "similarity": result["similarity"],

            "marks": result["marks"],

            "feedback": result["feedback"],

            "evaluatedAt": datetime.utcnow()

        }

        evaluations_collection().insert_one(
            evaluation
        )

        return evaluation


evaluation_service = EvaluationService()