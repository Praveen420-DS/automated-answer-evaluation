import { Navigate, Route, Routes } from 'react-router-dom';
import Landing from '../pages/Landing/Landing';
import Login from '../pages/Auth/Login';
import RoleSelection from '../pages/Auth/RoleSelection';
import Register from '../pages/Auth/Register';
import ForgotPassword from '../pages/Auth/ForgotPassword';
import FacultyDashboard from '../pages/Faculty/Dashboard';
import CreateExam from '../pages/Faculty/CreateExam';
import UploadQuestionPaper from '../pages/Faculty/UploadQuestionPaper';
import UploadAnswerKey from '../pages/Faculty/UploadAnswerKey';
import UploadAnswerSheets from '../pages/Faculty/UploadAnswerSheets';
import EvaluationProgress from '../pages/Faculty/EvaluationProgress';
import ResultMatrix from '../pages/Faculty/ResultMatrix';
import Reports from '../pages/Faculty/Reports';
import Analytics from '../pages/Faculty/Analytics';
import FacultyProfile from '../pages/Faculty/FacultyProfile';
import StudentDashboard from '../pages/Student/Dashboard';
import MyExams from '../pages/Student/MyExams';
import MyResults from '../pages/Student/Result';
import ViewAnswerSheet from '../pages/Student/ViewAnswerScript';
import Transcript from '../pages/Student/Transcript';
import DownloadReport from '../pages/Student/DownloadReport';
import HelpSupport from '../pages/Student/HelpSupport';
import StudentProfile from '../pages/Student/Profile';
import StudentResult from '../pages/Student/StudentResult';
import NotFound from '../pages/Error/NotFound';
import ProtectedRoute from './ProtectedRoute';
import AdminDashboard from '../pages/Admin/Dashboard';
import AdminStudents from '../pages/Admin/Students';
import AdminFaculty from '../pages/Admin/Faculty';
import AdminExams from '../pages/Admin/Exams';
import AdminAnalytics from '../pages/Admin/Analytics';
import AdminAISettings from '../pages/Admin/AISettings';
import AdminLogs from '../pages/Admin/Logs';
import AdminSettings from '../pages/Admin/Settings';

export default function AppRoutes() {
  return <Routes>
    <Route path="/" element={<Landing />} />
    <Route path="/login" element={<RoleSelection />} />
    <Route path="/login/:role" element={<Login />} />
    <Route path="/register" element={<Register />} />
    <Route path="/forgot-password" element={<ForgotPassword />} />
    <Route path="/faculty/dashboard" element={<ProtectedRoute role="faculty"><FacultyDashboard /></ProtectedRoute>} />
    <Route path="/faculty/create-exam" element={<ProtectedRoute role="faculty"><CreateExam /></ProtectedRoute>} />
    <Route path="/faculty/upload-question-paper" element={<ProtectedRoute role="faculty"><UploadQuestionPaper /></ProtectedRoute>} />
    <Route path="/faculty/upload-answer-key" element={<ProtectedRoute role="faculty"><UploadAnswerKey /></ProtectedRoute>} />
    <Route path="/faculty/upload-answer-sheets" element={<ProtectedRoute role="faculty"><UploadAnswerSheets /></ProtectedRoute>} />
    <Route path="/faculty/evaluation" element={<ProtectedRoute role="faculty"><EvaluationProgress /></ProtectedRoute>} />
    <Route path="/faculty/result-matrix" element={<ProtectedRoute role="faculty"><ResultMatrix /></ProtectedRoute>} />
    <Route path="/faculty/reports" element={<ProtectedRoute role="faculty"><Reports /></ProtectedRoute>} />
    <Route path="/faculty/analytics" element={<ProtectedRoute role="faculty"><Analytics /></ProtectedRoute>} />
    <Route path="/faculty/profile" element={<ProtectedRoute role="faculty"><FacultyProfile /></ProtectedRoute>} />
    <Route path="/student/dashboard" element={<ProtectedRoute role="student" standalone><StudentDashboard /></ProtectedRoute>} />
    <Route path="/student/exams" element={<ProtectedRoute role="student"><MyExams /></ProtectedRoute>} />
    <Route path="/student/results" element={<ProtectedRoute role="student"><MyResults /></ProtectedRoute>} />
    <Route path="/student/result/:evaluationId" element={<ProtectedRoute role="student"><StudentResult /></ProtectedRoute>} />
    <Route path="/student/answer-sheet" element={<ProtectedRoute role="student"><ViewAnswerSheet /></ProtectedRoute>} />
    <Route path="/student/transcript" element={<ProtectedRoute role="student"><Transcript /></ProtectedRoute>} />
    <Route path="/student/download-report" element={<ProtectedRoute role="student"><DownloadReport /></ProtectedRoute>} />
    <Route path="/student/help" element={<ProtectedRoute role="student"><HelpSupport /></ProtectedRoute>} />
    <Route path="/student/profile" element={<ProtectedRoute role="student"><StudentProfile /></ProtectedRoute>} />
    <Route path="/admin/dashboard" element={<ProtectedRoute role="admin"><AdminDashboard /></ProtectedRoute>} />
    <Route path="/admin/students" element={<ProtectedRoute role="admin"><AdminStudents /></ProtectedRoute>} />
    <Route path="/admin/faculty" element={<ProtectedRoute role="admin"><AdminFaculty /></ProtectedRoute>} />
    <Route path="/admin/exams" element={<ProtectedRoute role="admin"><AdminExams /></ProtectedRoute>} />
    <Route path="/admin/analytics" element={<ProtectedRoute role="admin"><AdminAnalytics /></ProtectedRoute>} />
    <Route path="/admin/ai-settings" element={<ProtectedRoute role="admin"><AdminAISettings /></ProtectedRoute>} />
    <Route path="/admin/logs" element={<ProtectedRoute role="admin"><AdminLogs /></ProtectedRoute>} />
    <Route path="/admin/settings" element={<ProtectedRoute role="admin"><AdminSettings /></ProtectedRoute>} />
    <Route path="/home" element={<Navigate to="/" replace />} />
    <Route path="*" element={<NotFound />} />
  </Routes>;
}
