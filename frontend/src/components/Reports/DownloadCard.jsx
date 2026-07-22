export default function DownloadCard({ onDownload=()=>{} }) { return <article className="card"><h3>Download report</h3><button onClick={onDownload}>Download PDF</button></article>; }
