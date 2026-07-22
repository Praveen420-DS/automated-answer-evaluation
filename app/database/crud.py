from sqlalchemy.orm import Session

from app.database.models import Evaluation


def create_evaluation(
    db: Session,
    question: str,
    model_answer: str,
    student_answer: str,
    marks: float,
    grade: str,
    feedback: str,
):
    evaluation = Evaluation(
        question=question,
        model_answer=model_answer,
        student_answer=student_answer,
        marks=marks,
        grade=grade,
        feedback=feedback,
    )

    db.add(evaluation)
    db.commit()
    db.refresh(evaluation)

    return evaluation


def get_all_evaluations(db: Session):
    return db.query(Evaluation).all()


def get_evaluation_by_id(db: Session, evaluation_id: int):
    return (
        db.query(Evaluation)
        .filter(Evaluation.id == evaluation_id)
        .first()
    )


def delete_evaluation(db: Session, evaluation_id: int):
    evaluation = (
        db.query(Evaluation)
        .filter(Evaluation.id == evaluation_id)
        .first()
    )

    if evaluation:
        db.delete(evaluation)
        db.commit()

    return evaluation