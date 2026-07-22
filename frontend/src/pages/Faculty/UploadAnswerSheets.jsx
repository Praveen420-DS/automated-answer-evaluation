import { useState } from "react";
import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";
import { FileText, PlayCircle, Trash2, UploadCloud } from "lucide-react";
import api from "../../services/api";
import "./upload-answer-sheets.css";

export default function UploadAnswerSheets() {
  const navigate = useNavigate();
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const chooseFiles = (event) => setFiles(Array.from(event.target.files || []));
  const removeFile = (index) => setFiles((current) => current.filter((_, fileIndex) => fileIndex !== index));

  async function uploadFiles() {
    if (!files.length) { toast.error("Choose at least one answer sheet."); return; }
    try {
      setUploading(true);
      await Promise.all(files.map((file) => { const form = new FormData(); form.append("file", file); return api.post("/evaluation/upload-answer-sheet", form, { headers: { "Content-Type": "multipart/form-data" } }); }));
      toast.success("Answer sheets uploaded. OCR processing can now begin.");
      navigate("/faculty/evaluation");
    } catch (error) { toast.error(error.response?.data?.message || "Unable to upload answer sheets."); }
    finally { setUploading(false); }
  }

  return <main className="answer-upload-page">
    <header><h1>Upload Student Answer Sheets</h1><p>Upload scanned answer sheets for OCR extraction and AI evaluation.</p></header>
    <section className="answer-upload-card">
      <label className="answer-dropzone"><UploadCloud /><strong>Select answer-sheet files</strong><span>PDF, JPG, JPEG, or PNG · You may select multiple files</span><span className="answer-file-button">Choose files<input type="file" multiple accept=".pdf,.jpg,.jpeg,.png" onChange={chooseFiles} /></span></label>
      {files.length > 0 && <div className="answer-file-list"><h2>Selected files ({files.length})</h2>{files.map((file, index) => <div key={`${file.name}-${index}`}><FileText /><span><strong>{file.name}</strong><small>{(file.size / 1024).toFixed(1)} KB</small></span><button onClick={() => removeFile(index)} aria-label={`Remove ${file.name}`}><Trash2 size={18} /></button></div>)}</div>}
      <footer><p>Files are uploaded securely and processed through OCR before evaluation.</p><button onClick={uploadFiles} disabled={uploading || !files.length}><PlayCircle size={18} /> {uploading ? "Uploading…" : "Upload and Start Evaluation"}</button></footer>
    </section>
  </main>;
}
