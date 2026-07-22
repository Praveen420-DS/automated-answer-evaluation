from datetime import datetime


class EvaluationModel:

    @staticmethod
    def create(

        student_id,

        student_name,

        exam_id,

        exam_name,

        marks,

        percentage,

        grade,

        feedback,

        pdf_report

    ):

        return {

            "studentId": student_id,

            "studentName": student_name,

            "examId": exam_id,

            "examName": exam_name,

            "marks": marks,

            "percentage": percentage,

            "grade": grade,

            "feedback": feedback,

            "pdfReport": pdf_report,

            "evaluatedAt": datetime.utcnow()

        }