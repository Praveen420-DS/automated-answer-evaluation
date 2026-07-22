import FullAuthLayout from "../components/Auth/AuthLayout";

export default function AuthLayout({ children, title = "Welcome to EvalAI", subtitle = "Continue to your evaluation workspace" }) {
  return <FullAuthLayout title={title} subtitle={subtitle}>{children}</FullAuthLayout>;
}
