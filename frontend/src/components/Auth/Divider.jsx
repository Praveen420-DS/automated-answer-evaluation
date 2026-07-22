export default function Divider({
  text = "OR",
}) {
  return (
    <div className="relative my-8">

      {/* Horizontal Line */}

      <div className="absolute inset-0 flex items-center">

        <div className="w-full border-t border-gray-300"></div>

      </div>

      {/* Center Text */}

      <div className="relative flex justify-center">

        <span className="bg-white px-4 text-sm font-medium text-gray-500 uppercase tracking-wider">

          {text}

        </span>

      </div>

    </div>
  );
}