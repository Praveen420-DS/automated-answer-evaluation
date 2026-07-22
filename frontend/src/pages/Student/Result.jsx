import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import toast from "react-hot-toast";
import { ClipboardX, FileText, RefreshCw } from "lucide-react";
import api from "../../services/api";
import "../../styles/results.css";
import "../../styles/result-state.css";

export default function Result() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadResults = async () => {
    setLoading(true);
    try {
      const { data } = await api.get("/student/results");
      // Only show completed evaluations. OCR uploads that have not yet been
      // evaluated must never appear as fabricated marks or feedback.
      setResults((data.results || []).filter((item) => item.status === "evaluated"));
    } catch {
      setResults([]);
      toast.error("Unable to load results");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadResults(); }, []);

  return (
    <main className="results-page">
        <header className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold">Results Overview</h1>
            <p className="text-gray-500">Your OCR-processed and evaluated answer sheets.</p>
          </div>
          <button onClick={loadResults} className="download-btn flex items-center gap-2">
            <RefreshCw size={16} /> Refresh
          </button>
        </header>

        {loading ? (
          <section className="result-status-card text-gray-500">Loading results...</section>
        ) : results.length === 0 ? (
          <section className="result-status-card">
            <div className="mx-auto mb-5 flex h-16 w-16 items-center justify-center rounded-full bg-violet-50 text-violet-600">
              <ClipboardX size={32} />
            </div>
            <h2 className="text-xl font-bold">No evaluated answer sheets yet</h2>
            <p className="mx-auto mt-2 max-w-md text-gray-500">
              Your results will appear here after staff upload your answer-sheet PDF and OCR processing and evaluation are completed.
            </p>
          </section>
        ) : (
          <section className="grid gap-4">
            {results.map((result) => (
              <Link key={result._id} to={`/student/result/${result._id}`} className="result-row hover:shadow-md">
                <div className="flex items-center gap-4"><FileText className="text-violet-600" /><div><h2 className="font-bold">{result.examName || result.subject || "Evaluated answer sheet"}</h2><p className="text-sm text-gray-500">{result.subject || "Answer-script evaluation"}</p></div></div>
                <b>{result.marks ?? 0} marks</b>
              </Link>
            ))}
          </section>
        )}
    </main>
  );
}
