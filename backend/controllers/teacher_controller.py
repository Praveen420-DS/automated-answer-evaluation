import os
import uuid
from datetime import datetime

from bson import ObjectId
from flask import jsonify, request

from database.mongodb import db
from services.document_service import extract_document
from parsers.question_parser import parse_questions
from parsers.model_answer_parser import parse_model_answers
from services.matching_service import match_questions_with_answers

UPLOAD_FOLDER = "uploads/exams"


# ==========================================================
# Upload Exam
# ==========================================================

def upload_exam():
    try:

        if "question_paper" not in request.files:
            return jsonify({
                "success": False,
                "message": "Question paper is required."
            }), 400

        if "model_answer" not in request.files:
            return jsonify({
                "success": False,
                "message": "Model answer is required."
            }), 400

        question_file = request.files["question_paper"]
        answer_file = request.files["model_answer"]

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        question_name = (
            str(uuid.uuid4()) + "_" + question_file.filename
        )

        answer_name = (
            str(uuid.uuid4()) + "_" + answer_file.filename
        )

        question_path = os.path.join(
            UPLOAD_FOLDER,
            question_name
        )

        answer_path = os.path.join(
            UPLOAD_FOLDER,
            answer_name
        )

        question_file.save(question_path)
        answer_file.save(answer_path)

        question_text = extract_document(question_path)
        answer_text = extract_document(answer_path)

        questions = parse_questions(question_text)

        model_answers = parse_model_answers(answer_text)

        matched_questions = match_questions_with_answers(
            questions,
            model_answers
        )

        exam = {

            "teacher_id": request.form.get("teacher_id"),

            "exam_name": request.form.get("exam_name"),

            "subject": request.form.get("subject"),

            "department": request.form.get("department"),

            "year": request.form.get("year"),

            "semester": request.form.get("semester"),

            "question_paper": question_name,

            "model_answer_file": answer_name,

            "questions": matched_questions,

            "status": "ACTIVE",

            "created_at": datetime.utcnow()

        }

        result = db.exams.insert_one(exam)

        return jsonify({

            "success": True,

            "message": "Exam uploaded successfully.",

            "exam_id": str(result.inserted_id)

        }), 201

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 500


# ==========================================================
# Get All Exams
# ==========================================================

def get_all_exams():

    try:

        exams = []

        for exam in db.exams.find():

            exam["_id"] = str(exam["_id"])

            exams.append(exam)

        return jsonify({

            "success": True,

            "count": len(exams),

            "data": exams

        }), 200

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 500


# ==========================================================
# Get One Exam
# ==========================================================

def get_exam(exam_id):

    try:

        exam = db.exams.find_one({

            "_id": ObjectId(exam_id)

        })

        if exam is None:

            return jsonify({

                "success": False,

                "message": "Exam not found."

            }), 404

        exam["_id"] = str(exam["_id"])

        return jsonify({

            "success": True,

            "data": exam

        }), 200

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 500


# ==========================================================
# Update Exam
# ==========================================================

def update_exam(exam_id):

    try:

        body = request.json

        db.exams.update_one(

            {

                "_id": ObjectId(exam_id)

            },

            {

                "$set": body

            }

        )

        return jsonify({

            "success": True,

            "message": "Exam updated successfully."

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 500


# ==========================================================
# Delete Exam
# ==========================================================

def delete_exam(exam_id):

    try:

        result = db.exams.delete_one({

            "_id": ObjectId(exam_id)

        })

        if result.deleted_count == 0:

            return jsonify({

                "success": False,

                "message": "Exam not found."

            }), 404

        return jsonify({

            "success": True,

            "message": "Exam deleted successfully."

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 500