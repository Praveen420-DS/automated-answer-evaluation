import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { CalendarDays, BookOpen, Clock, Save } from "lucide-react";
import api from "../../services/api";
import { toast } from "react-hot-toast";

export default function CreateExam() {
  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);

  const [exam, setExam] = useState({
    examName: "",
    subject: "",
    department: "",
    year: "",
    semester: "",
    totalMarks: "",
    duration: "",
    examDate: "",
    instructions: "",
  });

  const handleChange = (e) => {
    setExam({
      ...exam,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (
      !exam.examName ||
      !exam.subject ||
      !exam.department ||
      !exam.year ||
      !exam.semester ||
      !exam.totalMarks ||
      !exam.examDate
    ) {
      toast.error("Please fill all required fields");
      return;
    }

    try {
      setLoading(true);

      await api.post("/faculty/create-exam", exam);

      toast.success("Exam Created Successfully");

      navigate("/faculty/upload-question-paper");
    } catch (err) {
      toast.error("Unable to create exam");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 py-10">

      <div className="max-w-5xl mx-auto bg-white rounded-3xl shadow-lg p-10">

        <h1 className="text-4xl font-bold">
          Create New Exam
        </h1>

        <p className="text-gray-500 mt-2">
          Fill the examination details before uploading documents.
        </p>

        <form
          onSubmit={handleSubmit}
          className="mt-10 space-y-6"
        >

          <div className="grid md:grid-cols-2 gap-6">

            <div>
              <label className="font-medium">
                Exam Name *
              </label>

              <input
                type="text"
                name="examName"
                value={exam.examName}
                onChange={handleChange}
                className="mt-2 w-full border rounded-xl p-3"
                placeholder="Internal Assessment 1"
              />
            </div>

            <div>
              <label className="font-medium">
                Subject *
              </label>

              <input
                type="text"
                name="subject"
                value={exam.subject}
                onChange={handleChange}
                className="mt-2 w-full border rounded-xl p-3"
                placeholder="Artificial Intelligence"
              />
            </div>

            <div>
              <label className="font-medium">
                Department *
              </label>

              <select
                name="department"
                value={exam.department}
                onChange={handleChange}
                className="mt-2 w-full border rounded-xl p-3"
              >
                <option value="">Select Department</option>
                <option>AI & DS</option>
                <option>CSE</option>
                <option>IT</option>
                <option>ECE</option>
                <option>EEE</option>
                <option>MECH</option>
              </select>
            </div>

            <div>
              <label className="font-medium">
                Year *
              </label>

              <select
                name="year"
                value={exam.year}
                onChange={handleChange}
                className="mt-2 w-full border rounded-xl p-3"
              >
                <option value="">Select Year</option>
                <option>1</option>
                <option>2</option>
                <option>3</option>
                <option>4</option>
              </select>
            </div>

            <div>
              <label className="font-medium">
                Semester *
              </label>

              <select
                name="semester"
                value={exam.semester}
                onChange={handleChange}
                className="mt-2 w-full border rounded-xl p-3"
              >
                <option value="">Semester</option>
                <option>1</option>
                <option>2</option>
                <option>3</option>
                <option>4</option>
                <option>5</option>
                <option>6</option>
                <option>7</option>
                <option>8</option>
              </select>
            </div>

            <div>
              <label className="font-medium">
                Total Marks *
              </label>

              <input
                type="number"
                name="totalMarks"
                value={exam.totalMarks}
                onChange={handleChange}
                className="mt-2 w-full border rounded-xl p-3"
                placeholder="100"
              />
            </div>

            <div>
              <label className="font-medium">
                Exam Date *
              </label>

              <input
                type="date"
                name="examDate"
                value={exam.examDate}
                onChange={handleChange}
                className="mt-2 w-full border rounded-xl p-3"
              />
            </div>

            <div>
              <label className="font-medium">
                Duration
              </label>

              <input
                type="text"
                name="duration"
                value={exam.duration}
                onChange={handleChange}
                className="mt-2 w-full border rounded-xl p-3"
                placeholder="3 Hours"
              />
            </div>

          </div>

          <div>
            <label className="font-medium">
              Instructions
            </label>

            <textarea
              rows="5"
              name="instructions"
              value={exam.instructions}
              onChange={handleChange}
              className="mt-2 w-full border rounded-xl p-3"
              placeholder="Enter examination instructions..."
            />
          </div>

          <div className="flex justify-end">

            <button
              type="submit"
              disabled={loading}
              className="bg-indigo-600 hover:bg-indigo-700 text-white px-8 py-3 rounded-xl flex items-center gap-2"
            >
              <Save size={18} />

              {loading ? "Creating..." : "Create Exam"}

            </button>

          </div>

        </form>

      </div>

    </div>
  );
}
