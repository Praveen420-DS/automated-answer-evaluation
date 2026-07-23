import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { BookOpen, CalendarDays, Check, Clock, FilePlus2, HelpCircle, ImagePlus, Link, List, ListOrdered, Save, ShieldCheck, Sparkles, Underline } from "lucide-react";
import api from "../../services/api";
import { toast } from "react-hot-toast";

export default function CreateExam() {
  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);
  const [options, setOptions] = useState({ autoEvaluation: true, reports: true, password: false });

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

      const { data } = await api.post("/faculty/create-exam", exam);
      const examId = data?.data?._id;
      if (!examId) throw new Error("The server did not return an exam ID.");

      toast.success("Exam Created Successfully");

      navigate("/faculty/upload-question-paper", { state: { examId } });
    } catch (err) {
      toast.error("Unable to create exam");
    } finally {
      setLoading(false);
    }
  };

  const toggleOption = (name) => setOptions((current) => ({ ...current, [name]: !current[name] }));
  const field = (label, name, content, icon) => <label className="exam-field"><span>{label} <b>*</b></span><div className="exam-control">{icon}{content}</div></label>;

  return <main className="create-exam-page">
    <div className="exam-page-heading"><div className="heading-icon"><FilePlus2 /></div><div><h1>Create New Exam</h1><p>Fill in the exam details before uploading documents.</p></div><button type="button" onClick={() => toast("Complete the exam details, then create the exam to upload documents.")} className="how-it-works"><HelpCircle />How it works?</button></div>
    <form onSubmit={handleSubmit} className="exam-card">
      <section><div className="section-title"><BookOpen />Basic Information</div><div className="section-marker" />
        <div className="exam-grid">
          {field("Exam Name", "examName", <input name="examName" value={exam.examName} onChange={handleChange} placeholder="Internal Assessment 1" />, <FilePlus2 />)}
          {field("Subject", "subject", <input name="subject" value={exam.subject} onChange={handleChange} placeholder="Artificial Intelligence" />, <BookOpen />)}
          {field("Department", "department", <select name="department" value={exam.department} onChange={handleChange}><option value="">Select Department</option><option>Computer Science and Engineering</option><option>AI & DS</option><option>IT</option><option>ECE</option></select>)}
          {field("Year", "year", <select name="year" value={exam.year} onChange={handleChange}><option value="">Select Year</option><option>First Year</option><option>Second Year</option><option>Third Year</option><option>Fourth Year</option></select>)}
          {field("Semester", "semester", <select name="semester" value={exam.semester} onChange={handleChange}><option value="">Select Semester</option>{[1,2,3,4,5,6,7,8].map((number) => <option key={number}>Semester {number}</option>)}</select>)}
          {field("Total Marks", "totalMarks", <input type="number" name="totalMarks" value={exam.totalMarks} onChange={handleChange} placeholder="100" />, <ImagePlus />)}
          {field("Exam Date", "examDate", <input type="date" name="examDate" value={exam.examDate} onChange={handleChange} />, <CalendarDays />)}
          {field("Duration", "duration", <input name="duration" value={exam.duration} onChange={handleChange} placeholder="3 Hours" />, <Clock />)}
        </div>
        <label className="exam-instructions"><span>Exam Instructions</span><div className="editor"><div className="editor-tools"><b>B</b><i>I</i><Underline /><List /><ListOrdered /><Link /></div><textarea name="instructions" value={exam.instructions} onChange={handleChange} placeholder="Read all questions carefully.&#10;Answer all questions.&#10;Write neatly.&#10;No negative marking." /><small>{exam.instructions.length} / 500</small></div></label>
      </section>
      <section className="additional-section"><div className="section-title"><Sparkles />Additional Options</div><div className="section-marker" /><div className="option-grid">
        <Option enabled={options.autoEvaluation} onClick={() => toggleOption("autoEvaluation")} icon={<ShieldCheck />} title="Auto Evaluation" text="Enable AI evaluation for uploaded scripts" />
        <Option enabled={options.reports} onClick={() => toggleOption("reports")} icon={<BarChartIcon />} title="Generate Reports" text="Generate detailed reports automatically" />
        <Option enabled={options.password} onClick={() => toggleOption("password")} icon={<ShieldCheck />} title="Password Protection" text="Protect exam with password" />
      </div></section>
      <footer className="exam-actions"><button type="button" className="cancel-action" onClick={() => navigate(-1)}>Cancel</button><div><button type="button" className="draft-action" onClick={() => toast.success("Draft saved locally")}><Save />Save as Draft</button><button type="submit" disabled={loading} className="create-action">{loading ? "Creating..." : "Create Exam"} <span>→</span></button></div></footer>
    </form>
  </main>;
}

function BarChartIcon() { return <span className="bar-chart-icon">▂▅▇</span>; }
function Option({ enabled, onClick, icon, title, text }) { return <button type="button" className={`exam-option ${enabled ? "selected" : ""}`} onClick={onClick}><span className="option-check">{enabled && <Check />}</span><span className="option-icon">{icon}</span><span><b>{title}</b><small>{text}</small></span></button>; }
