from flask import Blueprint, request, jsonify
from bson import ObjectId
from datetime import datetime
import os
from pathlib import Path
from werkzeug.utils import secure_filename

from middleware.auth_middleware import faculty_required

from database.mongodb import (
    exams_collection,
    question_papers_collection,
    answer_keys_collection,
    questions_collection,
    answer_scripts_collection,
    evaluations_collection,
    users_collection,
)


faculty_bp = Blueprint("faculty", __name__)

UPLOAD_ROOT = Path(__file__).resolve().parents[1] / "uploads"
QUESTION_FOLDER = UPLOAD_ROOT / "question_papers"
ANSWER_KEY_FOLDER = UPLOAD_ROOT / "answer_keys"

os.makedirs(QUESTION_FOLDER, exist_ok=True)
os.makedirs(ANSWER_KEY_FOLDER, exist_ok=True)


# =====================================================
# CREATE EXAM
# =====================================================

@faculty_bp.route("/create-exam", methods=["POST"])
@faculty_required
def create_exam():

    data = request.get_json()

    exam = {

        "examName": data.get("examName"),
        "subject": data.get("subject"),
        "department": data.get("department"),
        "semester": data.get("semester"),
        "totalMarks": data.get("totalMarks"),
        "createdAt": datetime.utcnow()

    }

    result = exams_collection().insert_one(exam)

    exam["_id"] = str(result.inserted_id)

    return jsonify({

        "success": True,
        "message": "Exam Created Successfully",
        "data": exam

    }), 201


# =====================================================
# GET ALL EXAMS
# =====================================================

@faculty_bp.route("/all-exams", methods=["GET"])
@faculty_required
def get_all_exams():

    exams = []

    for exam in exams_collection().find():

        exam["_id"] = str(exam["_id"])

        exams.append(exam)

    return jsonify({

        "success": True,

        "count": len(exams),

        "data": exams

    })


# =====================================================
# GET SINGLE EXAM
# =====================================================

@faculty_bp.route("/exam/<exam_id>", methods=["GET"])
@faculty_required
def get_exam(exam_id):

    exam = exams_collection().find_one({

        "_id": ObjectId(exam_id)

    })

    if exam is None:

        return jsonify({

            "success": False,

            "message": "Exam Not Found"

        }), 404

    exam["_id"] = str(exam["_id"])

    return jsonify({

        "success": True,

        "data": exam

    })


# =====================================================
# UPDATE EXAM
# =====================================================

@faculty_bp.route("/update-exam/<exam_id>", methods=["PUT"])
@faculty_required
def update_exam(exam_id):

    data = request.get_json()

    exams_collection().update_one(

        {

            "_id": ObjectId(exam_id)

        },

        {

            "$set": data

        }

    )

    return jsonify({

        "success": True,

        "message": "Exam Updated Successfully"

    })


# =====================================================
# DELETE EXAM
# =====================================================

@faculty_bp.route("/delete-exam/<exam_id>", methods=["DELETE"])
@faculty_required
def delete_exam(exam_id):

    exams_collection().delete_one({

        "_id": ObjectId(exam_id)

    })

    return jsonify({

        "success": True,

        "message": "Exam Deleted Successfully"

    })


# =====================================================
# UPLOAD QUESTION PAPER
# =====================================================

@faculty_bp.route("/upload-question-paper", methods=["POST"])
@faculty_required
def upload_question_paper():

    if "file" not in request.files:

        return jsonify({

            "success": False,

            "message": "No File Uploaded"

        }), 400

    file = request.files["file"]

    filename = secure_filename(file.filename)
    if not filename:
        return jsonify({"success": False, "message": "Invalid filename"}), 400
    filepath = QUESTION_FOLDER / filename

    file.save(filepath)

    question_papers_collection().insert_one({

        "filename": filename,

        "path": str(filepath),

        "uploadedAt": datetime.utcnow()

    })

    # OCR is imported only for this request so the API can start even when the
    # optional OCR extras have not yet been installed.
    from ai.question_parser import question_parser

    # OCR

    text = question_parser.extract_text(filepath)

    # Parse Questions

    questions = question_parser.parse_questions(text)

    inserted = []

    for q in questions:

        q["createdAt"] = datetime.utcnow()

        result = questions_collection().insert_one(q)

        q["_id"] = str(result.inserted_id)

        inserted.append(q)

    return jsonify({

        "success": True,

        "message": "Question Paper Uploaded Successfully",

        "questionsFound": len(inserted),

        "questions": inserted

    })


# =====================================================
# UPLOAD ANSWER KEY
# =====================================================

@faculty_bp.route("/upload-answer-key", methods=["POST"])
@faculty_required
def upload_answer_key():

    if "file" not in request.files:

        return jsonify({

            "success": False,

            "message": "No File Uploaded"

        }), 400

    file = request.files["file"]

    filename = secure_filename(file.filename)
    if not filename:
        return jsonify({"success": False, "message": "Invalid filename"}), 400
    filepath = ANSWER_KEY_FOLDER / filename

    file.save(filepath)

    answer_keys_collection().insert_one({

        "filename": filename,

        "path": str(filepath),

        "uploadedAt": datetime.utcnow()

    })

    return jsonify({

        "success": True,

        "message": "Answer Key Uploaded Successfully"

    })


# =====================================================
# VIEW PARSED QUESTIONS
# =====================================================

@faculty_bp.route("/questions", methods=["GET"])
@faculty_required
def get_questions():

    data = []

    for q in questions_collection().find():

        q["_id"] = str(q["_id"])

        data.append(q)

    return jsonify({

        "success": True,

        "count": len(data),

        "questions": data

    })


# =====================================================
# DELETE QUESTION
# =====================================================

@faculty_bp.route("/question/<question_id>", methods=["DELETE"])
@faculty_required
def delete_question(question_id):

    questions_collection().delete_one({

        "_id": ObjectId(question_id)

    })

    return jsonify({

        "success": True,

        "message": "Question Deleted"

    })


# =====================================================
# FACULTY DASHBOARD
# =====================================================

@faculty_bp.route("/dashboard", methods=["GET"])
@faculty_required
def dashboard():

    return jsonify({

        "success": True,

        "statistics": {
            "totalExams": exams_collection().count_documents({}),
            "answerSheets": answer_scripts_collection().count_documents({}),
            "evaluated": evaluations_collection().count_documents({"status": "evaluated"}),
            "students": users_collection().count_documents({"role": "student"})

        }

    })
