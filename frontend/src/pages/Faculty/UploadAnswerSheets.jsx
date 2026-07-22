import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../services/api";
import toast from "react-hot-toast";
import {
  UploadCloud,
  Trash2,
  FileText,
  PlayCircle,
} from "lucide-react";

export default function UploadAnswerSheets() {

  const navigate = useNavigate();

  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleFiles = (e) => {
    setFiles(Array.from(e.target.files));
  };

  const removeFile = (index) => {
    const updated = [...files];
    updated.splice(index, 1);
    setFiles(updated);
  };

  const uploadFiles = async () => {

    if (files.length === 0) {
      toast.error("Please select answer sheets");
      return;
    }

    try {

      setLoading(true);

      await Promise.all(files.map((file) => {
        const formData = new FormData();
        formData.append("file", file);
        return api.post("/evaluation/upload-answer-sheet", formData, { headers: { "Content-Type": "multipart/form-data" } });
      }));

      toast.success("Answer Sheets Uploaded Successfully");

      navigate("/faculty/evaluation");

    } catch (err) {

      console.log(err);

      toast.error("Upload Failed");

    } finally {

      setLoading(false);

    }
  };

  return (

    <div className="min-h-screen bg-gray-100 py-10">

      <div className="max-w-6xl mx-auto bg-white rounded-3xl shadow-lg p-10">

        <h1 className="text-4xl font-bold">

          Upload Student Answer Sheets

        </h1>

        <p className="text-gray-500 mt-2">

          Upload all scanned answer sheets for AI evaluation.

        </p>

        <div className="mt-10 border-2 border-dashed border-indigo-400 rounded-3xl p-12 text-center">

          <UploadCloud
            size={70}
            className="mx-auto text-indigo-600"
          />

          <h2 className="text-2xl font-semibold mt-5">

            Select Multiple Files

          </h2>

          <p className="text-gray-500 mt-2">

            PDF, JPG, JPEG, PNG

          </p>

          <input
            multiple
            type="file"
            accept=".pdf,.jpg,.jpeg,.png"
            onChange={handleFiles}
            className="mt-8"
          />

        </div>

        {files.length > 0 && (

          <div className="mt-10">

            <h2 className="text-2xl font-bold mb-5">

              Selected Files

            </h2>

            <div className="space-y-4">

              {files.map((file, index) => (

                <div
                  key={index}
                  className="bg-gray-50 rounded-xl p-5 flex justify-between items-center"
                >

                  <div className="flex items-center gap-4">

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

                  <button
                    onClick={() => removeFile(index)}
                    className="text-red-600 hover:text-red-700"
                  >

                    <Trash2 />

                  </button>

                </div>

              ))}

            </div>

          </div>

        )}

        <div className="flex justify-end mt-10">

          <button
            onClick={uploadFiles}
            disabled={loading}
            className="bg-indigo-600 hover:bg-indigo-700 text-white px-8 py-3 rounded-xl flex items-center gap-3"
          >

            <PlayCircle size={20} />

            {loading ? "Uploading..." : "Start AI Evaluation"}

          </button>

        </div>

      </div>

    </div>

  );

}
