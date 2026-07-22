import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../services/api";
import {
  FileText,
  Upload,
  BarChart3,
  Users,
  LogOut,
  ClipboardCheck,
} from "lucide-react";

export default function Dashboard() {
  const navigate = useNavigate();

  const username = localStorage.getItem("username");
  const [stats, setStats] = useState(null);

  useEffect(() => {
    api.get("/faculty/dashboard").then(({ data }) => setStats(data.statistics)).catch(() => setStats({}));
  }, []);

  const logout = () => {
    localStorage.clear();
    navigate("/login");
  };

  const cards = [
    {
      title: "Total Exams",
      value: stats?.totalExams ?? "—",
      icon: <FileText size={30} />,
      color: "bg-blue-500",
    },
    {
      title: "Answer Sheets",
      value: stats?.questionPapers ?? "—",
      icon: <Upload size={30} />,
      color: "bg-green-500",
    },
    {
      title: "Evaluated",
      value: stats?.answerKeys ?? "—",
      icon: <ClipboardCheck size={30} />,
      color: "bg-purple-500",
    },
    {
      title: "Students",
      value: stats?.questions ?? "—",
      icon: <Users size={30} />,
      color: "bg-orange-500",
    },
  ];

  return (
    <div className="min-h-screen bg-gray-100">

      {/* Navbar */}
      <div className="bg-white shadow-sm px-8 py-5 flex justify-between items-center">

        <div>
          <h1 className="text-3xl font-bold">
            Faculty Dashboard
          </h1>

          <p className="text-gray-500 mt-1">
            Welcome, {username}
          </p>
        </div>

        <button
          onClick={logout}
          className="flex items-center gap-2 bg-red-500 hover:bg-red-600 text-white px-5 py-2 rounded-lg"
        >
          <LogOut size={18} />
          Logout
        </button>

      </div>

      <div className="max-w-7xl mx-auto p-8">

        {/* Statistics */}
        <div className="grid lg:grid-cols-4 md:grid-cols-2 gap-6">

          {cards.map((card) => (
            <div
              key={card.title}
              className="bg-white rounded-2xl shadow-md p-6"
            >
              <div
                className={`${card.color} w-14 h-14 rounded-xl text-white flex items-center justify-center`}
              >
                {card.icon}
              </div>

              <h2 className="mt-5 text-gray-500">
                {card.title}
              </h2>

              <h1 className="text-4xl font-bold mt-2">
                {card.value}
              </h1>
            </div>
          ))}

        </div>

        {/* Quick Actions */}
        <div className="mt-10">

          <h2 className="text-2xl font-bold mb-5">
            Quick Actions
          </h2>

          <div className="grid lg:grid-cols-3 gap-6">

            <button
              onClick={() => navigate("/faculty/create-exam")}
              className="bg-white rounded-2xl shadow p-8 hover:shadow-xl transition"
            >
              <FileText
                size={40}
                className="text-indigo-600"
              />

              <h3 className="text-xl font-semibold mt-5">
                Create Exam
              </h3>

              <p className="text-gray-500 mt-2">
                Create a new examination.
              </p>

            </button>

            <button
              onClick={() => navigate("/faculty/upload-question-paper")}
              className="bg-white rounded-2xl shadow p-8 hover:shadow-xl transition"
            >
              <Upload
                size={40}
                className="text-green-600"
              />

              <h3 className="text-xl font-semibold mt-5">
                Upload Files
              </h3>

              <p className="text-gray-500 mt-2">
                Upload question papers and answer sheets.
              </p>

            </button>

            <button
              onClick={() => navigate("/faculty/result-matrix")}
              className="bg-white rounded-2xl shadow p-8 hover:shadow-xl transition"
            >
              <BarChart3
                size={40}
                className="text-purple-600"
              />

              <h3 className="text-xl font-semibold mt-5">
                View Results
              </h3>

              <p className="text-gray-500 mt-2">
                Analyze evaluation reports.
              </p>

            </button>

          </div>

        </div>

        {/* Recent Activity */}
        <div className="mt-12 bg-white rounded-2xl shadow p-6">

          <h2 className="text-2xl font-bold mb-5">
            Recent Activity
          </h2>

          <table className="w-full">

            <thead>

              <tr className="border-b">

                <th className="text-left py-3">
                  Exam
                </th>

                <th className="text-left">
                  Subject
                </th>

                <th className="text-left">
                  Status
                </th>

              </tr>

            </thead>

            <tbody>

              <tr className="border-b">

                <td className="py-4">
                  Internal Assessment 1
                </td>

                <td>
                  Artificial Intelligence
                </td>

                <td className="text-green-600">
                  Completed
                </td>

              </tr>

              <tr className="border-b">

                <td className="py-4">
                  Semester Exam
                </td>

                <td>
                  Data Structures
                </td>

                <td className="text-orange-500">
                  Processing
                </td>

              </tr>

            </tbody>

          </table>

        </div>

      </div>

    </div>
  );
}
