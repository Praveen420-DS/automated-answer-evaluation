import { motion } from "framer-motion";
import { ArrowRight, LockKeyhole, ShieldCheck, GraduationCap, UserRoundCog } from "lucide-react";
import { useNavigate } from "react-router-dom";

import AuthLayout from "../../components/Auth/AuthLayout";

const roles = [
  {
    id: "student",
    label: "Student",
    description: "View exams, results, and feedback.",
    icon: GraduationCap,
    iconClass: "student",
  },
  {
    id: "staff",
    label: "Staff",
    description: "Create exams and evaluate answer scripts.",
    icon: UserRoundCog,
    iconClass: "staff",
  },
  {
    id: "admin",
    label: "Admin",
    description: "Manage users, settings, and the platform.",
    icon: ShieldCheck,
    iconClass: "admin",
  },
];

export default function RoleSelection() {
  const navigate = useNavigate();

  return (
    <AuthLayout
      title="Welcome to EvalAI"
      subtitle="Choose how you want to sign in"
    >
      <div className="role-list">
        {roles.map(({ id, label, description, icon: Icon, iconClass }) => (
          <motion.button
            key={id}
            type="button"
            whileHover={{ y: -2 }}
            whileTap={{ scale: 0.99 }}
            onClick={() => navigate(`/login/${id}`)}
            className="role-option"
          >
            <span className={`role-option-icon ${iconClass}`}>
              <Icon />
            </span>
            <span className="role-option-copy">
              <span>{label}</span>
              <small>{description}</small>
            </span>
            <ArrowRight className="role-option-arrow" />
          </motion.button>
        ))}
      </div>
      <p className="role-trust"><LockKeyhole /> Secure <b>•</b> Reliable <b>•</b> Intelligent</p>
    </AuthLayout>
  );
}
