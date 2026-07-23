import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";
import api from "../../services/api";
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
  ["Settings", Settings, "/student/profile"], ["Help & Support", HelpCircle, "/student/help"],
];
const quickLinks = [["My Exams", "View all your exams", ClipboardList, "/student/exams"], ["Results", "Check your results", LineChart, "/student/results"], ["Transcripts", "Download transcripts", FileText, "/student/transcript"], ["Reports", "View detailed reports", LineChart, "/student/download-report"]];

export default function StudentDashboard() {
  const navigate = useNavigate();
  const [student, setStudent] = useState(null);
  const [menuOpen, setMenuOpen] = useState(false);
  const [notificationsOpen, setNotificationsOpen] = useState(false);
  const [accountOpen, setAccountOpen] = useState(false);

  useEffect(() => { window.scrollTo(0, 0); loadDashboard(); }, []);
  async function loadDashboard() {
    try {
      const res = await api.get("/student/dashboard");
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
      <nav>{navItems.map(([label, Icon, path]) => <button key={label} onClick={() => { navigate(path); setMenuOpen(false); }} className={label === "Dashboard" ? "active" : ""}><Icon />{label}</button>)}</nav>
      <div className="student-help"><b>Need Help?</b><p>Our support team is here to assist you.</p><button onClick={() => navigate("/student/help")}><HelpCircle /> Contact Support</button></div>
    </aside>
    <main className="student-main">
      <header className="student-topbar"><button className="student-menu" onClick={() => setMenuOpen(!menuOpen)}><Menu /></button><span>Automated Answer Script Evaluation</span><div className="topbar-actions"><button className="notification" onClick={() => setNotificationsOpen((open) => !open)} aria-label="Notifications"><Bell /><i>3</i></button>{notificationsOpen && <div className="student-popover notifications-popover"><b>Notifications</b><p>Your profile is up to date.</p><p>New exam updates will appear here.</p></div>}<button className="student-avatar" onClick={() => navigate("/student/profile")} aria-label="Open profile">{student.photo ? <img src={`${import.meta.env.VITE_API_ORIGIN || "http://127.0.0.1:5000"}${student.photo}`} alt="Profile" /> : <UserRound />}</button><button className="student-account-button" onClick={() => setAccountOpen((open) => !open)}><span><b>{name}</b><small>Student</small></span><ChevronRight className="down" /></button>{accountOpen && <div className="student-popover account-popover"><button onClick={() => navigate("/student/profile")}>Profile</button><button onClick={logout}>Logout</button></div>}</div></header>
      <section className="student-content">
        <div className="dashboard-heading"><div><p>Welcome back, {name}! 👋</p><h1>Student Dashboard <span>👋</span></h1></div><button onClick={logout}><LogOut /> Logout</button></div>
        <section className="student-stats">{stats.map(([Icon, label, value, tone]) => <article key={label} className={`student-stat ${tone}`}><span><Icon /></span><p>{label}</p><strong>{value}</strong></article>)}</section>
        <section className="student-grid top-grid">
          <article className="student-card evaluations"><div className="card-title"><h2><ClipboardList /> Recent Evaluations</h2><button>All Exams <ChevronRight /></button></div><div className="evaluation-table"><div className="table-head"><span>Subject</span><span>Marks</span><span>Score</span><span>Status</span><span>Action</span></div>{exams.length ? exams.slice(0, 4).map((exam) => <div className="table-row" key={exam.evaluationId}><span>{exam.subject}</span><span>{exam.marks}</span><span>{exam.aiScore}%</span><span>{exam.status}</span><button onClick={() => navigate(`/student/result/${exam.evaluationId}`)}>View</button></div>) : <div className="empty-evaluations"><BookOpen /><b>No evaluations yet</b><p>Your evaluated answer scripts will appear here.</p></div>}</div><div className="evaluation-actions"><button onClick={() => navigate("/student/results")}>View All Results <ChevronRight /></button><button onClick={() => navigate("/student/transcript")}> <FileText /> Academic Transcript</button><button onClick={() => navigate("/student/download-report")}> <Download /> Download Reports</button></div></article>
          <article className="student-card performance"><h2>Performance Overview</h2>{exams.length ? <div className="performance-chart"><span className="y y1">100%</span><span className="y y2">75%</span><span className="y y3">50%</span><span className="y y4">25%</span><span className="y y5">0%</span><svg viewBox="0 0 310 180" preserveAspectRatio="none"><polyline points="20,132 72,105 123,86 176,86 228,40 290,28" fill="none" stroke="#6745ed" strokeWidth="2"/></svg></div> : <EmptyDashboardCard text="Complete an evaluated exam to view your performance." />}</article>
        </section>
        <section className="student-grid bottom-grid" style={{ gridTemplateColumns: "minmax(0, 1fr) minmax(0, 1.04fr) minmax(0, .9fr)" }}><article className="student-card activity"><h2>Recent Activity</h2>{exams.length ? exams.slice(0, 4).map((exam) => <div className="activity-row" key={exam.evaluationId}><span><Award /></span><div><b>{exam.subject || "Exam evaluation"}</b><p>{exam.status || "Evaluation status updated"}</p></div></div>) : <EmptyDashboardCard text="Your exam activity will appear here." />}</article><article className="student-card progress"><h2>Subject-wise Progress</h2>{exams.length ? <><div className="donut" /><div className="donut-value"><b>{student.averageMarks || 0}%</b><span>Overall</span></div><div className="subject-list">{exams.slice(0, 5).map((exam, i) => <p key={exam.evaluationId}><i className={`dot d${i}`} />{exam.subject}<b>{exam.marks || 0}%</b></p>)}</div></> : <EmptyDashboardCard text="Subject progress will appear after evaluation." />}</article><article className="student-card quick-links"><h2>Quick Links</h2>{quickLinks.map(([title, text, Icon, path]) => <button key={title} onClick={() => navigate(path)}><span><Icon /></span><div><b>{title}</b><small>{text}</small></div><ChevronRight /></button>)}</article></section>
      </section>
    </main>
  </div>;
}

function EmptyDashboardCard({ text }) { return <div className="grid min-h-52 place-items-center px-6 text-center text-sm text-slate-500"><BookOpen className="text-violet-400" /><p>{text}</p></div>; }
