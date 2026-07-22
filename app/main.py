import traceback

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.routes import router

from app.schemas import (
    EvaluationRequest,
    AutoEvaluationRequest,
    EvaluationResponse,
)

from app.core.gemini import generate_reference
from app.core.evaluator import evaluate_answer

from app.database.database import engine, get_db
from app.database.models import Base
from app.database.crud import (
    create_evaluation,
    get_all_evaluations
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Automated Answer Evaluation API",
    description="Backend API for OCR, answer parsing, AI evaluation and database storage",
    version="1.0.0"
)

# OCR + Answer Sheet API
app.include_router(router)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {
        "message": "Automated Answer Evaluation API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/generate-reference")
def generate_reference_api(request: QuestionRequest):
    return generate_reference(request.question)


@app.post("/evaluate")
def evaluate(request: EvaluationRequest):
    return evaluate_answer(
        expected_answer=request.expected_answer,
        student_answer=request.student_answer,
        keywords=request.keywords,
        concepts=request.concepts,
        rubric=request.rubric
    )


@app.post("/auto-evaluate")
def auto_evaluate(
    request: AutoEvaluationRequest,
    db: Session = Depends(get_db)
):
    try:
        reference = generate_reference(request.question)

        if "error" in reference:
            return {
                "status": "failed",
                "message": reference["error"]
            }

        result = evaluate_answer(
            expected_answer=reference["expected_answer"],
            student_answer=request.student_answer,
            keywords=reference["keywords"],
            concepts=reference["concepts"],
            rubric=reference["rubric"]
        )

        stored_evaluation = create_evaluation(
            db=db,
            question=request.question,
            model_answer=reference["expected_answer"],
            student_answer=request.student_answer,
            marks=float(result["final_score"]),
            grade=str(result["grade"]),
            feedback=str(result["feedback"])
        )

        result["reference"] = reference
        result["evaluation_id"] = stored_evaluation.id

        return result

    except Exception as error:
        traceback.print_exc()

        return {
            "status": "failed",
            "error": str(error)
        }


@app.get("/evaluations", response_model=list[EvaluationResponse])
def get_evaluations(
    db: Session = Depends(get_db)
):
    return get_all_evaluations(db)
