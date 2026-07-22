from sqlalchemy import Column, Integer, Float, String, Text
from app.database.database import Base


class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)

    question = Column(Text, nullable=False)

    model_answer = Column(Text, nullable=False)

    student_answer = Column(Text, nullable=False)

    marks = Column(Float, nullable=False)

    grade = Column(String(10), nullable=False)

    feedback = Column(Text, nullable=False)