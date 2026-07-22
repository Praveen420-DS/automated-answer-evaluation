import { motion } from "framer-motion";
import { GraduationCap, LockKeyhole, ScanLine, ShieldCheck, BrainCircuit } from "lucide-react";

export default function AuthLayout({
  title,
  subtitle,
  children,
}) {
  return (
    <div className="auth-page eval-auth-page">

      <div className="auth-grid">

        {/* Left Side */}

        <div className="auth-brand eval-auth-brand">

          <motion.div
            initial={{ opacity: 0, x: -80 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.7 }}
            className="eval-auth-brand-content"
          >

            <div className="eval-auth-logo">

              <div className="eval-auth-logo-icon">

                <GraduationCap size={42} />

              </div>

              <div>

                <h1>

                  EvalAI

                </h1>

                <p>

                  AI-Powered Answer Script Evaluation

                </p>

              </div>

            </div>

            <h2 className="eval-auth-heading">

              Evaluate Answer Scripts
              with Artificial Intelligence

            </h2>

            <p className="eval-auth-description">

              OCR extracts handwritten answers while AI evaluates,
              grades and generates feedback automatically.

            </p>

            <div className="eval-auth-points">

              <div className="eval-auth-point">

                <div className="eval-auth-point-icon">

                  <ScanLine size={28} />

                </div>

                <div className="eval-auth-point-copy">

                  <h3>

                    AI Powered Evaluation

                  </h3>

                  <p>

                    Semantic answer comparison with intelligent grading.

                  </p>

                </div>

              </div>

              <div className="eval-auth-point eval-auth-accuracy">

                <div className="eval-auth-point-icon">

                  <BrainCircuit size={28} />

                </div>

                <div className="eval-auth-point-copy">

                  <h3>

                    OCR Accuracy

                  </h3>

                  <p>

                    Extracts handwritten and printed text with high accuracy.

                  </p>

                </div>

              </div>

              <div className="eval-auth-point">
                <div className="eval-auth-point-icon"><ShieldCheck size={28} /></div>
                <div className="eval-auth-point-copy"><h3>Secure Platform</h3><p>Faculty and student authentication with role-based access.</p></div>
              </div>
            </div>
            <div className="eval-auth-badges" aria-hidden="true"><span className="grade-badge">A+</span><span className="accuracy-badge">99%</span><span className="lock-badge"><LockKeyhole /></span></div>

          </motion.div>

        </div>

        {/* Right Side */}

        <div className="auth-panel eval-auth-panel">

          <motion.div
            initial={{ opacity: 0, x: 80 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.7 }}
            className="auth-card eval-auth-card"
          >

            <div className="eval-auth-shield"><ShieldCheck /></div>
            <h2 className="auth-title eval-auth-title">

              {title}

            </h2>

            <p className="auth-subtitle eval-auth-subtitle">

              {subtitle}

            </p>

            <div className="eval-auth-rule" />
            <div className="auth-content eval-auth-content">

              {children}

            </div>

          </motion.div>

        </div>

      </div>

    </div>
  );
}
