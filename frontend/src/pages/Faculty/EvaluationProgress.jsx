import { useEffect, useState } from "react";
import { CheckCircle2, FileSearch, RefreshCw, UploadCloud } from "lucide-react";
import { useNavigate } from "react-router-dom";
import api from "../../services/api";
import "./evaluation-progress.css";

export default function EvaluationProgress() {
  const navigate = useNavigate();
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);

  async function loadProgress() {
    setLoading(true);
    try { const { data } = await api.get("/evaluation/ocr-results"); setRecords(Array.isArray(data.data) ? data.data : []); }
    catch { setRecords([]); }
    finally { setLoading(false); }
  }
  useEffect(() => { loadProgress(); }, []);

  const completed = records.filter((record) => record.status === "evaluated").length;
  return <main className="evaluation-progress-page">
    <header><div><h1>Evaluation Progress</h1><p>Track uploaded answer sheets through OCR and AI evaluation.</p></div><button onClick={loadProgress}><RefreshCw size={17} /> Refresh</button></header>
    {loading ? <section className="evaluation-empty">Loading evaluation progress…</section> : records.length === 0 ? <section className="evaluation-empty"><FileSearch size={44} /><h2>No answer sheets uploaded</h2><p>Upload student answer-sheet PDFs to begin OCR extraction and AI evaluation.</p><button onClick={() => navigate("/faculty/upload-answer-sheets")}><UploadCloud size={17} /> Upload Answer Sheets</button></section> : <><section className="evaluation-summary"><article><UploadCloud /><div><small>Uploaded</small><strong>{records.length}</strong></div></article><article><FileSearch /><div><small>OCR Processed</small><strong>{records.filter((record) => record.ocrText).length}</strong></div></article><article><CheckCircle2 /><div><small>Evaluated</small><strong>{completed}</strong></div></article></section><section className="evaluation-list"><h2>Uploaded Answer Sheets</h2>{records.map((record) => <div key={record._id || record.filename}><FileSearch /><div><strong>{record.filename || "Answer sheet"}</strong><small>{record.ocrText ? "OCR extracted" : "Waiting for OCR processing"}</small></div><span className={record.status === "evaluated" ? "complete" : "pending"}>{record.status === "evaluated" ? "Evaluated" : "In progress"}</span></div>)}</section></>}
  </main>;
}
