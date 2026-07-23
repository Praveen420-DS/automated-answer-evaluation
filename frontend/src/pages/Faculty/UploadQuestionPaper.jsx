import { useEffect, useRef, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import api from "../../services/api";
import { toast } from "react-hot-toast";
import { UploadCloud, FileText, ArrowRight, X } from "lucide-react";

const ACCEPTED_EXTENSIONS = ["pdf", "doc", "docx", "jpg", "jpeg", "png"];
const ACCEPTED_FILE_TYPES = ".pdf,.doc,.docx,.jpg,.jpeg,.png";

export default function UploadQuestionPaper() {
  const navigate = useNavigate();
  const { state } = useLocation();
  const inputRef = useRef(null);
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const [exams, setExams] = useState([]);
  const [selectedExamId, setSelectedExamId] = useState(state?.examId || "");

  useEffect(() => {
    let active = true;
    api.get("/faculty/all-exams")
      .then(({ data }) => active && setExams(data.data || []))
      .catch((error) => console.error("Unable to load exams:", error));
    return () => { active = false; };
  }, []);

  const setSelectedFile = (selectedFile) => {
    if (!selectedFile) return;
    const extension = selectedFile.name.split(".").pop()?.toLowerCase();
    if (!extension || !ACCEPTED_EXTENSIONS.includes(extension)) {
      toast.error("Choose a PDF, DOC, DOCX, JPG, JPEG, or PNG file.", { id: "question-paper-file-type" });
      return;
    }
    setFile(selectedFile);
  };

  const removeFile = () => {
    setFile(null);
    if (inputRef.current) inputRef.current.value = "";
  };

  const uploadQuestionPaper = async () => {
    if (!file) return toast.error("Please select a file.", { id: "question-paper-upload" });
    if (!selectedExamId) return toast.error("Select an exam before uploading its question paper.", { id: "question-paper-upload" });

    try {
      setLoading(true);
      const formData = new FormData();
      formData.append("file", file);
      formData.append("examId", selectedExamId);
      const token = localStorage.getItem("token");
      const response = await fetch(`${api.defaults.baseURL}/faculty/upload-question-paper`, {
        method: "POST",
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
        body: formData,
      });
      const data = await response.json().catch(() => ({}));
      if (!response.ok) throw { response: { data } };
      toast.success("Question paper uploaded successfully.");
      navigate("/faculty/upload-answer-key", { state: { examId: selectedExamId, questions: data.questions || [] } });
    } catch (error) {
      console.error("Question paper upload failed:", error);
      toast.error(error.response?.data?.message || "Unable to upload the question paper.", { id: "question-paper-upload" });
    } finally {
      setLoading(false);
    }
  };

  return <div className="min-h-screen bg-gray-100 py-10"><div className="max-w-4xl mx-auto bg-white rounded-3xl shadow-lg p-10">
    <h1 className="text-4xl font-bold">Upload Question Paper</h1>
    <p className="text-gray-500 mt-2">Supported formats: PDF, DOCX, JPG, JPEG, PNG</p>
    <label className="block mt-6 text-sm font-medium text-gray-700">Exam
      <select value={selectedExamId} onChange={(event) => setSelectedExamId(event.target.value)} className="mt-1 block w-full rounded-lg border border-gray-300 bg-white px-3 py-2">
        <option value="">Select an exam</option>
        {exams.map((exam) => <option key={exam._id} value={exam._id}>{exam.examName || exam.name || "Untitled exam"}</option>)}
      </select>
    </label>
    <div className={`mt-10 border-2 border-dashed rounded-2xl p-12 text-center transition-colors ${isDragging ? "border-indigo-700 bg-indigo-50" : "border-indigo-400"}`} onDragEnter={(event) => { event.preventDefault(); setIsDragging(true); }} onDragOver={(event) => { event.preventDefault(); event.dataTransfer.dropEffect = "copy"; setIsDragging(true); }} onDragLeave={(event) => { if (event.currentTarget === event.target) setIsDragging(false); }} onDrop={(event) => { event.preventDefault(); setIsDragging(false); setSelectedFile(event.dataTransfer.files?.[0]); }}>
      <UploadCloud size={70} className="mx-auto text-indigo-600" />
      <h2 className="text-2xl font-semibold mt-6">Select Question Paper</h2>
      <p className="text-gray-500 mt-2">Drag and drop a file here, or browse for one.</p>
      <input ref={inputRef} type="file" accept={ACCEPTED_FILE_TYPES} onChange={(event) => setSelectedFile(event.target.files?.[0])} style={{ display: "none" }} />
      <button type="button" onClick={() => inputRef.current?.click()} className="mt-8 bg-indigo-600 hover:bg-indigo-700 text-white px-5 py-2 rounded-lg">Browse files</button>
    </div>
    {file && <div className="mt-8 bg-gray-50 rounded-xl p-5 flex justify-between items-center"><div className="flex gap-3 items-center min-w-0"><FileText className="text-indigo-600 shrink-0" size={30} /><div className="min-w-0"><h3 className="font-semibold truncate">{file.name}</h3><p className="text-sm text-gray-500">{(file.size / 1024).toFixed(2)} KB</p></div></div><button type="button" onClick={removeFile} className="text-gray-500 hover:text-red-600" aria-label="Remove selected file"><X size={20} /></button></div>}
    <div className="flex justify-end mt-10"><button type="button" onClick={uploadQuestionPaper} disabled={loading || !file || !selectedExamId} className="bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-300 disabled:cursor-not-allowed text-white px-8 py-3 rounded-xl flex gap-2 items-center">{loading ? "Uploading..." : "Upload"}<ArrowRight size={20} /></button></div>
  </div></div>;
}
