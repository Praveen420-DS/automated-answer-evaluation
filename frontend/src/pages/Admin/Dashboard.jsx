import { useEffect, useState } from "react";
import axios from "axios";
import toast from "react-hot-toast";
import {
  Users,
  UserCog,
  FileText,
  Brain,
  Activity,
  Award,
  Database,
  ShieldCheck,
} from "lucide-react";
import { useNavigate } from "react-router-dom";

export default function AdminDashboard() {

  const navigate = useNavigate();

  const [dashboard, setDashboard] = useState(null);

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {

    try {

      const token = localStorage.getItem("token");

      const res = await axios.get(
        "http://127.0.0.1:5000/api/admin/dashboard",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setDashboard(res.data.statistics || res.data);

    } catch {

      toast.error("Unable to load dashboard");

    }

  };

  if (!dashboard)
    return (
      <div className="min-h-screen flex items-center justify-center">
        Loading...
      </div>
    );

  return (

    <div className="min-h-screen bg-gray-100">

      {/* Header */}

      <div className="bg-white shadow px-8 py-6">

        <h1 className="text-4xl font-bold">

          Admin Dashboard

        </h1>

        <p className="text-gray-500 mt-2">

          EvalAI System Overview

        </p>

      </div>

      <div className="max-w-7xl mx-auto py-8">

        {/* Statistics */}

        <div className="grid md:grid-cols-4 gap-6">

          <StatCard
            icon={<Users className="text-blue-600" size={40} />}
            title="Students"
            value={dashboard.students}
          />

          <StatCard
            icon={<UserCog className="text-green-600" size={40} />}
            title="Faculty"
            value={dashboard.faculty}
          />

          <StatCard
            icon={<FileText className="text-orange-600" size={40} />}
            title="Exams"
            value={dashboard.exams}
          />

          <StatCard
            icon={<Brain className="text-purple-600" size={40} />}
            title="AI Evaluations"
            value={dashboard.evaluations}
          />

        </div>

        {/* System Status */}

        <div className="grid lg:grid-cols-2 gap-8 mt-10">

          <div className="bg-white rounded-2xl shadow p-6">

            <h2 className="text-2xl font-bold mb-6">

              System Status

            </h2>

            <div className="space-y-5">

              <StatusRow
                icon={<Database className="text-green-600" />}
                label="MongoDB"
                status="Connected"
              />

              <StatusRow
                icon={<Brain className="text-blue-600" />}
                label="AI Engine"
                status="Running"
              />

              <StatusRow
                icon={<ShieldCheck className="text-purple-600" />}
                label="Authentication"
                status="Healthy"
              />

              <StatusRow
                icon={<Activity className="text-orange-600" />}
                label="OCR Service"
                status="Online"
              />

            </div>

          </div>

          <div className="bg-white rounded-2xl shadow p-6">

            <h2 className="text-2xl font-bold mb-6">

              Quick Actions

            </h2>

            <div className="grid grid-cols-2 gap-4">

              <ActionButton
                title="Students"
                onClick={() =>
                  navigate("/admin/students")
                }
              />

              <ActionButton
                title="Faculty"
                onClick={() =>
                  navigate("/admin/faculty")
                }
              />

              <ActionButton
                title="Exams"
                onClick={() =>
                  navigate("/admin/exams")
                }
              />

              <ActionButton
                title="Analytics"
                onClick={() =>
                  navigate("/admin/analytics")
                }
              />

              <ActionButton
                title="AI Settings"
                onClick={() =>
                  navigate("/admin/ai-settings")
                }
              />

              <ActionButton
                title="System Logs"
                onClick={() =>
                  navigate("/admin/logs")
                }
              />

            </div>

          </div>

        </div>

        {/* Recent Activities */}

        <div className="bg-white rounded-2xl shadow mt-10 p-6">

          <h2 className="text-2xl font-bold mb-6">

            Recent Activities

          </h2>

          <table className="w-full">

            <thead>

              <tr className="border-b">

                <th className="text-left py-3">

                  Time

                </th>

                <th className="text-left">

                  User

                </th>

                <th className="text-left">

                  Activity

                </th>

              </tr>

            </thead>

            <tbody>

              {(dashboard.activities || []).map((item, index) => (

                <tr
                  key={index}
                  className="border-b"
                >

                  <td className="py-4">

                    {item.time}

                  </td>

                  <td>

                    {item.user}

                  </td>

                  <td>

                    {item.activity}

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

function StatCard({ icon, title, value }) {
  return (
    <div className="bg-white rounded-2xl shadow p-6">
      {icon}
      <p className="text-gray-500 mt-4">{title}</p>
      <h2 className="text-3xl font-bold">{value}</h2>
    </div>
  );
}

function StatusRow({ icon, label, status }) {
  return (
    <div className="flex justify-between items-center border-b pb-3">
      <div className="flex items-center gap-3">
        {icon}
        <span>{label}</span>
      </div>
      <span className="text-green-600 font-semibold">
        {status}
      </span>
    </div>
  );
}

function ActionButton({ title, onClick }) {
  return (
    <button
      onClick={onClick}
      className="bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl p-4"
    >
      {title}
    </button>
  );
}
