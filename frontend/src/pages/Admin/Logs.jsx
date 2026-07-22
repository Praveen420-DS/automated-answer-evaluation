import { useEffect, useState } from "react";
import axios from "axios";
import toast from "react-hot-toast";
import {
  Search,
  RefreshCw,
  Download,
  Activity,
} from "lucide-react";

export default function Logs() {

  const [logs, setLogs] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    loadLogs();
  }, []);

  useEffect(() => {

    const result = logs.filter((log) =>
      log.user.toLowerCase().includes(search.toLowerCase()) ||
      log.action.toLowerCase().includes(search.toLowerCase()) ||
      log.module.toLowerCase().includes(search.toLowerCase())
    );

    setFiltered(result);

  }, [search, logs]);

  const loadLogs = async () => {

    try {

      const token = localStorage.getItem("token");

      const res = await axios.get(
        "http://127.0.0.1:5000/api/admin/logs",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setLogs(res.data.logs);

    } catch {

      toast.error("Unable to load logs");

    }

  };

  return (

    <div className="min-h-screen bg-gray-100">

      {/* Header */}

      <div className="bg-white shadow px-8 py-6 flex justify-between items-center">

        <div>

          <h1 className="text-4xl font-bold flex items-center gap-3">

            <Activity />

            System Logs

          </h1>

          <p className="text-gray-500 mt-2">

            Monitor all platform activities

          </p>

        </div>

        <div className="flex gap-3">

          <button
            className="bg-green-600 text-white px-5 py-3 rounded-xl flex items-center gap-2"
          >

            <Download size={18}/>

            Export

          </button>

          <button
            onClick={loadLogs}
            className="bg-indigo-600 text-white p-3 rounded-xl"
          >

            <RefreshCw size={18}/>

          </button>

        </div>

      </div>

      <div className="max-w-7xl mx-auto py-8">

        {/* Search */}

        <div className="bg-white rounded-2xl shadow p-6 mb-8">

          <div className="relative">

            <Search className="absolute left-4 top-4 text-gray-400"/>

            <input
              type="text"
              placeholder="Search logs..."
              value={search}
              onChange={(e)=>setSearch(e.target.value)}
              className="w-full border rounded-xl p-4 pl-12"
            />

          </div>

        </div>

        {/* Logs Table */}

        <div className="bg-white rounded-2xl shadow overflow-hidden">

          <table className="w-full">

            <thead className="bg-indigo-600 text-white">

              <tr>

                <th className="p-4 text-left">

                  Time

                </th>

                <th>User</th>

                <th>Module</th>

                <th>Action</th>

                <th>Status</th>

                <th>IP Address</th>

              </tr>

            </thead>

            <tbody>

              {filtered.map((log)=>(

                <tr
                  key={log._id}
                  className="border-b hover:bg-gray-50"
                >

                  <td className="p-4">

                    {log.time}

                  </td>

                  <td>{log.user}</td>

                  <td>{log.module}</td>

                  <td>{log.action}</td>

                  <td>

                    <span
                      className={`px-3 py-1 rounded-full text-sm ${
                        log.status==="Success"
                          ? "bg-green-100 text-green-700"
                          : "bg-red-100 text-red-700"
                      }`}
                    >

                      {log.status}

                    </span>

                  </td>

                  <td>{log.ip}</td>

                </tr>

              ))}

            </tbody>

          </table>

        </div>

      </div>

    </div>

  );

}