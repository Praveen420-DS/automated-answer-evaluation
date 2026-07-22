import { useEffect, useMemo, useState } from "react";
import { Download, Eye, FileBarChart, RefreshCw, Search } from "lucide-react";
import api from "../../services/api";
import "./result-matrix.css";

export default function ResultMatrix() {
  const [students, setStudents] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);

  async function loadResults() {
    setLoading(true);
    try {
      const { data } = await api.get("/evaluation/ocr-results");
      const rows = Array.isArray(data.data) ? data.data.filter((item) => item.status === "evaluated") : [];
      setStudents(rows);
    } catch { setStudents([]); }
    finally { setLoading(false); }
  }
  useEffect(() => { loadResults(); }, []);

  const results = useMemo(() => students.filter((student) => `${student.registerNo || ""} ${student.studentName || ""}`.toLowerCase().includes(search.toLowerCase())), [students, search]);
  const canExport = results.length > 0;

  return <main className="result-matrix-page">
    <header className="result-matrix-header"><div><h1>Result Matrix</h1><p>Review completed OCR and AI evaluations.</p></div><button onClick={loadResults}><RefreshCw size={17} /> Refresh</button></header>
    <section className="matrix-toolbar"><label><Search size={19} /><input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search register number or student name" /></label><div><button disabled={!canExport}><Download size={16} /> Export Excel</button><button disabled={!canExport}><Download size={16} /> Export PDF</button></div></section>
    <section className="matrix-card">
      {loading ? <div className="matrix-empty">Loading evaluation results…</div> : results.length === 0 ? <div className="matrix-empty"><FileBarChart size={42} /><h2>No evaluated results yet</h2><p>Results will appear after answer sheets are uploaded, OCR is processed, and evaluation is completed.</p></div> : <div className="matrix-table-wrap"><table><thead><tr><th>Register No</th><th>Name</th><th>Department</th><th>Total Marks</th><th>AI Score</th><th>Status</th><th>Action</th></tr></thead><tbody>{results.map((student) => <tr key={student._id}><td>{student.registerNo || "—"}</td><td>{student.studentName || "—"}</td><td>{student.department || "—"}</td><td>{student.marks ?? "—"}</td><td>{student.aiScore ?? "—"}%</td><td><span>Evaluated</span></td><td><button aria-label="View result"><Eye size={18} /></button></td></tr>)}</tbody></table></div>}
    </section>
  </main>;
}
