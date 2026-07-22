import { useEffect, useState } from "react";
import axios from "axios";
import toast from "react-hot-toast";
import {
  FileText,
  Download,
  Archive,
  FileSpreadsheet,
  RefreshCw,
} from "lucide-react";

export default function DownloadReport() {

  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadReports();
  }, []);

  const loadReports = async () => {

    try {

      const token = localStorage.getItem("token");

      const res = await axios.get(
        "http://127.0.0.1:5000/api/student/reports",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setReports(res.data.reports);

    } catch {

      toast.error("Unable to load reports");

    } finally {

      setLoading(false);

    }

  };

  const downloadReport = (examId) => {
    window.open(
      `http://127.0.0.1:5000/api/student/report/${examId}`
    );
  };

  const downloadTranscript = () => {
    window.open(
      "http://127.0.0.1:5000/api/student/transcript/pdf"
    );
  };

  const downloadSummary = () => {
    window.open(
      "http://127.0.0.1:5000/api/student/summary/pdf"
    );
  };

  const downloadAll = () => {
    window.open(
      "http://127.0.0.1:5000/api/student/reports/zip"
    );
  };

  return (

    <div className="min-h-screen bg-gray-100">

      <div className="bg-white shadow px-8 py-6">

        <div className="flex justify-between items-center">

          <div>

            <h1 className="text-4xl font-bold">

              Download Center

            </h1>

            <p className="text-gray-500 mt-2">

              Download Reports & Academic Documents

            </p>

          </div>

          <button
            onClick={loadReports}
            className="bg-indigo-600 text-white px-5 py-3 rounded-xl flex gap-2 items-center"
          >

            <RefreshCw size={18}/>

            Refresh

          </button>

        </div>

      </div>

      <div className="max-w-7xl mx-auto py-8">

        {/* Quick Downloads */}

        <div className="grid md:grid-cols-3 gap-6 mb-10">

          <button
            onClick={downloadTranscript}
            className="bg-white rounded-2xl shadow p-8 hover:shadow-xl transition"
          >

            <FileText
              className="text-indigo-600"
              size={45}
            />

            <h2 className="mt-5 text-xl font-bold">

              Transcript

            </h2>

            <p className="text-gray-500 mt-2">

              Download Academic Transcript

            </p>

          </button>

          <button
            onClick={downloadSummary}
            className="bg-white rounded-2xl shadow p-8 hover:shadow-xl transition"
          >

            <FileSpreadsheet
              className="text-green-600"
              size={45}
            />

            <h2 className="mt-5 text-xl font-bold">

              AI Summary

            </h2>

            <p className="text-gray-500 mt-2">

              AI Evaluation Summary

            </p>

          </button>

          <button
            onClick={downloadAll}
            className="bg-white rounded-2xl shadow p-8 hover:shadow-xl transition"
          >

            <Archive
              className="text-orange-600"
              size={45}
            />

            <h2 className="mt-5 text-xl font-bold">

              Download All

            </h2>

            <p className="text-gray-500 mt-2">

              ZIP File of All Reports

            </p>

          </button>

        </div>

        {/* Individual Reports */}

        <div className="bg-white rounded-3xl shadow-lg overflow-hidden">

          <table className="w-full">

            <thead className="bg-indigo-600 text-white">

              <tr>

                <th className="p-4 text-left">

                  Subject

                </th>

                <th className="text-left">

                  Exam

                </th>

                <th className="text-left">

                  Date

                </th>

                <th className="text-left">

                  Marks

                </th>

                <th className="text-left">

                  Download

                </th>

              </tr>

            </thead>

            <tbody>

              {loading ? (

                <tr>

                  <td
                    colSpan="5"
                    className="text-center py-10"
                  >

                    Loading...

                  </td>

                </tr>

              ) : (

                reports.map((report) => (

                  <tr
                    key={report.examId}
                    className="border-b hover:bg-gray-50"
                  >

                    <td className="p-4">

                      {report.subject}

                    </td>

                    <td>

                      {report.examName}

                    </td>

                    <td>

                      {report.date}

                    </td>

                    <td>

                      {report.marks}

                    </td>

                    <td>

                      <button
                        onClick={() =>
                          downloadReport(report.examId)
                        }
                        className="text-indigo-600"
                      >

                        <Download/>

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