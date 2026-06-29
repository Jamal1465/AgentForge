import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Compass, Cpu, HelpCircle, Tag, RefreshCw } from 'lucide-react';
import type { PluginsRegistryData } from '../types';

export const CapabilityMap: React.FC = () => {
  const [data, setData] = useState<PluginsRegistryData | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedCap, setSelectedCap] = useState<string | null>(null);

  const fetchRegistry = async () => {
    setLoading(true);
    const API_BASE = (import.meta.env.VITE_API_URL as string) || 'http://localhost:8080';
    try {
      const res = await fetch(`${API_BASE}/plugins`);
      if (res.ok) {
        const payload = await res.json();
        setData(payload);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRegistry();
  }, []);

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <div className="flex flex-col gap-2">
          <h2 className="text-3xl font-extrabold tracking-tight text-white flex items-center gap-3">
            <Compass className="w-8 h-8 text-indigo-400" />
            Semantic Capability Map
          </h2>
          <p className="text-slate-400 text-sm">
            AgentForge runs on semantic capability specifications. Decouple your system architecture from hardcoded roles.
          </p>
        </div>
        <button
          onClick={fetchRegistry}
          disabled={loading}
          className="p-2.5 bg-slate-900 border border-slate-800 rounded-xl hover:bg-slate-850 hover:text-slate-200 text-slate-400 transition-colors"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Capability Cards Grid */}
        <div className="lg:col-span-2 space-y-4">
          <span className="text-xxs font-extrabold uppercase text-slate-500 tracking-widest block">
            Declared System Capabilities
          </span>

          {loading && (
            <div className="space-y-4 animate-pulse">
              {[1, 2, 3].map((n) => (
                <div key={n} className="h-16 rounded-xl bg-slate-900/40 border border-slate-800" />
              ))}
            </div>
          )}

          {!loading && data && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {Object.keys(data.capability_map).map((cap) => {
                const plugins = data.capability_map[cap];
                const isSelected = selectedCap === cap;

                return (
                  <motion.div
                    key={cap}
                    onClick={() => setSelectedCap(cap)}
                    whileHover={{ y: -2 }}
                    className={`p-5 rounded-2xl border cursor-pointer backdrop-blur-md transition-all flex flex-col justify-between h-32 ${
                      isSelected
                        ? 'bg-indigo-600/10 border-indigo-500/80 shadow-[0_0_15px_rgba(99,102,241,0.15)] text-indigo-300'
                        : 'bg-slate-900/40 border-slate-800/80 hover:border-slate-700 text-slate-200'
                    }`}
                  >
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <Tag className={`w-4 h-4 ${isSelected ? 'text-indigo-400' : 'text-slate-400'}`} />
                        <h3 className="font-bold text-sm tracking-wide">{cap}</h3>
                      </div>
                      <p className="text-slate-500 text-[10px] leading-relaxed">
                        Required capability parsed from planning workflow nodes.
                      </p>
                    </div>

                    <div className="text-xxs text-slate-400 flex items-center justify-between border-t border-slate-800/80 pt-2">
                      <span>Mapped Agents:</span>
                      <span className="font-mono bg-slate-950 px-1.5 py-0.5 rounded border border-slate-800 font-semibold text-indigo-400">
                        {plugins.length}
                      </span>
                    </div>
                  </motion.div>
                );
              })}
            </div>
          )}
        </div>

        {/* Right Mapping Inspector Panel */}
        <div className="space-y-6">
          <span className="text-xxs font-extrabold uppercase text-slate-500 tracking-widest block">
            Resolution Resolver
          </span>

          <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800/80 backdrop-blur-md space-y-4">
            {selectedCap ? (
              <div className="space-y-4">
                <div>
                  <span className="text-xxs font-bold text-indigo-400 uppercase tracking-wider">Inspecting:</span>
                  <h3 className="font-extrabold text-white text-lg tracking-wide">{selectedCap}</h3>
                </div>

                <div className="space-y-3">
                  <span className="text-xxs font-bold text-slate-400 uppercase tracking-widest block">
                    Satisfying Plugins:
                  </span>
                  
                  {data?.capability_map[selectedCap]?.map((agentId) => {
                    const plugin = data.plugins.find((p) => p.agent_id === agentId);
                    return (
                      <div
                        key={agentId}
                        className="p-4 rounded-xl bg-slate-950/80 border border-slate-900 flex items-center justify-between hover:border-slate-800 transition-colors"
                      >
                        <div className="flex items-center gap-3">
                          <div className="p-2 bg-indigo-500/10 text-indigo-400 rounded-lg border border-indigo-500/20">
                            <Cpu className="w-3.5 h-3.5" />
                          </div>
                          <div>
                            <div className="text-xs font-bold text-slate-200">{plugin?.name || agentId}</div>
                            <div className="text-xxs text-slate-500 font-mono">{agentId}</div>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            ) : (
              <div className="text-center py-12 text-slate-500 space-y-3">
                <HelpCircle className="w-12 h-12 mx-auto text-slate-650" />
                <p className="text-xs">Select a declared capability on the left to resolve satisfying plugins.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
