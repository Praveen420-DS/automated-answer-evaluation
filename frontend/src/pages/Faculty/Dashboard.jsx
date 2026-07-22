import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { BarChart3, ClipboardCheck, FileText, Upload, Users } from "lucide-react";
import api from "../../services/api";
import "./faculty-dashboard.css";

const emptyStats = { totalExams: 0, answerSheets: 0, evaluated: 0, students: 0 };

export default function Dashboard() {
  const navigate = useNavigate();
  const [stats, setStats] = useState(emptyStats);
  const [exams, setExams] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadDashboard() {
      try {
        const [dashboardResponse, examsResponse] = await Promise.all([
          api.get("/faculty/dashboard"),
          api.get("/faculty/all-exams"),
        ]);
        setStats({ ...emptyStats, ...(dashboardResponse.data.statistics || {}) });
        setExams(Array.isArray(examsResponse.data.data) ? examsResponse.data.data : []);
      } catch {
        // An empty database is valid.  Keep the dashboard clean instead of
        // replacing it with placeholder data.
        setStats(emptyStats);
        setExams([]);
      } finally {
        setLoading(false);
      }
    }
    loadDashboard();
  }, []);

  const cards = [
    ["Total Exams", stats.totalExams, FileText, "text-violet-600 bg-violet-50"],
    ["Answer Sheets", stats.answerSheets, Upload, "text-emerald-600 bg-emerald-50"],
    ["Evaluated", stats.evaluated, ClipboardCheck, "text-purple-600 bg-purple-50"],
    ["Students", stats.students, Users, "text-orange-600 bg-orange-50"],
  ];

  return <main className="faculty-dashboard">
    <div className="faculty-dashboard__heading"><h1>Faculty Dashboard</h1><p>Manage your exams, uploads, and evaluations.</p></div>

    <section className="faculty-stats">
      {cards.map(([title, value, Icon, color]) => <article key={title} className="faculty-stat"><div className={`faculty-stat__icon ${color}`}><Icon size={24} /></div><p>{title}</p><strong>{loading ? "—" : value}</strong></article>)}
    </section>

    <section className="faculty-section"><h2>Quick Actions</h2><div className="faculty-actions">
      <Action icon={FileText} title="Create Exam" text="Create a new examination." onClick={() => navigate("/faculty/create-exam")} />
      <Action icon={Upload} title="Upload Answer Sheets" text="Upload student answer-sheet PDFs for OCR." onClick={() => navigate("/faculty/upload-answer-sheets")} />
      <Action icon={BarChart3} title="View Results" text="Review completed evaluations." onClick={() => navigate("/faculty/result-matrix")} />
    </div></section>

    <section className="faculty-section faculty-recent"><h2>Recent Exams</h2>
      {loading ? <p className="faculty-empty">Loading exams…</p> : exams.length === 0 ? <EmptyDashboard /> : <div className="mt-5 overflow-x-auto"><table className="w-full text-left"><thead className="border-b text-sm text-slate-500"><tr><th className="pb-3 font-medium">Exam</th><th className="pb-3 font-medium">Subject</th><th className="pb-3 font-medium">Semester</th><th className="pb-3 font-medium">Status</th></tr></thead><tbody>{exams.slice(0, 5).map((exam) => <tr key={exam._id} className="border-b last:border-0"><td className="py-4 font-medium">{exam.examName || "Untitled exam"}</td><td>{exam.subject || "—"}</td><td>{exam.semester ? `Semester ${exam.semester}` : "—"}</td><td><span className="rounded-full bg-blue-50 px-3 py-1 text-sm text-blue-700">Created</span></td></tr>)}</tbody></table></div>}
    </section>
  </main>;
}

function Action({ icon: Icon, title, text, onClick }) { return <button onClick={onClick} className="faculty-action"><Icon className="text-violet-600" size={28} /><h3>{title}</h3><p>{text}</p></button>; }
function EmptyDashboard() { return <div className="faculty-empty"><FileText className="mx-auto text-slate-300" size={38} /><strong className="mt-3">No exams created yet</strong><p>Create an exam, then upload the required documents to begin evaluation.</p></div>; }
