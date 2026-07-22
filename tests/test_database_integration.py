from __future__ import annotations

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import crud
from app.database.database import Base, get_db
from app.main import app
import app.main as main_module


def test_evaluation_crud_uses_the_current_sqlalchemy_schema(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'evaluations.db'}")
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine)()
    try:
        created = crud.create_evaluation(
            db=session,
            question="What is AI?",
            model_answer="Artificial intelligence.",
            student_answer="AI is machine intelligence.",
            marks=8.5,
            grade="A",
            feedback="Good coverage.",
        )
        assert created.id is not None
        assert crud.get_evaluation_by_id(session, created.id).grade == "A"
        assert len(crud.get_all_evaluations(session)) == 1
    finally:
        session.close()
        engine.dispose()


def test_evaluations_api_reads_from_the_dependency_session(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'api-evaluations.db'}")
    Base.metadata.create_all(bind=engine)
    testing_session = sessionmaker(bind=engine)

    def override_get_db():
        db = testing_session()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    try:
        with testing_session() as db:
            crud.create_evaluation(db, "Question", "Reference", "Student", 7.0, "B", "Feedback")
        response = TestClient(app).get("/evaluations")
    finally:
        app.dependency_overrides.pop(get_db, None)
        engine.dispose()

    assert response.status_code == 200
    assert response.json() == [{
        "id": 1,
        "question": "Question",
        "model_answer": "Reference",
        "student_answer": "Student",
        "marks": 7.0,
        "grade": "B",
        "feedback": "Feedback",
    }]


def test_auto_evaluate_persists_the_evaluation_through_get_db(tmp_path, monkeypatch):
    engine = create_engine(f"sqlite:///{tmp_path / 'auto-evaluate.db'}")
    Base.metadata.create_all(bind=engine)
    testing_session = sessionmaker(bind=engine)

    def override_get_db():
        db = testing_session()
        try:
            yield db
        finally:
            db.close()

    monkeypatch.setattr(
        main_module,
        "generate_reference",
        lambda question: {
            "expected_answer": "Reference answer",
            "keywords": ["reference"],
            "concepts": ["reference"],
            "rubric": {"reference": 10},
        },
    )
    monkeypatch.setattr(
        main_module,
        "evaluate_answer",
        lambda **kwargs: {"final_score": 9.0, "grade": "A", "feedback": ["✅ Good answer."]},
    )
    app.dependency_overrides[get_db] = override_get_db
    try:
        response = TestClient(app).post(
            "/auto-evaluate",
            json={"question": "Question", "student_answer": "Student"},
        )
        with testing_session() as db:
            records = crud.get_all_evaluations(db)
    finally:
        app.dependency_overrides.pop(get_db, None)
        engine.dispose()

    assert response.status_code == 200
    assert response.json()["evaluation_id"] == 1
    assert len(records) == 1
    assert records[0].feedback == "['✅ Good answer.']"
