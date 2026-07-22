from datetime import datetime


class QuestionModel:

    @staticmethod
    def create(

        exam_id,

        question_number,

        question,

        marks

    ):

        return {

            "examId": exam_id,

            "questionNumber": question_number,

            "question": question,

            "marks": marks,

            "createdAt": datetime.utcnow()

        }