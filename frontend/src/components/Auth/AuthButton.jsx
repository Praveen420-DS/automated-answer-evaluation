import { motion } from "framer-motion";

export default function AuthButton({
  text,
  loading = false,
  type = "submit",
  disabled = false,
  onClick,
}) {
  return (
    <motion.button
      whileHover={{
        scale: disabled || loading ? 1 : 1.02,
      }}
      whileTap={{
        scale: disabled || loading ? 1 : 0.98,
      }}
      transition={{
        duration: 0.2,
      }}
      type={type}
      onClick={onClick}
      disabled={disabled || loading}
      className={`w-full py-3 rounded-xl font-semibold text-white transition-all duration-300 flex items-center justify-center gap-3
      ${
        disabled || loading
          ? "bg-gray-400 cursor-not-allowed"
          : "bg-indigo-600 hover:bg-indigo-700 shadow-lg hover:shadow-xl"
      }`}
    >
      {loading ? (
        <>
          <svg
            className="animate-spin h-5 w-5"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-20"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />

            <path
              className="opacity-100"
              fill="currentColor"
              d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
            />
          </svg>

          <span>Please wait...</span>
        </>
      ) : (
        text
      )}
    </motion.button>
  );
}
