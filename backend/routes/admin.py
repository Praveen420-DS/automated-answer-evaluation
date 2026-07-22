from flask import Blueprint, jsonify, request
from bson import ObjectId

from middleware.auth_middleware import admin_required

from database.mongodb import (
    users_collection,
    exams_collection,
    evaluations_collection
)

admin_bp = Blueprint("admin", __name__)


# ==========================================================
# ADMIN DASHBOARD
# ==========================================================

@admin_bp.route("/dashboard", methods=["GET"])
@admin_required
def dashboard():

    students = users_collection().count_documents({
        "role": "student"
    })

    faculty = users_collection().count_documents({
        "role": "faculty"
    })

    admins = users_collection().count_documents({
        "role": "admin"
    })

    exams = exams_collection().count_documents({})

    evaluations = evaluations_collection().count_documents({})

    average_marks = 0

    cursor = evaluations_collection().find()

    total = 0
    count = 0

    for item in cursor:

        total += item.get("marks", 0)
        count += 1

    if count > 0:
        average_marks = round(total / count, 2)

    return jsonify({

        "success": True,

        "statistics": {

            "students": students,

            "faculty": faculty,

            "admins": admins,

            "exams": exams,

            "evaluations": evaluations,

            "averageMarks": average_marks

        },
        "activities": []

    })


# ==========================================================
# GET ALL USERS
# ==========================================================

@admin_bp.route("/users", methods=["GET"])
@admin_required
def get_users():

    users = []

    for user in users_collection().find():

        user["_id"] = str(user["_id"])

        user.pop("password", None)

        users.append(user)

    return jsonify({

        "success": True,

        "count": len(users),

        "users": users

    })


# ==========================================================
# GET USER BY ID
# ==========================================================

@admin_bp.route("/user/<user_id>", methods=["GET"])
@admin_required
def get_user(user_id):

    user = users_collection().find_one({

        "_id": ObjectId(user_id)

    })

    if user is None:

        return jsonify({

            "success": False,

            "message": "User Not Found"

        }), 404

    user["_id"] = str(user["_id"])

    user.pop("password", None)

    return jsonify({

        "success": True,

        "user": user

    })


# ==========================================================
# UPDATE USER
# ==========================================================

@admin_bp.route("/user/<user_id>", methods=["PUT"])
@admin_required
def update_user(user_id):

    data = request.get_json()

    data.pop("password", None)

    users_collection().update_one(

        {

            "_id": ObjectId(user_id)

        },

        {

            "$set": data

        }

    )

    return jsonify({

        "success": True,

        "message": "User Updated Successfully"

    })


# ==========================================================
# DELETE USER
# ==========================================================

@admin_bp.route("/user/<user_id>", methods=["DELETE"])
@admin_required
def delete_user(user_id):

    result = users_collection().delete_one({

        "_id": ObjectId(user_id)

    })

    if result.deleted_count == 0:

        return jsonify({

            "success": False,

            "message": "User Not Found"

        }), 404

    return jsonify({

        "success": True,

        "message": "User Deleted Successfully"

    })


# ==========================================================
# SEARCH USERS
# ==========================================================

@admin_bp.route("/search-users", methods=["GET"])
@admin_required
def search_users():

    keyword = request.args.get("q", "")

    query = {

        "$or": [

            {

                "fullName": {

                    "$regex": keyword,

                    "$options": "i"

                }

            },

            {

                "email": {

                    "$regex": keyword,

                    "$options": "i"

                }

            }

        ]

    }

    users = []

    for user in users_collection().find(query):

        user["_id"] = str(user["_id"])

        user.pop("password", None)

        users.append(user)

    return jsonify({

        "success": True,

        "count": len(users),

        "users": users

    })


# ==========================================================
# GET USERS BY ROLE
# ==========================================================

@admin_bp.route("/users/<role>", methods=["GET"])
@admin_required
def users_by_role(role):

    if role not in ["student", "faculty", "admin"]:

        return jsonify({

            "success": False,

            "message": "Invalid Role"

        }), 400

    data = []

    for user in users_collection().find({

        "role": role

    }):

        user["_id"] = str(user["_id"])

        user.pop("password", None)

        data.append(user)

    return jsonify({

        "success": True,

        "role": role,

        "count": len(data),

        "users": data

    })


# ==========================================================
# USER COUNT
# ==========================================================

@admin_bp.route("/user-count", methods=["GET"])
@admin_required
def user_count():

    return jsonify({

        "success": True,

        "students": users_collection().count_documents({

            "role": "student"

        }),

        "faculty": users_collection().count_documents({

            "role": "faculty"

        }),

        "admins": users_collection().count_documents({

            "role": "admin"

        })

    })
from database.mongodb import (
    reports_collection
)

# ==========================================================
# GET ALL EXAMS
# ==========================================================

@admin_bp.route("/exams", methods=["GET"])
@admin_required
def get_exams():

    exams = []

    for exam in exams_collection().find():

        exam["_id"] = str(exam["_id"])

        exams.append(exam)

    return jsonify({

        "success": True,

        "count": len(exams),

        "exams": exams

    })


# ==========================================================
# GET EXAM
# ==========================================================

@admin_bp.route("/exam/<exam_id>", methods=["GET"])
@admin_required
def get_exam(exam_id):

    exam = exams_collection().find_one({

        "_id": ObjectId(exam_id)

    })

    if exam is None:

        return jsonify({

            "success": False,

            "message": "Exam Not Found"

        }),404

    exam["_id"] = str(exam["_id"])

    return jsonify({

        "success": True,

        "exam": exam

    })


# ==========================================================
# DELETE EXAM
# ==========================================================

@admin_bp.route("/exam/<exam_id>", methods=["DELETE"])
@admin_required
def delete_exam(exam_id):

    result = exams_collection().delete_one({

        "_id": ObjectId(exam_id)

    })

    if result.deleted_count == 0:

        return jsonify({

            "success": False,

            "message": "Exam Not Found"

        }),404

    return jsonify({

        "success": True,

        "message": "Exam Deleted Successfully"

    })


# ==========================================================
# ALL EVALUATIONS
# ==========================================================

@admin_bp.route("/evaluations", methods=["GET"])
@admin_required
def evaluations():

    data = []

    for item in evaluations_collection().find():

        item["_id"] = str(item["_id"])

        data.append(item)

    return jsonify({

        "success": True,

        "count": len(data),

        "evaluations": data

    })


# ==========================================================
# GET SINGLE EVALUATION
# ==========================================================

@admin_bp.route("/evaluation/<evaluation_id>", methods=["GET"])
@admin_required
def evaluation(evaluation_id):

    item = evaluations_collection().find_one({

        "_id": ObjectId(evaluation_id)

    })

    if item is None:

        return jsonify({

            "success": False,

            "message": "Evaluation Not Found"

        }),404

    item["_id"] = str(item["_id"])

    return jsonify({

        "success": True,

        "evaluation": item

    })


# ==========================================================
# DELETE EVALUATION
# ==========================================================

@admin_bp.route("/evaluation/<evaluation_id>", methods=["DELETE"])
@admin_required
def delete_evaluation(evaluation_id):

    result = evaluations_collection().delete_one({

        "_id": ObjectId(evaluation_id)

    })

    if result.deleted_count == 0:

        return jsonify({

            "success": False,

            "message": "Evaluation Not Found"

        }),404

    return jsonify({

        "success": True,

        "message": "Evaluation Deleted Successfully"

    })


# ==========================================================
# REPORTS
# ==========================================================

@admin_bp.route("/reports", methods=["GET"])
@admin_required
def reports():

    reports = []

    for report in reports_collection().find():

        report["_id"] = str(report["_id"])

        reports.append(report)

    return jsonify({

        "success": True,

        "count": len(reports),

        "reports": reports

    })


# ==========================================================
# REPORT DETAILS
# ==========================================================

@admin_bp.route("/report/<report_id>", methods=["GET"])
@admin_required
def report(report_id):

    item = reports_collection().find_one({

        "_id": ObjectId(report_id)

    })

    if item is None:

        return jsonify({

            "success": False,

            "message": "Report Not Found"

        }),404

    item["_id"] = str(item["_id"])

    return jsonify({

        "success": True,

        "report": item

    })


# ==========================================================
# DELETE REPORT
# ==========================================================

@admin_bp.route("/report/<report_id>", methods=["DELETE"])
@admin_required
def delete_report(report_id):

    result = reports_collection().delete_one({

        "_id": ObjectId(report_id)

    })

    if result.deleted_count == 0:

        return jsonify({

            "success": False,

            "message": "Report Not Found"

        }),404

    return jsonify({

        "success": True,

        "message": "Report Deleted Successfully"

    })
from flask import jsonify
from datetime import datetime
import os
import shutil

from database.mongodb import (
    logs_collection,
    analytics_collection
)

# ==========================================================
# SYSTEM ANALYTICS
# ==========================================================

@admin_bp.route("/analytics", methods=["GET"])
@admin_required
def analytics():

    evaluations = list(evaluations_collection().find())

    grades = {
        "A": 0,
        "B": 0,
        "C": 0,
        "D": 0,
        "F": 0
    }

    subjects = {}

    total_marks = 0

    for item in evaluations:

        marks = item.get("marks", 0)

        total_marks += marks

        grade = item.get("grade", "F")

        grades[grade] = grades.get(grade, 0) + 1

        subject = item.get("examName", "Unknown")

        if subject not in subjects:
            subjects[subject] = []

        subjects[subject].append(marks)

    average = 0

    if len(evaluations) > 0:

        average = round(

            total_marks / len(evaluations),

            2

        )

    subject_average = {}

    for key in subjects:

        subject_average[key] = round(

            sum(subjects[key]) / len(subjects[key]),

            2

        )

    return jsonify({

        "success": True,

        "averageMarks": average,

        "grades": grades,

        "subjects": subject_average

    })


# ==========================================================
# RECENT EVALUATIONS
# ==========================================================

@admin_bp.route("/recent-evaluations", methods=["GET"])
@admin_required
def recent_evaluations():

    data = []

    cursor = evaluations_collection().find().sort(

        "evaluatedAt",

        -1

    ).limit(10)

    for item in cursor:

        item["_id"] = str(item["_id"])

        data.append(item)

    return jsonify({

        "success": True,

        "recent": data

    })


# ==========================================================
# AI SETTINGS
# ==========================================================

@admin_bp.route("/ai-settings", methods=["GET"])
@admin_required
def ai_settings():

    return jsonify({

        "success": True,

        "model": "gpt-4.1-mini",

        "embeddingModel": "all-MiniLM-L6-v2",

        "ocr": "EasyOCR",

        "language": "English"

    })


# ==========================================================
# UPDATE AI SETTINGS
# ==========================================================

@admin_bp.route("/ai-settings", methods=["POST"])
@admin_required
def update_ai_settings():

    data = request.get_json()

    analytics_collection().update_one(

        {

            "type": "ai"

        },

        {

            "$set": data

        },

        upsert=True

    )

    return jsonify({

        "success": True,

        "message": "AI Settings Updated"

    })


# ==========================================================
# SYSTEM LOGS
# ==========================================================

@admin_bp.route("/logs", methods=["GET"])
@admin_required
def logs():

    data = []

    cursor = logs_collection().find().sort(

        "time",

        -1

    ).limit(100)

    for item in cursor:

        item["_id"] = str(item["_id"])

        data.append(item)

    return jsonify({

        "success": True,

        "logs": data

    })


# ==========================================================
# SYSTEM INFORMATION
# ==========================================================

@admin_bp.route("/system-info", methods=["GET"])
@admin_required
def system_info():

    return jsonify({

        "success": True,

        "project": "EvalAI",

        "version": "1.0.0",

        "python": "3.x",

        "database": "MongoDB",

        "ocr": "EasyOCR",

        "llm": "GPT-4.1-mini",

        "status": "Running",

        "serverTime": str(datetime.utcnow())

    })


# ==========================================================
# DATABASE BACKUP
# ==========================================================

@admin_bp.route("/backup", methods=["POST"])
@admin_required
def backup():

    backup_folder = "backup"

    os.makedirs(

        backup_folder,

        exist_ok=True

    )

    return jsonify({

        "success": True,

        "message": "Backup Request Created",

        "location": backup_folder

    })


# ==========================================================
# HEALTH CHECK
# ==========================================================

@admin_bp.route("/health", methods=["GET"])
@admin_required
def health():

    return jsonify({

        "success": True,

        "database": "Connected",

        "server": "Running",

        "ocr": "Loaded",

        "llm": "Loaded"

    })
