import traceback

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.schemas import (
    EvaluationRequest,
    AutoEvaluationRequest
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
    version="1.0.0"
)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "Backend Running Successfully 🚀"}


@app.get("/health")
def health():
    return {"status": "Healthy"}


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

        print("\n========== AUTO EVALUATION ==========")

        reference = generate_reference(request.question)

        print("Gemini Response:")
        print(reference)

        if "error" in reference:
            return reference

        result = evaluate_answer(
            expected_answer=reference["expected_answer"],
            student_answer=request.student_answer,
            keywords=reference["keywords"],
            concepts=reference["concepts"],
            rubric=reference["rubric"]
        )

        print("\nEvaluation Result:")
        print(result)

        create_evaluation(
      create_evaluation(
    db=db,
    question=request.question,
    model_answer=reference["expected_answer"],
    student_answer=request.student_answer,
    marks=float(result["final_score"]),
    grade=str(result["grade"]),
    feedback=str(result["feedback"])
)
        )

        print("Saved Successfully")

        return result

    except Exception as e:

        traceback.print_exc()

        return {
            "status": "failed",
            "error": str(e)
        }


@app.get("/evaluations")
def get_evaluations(
    db: Session = Depends(get_db)
):
    return get_all_evaluations(db)