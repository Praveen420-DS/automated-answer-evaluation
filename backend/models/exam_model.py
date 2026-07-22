from datetime import datetime


class ExamModel:

    @staticmethod
    def create(

        exam_name,
        subject,
        department,
        semester,
        total_marks,
        faculty_id

    ):

        return {

            "examName": exam_name,

            "subject": subject,

            "department": department,

            "semester": semester,

            "totalMarks": total_marks,

            "facultyId": faculty_id,

            "status": "Created",

            "createdAt": datetime.utcnow(),

            "updatedAt": datetime.utcnow()

        }