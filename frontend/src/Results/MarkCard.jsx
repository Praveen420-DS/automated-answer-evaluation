import React from "react";
import "./MarksCard.css";

const MarksCard = ({ question }) => {

    if (!question) return null;

    return (

        <div className="marks-grid">

            <div className="marks-box">

                <h2>
                    {question.obtained_marks}
                </h2>

                <span>
                    Obtained
                </span>

            </div>

            <div className="marks-box">

                <h2>
                    {question.total_marks}
                </h2>

                <span>
                    Total
                </span>

            </div>

            <div className="marks-box">

                <h2>
                    {question.similarity_score}%
                </h2>

                <span>
                    Similarity
                </span>

            </div>

        </div>

    );
};

export default MarksCard;