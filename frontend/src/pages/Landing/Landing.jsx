import { motion } from "framer-motion";
import { useState } from "react";
import {
  ArrowRight, BrainCircuit, Check, CircleUserRound, Menu, ScanLine,
  ShieldCheck, Sparkles, Star, X
} from "lucide-react";
import { Link } from "react-router-dom";
import "./landing.css";

const featureItems = [
  { icon: ScanLine, title: "OCR-Ready", text: "High accuracy handwritten text extraction" },
  { icon: BrainCircuit, title: "Semantic Scoring", text: "AI-powered understanding and evaluation" },
  { icon: ShieldCheck, title: "Secure & Role-Based", text: "Protected dashboards for every user" },
];

function Logo() {
  return <Link to="/" className="landing-logo" aria-label="EvalAI home">
    <span className="landing-logo-mark">EA<i>✦</i></span>
    <span>Eval<span>AI</span></span>
  </Link>;
}

function HeroVisual() {
  return <div className="hero-visual" aria-hidden="true">
    <div className="visual-orb" />
    <div className="scanner"><span /><span /><b /></div>
    <div className="scanner-beam" />

    <motion.div className="floating-card ocr-card" animate={{ y: [0, -9, 0] }} transition={{ duration: 4, repeat: Infinity }}>
      <strong>OCR Processing</strong>
      <div className="ocr-content"><ScanLine /><div><i /><i /><i /></div><Check /></div>
    </motion.div>

    <motion.div className="floating-card ai-card" animate={{ y: [0, 9, 0] }} transition={{ duration: 4.6, repeat: Infinity }}>
      <strong>AI Evaluation</strong>
      <div className="ai-card-body"><BrainCircuit /><div><i /><i /></div><Check /></div>
    </motion.div>

    <div className="platform"><div /><div /></div>
    <motion.div className="answer-paper" initial={{ rotate: -4 }} animate={{ rotate: [-4, -2, -4], y: [0, -7, 0] }} transition={{ duration: 5, repeat: Infinity }}>
      <b>Answer Script</b>
      {["Explain the role of OCR in script evaluation.", "Describe semantic scoring with an example.", "How does AI deliver useful feedback?"].map((question, index) => <div className="answer-line" key={question}>
        <em>Q{index + 1}.</em><span>{question}</span><mark>{index === 0 ? "8" : index === 1 ? "9" : "A+"}</mark>
      </div>)}
    </motion.div>

    <div className="robot"><div className="robot-head"><span /><i /><span /></div><div className="robot-body"><b /></div><div className="robot-arm" /></div>

    <motion.div className="floating-card score-card" animate={{ y: [0, -8, 0] }} transition={{ duration: 4.2, repeat: Infinity }}>
      <strong>Score &amp; Feedback</strong><div className="score-ring"><b>92%</b><small>Accuracy</small></div><div className="stars">{[1, 2, 3, 4, 5].map((star) => <Star key={star} fill="currentColor" />)}</div>
    </motion.div>
    <motion.div className="floating-card analytics-card" animate={{ y: [0, 7, 0] }} transition={{ duration: 4.8, repeat: Infinity }}>
      <strong>Detailed Analytics</strong><div className="chart"><i /><i /><i /><i /><i /></div>
    </motion.div>
  </div>;
}

export default function Landing() {
  const [menuOpen, setMenuOpen] = useState(false);
  return <main className="landing-page">
    <header className="landing-nav">
      <Logo />
      <button className="menu-button" onClick={() => setMenuOpen(!menuOpen)} aria-label="Toggle navigation">{menuOpen ? <X /> : <Menu />}</button>
      <nav className={menuOpen ? "nav-links is-open" : "nav-links"}>
        <a className="active" href="#home" onClick={() => setMenuOpen(false)}>Home</a><a href="#features" onClick={() => setMenuOpen(false)}>Features</a><a href="#how-it-works" onClick={() => setMenuOpen(false)}>How It Works</a><a href="#about" onClick={() => setMenuOpen(false)}>About Us</a><a href="#contact" onClick={() => setMenuOpen(false)}>Contact</a>
      </nav>
      <Link to="/login" className="login-button"><CircleUserRound /> Login</Link>
    </header>

    <section id="home" className="hero-section">
      <div className="hero-copy">
        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="eyebrow-pill"><Sparkles /> AI-Powered Academic Intelligence</motion.div>
        <motion.h1 initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: .1 }}>Automated<br />Answer Script<br /><span>Evaluation</span></motion.h1>
        <div className="headline-rule" />
        <motion.p initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: .2 }}>Transforming manual evaluation into intelligent AI automation. Process answer scripts with OCR, transparent semantic scoring, and actionable feedback.</motion.p>
        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: .3 }}><Link to="/register" className="primary-cta">Get Started <ArrowRight /></Link></motion.div>
      </div>
      <HeroVisual />
    </section>

    <section id="features" className="feature-strip">
      {featureItems.map(({ icon: Icon, title, text }) => <article className="feature-item" key={title}><span className="feature-icon"><Icon /></span><div><h2>{title}</h2><p>{text}</p></div></article>)}
    </section>
    <section id="how-it-works" className="landing-anchor"><span>Upload, evaluate, and review results in one intelligent workflow.</span></section>
    <section id="about" className="landing-anchor"><span>Designed for educators who value clarity, fairness, and time.</span></section>
    <section id="contact" className="landing-anchor"><span>Ready to transform your evaluation process?</span></section>
  </main>;
}
