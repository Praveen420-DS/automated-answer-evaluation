import { useEffect, useState } from "react";
import api from "../../services/api";
import toast from "react-hot-toast";
import {
  FileText,
  Download,
  Archive,
  FileSpreadsheet,
  RefreshCw,
  Inbox,
} from "lucide-react";

export default function DownloadReport() {

  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadReports();
  }, []);

  const loadReports = async () => {

    try {

      const res = await api.get("/student/reports");

      setReports(Array.isArray(res.data.reports) ? res.data.reports : []);

    } catch (error) {
      // No uploaded/evaluated reports is a normal empty state, not an error.
      if (error.response?.status === 404) {
        setReports([]);
      } else {
        toast.error("Unable to load reports");
      }

    } finally {

      setLoading(false);

    }

  };

  const downloadReport = async (evaluationId) => {
    try {
      const response = await api.get(`/student/download/${evaluationId}`, { responseType: "blob" });
      const url = URL.createObjectURL(response.data); const link = document.createElement("a");
      link.href = url; link.download = "evaluation-report.pdf"; link.click(); URL.revokeObjectURL(url);
    } catch (error) { toast.error(error.response?.data?.message || "This report is not available yet."); }
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

        {loading ? (
          <div className="bg-white rounded-3xl shadow-lg py-20 text-center text-gray-500">
            Loading reports...
          </div>
        ) : reports.length === 0 ? (
          <div className="bg-white rounded-3xl shadow-lg py-20 px-6 text-center">
            <div className="mx-auto mb-5 flex h-16 w-16 items-center justify-center rounded-full bg-indigo-50 text-indigo-600">
              <Inbox size={32} />
            </div>
            <h2 className="text-xl font-bold text-gray-800">No reports available</h2>
            <p className="mt-2 text-gray-500">
              Your PDF reports will appear here once evaluation is complete.
            </p>
          </div>
        ) : (
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

              {reports.map((report) => (

                  <tr
                    key={report.id}
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
                          downloadReport(report.id)
                        }
                        className="text-indigo-600"
                      >

                        <Download/>

                      </button>

                    </td>

                  </tr>

                ))}

            </tbody>

          </table>

          </div>
        )}

      </div>

    </div>

  );

}
