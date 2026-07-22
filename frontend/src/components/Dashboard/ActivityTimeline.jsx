export default function ActivityTimeline({ items=[] }) { return <div className="card"><h3>Activity</h3>{items.map((item,i)=><p key={i}>{item}</p>)}</div>; }
