import { useEffect, useState } from "react";
import axios from "axios";
import toast from "react-hot-toast";

import {
  Users,
  Award,
  BookOpen,
  CheckCircle,
} from "lucide-react";

import {
  Bar,
  Doughnut,
} from "react-chartjs-2";

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Tooltip,
  Legend
);

export default function Analytics() {

  const [analytics, setAnalytics] = useState(null);

  useEffect(() => {
    loadAnalytics();
  }, []);

  const loadAnalytics = async () => {
    try {

      const res = await axios.get(
        "http://127.0.0.1:5000/api/analytics"
      );

      setAnalytics(res.data);

    } catch {

      toast.error("Unable to load analytics");

    }
  };

  if (!analytics)
    return (
      <div className="min-h-screen flex items-center justify-center">
        Loading...
      </div>
    );

  const marksChart = {
    labels: analytics.subjects,
    datasets: [
      {
        label: "Average Marks",
        data: analytics.averageMarks,
        backgroundColor: "#4F46E5",
      },
    ],
  };

  const passChart = {
    labels: ["Pass", "Fail"],
    datasets: [
      {
        data: [
          analytics.passCount,
          analytics.failCount,
        ],
        backgroundColor: [
          "#22C55E",
          "#EF4444",
        ],
      },
    ],
  };

  return (
    <div className="min-h-screen bg-gray-100">

      {/* Header */}

      <div className="bg-white shadow px-8 py-6">

        <h1 className="text-4xl font-bold">

          Analytics Dashboard

        </h1>

        <p className="text-gray-500 mt-2">

          AI Evaluation Statistics

        </p>

      </div>

      <div className="max-w-7xl mx-auto py-8">

        {/* Summary Cards */}

        <div className="grid md:grid-cols-4 gap-6">

          <div className="bg-white rounded-2xl shadow p-6">

            <Users
              size={40}
              className="text-blue-600"
            />

            <p className="mt-4 text-gray-500">

              Students

            </p>

            <h2 className="text-3xl font-bold">

              {analytics.totalStudents}

            </h2>

          </div>

          <div className="bg-white rounded-2xl shadow p-6">

            <Award
              size={40}
              className="text-green-600"
            />

            <p className="mt-4 text-gray-500">

              Average Marks

            </p>

            <h2 className="text-3xl font-bold">

              {analytics.averageOverall}%

            </h2>

          </div>

          <div className="bg-white rounded-2xl shadow p-6">

            <CheckCircle
              size={40}
              className="text-purple-600"
            />

            <p className="mt-4 text-gray-500">

              Pass Percentage

            </p>

            <h2 className="text-3xl font-bold">

              {analytics.passPercentage}%

            </h2>

          </div>

          <div className="bg-white rounded-2xl shadow p-6">

            <BookOpen
              size={40}
              className="text-orange-600"
            />

            <p className="mt-4 text-gray-500">

              Subjects

            </p>

            <h2 className="text-3xl font-bold">

              {analytics.subjects.length}

            </h2>

          </div>

        </div>

        {/* Charts */}

        <div className="grid lg:grid-cols-2 gap-8 mt-10">

          <div className="bg-white rounded-2xl shadow p-6">

            <h2 className="text-2xl font-bold mb-5">

              Subject-wise Average Marks

            </h2>

            <Bar data={marksChart} />

          </div>

          <div className="bg-white rounded-2xl shadow p-6">

            <h2 className="text-2xl font-bold mb-5">

              Pass / Fail Ratio

            </h2>

            <Doughnut data={passChart} />

          </div>

        </div>

        {/* Top Students */}

        <div className="bg-white rounded-2xl shadow mt-10 p-6">

          <h2 className="text-2xl font-bold mb-6">

            Top Performing Students

          </h2>

          <table className="w-full">

            <thead>

              <tr className="border-b">

                <th className="py-3 text-left">

                  Register No

                </th>

                <th className="text-left">

                  Name

                </th>

                <th className="text-left">

                  Marks

                </th>

              </tr>

            </thead>

            <tbody>

              {analytics.topStudents.map((student) => (

                <tr
                  key={student.registerNo}
                  className="border-b"
                >

                  <td className="py-4">

                    {student.registerNo}

                  </td>

                  <td>

                    {student.name}

                  </td>

                  <td>

                    {student.marks}

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