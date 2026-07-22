from database.mongodb import db
from bson import ObjectId


def latest_evaluation():

    result = db.evaluations.find_one(
        {},
        sort=[("_id", -1)]
    )

    if not result:
        return None

    result["_id"] = str(result["_id"])

    return result


def evaluation_by_id(result_id):

    result = db.evaluations.find_one(
        {
            "_id": ObjectId(result_id)
        }
    )

    if not result:
        return None

    result["_id"] = str(result["_id"])

    return result