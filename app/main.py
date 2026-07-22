from fastapi import FastAPI
<<<<<<< HEAD
from pydantic import BaseModel

from app.schemas import (
    EvaluationRequest,
    AutoEvaluationRequest
)

from app.core.gemini import generate_reference
from app.core.evaluator import evaluate_answer


# ---------------------------------------
# FastAPI
# ---------------------------------------
app = FastAPI(
    title="Automated Answer Evaluation API",
    description="AI Powered Automated Answer Evaluation System",
=======

from app.api.routes import router


app = FastAPI(
    title="Automated Answer Script Evaluation API",
    description="Backend API for automated answer sheet processing",
>>>>>>> backend-integration
    version="1.0.0"
)


<<<<<<< HEAD
# ---------------------------------------
# Request Model
# ---------------------------------------
class QuestionRequest(BaseModel):
    question: str


# ---------------------------------------
# Home
# ---------------------------------------
@app.get("/")
def home():

    return {
        "message": "Backend Running Successfully 🚀"
    }


# ---------------------------------------
# Health
# ---------------------------------------
@app.get("/health")
def health():

    return {
        "status": "Healthy"
    }


# ---------------------------------------
# Generate Reference
# ---------------------------------------
@app.post("/generate-reference")
def generate_reference_api(request: QuestionRequest):

    reference = generate_reference(request.question)

    return reference


# ---------------------------------------
# Evaluate
# ---------------------------------------
@app.post("/evaluate")
def evaluate(request: EvaluationRequest):

    result = evaluate_answer(
        expected_answer=request.expected_answer,
        student_answer=request.student_answer,
        keywords=request.keywords,
        concepts=request.concepts,
        rubric=request.rubric
    )

    return result


# ---------------------------------------
# Auto Evaluate
# ---------------------------------------
@app.post("/auto-evaluate")
def auto_evaluate(request: AutoEvaluationRequest):

    print("\n========== AUTO EVALUATION ==========")

    reference = generate_reference(request.question)

    print("Reference:")
    print(reference)

    # Check Gemini Error
    if "error" in reference:

        return {
            "status": "failed",
            "message": reference["error"]
        }

    # Validate Required Keys
    required = [
        "expected_answer",
        "keywords",
        "concepts",
        "rubric"
    ]

    for key in required:

        if key not in reference:

            return {
                "status": "failed",
                "message": f"Gemini did not return '{key}'",
                "response": reference
            }

    # Evaluate
    result = evaluate_answer(
        expected_answer=reference["expected_answer"],
        student_answer=request.student_answer,
        keywords=reference["keywords"],
        concepts=reference["concepts"],
        rubric=reference["rubric"]
    )

    result["reference"] = reference

    print("Evaluation Completed")

    return result
=======
app.include_router(router)


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
>>>>>>> backend-integration
