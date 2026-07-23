from database.mongodb import db
from bson import ObjectId


def latest_evaluation(student_email=None):

    result = db.evaluations.find_one(
        {"studentEmail": student_email} if student_email else {},
        sort=[("_id", -1)]
    )

    if not result:
        return None

    result["_id"] = str(result["_id"])

    return result


def evaluation_by_id(result_id, student_email=None):

    result = db.evaluations.find_one(
        {"_id": ObjectId(result_id), **({"studentEmail": student_email} if student_email else {})}
    )

    if not result:
        return None

    result["_id"] = str(result["_id"])

    return result
