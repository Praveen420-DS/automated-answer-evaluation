import { useState } from "react";
import { ArrowRight, Mail, UserPlus, UserRound } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";
import toast from "react-hot-toast";

import AuthLayout from "../../components/Auth/AuthLayout";
import AuthButton from "../../components/Auth/AuthButton";
import PasswordInput from "../../components/Auth/PasswordInput";
import TextInput from "../../components/Auth/TextInput";
import api from "../../services/api";

export default function Register() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ fullName: "", email: "", password: "" });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

  function updateField(event) {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
    setErrors((current) => ({ ...current, [name]: "" }));
  }

  function validate() {
    const nextErrors = {};
    if (form.fullName.trim().length < 2) nextErrors.fullName = "Enter your full name.";
    if (!/^\S+@\S+\.\S+$/.test(form.email)) nextErrors.email = "Enter a valid email address.";
    if (form.password.length < 8) nextErrors.password = "Use at least 8 characters.";
    setErrors(nextErrors);
    return Object.keys(nextErrors).length === 0;
  }

  async function submit(event) {
    event.preventDefault();
    if (!validate()) return;
    try {
      setLoading(true);
      const response = await api.post("/auth/register", { ...form, role: "student" });
      toast.success(response.data.message || "Account created successfully.");
      navigate("/login/student", { replace: true });
    } catch (error) {
      toast.error(error.response?.data?.message || "Unable to create your account.");
    } finally {
      setLoading(false);
    }
  }

  return <AuthLayout title="Welcome to EvalAI" subtitle="Continue to your evaluation workspace">
    <div className="register-intro"><span><UserPlus /></span><div><h3>Create Account</h3><p>Fill in your details to get started</p></div></div>
    <form onSubmit={submit} className="register-form">
      <TextInput label="Full Name" name="fullName" value={form.fullName} onChange={updateField} placeholder="Enter your full name" icon={UserRound} error={errors.fullName} required />
      <TextInput label="Email" type="email" name="email" value={form.email} onChange={updateField} placeholder="Enter your email address" icon={Mail} error={errors.email} required />
      <PasswordInput label="Password" name="password" value={form.password} onChange={updateField} placeholder="Create a strong password" error={errors.password} required />
      <AuthButton text={<><span>Register</span><ArrowRight size={20} /></>} loading={loading} />
    </form>
    <div className="register-or"><span />or<span /></div>
    <p className="register-signin">Already have an account? <Link to="/login">Sign in</Link></p>
  </AuthLayout>;
}
