import { useEffect, useState } from "react";
import api from "../../services/api";
import toast from "react-hot-toast";
import {
  Search,
  Plus,
  Edit,
  Trash2,
  KeyRound,
  Upload,
  Download,
  RefreshCw,
} from "lucide-react";

export default function Faculty() {

  const [faculty, setFaculty] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    loadFaculty();
  }, []);

  useEffect(() => {

    const data = faculty.filter((teacher) =>
      teacher.name.toLowerCase().includes(search.toLowerCase()) ||
      teacher.employeeId.toLowerCase().includes(search.toLowerCase())
    );

    setFiltered(data);

  }, [search, faculty]);

  const loadFaculty = async () => {

    try {

      const res = await api.get("/admin/users/faculty");
      setFaculty((res.data.users || []).map((teacher) => ({
        ...teacher,
        name: teacher.fullName || "Unnamed faculty",
        employeeId: teacher.facultyId || "—",
      })));

    } catch {

      toast.error("Unable to load faculty");

    }

  };

  const deleteFaculty = async (id) => {

    if (!window.confirm("Delete this faculty member?"))
      return;

    try {

      await api.delete(`/admin/user/${id}`);

      toast.success("Faculty Deleted");

      loadFaculty();

    } catch {

      toast.error("Delete Failed");

    }

  };

  const resetPassword = async (id) => {
    // Password reset delivery is intentionally handled through the secure
    // account-recovery flow rather than exposing a reset token in the UI.
    toast("Ask this user to use the Forgot Password page.");

  };

  return (

    <div className="min-h-screen bg-gray-100">

      {/* Header */}

      <div className="bg-white shadow px-8 py-6">

        <div className="flex justify-between items-center">

          <div>

            <h1 className="text-4xl font-bold">

              Faculty Management

            </h1>

            <p className="text-gray-500 mt-2">

              Manage Faculty Members

            </p>

          </div>

          <div className="flex gap-3">

            <button className="bg-green-600 text-white px-5 py-3 rounded-xl flex items-center gap-2">

              <Upload size={18}/>

              Import

            </button>

            <button className="bg-orange-600 text-white px-5 py-3 rounded-xl flex items-center gap-2">

              <Download size={18}/>

              Export

            </button>

            <button
              onClick={loadFaculty}
              className="bg-indigo-600 text-white p-3 rounded-xl"
            >

              <RefreshCw size={18}/>

            </button>

          </div>

        </div>

      </div>

      <div className="max-w-7xl mx-auto py-8">

        {/* Search */}

        <div className="bg-white rounded-2xl shadow p-6 mb-8">

          <div className="flex gap-5">

            <div className="relative flex-1">

              <Search className="absolute left-4 top-4 text-gray-400"/>

              <input
                type="text"
                placeholder="Search Faculty..."
                value={search}
                onChange={(e)=>setSearch(e.target.value)}
                className="w-full border rounded-xl p-4 pl-12"
              />

            </div>

            <button className="bg-indigo-600 text-white px-6 rounded-xl flex gap-2 items-center">

              <Plus size={18}/>

              Add Faculty

            </button>

          </div>

        </div>

        {/* Faculty Table */}

        <div className="bg-white rounded-2xl shadow overflow-hidden">

          <table className="w-full">

            <thead className="bg-indigo-600 text-white">

              <tr>

                <th className="p-4 text-left">

                  Employee ID

                </th>

                <th>Name</th>

                <th>Department</th>

                <th>Subject</th>

                <th>Email</th>

                <th>Actions</th>

              </tr>

            </thead>

            <tbody>

              {filtered.map((teacher)=>(

                <tr
                  key={teacher._id}
                  className="border-b hover:bg-gray-50"
                >

                  <td className="p-4">

                    {teacher.employeeId}

                  </td>

                  <td>{teacher.name}</td>

                  <td>{teacher.department}</td>

                  <td>{teacher.subject}</td>

                  <td>{teacher.email}</td>

                  <td>

                    <div className="flex gap-4">

                      <button className="text-indigo-600">

                        <Edit/>

                      </button>

                      <button
                        onClick={()=>resetPassword(teacher._id)}
                        className="text-yellow-600"
                      >

                        <KeyRound/>

                      </button>

                      <button
                        onClick={()=>deleteFaculty(teacher._id)}
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
