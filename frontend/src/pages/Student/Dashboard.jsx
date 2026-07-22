import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import toast from "react-hot-toast";
import {
  Award, Bell, BookOpen, ChevronRight, ClipboardList, Download, FileText,
  GraduationCap, HelpCircle, LayoutDashboard, LineChart, LogOut, Menu,
  Settings, UserRound, UsersRound
} from "lucide-react";
import "./student-dashboard.css";

const navItems = [
  ["Dashboard", LayoutDashboard, "/student/dashboard"], ["My Exams", ClipboardList, "/student/exams"],
  ["Results", LineChart, "/student/results"], ["Transcripts", FileText, "/student/transcript"],
  ["Reports", LineChart, "/student/download-report"], ["Profile", UserRound, "/student/profile"],
  ["Settings", Settings, "/student/profile"], ["Help & Support", HelpCircle, "#help"],
];
const quickLinks = [["My Exams", "View all your exams", ClipboardList, "/student/exams"], ["Results", "Check your results", LineChart, "/student/results"], ["Transcripts", "Download transcripts", FileText, "/student/transcript"], ["Reports", "View detailed reports", LineChart, "/student/download-report"]];

export default function StudentDashboard() {
  const navigate = useNavigate();
  const [student, setStudent] = useState(null);
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => { loadDashboard(); }, []);
  async function loadDashboard() {
    try {
      const res = await axios.get("http://127.0.0.1:5000/api/student/dashboard", { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } });
      setStudent(res.data);
    } catch { toast.error("Unable to load dashboard"); setStudent({ name: localStorage.getItem("username") || "Student", registerNo: "—", department: "—", averageMarks: 0, completedExams: 0, exams: [] }); }
  }
  function logout() { localStorage.clear(); navigate("/login"); }
  if (!student) return <div className="student-loading">Loading your dashboard…</div>;
  const exams = student.exams || [];
  const name = student.name || student.username || "Student";
  const stats = [[UserRound, "Register No", student.registerNo || "—", "violet"], [GraduationCap, "Department", student.department || "—", "green"], [Award, "Average Marks", `${student.averageMarks || 0}%`, "orange"], [FileText, "Exams Completed", student.completedExams || 0, "purple"]];

  return <div className="student-workspace">
    <aside className={menuOpen ? "student-sidebar open" : "student-sidebar"}>
      <div className="student-brand"><span><GraduationCap /></span>Eval<span>AI</span></div>
      <p className="student-panel-label">Student Panel</p>
      <nav>{navItems.map(([label, Icon, path]) => <button key={label} onClick={() => { if (path !== "#help") navigate(path); setMenuOpen(false); }} className={label === "Dashboard" ? "active" : ""}><Icon />{label}</button>)}</nav>
      <div id="help" className="student-help"><b>Need Help?</b><p>Our support team is here to assist you.</p><button><HelpCircle /> Contact Support</button></div>
    </aside>
    <main className="student-main">
      <header className="student-topbar"><button className="student-menu" onClick={() => setMenuOpen(!menuOpen)}><Menu /></button><span>Automated Answer Script Evaluation</span><div className="topbar-actions"><button className="notification"><Bell /><i>3</i></button><div className="student-avatar"><UserRound /></div><div><b>{name}</b><small>Student</small></div><ChevronRight className="down" /></div></header>
      <section className="student-content">
        <div className="dashboard-heading"><div><p>Welcome back, {name}! 👋</p><h1>Student Dashboard <span>👋</span></h1></div><button onClick={logout}><LogOut /> Logout</button></div>
        <section className="student-stats">{stats.map(([Icon, label, value, tone]) => <article key={label} className={`student-stat ${tone}`}><span><Icon /></span><p>{label}</p><strong>{value}</strong></article>)}</section>
        <section className="student-grid top-grid">
          <article className="student-card evaluations"><div className="card-title"><h2><ClipboardList /> Recent Evaluations</h2><button>All Exams <ChevronRight /></button></div><div className="evaluation-table"><div className="table-head"><span>Subject</span><span>Marks</span><span>AI Score</span><span>Status</span><span>Action</span></div>{exams.length ? exams.slice(0, 4).map((exam) => <div className="table-row" key={exam.examId}><span>{exam.subject}</span><span>{exam.marks}</span><span>{exam.aiScore}%</span><span>{exam.status}</span><button onClick={() => navigate(`/student/result/${exam.examId}`)}>View</button></div>) : <div className="empty-evaluations"><BookOpen /><b>No evaluations yet</b><p>Your evaluated answer scripts will appear here.</p></div>}</div><div className="evaluation-actions"><button onClick={() => navigate("/student/results")}>View All Results <ChevronRight /></button><button onClick={() => navigate("/student/transcript")}> <FileText /> Academic Transcript</button><button onClick={() => navigate("/student/download-report")}> <Download /> Download Reports</button></div></article>
          <article className="student-card performance"><h2>Performance Overview</h2><div className="performance-chart"><span className="y y1">100%</span><span className="y y2">75%</span><span className="y y3">50%</span><span className="y y4">25%</span><span className="y y5">0%</span><svg viewBox="0 0 310 180" preserveAspectRatio="none"><defs><linearGradient id="chartFill" x1="0" x2="0" y1="0" y2="1"><stop stopColor="#7855ed" stopOpacity=".28" /><stop offset="1" stopColor="#7855ed" stopOpacity=".03" /></linearGradient></defs><path d="M20 132 L72 105 L123 86 L176 86 L228 40 L290 28 L290 165 L20 165Z" fill="url(#chartFill)"/><polyline points="20,132 72,105 123,86 176,86 228,40 290,28" fill="none" stroke="#6745ed" strokeWidth="2"/>{[[20,132],[72,105],[123,86],[176,86],[228,40],[290,28]].map(([cx,cy]) => <circle key={cx} cx={cx} cy={cy} r="4" fill="#6745ed"/>)}</svg><div className="months">Jan <span>Feb</span><span>Mar</span><span>Apr</span><span>May</span><span>Jun</span></div></div></article>
        </section>
        <section className="student-grid bottom-grid"><article className="student-card activity"><h2>Recent Activity</h2>{[["New exam ‘Data Structures’ completed", "You have completed the exam successfully.", ClipboardList], ["Answer script evaluated", "AI evaluation completed for Data Structures.", Award], ["Report downloaded", "You downloaded the report for Mathematics.", Download], ["Profile updated", "Your profile information has been updated.", UserRound]].map(([title, text, Icon], i) => <div className="activity-row" key={title}><span><Icon /></span><div><b>{title}</b><p>{text}</p></div><small>{i === 3 ? "1 week ago" : `${i + 2} days ago`}</small></div>)}</article><article className="student-card progress"><h2>Subject-wise Progress</h2><div className="donut" /><div className="donut-value"><b>0%</b><span>Overall</span></div><div className="subject-list">{["Data Structures", "Machine Learning", "Mathematics", "Database Systems", "Others"].map((subject, i) => <p key={subject}><i className={`dot d${i}`} />{subject}<b>0%</b></p>)}</div></article><article className="student-card quick-links"><h2>Quick Links</h2>{quickLinks.map(([title, text, Icon, path]) => <button key={title} onClick={() => navigate(path)}><span><Icon /></span><div><b>{title}</b><small>{text}</small></div><ChevronRight /></button>)}</article></section>
      </section>
    </main>
  </div>;
}
