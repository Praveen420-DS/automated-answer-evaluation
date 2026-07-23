from flask import Blueprint, request, jsonify
from bson import ObjectId
from datetime import datetime
from uuid import uuid4
import os
from pathlib import Path
from werkzeug.utils import secure_filename
from parsers.question_parser import parse_questions

from middleware.auth_middleware import faculty_required
from flask_jwt_extended import get_jwt_identity

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
ALLOWED_DOCUMENT_EXTENSIONS = {".pdf", ".docx", ".png", ".jpg", ".jpeg"}

os.makedirs(QUESTION_FOLDER, exist_ok=True)
os.makedirs(ANSWER_KEY_FOLDER, exist_ok=True)


def _owned_exam(exam_id):
    """Return an exam only when it belongs to the authenticated faculty user."""
    try:
        return exams_collection().find_one({
            "_id": ObjectId(exam_id), "facultyId": get_jwt_identity(),
        })
    except Exception:
        return None


def _extract_document_text(filepath: Path) -> str:
    """Use the existing format parsers for faculty-uploaded text documents."""
    extension = filepath.suffix.lower()
    if extension == ".pdf":
        from parsers.pdf_parser import extract_pdf_text
        return extract_pdf_text(filepath)
    if extension == ".docx":
        from parsers.docx_parser import extract_docx_text
        return extract_docx_text(filepath)
    if extension in {".png", ".jpg", ".jpeg"}:
        from parsers.image_parser import extract_image_text
        return extract_image_text(filepath)
    raise ValueError("Only PDF, DOCX, PNG, JPG, and JPEG files are supported.")


def _valid_document_filename(filename: str) -> bool:
    return Path(filename).suffix.lower() in ALLOWED_DOCUMENT_EXTENSIONS


# =====================================================
# CREATE EXAM
# =====================================================

@faculty_bp.route("/create-exam", methods=["POST"])
@faculty_required
def create_exam():

    data = request.get_json(silent=True) or {}

    exam = {

        "examName": data.get("examName"),
        "title": data.get("title") or data.get("examName"),
        "subject": data.get("subject"),
        "department": data.get("department"),
        "semester": data.get("semester"),
        "totalMarks": data.get("totalMarks"),
        "facultyId": get_jwt_identity(),
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

    for exam in exams_collection().find({"facultyId": get_jwt_identity()}):

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

    exam = _owned_exam(exam_id)

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

    if not _owned_exam(exam_id):
        return jsonify({"success": False, "message": "Exam Not Found"}), 404
    exams_collection().update_one(
        {"_id": ObjectId(exam_id), "facultyId": get_jwt_identity()},

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

    if not _owned_exam(exam_id):
        return jsonify({"success": False, "message": "Exam Not Found"}), 404
    exams_collection().delete_one({"_id": ObjectId(exam_id), "facultyId": get_jwt_identity()})

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

    file = request.files.get("file")
    if not file or not file.filename:
        return jsonify({"success": False, "message": "No File Uploaded"}), 400
    exam_id = request.form.get("examId")
    if not exam_id:
        return jsonify({"success": False, "message": "examId is required"}), 400
    if not _owned_exam(exam_id):
        return jsonify({"success": False, "message": "Exam Not Found"}), 404
    try:
        ObjectId(exam_id)
    except Exception:
        return jsonify({"success": False, "message": "Invalid examId"}), 400

    filename = secure_filename(file.filename)
    if not filename:
        return jsonify({"success": False, "message": "Invalid filename"}), 400
    if not _valid_document_filename(filename):
        return jsonify({"success": False, "message": "Only PDF, DOCX, PNG, JPG, and JPEG files are supported."}), 400
    filepath = QUESTION_FOLDER / f"{uuid4().hex}{Path(filename).suffix.lower()}"

    try:
        file.save(filepath)
        text = _extract_document_text(filepath)
        questions = parse_questions(text)
    except Exception as error:
        filepath.unlink(missing_ok=True)
        return jsonify({"success": False, "message": f"Could not read question paper: {error}"}), 422
    if not questions:
        filepath.unlink(missing_ok=True)
        return jsonify({"success": False, "message": "No questions could be parsed. Use the expected Q1 ... (5 Marks) format."}), 422

    question_papers_collection().insert_one({
        "filename": filename, "path": str(filepath), "examId": exam_id,
        "uploadedAt": datetime.utcnow(),
    })

    inserted = []

    for q in questions:
        q["examId"] = exam_id
        q["questionNumber"] = q.get("number", q.get("questionNumber"))
        q["questionText"] = q.get("question", q.get("questionText", ""))
        q["maxMarks"] = q.get("marks", q.get("maxMarks", 0))
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
    file = request.files.get("file")
    exam_id = request.form.get("examId")
    if not exam_id:
        return jsonify({"success": False, "message": "examId is required"}), 400
    if not _owned_exam(exam_id):
        return jsonify({"success": False, "message": "Exam Not Found"}), 404
    try:
        ObjectId(exam_id)
    except Exception:
        return jsonify({"success": False, "message": "Invalid examId"}), 400

    if file and file.filename:
        filename = secure_filename(file.filename)
        if not filename:
            return jsonify({"success": False, "message": "Invalid filename"}), 400
        if not _valid_document_filename(filename):
            return jsonify({"success": False, "message": "Only PDF, DOCX, PNG, JPG, and JPEG files are supported."}), 400
        filepath = ANSWER_KEY_FOLDER / f"{uuid4().hex}{Path(filename).suffix.lower()}"
        file.save(filepath)
        answer_keys_collection().insert_one({"filename": filename, "path": str(filepath), "examId": exam_id, "uploadedAt": datetime.utcnow()})

    # A frontend may submit parsed reference answers alongside the source file.
    # Keeping this optional preserves existing file-only uploads.
    import json
    try:
        references = json.loads(request.form.get("referenceAnswers", "[]"))
    except ValueError:
        return jsonify({"success": False, "message": "referenceAnswers must be JSON"}), 400
    if not references:
        return jsonify({"success": False, "message": "Provide a source file or at least one reference answer."}), 400
    created_references = 0
    for reference in references:
        number = reference.get("questionNumber")
        answer = (reference.get("referenceAnswer") or "").strip()
        if number is None or not answer:
            return jsonify({"success": False, "message": "Each reference answer needs a questionNumber and referenceAnswer."}), 400
        question = questions_collection().find_one({"examId": exam_id, "questionNumber": number})
        if not question:
            return jsonify({"success": False, "message": f"Question {number} was not found for this exam."}), 400
        answer_keys_collection().update_one({"examId": exam_id, "questionNumber": number, "referenceAnswer": {"$exists": True}}, {"$set": {
            "examId": exam_id, "questionId": str(question["_id"]) if question else None,
            "questionNumber": number, "referenceAnswer": answer,
            "rubric": reference.get("rubric"), "keywords": reference.get("keywords", []),
            "concepts": reference.get("concepts", []), "updatedAt": datetime.utcnow(),
        }}, upsert=True)
        created_references += 1

    return jsonify({

        "success": True,

        "message": "Answer Key Uploaded Successfully",
        "referenceAnswersStored": created_references

    })


# =====================================================
# VIEW PARSED QUESTIONS
# =====================================================

@faculty_bp.route("/questions", methods=["GET"])
@faculty_required
def get_questions():

    data = []

    exam_id = request.args.get("examId")
    if exam_id and not _owned_exam(exam_id):
        return jsonify({"success": False, "message": "Exam Not Found"}), 404
    query = {"examId": exam_id} if exam_id else {"examId": {"$in": [str(item["_id"]) for item in exams_collection().find({"facultyId": get_jwt_identity()}, {"_id": 1})]}}
    for q in questions_collection().find(query):

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

    try:
        question = questions_collection().find_one({"_id": ObjectId(question_id)})
    except Exception:
        question = None
    if not question or not _owned_exam(question.get("examId")):
        return jsonify({"success": False, "message": "Question Not Found"}), 404
    questions_collection().delete_one({"_id": question["_id"]})

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
            "totalExams": exams_collection().count_documents({"facultyId": get_jwt_identity()}),
            "answerSheets": answer_scripts_collection().count_documents({"facultyId": get_jwt_identity()}),
            "evaluated": evaluations_collection().count_documents({"facultyId": get_jwt_identity(), "status": "evaluated"}),
            "students": users_collection().count_documents({"role": "student"})

        }

    })
