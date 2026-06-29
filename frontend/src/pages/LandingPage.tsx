import React from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Play, Settings, Compass, ShieldCheck, Database, Award } from 'lucide-react';

export const LandingPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col items-center justify-center min-h-[80vh] relative overflow-hidden">
      {/* Background radial highlight */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-indigo-500/10 rounded-full blur-[120px] pointer-events-none" />

      {/* Hero Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="text-center max-w-3xl mb-12"
      >
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900 border border-slate-800 text-xs font-semibold text-indigo-400 mb-6">
          <Award className="w-3.5 h-3.5" />
          <span>Industry-Grade Capability Planning</span>
        </div>
        
        <h1 className="text-5xl md:text-6xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white via-indigo-200 to-indigo-500 mb-6">
          Multi-Agent Project Architect
        </h1>
        
        <p className="text-lg text-slate-400 leading-relaxed">
          AgentForge generates secure, professional-grade software blueprints and documents 
          leveraging capability-routed agent plugins. Zero hardcoding. 100% extensible.
        </p>
      </motion.div>

      {/* Primary Action Buttons */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.6, delay: 0.1 }}
        className="flex flex-col sm:flex-row gap-4 mb-16 z-10"
      >
        <button
          onClick={() => navigate('/dashboard')}
          className="flex items-center justify-center gap-3 px-8 py-4 bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded-xl border border-indigo-400/20 shadow-[0_0_30px_rgba(99,102,241,0.4)] transition-all transform hover:-translate-y-0.5 duration-200 group"
        >
          <Play className="w-5 h-5 group-hover:scale-110 transition-transform" />
          <span>Launch Generator Console</span>
        </button>
        
        <button
          onClick={() => navigate('/registry')}
          className="flex items-center justify-center gap-3 px-8 py-4 bg-slate-900 hover:bg-slate-800/80 text-slate-200 font-bold rounded-xl border border-slate-800 transition-all transform hover:-translate-y-0.5 duration-200"
        >
          <Settings className="w-5 h-5" />
          <span>Inspect Plugin Registry</span>
        </button>
      </motion.div>

      {/* Grid Features */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.2 }}
        className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-5xl"
      >
        {/* Card 1 */}
        <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800/80 backdrop-blur-md flex flex-col gap-3">
          <div className="p-3 bg-indigo-500/10 text-indigo-400 rounded-xl border border-indigo-500/20 w-fit">
            <Compass className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-lg text-slate-100">Capability-First Routing</h3>
          <p className="text-sm text-slate-400 leading-relaxed">
            Tasks are dynamically routed based on matching semantic capabilities. Agents are fully decoupled from concrete engineering roles.
          </p>
        </div>

        {/* Card 2 */}
        <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800/80 backdrop-blur-md flex flex-col gap-3">
          <div className="p-3 bg-purple-500/10 text-purple-400 rounded-xl border border-purple-500/20 w-fit">
            <Database className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-lg text-slate-100">Rich Artifact Outputs</h3>
          <p className="text-sm text-slate-400 leading-relaxed">
            Generates 10 complete, comprehensive markdown documents containing database indexing, C4 diagrams, and risk matrices.
          </p>
        </div>

        {/* Card 3 */}
        <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800/80 backdrop-blur-md flex flex-col gap-3">
          <div className="p-3 bg-emerald-500/10 text-emerald-400 rounded-xl border border-emerald-500/20 w-fit">
            <ShieldCheck className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-lg text-slate-100">Quality Gates & Auditing</h3>
          <p className="text-sm text-slate-400 leading-relaxed">
            All agent outputs are audited for security threats (PII/secrets) and checked by automated evaluation score rubrics.
          </p>
        </div>
      </motion.div>
    </div>
  );
};
