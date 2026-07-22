import { useState } from "react";
import { Link, NavLink } from "react-router-dom";
import { Menu, X, GraduationCap } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

const navItems = [
  {
    title: "Home",
    path: "/",
  },
  {
    title: "Features",
    path: "/#features",
  },
  {
    title: "Workflow",
    path: "/#workflow",
  },
  {
    title: "About",
    path: "/#about",
  },
  {
    title: "Contact",
    path: "/#contact",
  },
];

export default function Navbar() {
  const [open, setOpen] = useState(false);

  return (
    <header className="fixed top-0 left-0 w-full bg-white/90 backdrop-blur-lg border-b border-gray-200 z-50">

      <div className="max-w-7xl mx-auto px-6">

        <div className="h-20 flex justify-between items-center">

          {/* Logo */}

          <Link
            to="/"
            className="flex items-center gap-3"
          >
            <div className="w-12 h-12 rounded-2xl bg-indigo-600 flex items-center justify-center shadow-lg">

              <GraduationCap
                className="text-white"
                size={26}
              />

            </div>

            <div>

              <h1 className="text-xl font-bold text-gray-900">

                EvalAI

              </h1>

              <p className="text-xs text-gray-500">

                Automated Answer Evaluation

              </p>

            </div>

          </Link>

          {/* Desktop Menu */}

          <nav className="hidden lg:flex gap-8">

            {navItems.map((item) => (

              <NavLink
                key={item.title}
                to={item.path}
                className={({ isActive }) =>
                  isActive
                    ? "text-indigo-600 font-semibold"
                    : "text-gray-600 hover:text-indigo-600 transition"
                }
              >
                {item.title}
              </NavLink>

            ))}

          </nav>

          {/* Buttons */}

          <div className="hidden lg:flex gap-4">

            <Link
              to="/login"
              className="px-5 py-2 rounded-xl border border-gray-300 hover:bg-gray-100 transition"
            >
              Login
            </Link>

            <Link
              to="/register"
              className="px-5 py-2 rounded-xl bg-indigo-600 text-white hover:bg-indigo-700 transition"
            >
              Register
            </Link>

          </div>

          {/* Mobile Menu Button */}

          <button
            className="lg:hidden"
            onClick={() => setOpen(!open)}
          >
            {open ? <X size={30} /> : <Menu size={30} />}
          </button>

        </div>

      </div>

      {/* Mobile Menu */}

      <AnimatePresence>

        {open && (

          <motion.div
            initial={{
              opacity: 0,
              y: -30,
            }}
            animate={{
              opacity: 1,
              y: 0,
            }}
            exit={{
              opacity: 0,
              y: -30,
            }}
            transition={{
              duration: 0.3,
            }}
            className="lg:hidden bg-white border-t border-gray-200"
          >

            <div className="flex flex-col p-6 gap-6">

              {navItems.map((item) => (

                <NavLink
                  key={item.title}
                  to={item.path}
                  onClick={() => setOpen(false)}
                  className="text-lg text-gray-700 hover:text-indigo-600"
                >
                  {item.title}
                </NavLink>

              ))}

              <Link
                to="/login"
                className="w-full text-center py-3 rounded-xl border border-gray-300"
              >
                Login
              </Link>

              <Link
                to="/register"
                className="w-full text-center py-3 rounded-xl bg-indigo-600 text-white"
              >
                Register
              </Link>

            </div>

          </motion.div>

        )}

      </AnimatePresence>

    </header>
  );
}