export default function Modal({ open, children }) { return open ? <div role="dialog" className="card">{children}</div> : null; }
