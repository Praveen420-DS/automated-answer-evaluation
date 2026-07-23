import { useState } from "react";
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

  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFile = (e) => {
    if (e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  const uploadAnswerKey = async () => {
    if (!file) {
      toast.error("Please choose an answer key.");
      return;
    }
    if (!examId) {
      toast.error("Create or select an exam before uploading its answer key.");
      navigate("/faculty/create-exam");
      return;
    }

    try {
      setLoading(true);

      const formData = new FormData();
      formData.append("file", file);
      formData.append("examId", examId);

      await api.post(
        "/faculty/upload-answer-key",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      toast.success("Answer Key Uploaded Successfully");

      navigate("/faculty/upload-answer-sheets", { state: { examId } });

    } catch (err) {
      console.log(err);
      toast.error("Upload Failed");
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
