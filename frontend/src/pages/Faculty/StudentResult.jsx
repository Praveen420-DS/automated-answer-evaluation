import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import toast from "react-hot-toast";
import {
  User,
  GraduationCap,
  Award,
  FileText,
  Download,
} from "lucide-react";

export default function StudentResult() {
  const { registerNo } = useParams();

  const [student, setStudent] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStudent();
  }, []);

  const loadStudent = async () => {
    try {
      const res = await axios.get(
        `http://127.0.0.1:5000/api/student-result/${registerNo}`
      );

      setStudent(res.data);

    } catch (err) {
      toast.error("Unable to load student result");
    } finally {
      setLoading(false);
    }
  };

  const downloadReport = () => {
    window.open(
      `http://127.0.0.1:5000/api/report/${registerNo}`
    );
  };

  if (loading)
    return (
      <div className="min-h-screen flex justify-center items-center">
        Loading...
      </div>
    );

  return (
    <div className="min-h-screen bg-gray-100 py-10">

      <div className="max-w-7xl mx-auto">

        {/* Student Info */}

        <div className="bg-white rounded-3xl shadow-lg p-8">

          <div className="flex justify-between">

            <div>

              <h1 className="text-4xl font-bold">

                Student Evaluation

              </h1>

              <p className="text-gray-500 mt-2">

                AI Generated Report

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

                {student.name}

              </h3>

            </div>

            <div className="bg-green-50 rounded-2xl p-5">

              <GraduationCap className="text-green-600" />

              <p className="mt-3 text-gray-500">

                Register No

              </p>

              <h3 className="font-bold">

                {student.registerNo}

              </h3>

            </div>

            <div className="bg-orange-50 rounded-2xl p-5">

              <Award className="text-orange-600" />

              <p className="mt-3 text-gray-500">

                Marks

              </p>

              <h3 className="font-bold">

                {student.totalMarks}/100

              </h3>

            </div>

            <div className="bg-purple-50 rounded-2xl p-5">

              <FileText className="text-purple-600" />

              <p className="mt-3 text-gray-500">

                AI Score

              </p>

              <h3 className="font-bold">

                {student.aiScore}%

              </h3>

            </div>

          </div>

        </div>

        {/* Question Wise Evaluation */}

        <div className="bg-white rounded-3xl shadow-lg mt-10 p-8">

          <h2 className="text-3xl font-bold">

            Question Wise Evaluation

          </h2>

          <div className="space-y-8 mt-8">

            {student.questions.map((q) => (

              <div
                key={q.questionNo}
                className="border rounded-2xl p-6"
              >

                <h3 className="text-xl font-bold">

                  Question {q.questionNo}

                </h3>

                <div className="mt-6">

                  <p className="font-semibold">

                    Student Answer

                  </p>

                  <p className="bg-gray-100 rounded-xl p-4 mt-2">

                    {q.studentAnswer}

                  </p>

                </div>

                <div className="mt-6">

                  <p className="font-semibold">

                    Correct Answer

                  </p>

                  <p className="bg-green-50 rounded-xl p-4 mt-2">

                    {q.correctAnswer}

                  </p>

                </div>

                <div className="grid md:grid-cols-3 gap-6 mt-6">

                  <div className="bg-blue-50 rounded-xl p-5">

                    <h4 className="font-semibold">

                      Similarity

                    </h4>

                    <p className="text-3xl font-bold text-blue-600">

                      {q.similarity}%

                    </p>

                  </div>

                  <div className="bg-green-50 rounded-xl p-5">

                    <h4 className="font-semibold">

                      Marks

                    </h4>

                    <p className="text-3xl font-bold text-green-600">

                      {q.marks}
                    </p>

                  </div>

                  <div className="bg-yellow-50 rounded-xl p-5">

                    <h4 className="font-semibold">

                      AI Feedback

                    </h4>

                    <p className="text-sm mt-2">

                      {q.feedback}

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