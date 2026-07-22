from __future__ import annotations

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.evaluation.deterministic_evaluator import evaluate_answers
from app.feedback.feedback_generator import generate_feedback
from app.ocr.extractor import extract_document
from app.ocr.input_handler import (
    InputValidationError,
    cleanup_path,
    save_upload_file,
)
from app.parser.answer_parser import parse_ocr_result


router = APIRouter(prefix="/api", tags=["Answer Sheet"])


@router.post("/upload")
async def upload_answer_sheet(
    file: UploadFile = File(...),
    expected_answer: str | None = Form(default=None),
    maximum_score: float = Form(default=10.0),
):
    saved_path = None

    try:
        saved_path = save_upload_file(file)

        ocr_result = extract_document(saved_path)
        parsed_answers = parse_ocr_result(ocr_result)
        evaluation = evaluate_answers(
            parsed_answers,
            expected_answer=expected_answer,
            maximum_score=maximum_score,
        )
        feedback = generate_feedback(evaluation)

        return {
            "success": True,
            "filename": file.filename,
            "ocr": ocr_result.model_dump(),
            "parsed_answers": parsed_answers,
            "evaluation": evaluation,
            "feedback": feedback,
        }

    except InputValidationError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Processing failed: {error}") from error

    finally:
        if saved_path is not None:
            cleanup_path(saved_path)


@router.post("/ocr")
async def ocr_only(file: UploadFile = File(...)):
    saved_path = None

    try:
        saved_path = save_upload_file(file)
        ocr_result = extract_document(saved_path)
        return {
            "success": True,
            "filename": file.filename,
            "ocr": ocr_result.model_dump(),
        }

    except InputValidationError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    except Exception as error:
        raise HTTPException(status_code=500, detail=f"OCR failed: {error}") from error

    finally:
        if saved_path is not None:
            cleanup_path(saved_path)
