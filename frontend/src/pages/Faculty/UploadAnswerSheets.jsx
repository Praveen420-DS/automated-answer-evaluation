import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import toast from "react-hot-toast";
import { FileText, PlayCircle, Trash2, UploadCloud } from "lucide-react";
import api from "../../services/api";
import "./upload-answer-sheets.css";

export default function UploadAnswerSheets() {
  const navigate = useNavigate();
  const { state } = useLocation();
  const examId = state?.examId;
  const [files, setFiles] = useState([]);
  const [studentEmail, setStudentEmail] = useState("");
  const [uploading, setUploading] = useState(false);
  const chooseFiles = (event) => setFiles(Array.from(event.target.files || []));
  const removeFile = (index) => setFiles((current) => current.filter((_, fileIndex) => fileIndex !== index));

  async function uploadFiles() {
    if (!files.length) { toast.error("Choose at least one answer sheet."); return; }
    if (!examId) { toast.error("Create or select an exam before uploading answer sheets."); navigate("/faculty/create-exam"); return; }
    if (!studentEmail.trim()) { toast.error("Enter the student email for these answer sheets."); return; }
    try {
      setUploading(true);
      const uploads = await Promise.all(files.map((file) => { const form = new FormData(); form.append("file", file); form.append("examId", examId); form.append("studentEmail", studentEmail.trim()); return api.post("/evaluation/upload-answer-sheet", form, { headers: { "Content-Type": "multipart/form-data" } }); }));
      toast.success("Answer sheets uploaded. OCR processing can now begin.");
      navigate("/faculty/evaluation", { state: { examId, answerSheetIds: uploads.map(({ data }) => data.answerSheetId).filter(Boolean) } });
    } catch (error) { toast.error(error.response?.data?.message || "Unable to upload answer sheets."); }
    finally { setUploading(false); }
  }

  return <main className="answer-upload-page">
    <header><h1>Upload Student Answer Sheets</h1><p>Upload scanned answer sheets for OCR extraction and AI evaluation.</p></header>
    <section className="answer-upload-card">
      <label className="answer-dropzone"><UploadCloud /><strong>Select answer-sheet files</strong><span>PDF, JPG, JPEG, or PNG · You may select multiple files</span><span className="answer-file-button">Choose files<input type="file" multiple accept=".pdf,.jpg,.jpeg,.png" onChange={chooseFiles} /></span></label>
      <label className="answer-student-email">Student email<input type="email" value={studentEmail} onChange={(event) => setStudentEmail(event.target.value)} placeholder="student@example.com" required /></label>
      {files.length > 0 && <div className="answer-file-list"><h2>Selected files ({files.length})</h2>{files.map((file, index) => <div key={`${file.name}-${index}`}><FileText /><span><strong>{file.name}</strong><small>{(file.size / 1024).toFixed(1)} KB</small></span><button onClick={() => removeFile(index)} aria-label={`Remove ${file.name}`}><Trash2 size={18} /></button></div>)}</div>}
      <footer><p>Files are uploaded securely and processed through OCR before evaluation.</p><button onClick={uploadFiles} disabled={uploading || !files.length}><PlayCircle size={18} /> {uploading ? "Uploading…" : "Upload and Start Evaluation"}</button></footer>
    </section>
  </main>;
}
