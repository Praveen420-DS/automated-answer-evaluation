import React, { useState } from "react";
import "./QuestionList.css";

const QuestionList = ({ questions }) => {
  const [selectedQuestion, setSelectedQuestion] = useState(0);

  if (!questions || questions.length === 0) {
    return (
      <div className="empty-question">
        <h3>No Evaluated Questions Available</h3>
        <p>
          Upload a Question Paper, Model Answer and
          Student Answer Script to view evaluation.
        </p>
      </div>
    );
  }

  const current = questions[selectedQuestion];

  return (
    <div className="question-layout">

      {/* ================= Left Panel ================= */}

      <div className="question-sidebar">

        <h2>Question List</h2>

        {questions.map((question, index) => (

          <div
            key={index}
            className={
              selectedQuestion === index
                ? "question-item active-question"
                : "question-item"
            }
            onClick={() => setSelectedQuestion(index)}
          >

            <div>

              <h4>
                Question {question.question_number}
              </h4>

              <p>
                {question.question.substring(0,60)}...
              </p>

            </div>

            <span>

              {question.obtained_marks}/
              {question.total_marks}

            </span>

          </div>

        ))}

      </div>

      {/* ================= Right Panel ================= */}

      <div className="answer-panel">

        <div className="question-card">

          <h2>
            Question {current.question_number}
          </h2>

          <p>
            {current.question}
          </p>

        </div>

        <div className="answer-card">

          <h3>
            Model Answer
          </h3>

          <p>

            {current.model_answer}

          </p>

        </div>

        <div className="answer-card">

          <h3>
            Student Answer
          </h3>

          <p>

            {current.student_answer}

          </p>

        </div>

        <div className="feedback-card">

          <h3>
            AI Feedback
          </h3>

          <p>

            {current.feedback}

          </p>

        </div>

        <div className="marks-card">

          <div>

            <h2>

              {current.obtained_marks}

            </h2>

            <p>

              Marks Obtained

            </p>

          </div>

          <div>

            <h2>

              {current.total_marks}

            </h2>

            <p>

              Total Marks

            </p>

          </div>

          <div>

            <h2>

              {current.similarity_score}%

            </h2>

            <p>

              AI Similarity

            </p>

          </div>

        </div>

      </div>

    </div>
  );
};

export default QuestionList;