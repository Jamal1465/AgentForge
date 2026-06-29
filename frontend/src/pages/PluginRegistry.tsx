import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Settings, Cpu, Tag, RefreshCw } from 'lucide-react';
import type { PluginInfo } from '../types';

export const PluginRegistry: React.FC = () => {
  const [plugins, setPlugins] = useState<PluginInfo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchPlugins = async () => {
    setLoading(true);
    setError(null);
    const API_BASE = (import.meta.env.VITE_API_URL as string) || 'http://localhost:8080';

    try {
      const res = await fetch(`${API_BASE}/plugins`);
      if (!res.ok) throw new Error('Failed to load plugin registry.');
      const data = await res.json();
      setPlugins(data.plugins || []);
    } catch (err: any) {
      setError(err.message || 'Error occurred');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPlugins();
  }, []);

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <div className="flex flex-col gap-2">
          <h2 className="text-3xl font-extrabold tracking-tight text-white flex items-center gap-3">
            <Settings className="w-8 h-8 text-indigo-400" />
            Agent Plugin Registry
          </h2>
          <p className="text-slate-400 text-sm">
            Inspect build-in and custom plugins loaded into the AgentForge orchestrator runtime.
          </p>
        </div>
        <button
          onClick={fetchPlugins}
          disabled={loading}
          className="p-2.5 bg-slate-900 border border-slate-800 rounded-xl hover:bg-slate-850 hover:text-slate-200 text-slate-400 transition-colors"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
        </button>
      </div>

      {loading && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-pulse">
          {[1, 2, 3].map((n) => (
            <div key={n} className="h-44 rounded-2xl bg-slate-900/40 border border-slate-800" />
          ))}
        </div>
      )}

      {error && (
        <div className="p-6 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-300 text-sm">
          {error}
        </div>
      )}

      {!loading && !error && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {plugins.map((plugin, index) => {
            const isHighRisk = plugin.risk_level === 'high' || plugin.risk_level === 'critical';
            return (
              <motion.div
                key={plugin.agent_id}
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: index * 0.05 }}
                className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800/80 hover:border-indigo-500/30 backdrop-blur-md flex flex-col justify-between gap-4 transition-all group"
              >
                <div className="space-y-2">
                  <div className="flex justify-between items-start">
                    <div className="p-2 bg-indigo-500/10 text-indigo-400 rounded-lg border border-indigo-500/20 w-fit">
                      <Cpu className="w-4 h-4" />
                    </div>
                    <div className="flex gap-2">
                      <span className="px-2 py-0.5 rounded bg-slate-950 border border-slate-800 text-[10px] text-slate-400 font-mono">
                        v{plugin.version}
                      </span>
                      <span className={`px-2 py-0.5 rounded text-[10px] uppercase font-bold tracking-wider ${
                        isHighRisk 
                          ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20' 
                          : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                      }`}>
                        {plugin.risk_level} Risk
                      </span>
                    </div>
                  </div>

                  <div>
                    <h3 className="font-bold text-white text-base group-hover:text-indigo-300 transition-colors">
                      {plugin.name}
                    </h3>
                    <span className="text-xxs text-slate-500 font-mono">{plugin.agent_id}</span>
                  </div>
                </div>

                <div className="space-y-2 pt-2 border-t border-slate-800/80">
                  <span className="text-xxs font-bold text-slate-400 uppercase tracking-widest block">
                    Satisfies Capabilities:
                  </span>
                  <div className="flex flex-wrap gap-1.5">
                    {plugin.capabilities.map((cap) => (
                      <span
                        key={cap}
                        className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-slate-950 text-indigo-300 text-xxs border border-indigo-500/15"
                      >
                        <Tag className="w-2.5 h-2.5" />
                        {cap}
                      </span>
                    ))}
                  </div>
                </div>
              </motion.div>
            );
          })}
        </div>
      )}
    </div>
  );
};
