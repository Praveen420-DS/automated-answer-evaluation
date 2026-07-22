import { useMemo, useState } from "react";
import { BarChart3, CalendarDays, ChevronDown, Download, FileSpreadsheet, FileText, LockKeyhole, RefreshCw, Search, ShieldCheck, Star } from "lucide-react";
import { toast } from "react-hot-toast";

const reports = [];
const metrics = [[FileText,"Total Reports","0","No reports yet","violet"],[FileText,"PDF Reports","0","No reports generated","green"],[Download,"Total Downloads","0","No downloads yet","blue"],[Star,"Average AI Score","0%","No evaluation data","orange"],[CalendarDays,"Latest Report","—","No reports yet","red"]];

export default function Reports() {
  const [query, setQuery] = useState("");
  const [refreshing, setRefreshing] = useState(false);
  const visibleReports = useMemo(() => reports.filter((report) => report.slice(0, 3).join(" ").toLowerCase().includes(query.toLowerCase())), [query]);
  const refresh = () => { setRefreshing(true); setTimeout(() => { setRefreshing(false); toast.success("Reports refreshed"); }, 500); };
  const download = (name) => toast.success(`${name} download started`);
  return <main className="reports-page">
    <header className="reports-heading"><div><h1>Reports Dashboard</h1><p>View, analyze and download examination reports and AI evaluation summaries.</p></div><button onClick={refresh} className="reports-refresh"><RefreshCw className={refreshing ? "spin" : ""} />Refresh</button></header>
    <section className="report-metrics">{metrics.map(([Icon, title, value, note, tone]) => <article key={title} className="report-metric"><span className={`metric-icon ${tone}`}><Icon /></span><div><small>{title}</small><b>{value}</b><em className={tone}>{note}</em></div></article>)}</section>
    <section className="report-controls"><label className="report-search"><Search /><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search by exam name, subject or keyword..." /></label><div className="report-filter-row"><Filter text="All Exams" /><Filter text="All Departments" /><Filter text="All Semesters" /><button disabled className="date-filter"><CalendarDays />No report dates available</button><button disabled className="excel-export"><FileSpreadsheet />Export Excel</button><button disabled className="pdf-export"><FileText />Export PDF</button></div></section>
    <section className="reports-table-card"><div className="report-table-wrap"><table className="reports-table"><thead><tr><th>#</th><th>Exam Name</th><th>Subject</th><th>Department</th><th>Students</th><th>AI Avg Score</th><th>Generated On</th><th>Actions</th></tr></thead><tbody><tr><td colSpan="8" className="reports-empty"><FileText /><b>No reports available</b><span>Reports will appear here after you upload and evaluate answer scripts.</span></td></tr></tbody></table></div><footer className="table-footer"><span>Showing 0 to 0 of 0 reports</span></footer></section>
    <section className="reports-bottom"><AnalyticsCard /><DistributionCard /><DownloadsCard /></section>
    <footer className="reports-security"><ShieldCheck /><div><b>All reports are securely generated and stored. You can download or share reports with students.</b><span>Reports are generated using AI and verified for accuracy.</span></div><LockKeyhole /><div><b>Secure & Confidential</b><span>Your data is protected</span></div></footer>
  </main>;
}
function Filter({ text }) { return <button disabled className="select-filter">{text}<ChevronDown /></button>; }
function AnalyticsCard() { return <article className="report-panel analytics-panel"><h2>Report Analytics</h2>{[["Average Marks","0%","violet"],["Pass Percentage","0%","green"],["AI Accuracy","0%","blue"],["Total Evaluated Scripts","0","violet"]].map(([label,value,tone]) => <div className="analytics-row" key={label}><span className={tone}><BarChart3 /></span><b>{label}</b><em className={tone}>{value}</em></div>)}</article>; }
function DistributionCard() { return <article className="report-panel distribution-panel"><h2>Grade Distribution</h2><div className="distribution-content"><div className="donut empty-donut"><b>0<small>Total</small></b></div><ul>{[["A (90-100)","0% (0)","green"],["B (80-89)","0% (0)","blue"],["C (70-79)","0% (0)","orange"],["D (60-69)","0% (0)","purple"],["F (0-59)","0% (0)","red"]].map(([label,value,tone]) => <li key={label}><i className={tone}/><span>{label}</span><b>{value}</b></li>)}</ul></div></article>; }
function DownloadsCard() { return <article className="report-panel downloads-panel"><h2>Recent Downloads</h2><div className="downloads-empty"><Download /><b>No downloads yet</b><span>Your downloaded reports will appear here.</span></div></article>; }
