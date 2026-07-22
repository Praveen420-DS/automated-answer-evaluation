import React from "react";

export default function TextInput({
  label,
  type = "text",
  name,
  value,
  onChange,
  placeholder,
  icon: Icon,
  error,
  required = false,
  disabled = false,
}) {
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

      {/* Input */}

      <div
        className={`flex items-center rounded-xl border transition-all duration-300 bg-white px-4 py-3

        ${
          error
            ? "border-red-500 focus-within:ring-2 focus-within:ring-red-300"
            : "border-gray-300 focus-within:border-indigo-600 focus-within:ring-2 focus-within:ring-indigo-200"
        }`}
        style={{ width: "100%", minHeight: 64, padding: "14px 18px" }}
      >
        {Icon && (
          <Icon
            size={20}
            className={`mr-3 ${
              error ? "text-red-500" : "text-gray-400"
            }`}
          />
        )}

        <input
          id={name}
          name={name}
          type={type}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          required={required}
          disabled={disabled}
          className="w-full outline-none bg-transparent text-gray-800 placeholder:text-gray-400"
          style={{ border: "none", boxShadow: "none", padding: 0, minWidth: 0, fontSize: "16px" }}
        />
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
