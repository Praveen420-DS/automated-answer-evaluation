from flask import Blueprint, request, jsonify
from datetime import datetime
import os
from pathlib import Path
from werkzeug.utils import secure_filename
from uuid import uuid4

from database.mongodb import (
    answer_scripts_collection,
    evaluations_collection,
    exams_collection,
    questions_collection,
    answer_keys_collection,
    users_collection,
    reports_collection,
    ensure_evaluation_indexes,
)
from bson import ObjectId
from flask_jwt_extended import get_jwt_identity

from middleware.auth_middleware import faculty_required
from services.app_ocr_adapter import OCRProcessingError, extract_and_parse
from services.evaluation_pipeline import evaluate_exam
from services.report_service import generate_evaluation_report

evaluation_bp = Blueprint("evaluation", __name__)

UPLOAD_FOLDER = Path(__file__).resolve().parents[1] / "uploads" / "answer_scripts"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@evaluation_bp.route("/start", methods=["POST"])
@faculty_required
def start_evaluation():
    ensure_evaluation_indexes()
    data = request.get_json(silent=True) or {}
    exam_id = data.get("examId")
    answer_sheet_id = data.get("answerSheetId")
    if not exam_id or not answer_sheet_id:
        return jsonify({"success": False, "message": "examId and answerSheetId are required."}), 400
    try:
        exam = exams_collection().find_one({"_id": ObjectId(exam_id)})
        answer_sheet = answer_scripts_collection().find_one({"_id": ObjectId(answer_sheet_id), "examId": exam_id})
    except Exception:
        return jsonify({"success": False, "message": "Invalid examId or answerSheetId."}), 400
    if not exam or not answer_sheet:
        return jsonify({"success": False, "message": "Exam or answer sheet was not found."}), 404

    questions = list(questions_collection().find({"examId": exam_id}).sort("questionNumber", 1))
    references = list(answer_keys_collection().find({"examId": exam_id, "referenceAnswer": {"$exists": True}}))
    if not questions or not references:
        return jsonify({"success": False, "message": "Questions and parsed reference answers are required before evaluation."}), 422
    reference_by_number = {str(item.get("questionNumber")): item for item in references}
    if not all(str(question.get("questionNumber")) in reference_by_number for question in questions):
        return jsonify({"success": False, "message": "A reference answer is missing for one or more questions."}), 422

    try:
        processed = extract_and_parse(answer_sheet["path"])
    except OCRProcessingError as error:
        answer_scripts_collection().update_one({"_id": answer_sheet["_id"]}, {"$set": {"ocrStatus": "failed", "ocrError": str(error), "updatedAt": datetime.utcnow()}})
        return jsonify({"success": False, "message": "OCR runtime unavailable. Check PaddleOCR/PyTorch installation.", "detail": str(error)}), 503

    student_answers = {str(answer.get("question_number")): answer.get("answer_text", "") for answer in processed["parsed_answers"] if answer.get("question_number") is not None}
    pipeline_questions = [{
        "number": str(question.get("questionNumber")), "question": question.get("questionText", question.get("question", "")),
        "marks": question.get("maxMarks", question.get("marks", 0)),
    } for question in questions]
    model_answers = {str(number): reference["referenceAnswer"] for number, reference in reference_by_number.items()}
    outcome = evaluate_exam(pipeline_questions, model_answers, student_answers)
    question_by_number = {str(question.get("questionNumber")): question for question in questions}
    question_results = []
    for item in outcome["questions"]:
        question = question_by_number[str(item["question_number"])]
        question_results.append({
            "questionNumber": item["question_number"], "questionId": str(question["_id"]),
            "score": item["score"], "maxScore": item["maximum_score"], "grade": item["grade"],
            "confidence": item["confidence"], "feedback": item["feedback"],
            "missingConcepts": item["missing_concepts"], "ocrText": item["student_answer"],
            "evaluationMetadata": item["evaluation_metadata"],
        })
    student = users_collection().find_one({"email": answer_sheet.get("studentEmail")}) or {}
    now = datetime.utcnow()
    evaluation = {
        "examId": exam_id, "examName": exam.get("examName", exam.get("title", "")), "subject": exam.get("subject", ""),
        "studentId": answer_sheet.get("studentId") or str(student.get("_id", "")), "studentEmail": answer_sheet.get("studentEmail"),
        "studentName": student.get("fullName", ""), "answerSheetId": str(answer_sheet["_id"]),
        "questionResults": question_results, "totalScore": outcome["summary"]["total_marks"],
        "marks": outcome["summary"]["total_marks"], "totalMarks": outcome["summary"]["maximum_marks"],
        "percentage": outcome["summary"]["percentage"], "overallGrade": outcome["summary"]["grade"],
        "grade": outcome["summary"]["grade"], "status": "evaluated", "createdAt": now, "updatedAt": now, "evaluatedAt": now,
    }
    existing = evaluations_collection().find_one({"answerSheetId": evaluation["answerSheetId"]})
    if existing:
        evaluations_collection().update_one({"_id": existing["_id"]}, {"$set": evaluation})
        evaluation_id = existing["_id"]
    else:
        evaluation_id = evaluations_collection().insert_one(evaluation).inserted_id
    evaluation["_id"] = evaluation_id
    report_path = generate_evaluation_report(evaluation)
    if report_path:
        evaluations_collection().update_one({"_id": evaluation_id}, {"$set": {"pdfReport": report_path}})
        reports_collection().update_one({"evaluationId": str(evaluation_id)}, {"$set": {"evaluationId": str(evaluation_id), "examId": exam_id, "studentEmail": evaluation["studentEmail"], "path": report_path, "updatedAt": now}, "$setOnInsert": {"createdAt": now}}, upsert=True)
    answer_scripts_collection().update_one({"_id": answer_sheet["_id"]}, {"$set": {"ocrStatus": "completed", "ocr": processed["ocr"], "parsedAnswers": processed["parsed_answers"], "updatedAt": now}})
    return jsonify({"success": True, "evaluationId": str(evaluation_id), "summary": outcome["summary"], "questionResults": question_results, "reportAvailable": bool(report_path)}), 200


# ==========================================
# Upload Student Answer Sheet
# ==========================================

@evaluation_bp.route("/upload-answer-sheet", methods=["POST"])
@faculty_required
def upload_answer_sheet():

    if "file" not in request.files:

        return jsonify({
            "success": False,
            "message": "No file uploaded"
        }), 400

    file = request.files["file"]
    exam_id = request.form.get("examId")
    student_email = (request.form.get("studentEmail") or "").strip().lower()
    if not exam_id or not student_email:
        return jsonify({"success": False, "message": "examId and studentEmail are required"}), 400
    try:
        if not exams_collection().find_one({"_id": ObjectId(exam_id)}):
            return jsonify({"success": False, "message": "Exam Not Found"}), 404
    except Exception:
        return jsonify({"success": False, "message": "Invalid examId"}), 400
    student = users_collection().find_one({"email": student_email, "role": "student"})
    if not student:
        return jsonify({"success": False, "message": "Student Not Found"}), 404

    filename = secure_filename(file.filename)
    if not filename:
        return jsonify({"success": False, "message": "Invalid filename"}), 400

    filepath = UPLOAD_FOLDER / f"{uuid4().hex}{Path(filename).suffix.lower()}"

    file.save(filepath)

    result = answer_scripts_collection().insert_one({

        "filename": filename,
        "path": str(filepath),
        "examId": exam_id,
        "studentId": str(student["_id"]),
        "studentEmail": student_email,
        "ocrStatus": "pending",
        "uploadedAt": datetime.utcnow()

    }).inserted_id

    return jsonify({

        "success": True,
        "message": "Answer Sheet Uploaded Successfully",
        "file": filename,
        "answerSheetId": str(result)

    })


# ==========================================
# OCR Extraction
# ==========================================

@evaluation_bp.route("/ocr/<filename>", methods=["GET"])
@faculty_required
def run_ocr(filename):

    filename = secure_filename(filename)
    filepath = UPLOAD_FOLDER / filename

    if not os.path.exists(filepath):

        return jsonify({

            "success": False,
            "message": "File Not Found"

        }), 404

    try:
        result = extract_and_parse(filepath)
    except OCRProcessingError as error:
        return jsonify({
            "success": False,
            "message": str(error)
        }), 422

    evaluations_collection().insert_one({

        "filename": filename,
        "ocrText": result["ocr"]["full_text"],
        "ocr": result["ocr"],
        "parsedAnswers": result["parsed_answers"],
        "createdAt": datetime.utcnow()

    })

    return jsonify({

        "success": True,
        "filename": filename,
        "text": result["ocr"]["full_text"],
        "parsedAnswers": result["parsed_answers"],

    })


# ==========================================
# View OCR Result
# ==========================================

@evaluation_bp.route("/ocr-results", methods=["GET"])
@faculty_required
def get_results():

    data = []

    for doc in evaluations_collection().find():

        doc["_id"] = str(doc["_id"])

        data.append(doc)

    return jsonify({

        "success": True,
        "count": len(data),
        "data": data

    })
