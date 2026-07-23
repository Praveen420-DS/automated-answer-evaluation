import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import api from "../../services/api";
import { toast } from "react-hot-toast";
import {
  UploadCloud,
  FileCheck2,
  ArrowRight,
} from "lucide-react";

export default function UploadAnswerKey() {
  const navigate = useNavigate();
  const { state } = useLocation();
  const examId = state?.examId;
  const [questions, setQuestions] = useState(state?.questions || []);
  const [referenceAnswers, setReferenceAnswers] = useState(() =>
    (state?.questions || []).map((question) => ({ questionNumber: question.questionNumber, referenceAnswer: "" }))
  );

  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFile = (e) => {
    if (e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  useEffect(() => {
    if (questions.length || !examId) return;
    api.get(`/faculty/questions?examId=${examId}`).then(({ data }) => {
      const parsed = data.questions || [];
      setQuestions(parsed);
      setReferenceAnswers(parsed.map((question) => ({ questionNumber: question.questionNumber, referenceAnswer: "" })));
    }).catch(() => toast.error("Unable to load parsed questions."));
  }, [examId, questions.length]);

  const updateReference = (questionNumber, referenceAnswer) => {
    setReferenceAnswers((current) => current.map((item) => item.questionNumber === questionNumber ? { ...item, referenceAnswer } : item));
  };

  const uploadAnswerKey = async () => {
    if (!examId) {
      toast.error("Create or select an exam before uploading its answer key.");
      navigate("/faculty/create-exam");
      return;
    }
    if (!referenceAnswers.length || referenceAnswers.some((item) => !item.referenceAnswer.trim())) {
      toast.error("Add a reference answer for every parsed question.");
      return;
    }

    try {
      setLoading(true);

      const formData = new FormData();
      if (file) formData.append("file", file);
      formData.append("examId", examId);
      formData.append("referenceAnswers", JSON.stringify(referenceAnswers));

      const token = localStorage.getItem("token");
      const response = await fetch(`${api.defaults.baseURL}/faculty/upload-answer-key`, {
        method: "POST",
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
        body: formData,
      });
      const result = await response.json().catch(() => ({}));
      if (!response.ok) throw { response: { data: result } };

      toast.success("Answer Key Uploaded Successfully");

      navigate("/faculty/upload-answer-sheets", { state: { examId } });

    } catch (err) {
      console.error("Answer key upload failed:", err);
      toast.error(err.response?.data?.message || "Unable to upload the answer key.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 py-10">

      <div className="max-w-4xl mx-auto bg-white rounded-3xl shadow-lg p-10">

        <h1 className="text-4xl font-bold">
          Upload Answer Key
        </h1>

        <p className="text-gray-500 mt-2">
          Upload the official answer key for AI evaluation.
        </p>

        <div className="mt-10 border-2 border-dashed border-green-400 rounded-3xl p-14 text-center">

          <UploadCloud
            size={70}
            className="mx-auto text-green-600"
          />

          <h2 className="text-2xl font-semibold mt-6">
            Select Answer Key
          </h2>

          <p className="text-gray-500 mt-2">
            PDF, DOCX, JPG, JPEG or PNG
          </p>

          <input
            type="file"
            accept=".pdf,.doc,.docx,.jpg,.jpeg,.png"
            onChange={handleFile}
            className="mt-8"
          />

          <p className="mt-4 text-sm text-gray-500">A source answer-key file is optional when entering reference answers below.</p>

        </div>

        {file && (

          <div className="mt-8 bg-green-50 rounded-xl p-5 flex justify-between items-center">

            <div className="flex gap-3 items-center">

              <FileCheck2
                size={32}
                className="text-green-600"
              />

              <div>

                <h3 className="font-semibold">

                  {file.name}

                </h3>

                <p className="text-sm text-gray-500">

                  {(file.size / 1024).toFixed(2)} KB

                </p>

              </div>

            </div>

          </div>

        )}

        <section className="mt-8 space-y-5">
          <h2 className="text-xl font-semibold">Reference Answers</h2>
          {questions.length ? questions.map((question) => {
            const current = referenceAnswers.find((item) => item.questionNumber === question.questionNumber);
            return <label key={question._id || question.questionNumber} className="block rounded-xl border p-4 text-left">
              <b>Q{question.questionNumber}: {question.questionText || question.question}</b>
              <textarea className="mt-3 w-full rounded border p-3" rows="4" value={current?.referenceAnswer || ""} onChange={(event) => updateReference(question.questionNumber, event.target.value)} placeholder="Canonical reference answer" />
            </label>;
          }) : <p className="text-sm text-red-600">No parsed questions are available for this exam. Upload and parse the question paper first.</p>}
        </section>

        <div className="flex justify-end mt-10">

          <button
            onClick={uploadAnswerKey}
            disabled={loading}
            className="bg-green-600 hover:bg-green-700 text-white px-8 py-3 rounded-xl flex gap-2 items-center"
          >

            {loading ? "Uploading..." : "Upload"}

            <ArrowRight size={20} />

          </button>

        </div>

      </div>

    </div>
  );
}
