import { useEffect, useState } from "react";
import { CalendarDays, ClipboardList, RefreshCw } from "lucide-react";
import toast from "react-hot-toast";
import api from "../../services/api";

export default function MyExams() {
  const [exams, setExams] = useState([]);
  const [loading, setLoading] = useState(true);
  async function loadExams() {
    setLoading(true);
    try { const { data } = await api.get("/student/exams"); setExams(data.exams || []); }
    catch { setExams([]); toast.error("Unable to load your exams."); }
    finally { setLoading(false); }
  }
  useEffect(() => { loadExams(); }, []);
  return <main className="results-page"><header className="flex items-center justify-between mb-6"><div><h1 className="text-2xl font-bold">My Exams</h1><p className="text-gray-500">Track the status of your submitted answer sheets.</p></div><button onClick={loadExams} className="download-btn flex items-center gap-2"><RefreshCw size={16} /> Refresh</button></header>{loading ? <section className="result-status-card text-gray-500">Loading exams…</section> : exams.length === 0 ? <section className="result-status-card"><ClipboardList className="mx-auto mb-4 text-violet-600" size={38}/><h2 className="text-xl font-bold">No exams yet</h2><p className="mt-2 text-gray-500">Your assigned or submitted exams will appear here.</p></section> : <section className="grid gap-4">{exams.map((exam) => <article key={exam.id} className="result-row"><div className="flex items-center gap-4"><CalendarDays className="text-violet-600"/><div><h2 className="font-bold">{exam.examName}</h2><p className="text-sm text-gray-500">{exam.subject} · {exam.date}</p></div></div><div className="text-right"><b className="capitalize">{exam.status}</b><p className="text-sm text-gray-500">{exam.status === "evaluated" ? `${exam.marks}/${exam.totalMarks}` : "Awaiting evaluation"}</p></div></article>)}</section>}</main>;
}
