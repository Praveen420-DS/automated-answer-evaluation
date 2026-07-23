import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import api from "../../services/api";
import { toast } from "react-hot-toast";
import { UploadCloud, FileText, ArrowRight } from "lucide-react";

export default function UploadQuestionPaper() {
  const navigate = useNavigate();
  const { state } = useLocation();
  const examId = state?.examId;

  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const selectFile = (e) => {
    if (e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  const uploadQuestionPaper = async () => {
    if (!file) {
      toast.error("Please select a file.");
      return;
    }
    if (!examId) {
      toast.error("Create or select an exam before uploading its question paper.");
      navigate("/faculty/create-exam");
      return;
    }

    try {
      setLoading(true);

      const formData = new FormData();
      formData.append("file", file);
      formData.append("examId", examId);

      await api.post(
        "/faculty/upload-question-paper",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      toast.success("Question Paper Uploaded Successfully");

      navigate("/faculty/upload-answer-key", { state: { examId } });
    } catch (err) {
      console.error(err);
      toast.error("Upload Failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 py-10">

      <div className="max-w-4xl mx-auto bg-white rounded-3xl shadow-lg p-10">

        <h1 className="text-4xl font-bold">
          Upload Question Paper
        </h1>

        <p className="text-gray-500 mt-2">
          Supported Formats: PDF, DOCX, JPG, JPEG, PNG
        </p>

        <div className="mt-10 border-2 border-dashed border-indigo-400 rounded-2xl p-12 text-center">

          <UploadCloud
            size={70}
            className="mx-auto text-indigo-600"
          />

          <h2 className="text-2xl font-semibold mt-6">
            Select Question Paper
          </h2>

          <p className="text-gray-500 mt-2">
            Drag & Drop or Browse your file
          </p>

          <input
            type="file"
            accept=".pdf,.doc,.docx,.jpg,.jpeg,.png"
            onChange={selectFile}
            className="mt-8"
          />

        </div>

        {file && (

          <div className="mt-8 bg-gray-50 rounded-xl p-5 flex justify-between items-center">

            <div className="flex gap-3 items-center">

              <FileText
                className="text-indigo-600"
                size={30}
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

        <div className="flex justify-end mt-10">

          <button
            onClick={uploadQuestionPaper}
            disabled={loading}
            className="bg-indigo-600 hover:bg-indigo-700 text-white px-8 py-3 rounded-xl flex gap-2 items-center"
          >

            {loading ? "Uploading..." : "Upload"}

            <ArrowRight size={20} />

          </button>

        </div>

      </div>

    </div>
  );
}
