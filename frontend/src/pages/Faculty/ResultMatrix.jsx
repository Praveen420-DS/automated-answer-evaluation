import { useEffect, useState } from "react";
import axios from "axios";
import toast from "react-hot-toast";
import {
  Search,
  Download,
  Eye,
  RefreshCw,
} from "lucide-react";

export default function ResultMatrix() {
  const [students, setStudents] = useState([]);
  const [filteredStudents, setFilteredStudents] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadResults();
  }, []);

  useEffect(() => {
    const filtered = students.filter(
      (student) =>
        student.registerNo
          .toLowerCase()
          .includes(search.toLowerCase()) ||
        student.name
          .toLowerCase()
          .includes(search.toLowerCase())
    );

    setFilteredStudents(filtered);
  }, [search, students]);

  const loadResults = async () => {
    try {
      const res = await axios.get(
        "http://127.0.0.1:5000/api/results"
      );

      setStudents(res.data.results);
      setFilteredStudents(res.data.results);
    } catch (err) {
      toast.error("Unable to load results");
    } finally {
      setLoading(false);
    }
  };

  const exportExcel = () => {
    window.open(
      "http://127.0.0.1:5000/api/export/excel"
    );
  };

  const exportPDF = () => {
    window.open(
      "http://127.0.0.1:5000/api/export/pdf"
    );
  };

  return (
    <div className="min-h-screen bg-gray-100">

      {/* Header */}

      <div className="bg-white shadow px-8 py-6">

        <div className="flex justify-between items-center">

          <div>

            <h1 className="text-4xl font-bold">

              Result Matrix

            </h1>

            <p className="text-gray-500 mt-2">

              AI Evaluation Results

            </p>

          </div>

          <button
            onClick={loadResults}
            className="flex gap-2 items-center bg-indigo-600 text-white px-5 py-3 rounded-xl"
          >

            <RefreshCw size={18} />

            Refresh

          </button>

        </div>

      </div>

      <div className="max-w-7xl mx-auto py-8">

        {/* Search */}

        <div className="bg-white rounded-2xl shadow p-6 mb-8">

          <div className="relative">

            <Search
              size={20}
              className="absolute left-4 top-4 text-gray-400"
            />

            <input
              type="text"
              placeholder="Search Register Number or Student Name..."
              value={search}
              onChange={(e) =>
                setSearch(e.target.value)
              }
              className="w-full pl-12 p-4 rounded-xl border"
            />

          </div>

        </div>

        {/* Export Buttons */}

        <div className="flex gap-5 mb-8">

          <button
            onClick={exportExcel}
            className="bg-green-600 text-white px-6 py-3 rounded-xl"
          >

            <Download
              size={18}
              className="inline mr-2"
            />

            Export Excel

          </button>

          <button
            onClick={exportPDF}
            className="bg-red-600 text-white px-6 py-3 rounded-xl"
          >

            <Download
              size={18}
              className="inline mr-2"
            />

            Export PDF

          </button>

        </div>

        {/* Table */}

        <div className="bg-white rounded-2xl shadow overflow-hidden">

          <table className="w-full">

            <thead className="bg-indigo-600 text-white">

              <tr>

                <th className="p-4">Register No</th>

                <th>Name</th>

                <th>Department</th>

                <th>Total Marks</th>

                <th>AI Score</th>

                <th>Status</th>

                <th>Action</th>

              </tr>

            </thead>

            <tbody>

              {loading ? (

                <tr>

                  <td
                    colSpan="7"
                    className="text-center py-10"
                  >

                    Loading...

                  </td>

                </tr>

              ) : filteredStudents.length === 0 ? (

                <tr>

                  <td
                    colSpan="7"
                    className="text-center py-10"
                  >

                    No Results Found

                  </td>

                </tr>

              ) : (

                filteredStudents.map((student) => (

                  <tr
                    key={student.registerNo}
                    className="border-b hover:bg-gray-50"
                  >

                    <td className="p-4">

                      {student.registerNo}

                    </td>

                    <td>{student.name}</td>

                    <td>{student.department}</td>

                    <td>

                      {student.totalMarks}

                    </td>

                    <td>

                      {student.aiScore}%

                    </td>

                    <td>

                      <span
                        className={`px-3 py-1 rounded-full text-sm ${
                          student.status === "Pass"
                            ? "bg-green-100 text-green-700"
                            : "bg-red-100 text-red-700"
                        }`}
                      >

                        {student.status}

                      </span>

                    </td>

                    <td>

                      <button
                        className="text-indigo-600 hover:text-indigo-800"
                      >

                        <Eye />

                      </button>

                    </td>

                  </tr>

                ))

              )}

            </tbody>

          </table>

        </div>

      </div>

    </div>
  );
}