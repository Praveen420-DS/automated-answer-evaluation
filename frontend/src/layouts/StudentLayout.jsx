import Navbar from '../components/Navbar/Navbar'; import StudentSidebar from '../components/Sidebar/StudentSidebar';
export default function StudentLayout({children}){return <div className="app-shell"><StudentSidebar/><div className="app-content"><Navbar/>{children}</div></div>}
