import { motion } from "framer-motion";
import { ArrowRight, BrainCircuit, ScanLine, ShieldCheck } from "lucide-react";
import { Link } from "react-router-dom";

export default function Hero() {
  return (
    <section className="relative min-h-screen overflow-hidden bg-gradient-to-br from-white via-[#faf9ff] to-[#eef0ff] px-6 py-20 lg:px-16">
      <div className="absolute -right-32 top-16 h-96 w-96 rounded-full bg-violet-200/40 blur-3xl" />
      <div className="relative mx-auto grid max-w-7xl items-center gap-14 lg:grid-cols-2">
        <motion.div initial={{ opacity: 0, x: -32 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: .55 }}>
          <span className="inline-flex items-center gap-2 rounded-full border border-violet-100 bg-white px-5 py-2.5 font-semibold text-violet-600 shadow-sm">✦ AI-Powered Academic Intelligence</span>
          <h1 className="mt-8 text-5xl font-extrabold leading-tight tracking-tight text-slate-950 lg:text-7xl">Automated<br />Answer Script<br /><span className="bg-gradient-to-r from-blue-500 via-violet-600 to-fuchsia-500 bg-clip-text text-transparent">Evaluation</span></h1>
          <p className="mt-7 max-w-xl text-lg leading-8 text-slate-500">Transforming manual evaluation into intelligent AI automation with transparent scoring and actionable feedback.</p>
          <Link to="/register" className="mt-9 inline-flex items-center gap-3 rounded-2xl bg-gradient-to-r from-indigo-600 to-violet-600 px-7 py-4 font-semibold text-white shadow-xl shadow-violet-300/40">Get Started <ArrowRight size={20} /></Link>
        </motion.div>
        <motion.div initial={{ opacity: 0, x: 32 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: .55 }} className="relative mx-auto h-[430px] w-full max-w-lg">
          <div className="absolute inset-8 rounded-full bg-violet-200/50 blur-3xl" />
          <div className="absolute inset-x-14 bottom-6 h-56 rounded-[36px] border border-violet-100 bg-white/80 shadow-2xl backdrop-blur"><div className="m-7 rounded-2xl border border-slate-100 bg-white p-5 shadow-sm"><div className="flex items-center justify-between"><span className="font-bold text-slate-800">Answer Script</span><span className="rounded-full bg-violet-100 px-3 py-1 text-sm font-bold text-violet-600">A+</span></div><div className="mt-5 space-y-3">{[1, 2, 3].map((line) => <div key={line} className="h-2 rounded-full bg-slate-100" style={{ width: `${95 - line * 12}%` }} />)}</div></div></div>
          <div className="absolute left-0 top-20 rounded-2xl border border-violet-100 bg-white p-4 shadow-xl"><ScanLine className="text-violet-600" /><p className="mt-2 text-sm font-bold text-slate-800">OCR Ready</p></div>
          <div className="absolute right-0 top-12 rounded-2xl border border-violet-100 bg-white p-4 shadow-xl"><BrainCircuit className="text-violet-600" /><p className="mt-2 text-sm font-bold text-slate-800">AI Scoring</p></div>
          <div className="absolute bottom-0 right-8 rounded-2xl border border-violet-100 bg-white p-4 shadow-xl"><ShieldCheck className="text-violet-600" /><p className="mt-2 text-sm font-bold text-slate-800">Secure</p></div>
        </motion.div>
      </div>
    </section>
  );
}
