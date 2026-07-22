from flask import Blueprint, jsonify, send_file, send_from_directory, request
from flask_jwt_extended import get_jwt_identity
from bson import ObjectId
import os
from pathlib import Path
from uuid import uuid4
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from middleware.auth_middleware import student_required

from database.mongodb import (
    users_collection,
    evaluations_collection
)
from utils.student_excel import update_student_password

student_bp = Blueprint("student", __name__)
PROFILE_UPLOAD_DIRECTORY = Path(__file__).resolve().parents[1] / "uploads" / "profile_photos"
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def profile_payload(user):
    return {
        "name": user.get("fullName", ""),
        "email": user.get("email", ""),
        "mobile": user.get("mobile", ""),
        "department": user.get("department", "Not assigned"),
        "year": user.get("year", "Not assigned"),
        "photo": user.get("photo", ""),
        "role": user.get("role", "student"),
    }


# =====================================================
# STUDENT DASHBOARD
# =====================================================

@student_bp.route("/dashboard", methods=["GET"])
@student_required
def dashboard():

    email = get_jwt_identity()

    user = users_collection().find_one({
        "email": email
    })

    if not user:

        return jsonify({
            "success": False,
            "message": "Student not found"
        }), 404

    evaluations = list(
        evaluations_collection().find({
            "studentEmail": email
        })
    )

    total = len(evaluations)

    average = 0

    if total > 0:

        average = round(

            sum(x.get("marks", 0) for x in evaluations) / total,

            2

        )

    return jsonify({
        "name": user.get("fullName"),
        "email": user.get("email"),
        "registerNo": user.get("rollNo") or user.get("studentId", "—"),
        "department": user.get("department", "—"),
        "averageMarks": average,
        "completedExams": total,
        "exams": [
            {
                "examId": str(item.get("_id", "")),
                "subject": item.get("subject") or item.get("examName", "—"),
                "marks": item.get("marks", 0),
                "aiScore": item.get("aiScore", item.get("similarity", 0)),
                "status": item.get("status", "Pass" if item.get("marks", 0) >= 40 else "Pending"),
            }
            for item in evaluations
        ],
    })


# =====================================================
# PROFILE
# =====================================================

@student_bp.route("/profile", methods=["GET"])
@student_required
def profile():

    email = get_jwt_identity()

    user = users_collection().find_one({

        "email": email

    })

    if not user:

        return jsonify({

            "success": False,

            "message": "Student Not Found"

        }), 404

    return jsonify({
        "success": True,
        "data": profile_payload(user)
    })


# =====================================================
# UPDATE PROFILE
# =====================================================

@student_bp.route("/profile", methods=["PUT"])
@student_required
def update_profile():

    email = get_jwt_identity()

    data = request.get_json(silent=True) or {}
    user = users_collection().find_one({"email": email})
    if not user:
        return jsonify({"success": False, "message": "Student Not Found"}), 404

    full_name = (data.get("name") or "").strip()
    mobile = (data.get("mobile") or "").strip()
    if not full_name:
        return jsonify({"success": False, "message": "Name is required."}), 400

    updates = {"fullName": full_name, "mobile": mobile}
    new_password = data.get("newPassword") or ""
    if new_password:
        current_password = data.get("currentPassword") or ""
        if not current_password:
            return jsonify({"success": False, "message": "Enter your current password to set a new password."}), 400
        if not check_password_hash(user["password"], current_password):
            return jsonify({"success": False, "message": "Your current password is incorrect."}), 400
        if len(new_password) < 8:
            return jsonify({"success": False, "message": "Your new password must contain at least 8 characters."}), 400
        password_hash = generate_password_hash(new_password)
        try:
            workbook_updated = update_student_password(email=email, password_hash=password_hash)
            if not workbook_updated:
                return jsonify({"success": False, "message": "Student record was not found in the Excel workbook."}), 404
        except Exception:
            return jsonify({"success": False, "message": "Unable to save the new password to the student workbook."}), 500
        updates["password"] = password_hash

    users_collection().update_one({"email": email}, {"$set": updates})
    updated_user = users_collection().find_one({"email": email})

    return jsonify({

        "success": True,

        "message": "Profile Updated",
        "data": profile_payload(updated_user)
    })


@student_bp.route("/profile/photo", methods=["POST"])
@student_required
def upload_profile_photo():
    email = get_jwt_identity()
    image = request.files.get("photo")
    if not image or not image.filename:
        return jsonify({"success": False, "message": "Choose an image to upload."}), 400

    extension = Path(secure_filename(image.filename)).suffix.lower()
    if extension not in ALLOWED_IMAGE_EXTENSIONS or not (image.mimetype or "").startswith("image/"):
        return jsonify({"success": False, "message": "Use a JPG, PNG, or WEBP image."}), 400

    PROFILE_UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid4().hex}{extension}"
    image.save(PROFILE_UPLOAD_DIRECTORY / filename)
    photo_url = f"/api/student/profile/photo/{filename}"
    users_collection().update_one({"email": email}, {"$set": {"photo": photo_url}})
    return jsonify({"success": True, "message": "Profile photo updated.", "photo": photo_url})


@student_bp.route("/profile/photo/<filename>", methods=["GET"])
def get_profile_photo(filename):
    return send_from_directory(PROFILE_UPLOAD_DIRECTORY, filename)


# =====================================================
# ALL RESULTS
# =====================================================

@student_bp.route("/results", methods=["GET"])
@student_required
def results():

    email = get_jwt_identity()

    data = []

    cursor = evaluations_collection().find({

        "studentEmail": email

    })

    for item in cursor:

        item["_id"] = str(item["_id"])

        data.append(item)

    return jsonify({

        "success": True,

        "count": len(data),

        "results": data

    })


# =====================================================
# SINGLE RESULT
# =====================================================

@student_bp.route("/result/<evaluation_id>", methods=["GET"])
@student_required
def result(evaluation_id):

    email = get_jwt_identity()

    evaluation = evaluations_collection().find_one({

        "_id": ObjectId(evaluation_id),

        "studentEmail": email

    })

    if evaluation is None:

        return jsonify({

            "success": False,

            "message": "Result Not Found"

        }), 404

    evaluation["_id"] = str(evaluation["_id"])

    return jsonify({

        "success": True,

        "data": evaluation

    })


# =====================================================
# DOWNLOAD PDF REPORT
# =====================================================

@student_bp.route("/download/<evaluation_id>", methods=["GET"])
@student_required
def download(evaluation_id):

    email = get_jwt_identity()

    evaluation = evaluations_collection().find_one({

        "_id": ObjectId(evaluation_id),

        "studentEmail": email

    })

    if evaluation is None:

        return jsonify({

            "success": False,

            "message": "Evaluation Not Found"

        }), 404

    pdf = evaluation.get("pdfReport")

    if not pdf:

        return jsonify({

            "success": False,

            "message": "PDF Not Generated"

        }), 404

    if not os.path.exists(pdf):

        return jsonify({

            "success": False,

            "message": "File Missing"

        }), 404

    return send_file(

        pdf,

        as_attachment=True

    )


# =====================================================
# PERFORMANCE
# =====================================================

@student_bp.route("/performance", methods=["GET"])
@student_required
def performance():

    email = get_jwt_identity()

    cursor = evaluations_collection().find({

        "studentEmail": email

    })

    exams = []

    grades = {}

    total = 0

    marks = 0

    for item in cursor:

        total += 1

        score = item.get("marks", 0)

        grade = item.get("grade", "F")

        marks += score

        exams.append({

            "exam": item.get("examName"),

            "marks": score,

            "grade": grade

        })

        grades[grade] = grades.get(grade, 0) + 1

    average = 0

    if total > 0:

        average = round(

            marks / total,

            2

        )

    return jsonify({

        "success": True,

        "averageMarks": average,

        "gradeDistribution": grades,

        "history": exams

    })


# =====================================================
# RECENT RESULTS
# =====================================================

@student_bp.route("/recent", methods=["GET"])
@student_required
def recent():

    email = get_jwt_identity()

    data = []

    cursor = evaluations_collection().find({

        "studentEmail": email

    }).sort("evaluatedAt", -1).limit(5)

    for item in cursor:

        item["_id"] = str(item["_id"])

        data.append(item)

    return jsonify({

        "success": True,

        "recent": data

    })


# =====================================================
# STUDENT GRADES
# =====================================================

@student_bp.route("/grades", methods=["GET"])
@student_required
def grades():

    email = get_jwt_identity()

    cursor = evaluations_collection().find({

        "studentEmail": email

    })

    grade_list = []

    for item in cursor:

        grade_list.append({

            "exam": item.get("examName"),

            "grade": item.get("grade"),

            "marks": item.get("marks")

        })

    return jsonify({

        "success": True,

        "grades": grade_list

    })
