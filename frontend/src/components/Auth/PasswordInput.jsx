import React, { useState } from "react";
import { Lock, Eye, EyeOff } from "lucide-react";

export default function PasswordInput({
  label,
  name,
  value,
  onChange,
  placeholder = "Enter your password",
  error,
  required = false,
  disabled = false,
}) {
  const [showPassword, setShowPassword] = useState(false);

  return (
    <div className="mb-6">
      {/* Label */}
      <label
        htmlFor={name}
        className="block text-sm font-semibold text-gray-700 mb-2"
      >
        {label}
        {required && (
          <span className="text-red-500 ml-1">*</span>
        )}
      </label>

      {/* Input Container */}
      <div
        className={`flex items-center rounded-xl border bg-white px-4 py-3 transition-all duration-300 ${
          error
            ? "border-red-500 focus-within:ring-2 focus-within:ring-red-300"
            : "border-gray-300 focus-within:border-indigo-600 focus-within:ring-2 focus-within:ring-indigo-200"
        }`}
        style={{ width: "100%", minHeight: 64, padding: "14px 18px" }}
      >
        {/* Lock Icon */}
        <Lock
          size={20}
          className={`mr-3 ${
            error ? "text-red-500" : "text-gray-400"
          }`}
        />

        {/* Password Field */}
        <input
          id={name}
          name={name}
          type={showPassword ? "text" : "password"}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          required={required}
          disabled={disabled}
          className="flex-1 outline-none bg-transparent text-gray-800 placeholder:text-gray-400"
          style={{ border: "none", boxShadow: "none", padding: 0, minWidth: 0, fontSize: "16px" }}
        />

        {/* Show / Hide Button */}
        <button
          type="button"
          onClick={() => setShowPassword(!showPassword)}
          className="text-gray-500 hover:text-indigo-600 transition"
        >
          {showPassword ? (
            <EyeOff size={20} />
          ) : (
            <Eye size={20} />
          )}
        </button>
      </div>

      {/* Error */}
      {error && (
        <p className="text-red-500 text-sm mt-2">
          {error}
        </p>
      )}
    </div>
  );
}
