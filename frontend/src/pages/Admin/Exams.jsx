import { useEffect, useMemo, useState } from "react";
import axios from "axios";
import toast from "react-hot-toast";
import { Edit3, Eye, Plus, RefreshCw, Search, Trash2 } from "lucide-react";

const API_URL = "http://127.0.0.1:5000/api/admin/exams";

export default function Exams() {
  const [exams, setExams] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);

  const loadExams = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem("token");
      const { data } = await axios.get(API_URL, { headers: { Authorization: `Bearer ${token}` } });
      setExams(Array.isArray(data.exams) ? data.exams : []);
    } catch {
      setExams([]);
      toast.error("Unable to load exams");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadExams(); }, []);

  const filtered = useMemo(() => {
    const term = search.trim().toLowerCase();
    if (!term) return exams;
    return exams.filter((exam) => `${exam.examName || ""} ${exam.subject || ""} ${exam.faculty || ""}`.toLowerCase().includes(term));
  }, [exams, search]);

  const deleteExam = async (id) => {
    if (!window.confirm("Delete this exam?")) return;
    try {
      const token = localStorage.getItem("token");
      await axios.delete(`${API_URL}/${id}`, { headers: { Authorization: `Bearer ${token}` } });
      toast.success("Exam deleted");
      loadExams();
    } catch {
      toast.error("Delete failed");
    }
  };

  return <main className="admin-exams-page">
    <header className="admin-exams-heading">
      <div>
        <h1>Exam Management</h1>
        <p>Create and manage examinations</p>
      </div>
      <button className="admin-create-exam" type="button"><Plus />Create Exam</button>
    </header>

    <section className="admin-exams-toolbar" aria-label="Exam search controls">
      <label className="admin-exams-search">
        <Search aria-hidden="true" />
        <input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search exams..." aria-label="Search exams" />
      </label>
      <button className="admin-refresh" type="button" onClick={loadExams} aria-label="Refresh exams" title="Refresh exams"><RefreshCw className={loading ? "is-spinning" : ""} /></button>
    </section>

    <section className="admin-exams-table-card">
      <div className="admin-exams-table-wrap">
        <table className="admin-exams-table">
          <thead><tr><th>Exam</th><th>Subject</th><th>Date</th><th>Faculty</th><th>Status</th><th>Actions</th></tr></thead>
          <tbody>
            {loading ? <tr><td colSpan="6" className="admin-exams-empty">Loading exams…</td></tr> : filtered.length === 0 ? <tr><td colSpan="6" className="admin-exams-empty">No exams found.</td></tr> : filtered.map((exam) => <tr key={exam._id}>
              <td className="exam-name">{exam.examName}</td><td>{exam.subject}</td><td>{exam.examDate}</td><td>{exam.faculty}</td>
              <td><span className={`exam-status ${String(exam.status || "draft").toLowerCase()}`}>{exam.status || "Draft"}</span></td>
              <td><div className="admin-exam-actions"><button title="View exam" aria-label="View exam"><Eye /></button><button title="Edit exam" aria-label="Edit exam"><Edit3 /></button><button className="delete" title="Delete exam" aria-label="Delete exam" onClick={() => deleteExam(exam._id)}><Trash2 /></button></div></td>
            </tr>)}
          </tbody>
        </table>
      </div>
    </section>
  </main>;
}
