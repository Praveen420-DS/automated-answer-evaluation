import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import toast from "react-hot-toast";
import {
  User,
  Award,
  Brain,
  FileText,
  Download,
  CheckCircle,
} from "lucide-react";

export default function StudentResult() {

  const { examId } = useParams();

  const [result, setResult] = useState(null);
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    loadResult();
  }, []);

  const loadResult = async () => {

    try {

      const token = localStorage.getItem("token");

      const res = await axios.get(
        `http://127.0.0.1:5000/api/student/result/${examId}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setResult(res.data.data);

    } catch {

      setFailed(true); toast.error("Unable to load result");

    }

  };

  const downloadReport = () => {
    const token = localStorage.getItem("token");
    axios.get(`http://127.0.0.1:5000/api/student/download/${examId}`, { headers: { Authorization: `Bearer ${token}` }, responseType: "blob" }).then((response) => {
      const url = URL.createObjectURL(response.data); const link = document.createElement("a");
      link.href = url; link.download = "evaluation-report.pdf"; link.click(); URL.revokeObjectURL(url);
    }).catch(() => toast.error("Report is not available yet."));

  };

  if (!result)
    return (
      <div className="min-h-screen flex justify-center items-center">
        {failed ? "Result is unavailable. Please try again later." : "Loading..."}
      </div>
    );

  return (

    <div className="min-h-screen bg-gray-100 py-10">

      <div className="max-w-7xl mx-auto">

        {/* Header */}

        <div className="bg-white rounded-3xl shadow-lg p-8">

          <div className="flex justify-between items-center">

            <div>

              <h1 className="text-4xl font-bold">

                Exam Evaluation Report

              </h1>

              <p className="text-gray-500 mt-2">

                AI Generated Answer Analysis

              </p>

            </div>

            <button
              onClick={downloadReport}
              className="bg-indigo-600 text-white px-6 py-3 rounded-xl flex gap-2 items-center"
            >

              <Download size={18} />

              Download PDF

            </button>

          </div>

          <div className="grid md:grid-cols-4 gap-6 mt-10">

            <div className="bg-blue-50 rounded-2xl p-5">

              <User className="text-blue-600" />

              <p className="mt-3 text-gray-500">

                Student

              </p>

              <h3 className="font-bold">

                {result.studentName}

              </h3>

            </div>

            <div className="bg-green-50 rounded-2xl p-5">

              <FileText className="text-green-600" />

              <p className="mt-3 text-gray-500">

                Subject

              </p>

              <h3 className="font-bold">

                {result.subject}

              </h3>

            </div>

            <div className="bg-orange-50 rounded-2xl p-5">

              <Award className="text-orange-600" />

              <p className="mt-3 text-gray-500">

                Final Marks

              </p>

              <h3 className="font-bold">

                {result.marks}/{result.totalMarks}

              </h3>

            </div>

            <div className="bg-purple-50 rounded-2xl p-5">

              <Brain className="text-purple-600" />

              <p className="mt-3 text-gray-500">

                AI Similarity

              </p>

              <h3 className="font-bold">

                {result.percentage}%

              </h3>

            </div>

          </div>

        </div>

        {/* Question Wise Evaluation */}

        <div className="bg-white rounded-3xl shadow-lg mt-10 p-8">

          <h2 className="text-3xl font-bold">

            Question Wise Analysis

          </h2>

          <div className="space-y-8 mt-8">

            {(result.questionResults || []).map((question) => (

              <div
                key={question.questionNumber}
                className="border rounded-2xl p-6"
              >

                <div className="flex justify-between items-center">

                  <h3 className="text-2xl font-bold">

                    Question {question.questionNumber}

                  </h3>

                  <span className="bg-green-100 text-green-700 px-4 py-2 rounded-full flex items-center gap-2">

                    <CheckCircle size={16} />

                    {question.score}/{question.maxScore} Marks

                  </span>

                </div>

                <div className="mt-6">

                  <h4 className="font-semibold">

                    Your Answer

                  </h4>

                  <div className="bg-gray-100 rounded-xl p-4 mt-2">

                    {question.ocrText}

                  </div>

                </div>

                <div className="mt-6">

                  <h4 className="font-semibold">

                    Correct Answer

                  </h4>

                  <div className="bg-green-50 rounded-xl p-4 mt-2">

                    {question.feedback}

                  </div>

                </div>

                <div className="grid md:grid-cols-2 gap-6 mt-6">

                  <div className="bg-blue-50 rounded-xl p-5">

                    <h4 className="font-semibold">

                      AI Similarity

                    </h4>

                    <p className="text-3xl font-bold text-blue-600">

                      {question.confidence}

                    </p>

                  </div>

                  <div className="bg-yellow-50 rounded-xl p-5">

                    <h4 className="font-semibold">

                      AI Feedback

                    </h4>

                    <p className="mt-2">

                      {question.feedback}

                    </p>

                  </div>

                </div>

              </div>

            ))}

          </div>

        </div>

      </div>

    </div>

  );

}
