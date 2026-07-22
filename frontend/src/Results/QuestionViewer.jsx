import React from "react";
import "./QuestionViewer.css";

const QuestionViewer = ({ question }) => {

    if (!question) {
        return (
            <div className="empty-viewer">

                <h2>
                    Select a Question
                </h2>

            </div>
        );
    }

    return (

        <div className="viewer">

            {/* Question */}

            <div className="viewer-card">

                <h2>
                    Question
                </h2>

                <p>
                    {question.question}
                </p>

            </div>

            {/* Model Answer */}

            <div className="viewer-card">

                <h2>
                    Model Answer
                </h2>

                <p>
                    {question.model_answer}
                </p>

            </div>

            {/* Student Answer */}

            <div className="viewer-card">

                <h2>
                    Student Answer
                </h2>

                <p>
                    {question.student_answer}
                </p>

            </div>

            {/* AI Feedback */}

            <div className="viewer-card">

                <h2>
                    AI Feedback
                </h2>

                <p>
                    {question.feedback}
                </p>

            </div>

        </div>

    );
};

export default QuestionViewer;