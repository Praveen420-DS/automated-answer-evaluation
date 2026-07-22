import { useEffect, useMemo, useState } from "react";
import toast from "react-hot-toast";
import { Bar, Doughnut } from "react-chartjs-2";
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, ArcElement, Tooltip, Legend } from "chart.js";
import { Brain, Download, FileText, ScanLine, Users } from "lucide-react";
import api from "../../services/api";

ChartJS.register(CategoryScale, LinearScale, BarElement, ArcElement, Tooltip, Legend);
const number = (value) => Number.isFinite(Number(value)) ? Number(value) : 0;

export default function Analytics() {
  const [analytics, setAnalytics] = useState(null);
  const [stats, setStats] = useState({});
  useEffect(() => { Promise.all([api.get("/admin/analytics"), api.get("/admin/dashboard")]).then(([a, d]) => { setAnalytics(a.data); setStats(d.data.statistics || {}); }).catch(() => { setAnalytics({ grades: {}, subjects: {}, averageMarks: 0 }); toast.error("Unable to load analytics"); }); }, []);
  const subjects = useMemo(() => Object.entries(analytics?.subjects || {}), [analytics]);
  const grades = analytics?.grades || {};
  const pass = number(grades.A) + number(grades.B) + number(grades.C) + number(grades.D);
  const fail = number(grades.F);
  if (!analytics) return <main className="admin-analytics-page"><p className="analytics-loading">Loading analytics…</p></main>;
  const hasData = subjects.length > 0 || pass + fail > 0;
  return <main className="admin-analytics-page">
    <header className="admin-analytics-heading"><div><h1>System Analytics</h1><p>Complete AI evaluation statistics</p></div><button><Download />Export Report</button></header>
    <section className="analytics-kpis"><Kpi icon={<Users />} label="Students" value={number(stats.students)} tone="blue"/><Kpi icon={<FileText />} label="Exams" value={number(stats.exams)} tone="green"/><Kpi icon={<Brain />} label="AI Evaluations" value={number(stats.evaluations)} tone="purple"/><Kpi icon={<ScanLine />} label="Average Marks" value={`${number(analytics.averageMarks)}%`} tone="orange"/></section>
    {!hasData ? <section className="analytics-empty"><Brain /><h2>No evaluation data yet</h2><p>Analytics will appear here once answer scripts have been evaluated.</p></section> : <section className="analytics-charts"><article><h2>Subject Performance</h2>{subjects.length ? <Bar data={{ labels: subjects.map(([name]) => name), datasets: [{ label: "Average marks", data: subjects.map(([, mark]) => number(mark)), backgroundColor: "#6448ed", borderRadius: 6 }] }} options={{ responsive: true, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, max: 100 } } }} /> : <EmptyChart />}</article><article><h2>Pass / Fail</h2>{pass + fail ? <Doughnut data={{ labels:["Pass", "Fail"], datasets:[{ data:[pass, fail], backgroundColor:["#22b86a", "#f04c58"], borderWidth:0 }] }} options={{ plugins:{ legend:{ position:"bottom" } }, cutout:"65%" }} /> : <EmptyChart />}</article></section>}
  </main>;
}
function Kpi({ icon, label, value, tone }) { return <article className={`analytics-kpi ${tone}`}><span>{icon}</span><div><small>{label}</small><b>{value}</b></div></article>; }
function EmptyChart() { return <div className="chart-empty">No data available</div>; }
