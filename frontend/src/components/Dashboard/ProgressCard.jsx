export default function ProgressCard({ label='Evaluation progress', value=0 }) { return <article className="card"><b>{label}</b><progress value={value} max="100" /> {value}%</article>; }
