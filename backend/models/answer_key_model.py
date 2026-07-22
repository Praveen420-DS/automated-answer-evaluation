from datetime import datetime


class AnswerKeyModel:

    @staticmethod
    def create(

        exam_id,

        question_number,

        answer

    ):

        return {

            "examId": exam_id,

            "questionNumber": question_number,

            "answer": answer,

            "createdAt": datetime.utcnow()

        }