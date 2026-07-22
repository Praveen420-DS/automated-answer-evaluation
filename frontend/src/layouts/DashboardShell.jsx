import { BarChart3, ClipboardCheck, FileText, GraduationCap, LayoutDashboard, LogOut, Settings, Upload, Users } from "lucide-react";
import { NavLink, useNavigate } from "react-router-dom";
import useAuth from "../hooks/useAuth";

const navigation = {
  admin: [["Dashboard", "/admin/dashboard", LayoutDashboard], ["Students", "/admin/students", GraduationCap], ["Faculty", "/admin/faculty", Users], ["Exams", "/admin/exams", FileText], ["Analytics", "/admin/analytics", BarChart3], ["Settings", "/admin/settings", Settings]],
  faculty: [["Dashboard", "/faculty/dashboard", LayoutDashboard], ["Create exam", "/faculty/create-exam", FileText], ["Upload scripts", "/faculty/upload-answer-sheets", Upload], ["Evaluation", "/faculty/evaluation", ClipboardCheck], ["Results", "/faculty/result-matrix", BarChart3], ["Reports", "/faculty/reports", FileText]],
  student: [["Dashboard", "/student/dashboard", LayoutDashboard], ["My exams", "/student/exams", FileText], ["Results", "/student/results", ClipboardCheck], ["Transcript", "/student/transcript", GraduationCap], ["Reports", "/student/download-report", Upload], ["Profile", "/student/profile", Settings]],
};

export default function DashboardShell({ children }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const links = navigation[user?.role] || [];
  const handleLogout = () => { logout(); navigate("/login", { replace: true }); };
  return <div className="dashboard-shell">
    <aside className="dashboard-sidebar">
      <NavLink to="/" className="dashboard-brand"><span>✦</span> EvalAI</NavLink>
      <p className="sidebar-role">{user?.role || "account"} panel</p>
      <nav>{links.map(([label, path, Icon]) => <NavLink key={path} to={path} className={({ isActive }) => `sidebar-link ${isActive ? "active" : ""}`}><Icon size={17} />{label}</NavLink>)}</nav>
      <button type="button" onClick={handleLogout} className="sidebar-link sidebar-logout"><LogOut size={17} />Logout</button>
    </aside>
    <section className="dashboard-main"><header className="dashboard-topbar"><div><span className="eyebrow">Automated Answer Script Evaluation</span><strong>EvalAI Workspace</strong></div><div className="account-chip"><span>{(user?.fullName || user?.username || "U").slice(0, 1).toUpperCase()}</span><div><b>{user?.fullName || user?.username || "Account"}</b><small>{user?.role}</small></div></div></header>{children}</section>
  </div>;
}
