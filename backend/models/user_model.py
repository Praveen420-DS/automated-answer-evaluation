from datetime import datetime


class UserModel:

    @staticmethod
    def create(
        full_name,
        email,
        password,
        role="student",
        department="",
        semester=""
    ):

        return {

            "fullName": full_name,

            "email": email.lower(),

            "password": password,

            "role": role,

            "department": department,

            "semester": semester,

            "isActive": True,

            "createdAt": datetime.utcnow(),

            "updatedAt": datetime.utcnow()

        }