import { useEffect, useState } from "react";
import axios from "axios";
import toast from "react-hot-toast";
import {
  Search,
  Plus,
  Edit,
  Trash2,
  Eye,
  RefreshCw,
} from "lucide-react";

export default function Exams() {

  const [exams, setExams] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    loadExams();
  }, []);

  useEffect(() => {

    const data = exams.filter((exam) =>
      exam.subject.toLowerCase().includes(search.toLowerCase()) ||
      exam.examName.toLowerCase().includes(search.toLowerCase())
    );

    setFiltered(data);

  }, [search, exams]);

  const loadExams = async () => {

    try {

      const token = localStorage.getItem("token");

      const res = await axios.get(
        "http://127.0.0.1:5000/api/admin/exams",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setExams(res.data.exams);

    } catch {

      toast.error("Unable to load exams");

    }

  };

  const deleteExam = async (id) => {

    if (!window.confirm("Delete this exam?"))
      return;

    try {

      const token = localStorage.getItem("token");

      await axios.delete(
        `http://127.0.0.1:5000/api/admin/exams/${id}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      toast.success("Exam Deleted");

      loadExams();

    } catch {

      toast.error("Delete Failed");

    }

  };

  return (

    <div className="min-h-screen bg-gray-100">

      <div className="bg-white shadow px-8 py-6">

        <div className="flex justify-between items-center">

          <div>

            <h1 className="text-4xl font-bold">

              Exam Management

            </h1>

            <p className="text-gray-500 mt-2">

              Create and manage examinations

            </p>

          </div>

          <button className="bg-indigo-600 text-white px-6 py-3 rounded-xl flex items-center gap-2">

            <Plus size={18}/>

            Create Exam

          </button>

        </div>

      </div>

      <div className="max-w-7xl mx-auto py-8">

        <div className="bg-white rounded-2xl shadow p-6 mb-8">

          <div className="flex gap-4">

            <div className="relative flex-1">

              <Search
                className="absolute left-4 top-4 text-gray-400"
              />

              <input
                type="text"
                placeholder="Search Exams..."
                value={search}
                onChange={(e)=>setSearch(e.target.value)}
                className="w-full border rounded-xl pl-12 p-4"
              />

            </div>

            <button
              onClick={loadExams}
              className="bg-indigo-600 text-white px-4 rounded-xl"
            >

              <RefreshCw/>

            </button>

          </div>

        </div>

        <div className="bg-white rounded-2xl shadow overflow-hidden">

          <table className="w-full">

            <thead className="bg-indigo-600 text-white">

              <tr>

                <th className="p-4 text-left">

                  Exam

                </th>

                <th>Subject</th>

                <th>Date</th>

                <th>Faculty</th>

                <th>Status</th>

                <th>Actions</th>

              </tr>

            </thead>

            <tbody>

              {filtered.map((exam)=>(

                <tr
                  key={exam._id}
                  className="border-b hover:bg-gray-50"
                >

                  <td className="p-4">

                    {exam.examName}

                  </td>

                  <td>{exam.subject}</td>

                  <td>{exam.examDate}</td>

                  <td>{exam.faculty}</td>

                  <td>

                    <span
                      className={`px-3 py-1 rounded-full text-sm ${
                        exam.status==="Completed"
                        ? "bg-green-100 text-green-700"
                        : exam.status==="Running"
                        ? "bg-yellow-100 text-yellow-700"
                        : "bg-blue-100 text-blue-700"
                      }`}
                    >

                      {exam.status}

                    </span>

                  </td>

                  <td>

                    <div className="flex gap-3">

                      <button
                        className="text-blue-600"
                      >

                        <Eye/>

                      </button>

                      <button
                        className="text-indigo-600"
                      >

                        <Edit/>

                      </button>

                      <button
                        onClick={()=>deleteExam(exam._id)}
                        className="text-red-600"
                      >

                        <Trash2/>

                      </button>

                    </div>

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