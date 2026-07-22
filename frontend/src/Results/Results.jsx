import React, { useEffect, useState } from "react";
import axios from "axios";
import "./Results.css";

const Results = () => {
  const [evaluation, setEvaluation] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchEvaluation();
  }, []);

  const fetchEvaluation = async () => {
    try {
      const res = await axios.get(
        "http://127.0.0.1:5000/api/results/latest"
      );

      setEvaluation(res.data);
    } catch (err) {
      console.log(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="loading-screen">
        Loading Evaluation...
      </div>
    );
  }

  if (!evaluation) {
    return (
      <div className="loading-screen">
        No Evaluation Found
      </div>
    );
  }

  return (
    <div className="results-page">

      {/* ================= Sidebar ================= */}

      <aside className="sidebar">

        <h2 className="logo">
          Eval<span>AI</span>
        </h2>

        <ul>

          <li>Dashboard</li>

          <li>Upload Question Paper</li>

          <li>Upload Model Answer</li>

          <li>Upload Answer Script</li>

          <li className="active">
            Results
          </li>

          <li>Reports</li>

          <li>Settings</li>

        </ul>

      </aside>

      {/* ================= Main ================= */}

      <main className="main-content">

        {/* Header */}

        <header className="header">

          <div>

            <h1>
              Automated Answer Script Evaluation
            </h1>

            <p>
              AI Powered Evaluation Dashboard
            </p>

          </div>

          <button className="download-btn">
            Download Report
          </button>

        </header>

        {/* Student Information */}

        <section className="student-card">

          <div>

            <h2>{evaluation.student.name}</h2>

            <p>
              Roll No :
              {evaluation.student.roll_no}
            </p>

            <p>
              Department :
              {evaluation.student.department}
            </p>

            <p>
              Year :
              {evaluation.student.year}
            </p>

          </div>

        </section>

        {/* Statistics */}

        <section className="stats-grid">

          <div className="card">

            <h4>Total Marks</h4>

            <h2>
              {evaluation.summary.total_marks}
            </h2>

          </div>

          <div className="card">

            <h4>Percentage</h4>

            <h2>
              {evaluation.summary.percentage}%
            </h2>

          </div>

          <div className="card">

            <h4>Grade</h4>

            <h2>
              {evaluation.summary.grade}
            </h2>

          </div>

          <div className="card">

            <h4>Questions</h4>

            <h2>
              {evaluation.questions.length}
            </h2>

          </div>

        </section>

        {/* Placeholder */}

        <section className="content-placeholder">

          <h2>
            Question Evaluation
          </h2>

          <p>
            Questions uploaded by the teacher
            will be displayed here after
            AI evaluation.
          </p>

        </section>

      </main>

    </div>
  );
};

export default Results;