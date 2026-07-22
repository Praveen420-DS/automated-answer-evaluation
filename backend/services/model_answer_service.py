from flask import request, jsonify

from services.document_service import extract_document

from parsers.question_parser import parse_questions

from parsers.model_answer_parser import parse_model_answers

from services.matching_service import (
    match_questions_with_answers
)

from services.model_answer_service import save_exam


def upload_exam():

    question_file = request.files["question_paper"]

    answer_file = request.files["model_answer"]

    question_text = extract_document(
        question_file.filename
    )

    answer_text = extract_document(
        answer_file.filename
    )

    questions = parse_questions(
        question_text
    )

    answers = parse_model_answers(
        answer_text
    )

    matched = match_questions_with_answers(
        questions,
        answers
    )

    exam = {

        "exam_name": request.form.get(
            "exam_name"
        ),

        "subject": request.form.get(
            "subject"
        ),

        "questions": matched

    }

    exam_id = save_exam(exam)

    return jsonify({

        "success": True,

        "exam_id": exam_id

    })