import { Navigate } from "react-router-dom";
import useAuth from "../hooks/useAuth";
import DashboardShell from "../layouts/DashboardShell";

export default function ProtectedRoute({
    children,
    role,
    standalone = false,
}) {
    const { user, loading } = useAuth();

    if (loading) {
        return <h2>Loading...</h2>;
    }

    if (!user) {
        return <Navigate to="/login" replace />;
    }

    if (role && user.role !== role) {
        return <Navigate to="/" replace />;
    }

    return standalone ? children : <DashboardShell>{children}</DashboardShell>;
}
