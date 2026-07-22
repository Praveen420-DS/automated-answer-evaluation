export default function PageHeader({ title, description }) { return <header><h1>{title}</h1>{description && <p className="muted">{description}</p>}</header>; }
