import { useEffect, useState } from "react";
import api from "../../services/api";
import toast from "react-hot-toast";
import {
  Search,
  Plus,
  Edit,
  Trash2,
  Upload,
  Download,
  RefreshCw,
} from "lucide-react";

export default function Students() {

  const [students, setStudents] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    loadStudents();
  }, []);

  useEffect(() => {

    const data = students.filter((student) =>
      student.name.toLowerCase().includes(search.toLowerCase()) ||
      student.registerNo.toLowerCase().includes(search.toLowerCase())
    );

    setFiltered(data);

  }, [search, students]);

  const loadStudents = async () => {

    try {

      const res = await api.get("/admin/users/student");
      setStudents((res.data.users || []).map((student) => ({
        ...student,
        name: student.fullName || "Unnamed student",
        registerNo: student.rollNo || student.studentId || "—",
      })));

    } catch {

      toast.error("Unable to load students");

    }

  };

  const deleteStudent = async (id) => {

    if (!window.confirm("Delete this student?")) return;

    try {

      await api.delete(`/admin/user/${id}`);

      toast.success("Student Deleted");

      loadStudents();

    } catch {

      toast.error("Delete Failed");

    }

  };

  return (

    <div className="min-h-screen bg-gray-100">

      {/* Header */}

      <div className="bg-white shadow px-8 py-6">

        <div className="flex justify-between items-center">

          <div>

            <h1 className="text-4xl font-bold">

              Student Management

            </h1>

            <p className="text-gray-500 mt-2">

              Manage all registered students

            </p>

          </div>

          <div className="flex gap-3">

            <button className="bg-green-600 text-white px-5 py-3 rounded-xl flex items-center gap-2">

              <Upload size={18}/>

              Import Excel

            </button>

            <button className="bg-orange-600 text-white px-5 py-3 rounded-xl flex items-center gap-2">

              <Download size={18}/>

              Export Excel

            </button>

            <button
              onClick={loadStudents}
              className="bg-indigo-600 text-white px-5 py-3 rounded-xl"
            >

              <RefreshCw size={18}/>

            </button>

          </div>

        </div>

      </div>

      <div className="max-w-7xl mx-auto py-8">

        {/* Search */}

        <div className="bg-white rounded-2xl shadow p-6 mb-8">

          <div className="flex justify-between gap-5">

            <div className="relative flex-1">

              <Search
                className="absolute left-4 top-4 text-gray-400"
              />

              <input
                type="text"
                placeholder="Search Student..."
                value={search}
                onChange={(e)=>setSearch(e.target.value)}
                className="w-full border rounded-xl p-4 pl-12"
              />

            </div>

            <button
              className="bg-indigo-600 text-white px-6 rounded-xl flex items-center gap-2"
            >

              <Plus size={18}/>

              Add Student

            </button>

          </div>

        </div>

        {/* Student Table */}

        <div className="bg-white rounded-2xl shadow overflow-hidden">

          <table className="w-full">

            <thead className="bg-indigo-600 text-white">

              <tr>

                <th className="p-4 text-left">

                  Register No

                </th>

                <th>Name</th>

                <th>Department</th>

                <th>Year</th>

                <th>Email</th>

                <th>Action</th>

              </tr>

            </thead>

            <tbody>

              {filtered.map((student)=>(

                <tr
                  key={student._id}
                  className="border-b hover:bg-gray-50"
                >

                  <td className="p-4">

                    {student.registerNo}

                  </td>

                  <td>{student.name}</td>

                  <td>{student.department}</td>

                  <td>{student.year}</td>

                  <td>{student.email}</td>

                  <td>

                    <div className="flex gap-4">

                      <button
                        className="text-indigo-600"
                      >

                        <Edit/>

                      </button>

                      <button
                        onClick={()=>deleteStudent(student._id)}
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
