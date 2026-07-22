import { Link } from "react-router-dom";

export default function RememberMe({
  checked,
  onChange,
}) {
  return (
    <div className="flex items-center justify-between mb-6">

      {/* Remember Me */}

      <label className="flex items-center gap-3 cursor-pointer">

        <input
          type="checkbox"
          checked={checked}
          onChange={onChange}
          className="w-4 h-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
        />

        <span className="text-gray-600">

          Remember Me

        </span>

      </label>

      {/* Forgot Password */}

      <Link
        to="/forgot-password"
        className="text-indigo-600 hover:text-indigo-700 font-medium transition"
      >
        Forgot Password?
      </Link>

    </div>
  );
}