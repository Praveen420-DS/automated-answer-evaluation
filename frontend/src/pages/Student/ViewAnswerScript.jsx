import { useEffect, useState } from "react";
import axios from "axios";
import toast from "react-hot-toast";
import {
  User,
  GraduationCap,
  Award,
  BookOpen,
  Download,
} from "lucide-react";

export default function Transcript() {

  const [transcript, setTranscript] = useState(null);
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    loadTranscript();
  }, []);

  const loadTranscript = async () => {

    try {

      const token = localStorage.getItem("token");

      const res = await axios.get(
        "http://127.0.0.1:5000/api/student/transcript",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setTranscript(res.data);

    } catch {

      setFailed(true); toast.error("Unable to load transcript");

    }

  };

  const downloadTranscript = () => {

    window.open(
      "http://127.0.0.1:5000/api/student/transcript/pdf"
    );

  };

  if (!transcript)
    return (
      <div className="min-h-screen flex justify-center items-center">
        {failed ? "Transcript is unavailable. Please try again later." : "Loading..."}
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

                Academic Transcript

              </h1>

              <p className="text-gray-500 mt-2">

                Complete Academic Record

              </p>

            </div>

            <button
              onClick={downloadTranscript}
              className="bg-indigo-600 text-white px-6 py-3 rounded-xl flex items-center gap-2"
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

                {transcript.name}

              </h3>

            </div>

            <div className="bg-green-50 rounded-2xl p-5">

              <GraduationCap className="text-green-600" />

              <p className="mt-3 text-gray-500">

                Register No

              </p>

              <h3 className="font-bold">

                {transcript.registerNo}

              </h3>

            </div>

            <div className="bg-orange-50 rounded-2xl p-5">

              <Award className="text-orange-600" />

              <p className="mt-3 text-gray-500">

                CGPA

              </p>

              <h3 className="font-bold">

                {transcript.cgpa}

              </h3>

            </div>

            <div className="bg-purple-50 rounded-2xl p-5">

              <BookOpen className="text-purple-600" />

              <p className="mt-3 text-gray-500">

                Total Credits

              </p>

              <h3 className="font-bold">

                {transcript.totalCredits}

              </h3>

            </div>

          </div>

        </div>

        {/* Semester Table */}

        <div className="bg-white rounded-3xl shadow-lg mt-10 p-8">

          <h2 className="text-3xl font-bold mb-6">

            Semester-wise Performance

          </h2>

          <table className="w-full">

            <thead className="bg-indigo-600 text-white">

              <tr>

                <th className="p-4 text-left">

                  Semester

                </th>

                <th className="text-left">

                  SGPA

                </th>

                <th className="text-left">

                  Credits

                </th>

                <th className="text-left">

                  Result

                </th>

              </tr>

            </thead>

            <tbody>

              {transcript.semesters.map((semester) => (

                <tr
                  key={semester.semester}
                  className="border-b hover:bg-gray-50"
                >

                  <td className="p-4">

                    Semester {semester.semester}

                  </td>

                  <td>

                    {semester.sgpa}

                  </td>

                  <td>

                    {semester.credits}

                  </td>

                  <td>

                    <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full">

                      {semester.result}

                    </span>

                  </td>

                </tr>

              ))}

            </tbody>

          </table>

        </div>

        {/* Subject Performance */}

        <div className="bg-white rounded-3xl shadow-lg mt-10 p-8">

          <h2 className="text-3xl font-bold mb-6">

            Subject-wise Marks

          </h2>

          <table className="w-full">

            <thead className="bg-indigo-600 text-white">

              <tr>

                <th className="p-4 text-left">

                  Subject

                </th>

                <th className="text-left">

                  Semester

                </th>

                <th className="text-left">

                  Marks

                </th>

                <th className="text-left">

                  Grade

                </th>

              </tr>

            </thead>

            <tbody>

              {transcript.subjects.map((subject) => (

                <tr
                  key={subject.code}
                  className="border-b hover:bg-gray-50"
                >

                  <td className="p-4">

                    {subject.name}

                  </td>

                  <td>

                    {subject.semester}

                  </td>

                  <td>

                    {subject.marks}

                  </td>

                  <td>

                    {subject.grade}

                  </td>

                </tr>

              ))}

            </tbody>

          </table>

        </div>

      </div>

    </div>

  );

}
