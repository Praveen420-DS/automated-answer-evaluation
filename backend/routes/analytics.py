from flask import Blueprint, jsonify
from database.mongodb import (
    evaluations_collection,
    exams_collection,
    users_collection
)
from middleware.auth_middleware import admin_required

analytics_bp = Blueprint("analytics", __name__)


# ===========================================
# Dashboard Statistics
# ===========================================

@analytics_bp.route("/dashboard", methods=["GET"])
@admin_required
def dashboard():

    evaluations = list(evaluations_collection().find())
    exams = list(exams_collection().find())

    students = users_collection().count_documents({
        "role": "student"
    })

    faculty = users_collection().count_documents({
        "role": "faculty"
    })

    total_marks = 0

    grade_count = {
        "A":0,
        "B":0,
        "C":0,
        "D":0,
        "F":0
    }

    pass_count = 0

    subject_stats = {}

    recent = []

    for item in evaluations:

        marks = item.get("marks",0)

        total_marks += marks

        grade = item.get("grade","F")

        grade_count[grade] += 1

        if marks >= 40:

            pass_count += 1

        subject = item.get("examName","Unknown")

        if subject not in subject_stats:

            subject_stats[subject]=[]

        subject_stats[subject].append(marks)

        recent.append({

            "student":item.get("studentName"),

            "exam":item.get("examName"),

            "marks":marks,

            "grade":grade

        })

    average_marks = 0

    if len(evaluations)>0:

        average_marks = round(

            total_marks/len(evaluations),

            2

        )

    pass_percentage = 0

    if len(evaluations)>0:

        pass_percentage = round(

            pass_count*100/len(evaluations),

            2

        )

    subject_average = {}

    for key in subject_stats:

        subject_average[key]=round(

            sum(subject_stats[key])/len(subject_stats[key]),

            2

        )

    return jsonify({

        "success":True,

        "statistics":{

            "students":students,

            "faculty":faculty,

            "totalExams":len(exams),

            "evaluations":len(evaluations),

            "averageMarks":average_marks,

            "passPercentage":pass_percentage

        },

        "grades":grade_count,

        "subjects":subject_average,

        "recent":recent[-10:]

    })