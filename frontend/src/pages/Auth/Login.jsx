import { useState } from "react";
import { User } from "lucide-react";
import { toast } from "react-hot-toast";
import { useNavigate, Link, Navigate, useParams } from "react-router-dom";

import AuthLayout from "../../components/Auth/AuthLayout";
import TextInput from "../../components/Auth/TextInput";
import PasswordInput from "../../components/Auth/PasswordInput";
import AuthButton from "../../components/Auth/AuthButton";

import api from "../../services/api";
import useAuth from '../../hooks/useAuth';

export default function Login() {
  const navigate = useNavigate();
  const { role: selectedRole } = useParams();
  const { login } = useAuth();

  const roleDetails = {
    student: { label: "Student", apiRole: "student" },
    staff: { label: "Staff", apiRole: "faculty" },
    admin: { label: "Admin", apiRole: "admin" },
  }[selectedRole];

  if (!roleDetails) {
    return <Navigate to="/login" replace />;
  }

  const [form, setForm] = useState({
    username: "",
    password: "",
  });

  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });

    setErrors({
      ...errors,
      [e.target.name]: "",
    });
  };

  const validate = () => {
    let err = {};

    if (!form.username.trim()) {
      err.username = "Username is required";
    }

    if (!form.password.trim()) {
      err.password = "Password is required";
    }

    setErrors(err);

    return Object.keys(err).length === 0;
  };

  const handleLogin = async (e) => {
    e.preventDefault();

    if (!validate()) return;

    try {
      setLoading(true);

      const res = await api.post("/auth/login", form);

      if (res.data.success) {
        const payload = res.data.data || res.data;
        const user = payload.user || { username: form.username, role: payload.role };
        const apiRole = String(user.role || payload.role || '').toLowerCase();
        const role = apiRole === 'staff' ? 'faculty' : apiRole;
        const destination = role === 'student' ? '/student/dashboard' :
          role === 'faculty' ? '/faculty/dashboard' :
          role === 'admin' ? '/admin/dashboard' : null;

        if (!destination) {
          toast.error('Your account does not have a valid role.');
          return;
        }
        if (role !== roleDetails.apiRole) {
          toast.error(`This account is not registered as ${roleDetails.label}.`);
          return;
        }
        toast.success("Login Successful");
        const token = payload.token || res.data.token || '';
        if (!token) throw new Error("Authentication token was not returned.");
        localStorage.setItem("role", role);
        localStorage.setItem("username", user.username || form.username);
        login(token, { ...user, username: user.username || form.username, role });
        navigate(destination, { replace: true });
      } else {
        toast.error(res.data.message);
      }
    } catch (err) {
      toast.error(
        err.response?.data?.message || "Invalid Username or Password"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthLayout
      title={`${roleDetails.label} Login`}
      subtitle={`Login to your ${roleDetails.label.toLowerCase()} EvalAI account`}
    >
      <Link to="/login" className="mb-6 inline-block text-sm font-medium text-indigo-600 hover:underline">
        ← Choose a different role
      </Link>
      <form onSubmit={handleLogin}>

        <TextInput
          label="Username"
          name="username"
          placeholder="Enter Username"
          value={form.username}
          onChange={handleChange}
          icon={User}
          error={errors.username}
          required
        />

        <PasswordInput
          label="Password"
          name="password"
          value={form.password}
          onChange={handleChange}
          error={errors.password}
          required
        />

        <div className="flex justify-end mb-6">
          <Link
            to="/forgot-password"
            className="text-indigo-600 hover:underline"
          >
            Forgot Password?
          </Link>
        </div>

        <AuthButton
          text="Login"
          loading={loading}
        />

        <div className="mt-9 border-t border-slate-200 pt-8 text-center text-sm text-slate-500">
          Don't have an account? <Link to="/register" className="font-semibold text-indigo-600 hover:underline">Sign up here</Link>
        </div>

      </form>
    </AuthLayout>
  );
}
