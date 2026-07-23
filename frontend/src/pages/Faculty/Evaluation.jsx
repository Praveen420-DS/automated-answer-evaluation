import { useState } from "react";
import api from "../../services/api";
import toast from "react-hot-toast";
import { useLocation, useNavigate } from "react-router-dom";
import {
  Brain,
  ScanSearch,
  FileCheck,
  CheckCircle2,
} from "lucide-react";

export default function Evaluation() {

  const navigate = useNavigate();
  const { state } = useLocation();
  const examId = state?.examId;
  const answerSheetIds = state?.answerSheetIds || [];

  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState("Ready to Start");
  const [progress, setProgress] = useState(0);

  const startEvaluation = async () => {

    try {

      setLoading(true);

      setStatus("Starting OCR...");

      setProgress(10);

      if (!examId || !answerSheetIds.length) {
        toast.error("Upload an answer sheet for an exam before starting evaluation.");
        navigate("/faculty/upload-answer-sheets", { state: { examId } });
        return;
      }
      const response = await api.post("/evaluation/start", { examId, answerSheetId: answerSheetIds[0] });

      if (response.data.success) {

        setStatus("Extracting Answers...");
        setProgress(40);

        setTimeout(() => {

          setStatus("AI Evaluating...");
          setProgress(70);

        },1000);

        setTimeout(() => {

          setStatus("Generating Reports...");
          setProgress(95);

        },2000);

        setTimeout(() => {

          setStatus("Completed");
          setProgress(100);

          toast.success("Evaluation Completed");

          navigate("/faculty/result-matrix");

        },3000);

      }

    }

    catch(err){

      console.log(err);

      toast.error("Evaluation Failed");

    }

    finally{

      setLoading(false);

    }

  };

  return (

    <div className="min-h-screen bg-gray-100 py-10">

      <div className="max-w-5xl mx-auto bg-white rounded-3xl shadow-lg p-10">

        <h1 className="text-4xl font-bold">

          AI Evaluation

        </h1>

        <p className="text-gray-500 mt-3">

          OCR + AI + Semantic Similarity Evaluation

        </p>

        <div className="grid md:grid-cols-4 gap-6 mt-10">

          <div className="bg-blue-50 rounded-2xl p-6 text-center">

            <ScanSearch
              className="mx-auto text-blue-600"
              size={45}
            />

            <h3 className="mt-4 font-semibold">

              OCR

            </h3>

          </div>

          <div className="bg-green-50 rounded-2xl p-6 text-center">

            <Brain
              className="mx-auto text-green-600"
              size={45}
            />

            <h3 className="mt-4 font-semibold">

              AI Engine

            </h3>

          </div>

          <div className="bg-orange-50 rounded-2xl p-6 text-center">

            <FileCheck
              className="mx-auto text-orange-600"
              size={45}
            />

            <h3 className="mt-4 font-semibold">

              Marks Calculation

            </h3>

          </div>

          <div className="bg-purple-50 rounded-2xl p-6 text-center">

            <CheckCircle2
              className="mx-auto text-purple-600"
              size={45}
            />

            <h3 className="mt-4 font-semibold">

              Report

            </h3>

          </div>

        </div>

        <div className="mt-12">

          <div className="flex justify-between">

            <span>Status</span>

            <span>{status}</span>

          </div>

          <div className="w-full bg-gray-200 rounded-full h-5 mt-3">

            <div
              className="bg-indigo-600 h-5 rounded-full transition-all duration-500"
              style={{
                width: `${progress}%`,
              }}
            />

          </div>

        </div>

        <div className="mt-12 text-center">

          <button
            disabled={loading}
            onClick={startEvaluation}
            className="bg-indigo-600 hover:bg-indigo-700 text-white px-10 py-4 rounded-xl text-lg"
          >

            {loading
              ? "Evaluating..."
              : "Start AI Evaluation"}

          </button>

        </div>

      </div>

    </div>

  );

}
