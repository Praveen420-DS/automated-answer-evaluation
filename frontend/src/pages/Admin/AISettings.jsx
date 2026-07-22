import { useEffect, useState } from "react";
import axios from "axios";
import toast from "react-hot-toast";
import {
  Brain,
  Save,
  SlidersHorizontal,
  ScanText,
  Award,
  Settings2,
} from "lucide-react";

export default function AISettings() {
  const [settings, setSettings] = useState({
    aiModel: "OpenAI",
    similarityThreshold: 80,
    ocrConfidence: 90,
    maxMarks: 10,
    partialMarking: true,
    autoEvaluation: true,
  });

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      const token = localStorage.getItem("token");

      const res = await axios.get(
        "http://127.0.0.1:5000/api/admin/ai-settings",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setSettings(res.data);

    } catch {
      toast.error("Unable to load settings");
    }
  };

  const handleChange = (e) => {
    setSettings({
      ...settings,
      [e.target.name]:
        e.target.type === "checkbox"
          ? e.target.checked
          : e.target.value,
    });
  };

  const saveSettings = async () => {
    try {
      const token = localStorage.getItem("token");

      await axios.put(
        "http://127.0.0.1:5000/api/admin/ai-settings",
        settings,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      toast.success("AI Settings Saved");

    } catch {
      toast.error("Save Failed");
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">

      <div className="bg-white shadow px-8 py-6">

        <h1 className="text-4xl font-bold flex items-center gap-3">
          <Brain />
          AI Settings
        </h1>

        <p className="text-gray-500 mt-2">
          Configure the AI evaluation engine.
        </p>

      </div>

      <div className="max-w-5xl mx-auto py-10">

        <div className="bg-white rounded-2xl shadow p-8 space-y-8">

          <div>

            <label className="font-semibold flex items-center gap-2">
              <Brain size={18}/>
              AI Model
            </label>

            <select
              name="aiModel"
              value={settings.aiModel}
              onChange={handleChange}
              className="mt-3 w-full border rounded-xl p-3"
            >
              <option>OpenAI</option>
              <option>Gemini</option>
              <option>Llama 3</option>
              <option>Mistral</option>
            </select>

          </div>

          <div>

            <label className="font-semibold flex items-center gap-2">
              <SlidersHorizontal size={18}/>
              Similarity Threshold (%)
            </label>

            <input
              type="range"
              min="50"
              max="100"
              name="similarityThreshold"
              value={settings.similarityThreshold}
              onChange={handleChange}
              className="w-full mt-3"
            />

            <p>{settings.similarityThreshold}%</p>

          </div>

          <div>

            <label className="font-semibold flex items-center gap-2">
              <ScanText size={18}/>
              OCR Confidence (%)
            </label>

            <input
              type="range"
              min="50"
              max="100"
              name="ocrConfidence"
              value={settings.ocrConfidence}
              onChange={handleChange}
              className="w-full mt-3"
            />

            <p>{settings.ocrConfidence}%</p>

          </div>

          <div>

            <label className="font-semibold flex items-center gap-2">
              <Award size={18}/>
              Maximum Marks Per Question
            </label>

            <input
              type="number"
              name="maxMarks"
              value={settings.maxMarks}
              onChange={handleChange}
              className="mt-3 border rounded-xl p-3 w-full"
            />

          </div>

          <div className="flex justify-between items-center">

            <div>

              <h3 className="font-semibold">
                Partial Marking
              </h3>

              <p className="text-gray-500 text-sm">
                Allow AI to award partial marks.
              </p>

            </div>

            <input
              type="checkbox"
              name="partialMarking"
              checked={settings.partialMarking}
              onChange={handleChange}
              className="w-5 h-5"
            />

          </div>

          <div className="flex justify-between items-center">

            <div>

              <h3 className="font-semibold">
                Automatic Evaluation
              </h3>

              <p className="text-gray-500 text-sm">
                Automatically evaluate uploaded answer sheets.
              </p>

            </div>

            <input
              type="checkbox"
              name="autoEvaluation"
              checked={settings.autoEvaluation}
              onChange={handleChange}
              className="w-5 h-5"
            />

          </div>

          <button
            onClick={saveSettings}
            className="bg-indigo-600 hover:bg-indigo-700 text-white px-8 py-3 rounded-xl flex items-center gap-2"
          >
            <Save size={18}/>
            Save Settings
          </button>

        </div>

      </div>

    </div>
  );
}