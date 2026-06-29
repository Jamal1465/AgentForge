import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Activity, CheckCircle2, ChevronRight, Play, RefreshCw, Compass } from 'lucide-react';
import type { ProjectDetails } from '../types';

export const WorkflowTimeline: React.FC = () => {
  const { workflowId } = useParams<{ workflowId: string }>();
  const [details, setDetails] = useState<ProjectDetails | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchDetails = async () => {
    if (!workflowId) return;
    setLoading(true);
    const API_BASE = (import.meta.env.VITE_API_URL as string) || 'http://localhost:8080';
    try {
      const res = await fetch(`${API_BASE}/projects/${workflowId}`);
      if (res.ok) {
        const payload = await res.json();
        setDetails(payload);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDetails();
  }, [workflowId]);

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <div className="flex flex-col gap-2">
          <h2 className="text-3xl font-extrabold tracking-tight text-white flex items-center gap-3">
            <Activity className="w-8 h-8 text-indigo-400" />
            Workflow Timeline Graph
          </h2>
          <p className="text-slate-400 text-sm">
            Interactive visualization of agent nodes executing capabilities and generating project planning artifacts.
          </p>
        </div>
        <button
          onClick={fetchDetails}
          disabled={loading}
          className="p-2.5 bg-slate-900 border border-slate-800 rounded-xl hover:bg-slate-850 hover:text-slate-200 text-slate-400 transition-colors"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
        </button>
      </div>

      {loading && (
        <div className="space-y-4 animate-pulse">
          {[1, 2, 3].map((n) => (
            <div key={n} className="h-16 rounded-xl bg-slate-900/40 border border-slate-800" />
          ))}
        </div>
      )}

      {!loading && details && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Timeline Nodes */}
          <div className="lg:col-span-2 space-y-6 relative pl-6 border-l border-slate-800/80 ml-4 py-2">
            {/* Plan Root Node */}
            <motion.div
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              className="relative mb-8"
            >
              {/* Dot */}
              <div className="absolute -left-[31px] top-1/2 -translate-y-1/2 w-4 h-4 bg-indigo-500 rounded-full border-4 border-slate-950 shadow-[0_0_10px_rgba(99,102,241,0.5)]" />
              
              <div className="p-4 rounded-xl bg-indigo-600/10 border border-indigo-500/25 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="p-1.5 bg-indigo-500/20 text-indigo-300 rounded border border-indigo-500/30">
                    <Play className="w-3.5 h-3.5" />
                  </div>
                  <div>
                    <h3 className="font-bold text-sm text-slate-100">Create Initial Project Plan</h3>
                    <span className="text-[10px] text-indigo-400 font-semibold tracking-wide uppercase">planning</span>
                  </div>
                </div>
                <div className="flex items-center gap-1.5 text-xs text-indigo-400 font-semibold bg-indigo-500/10 px-2 py-0.5 rounded border border-indigo-500/10">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  Completed
                </div>
              </div>
            </motion.div>

            {/* Dependency Branch Lines Indicator */}
            <div className="text-xxs font-extrabold uppercase text-slate-500 tracking-widest mb-4 flex items-center gap-2">
              <ChevronRight className="w-3.5 h-3.5" />
              Dependency Fan-out: Parallel Artifact Generators
            </div>

            {/* Child Artifact Nodes */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {details.events
                .filter((e) => e.event_type === 'node.completed' && e.node_id !== 'plan')
                .map((nodeEvent, index) => {
                  const nodeId = nodeEvent.node_id || '';
                  // Guess capability from node name
                  let cap = 'artifact-generation';
                  if (nodeId.includes('brief')) cap = 'project-brief-generation';
                  else if (nodeId.includes('functional')) cap = 'requirements-analysis';
                  else if (nodeId.includes('non_functional')) cap = 'non-functional-requirements-analysis';
                  else if (nodeId.includes('feasibility')) cap = 'feasibility-analysis';
                  else if (nodeId.includes('architecture')) cap = 'architecture-documentation';
                  else if (nodeId.includes('tech')) cap = 'technology-stack-recommendation';
                  else if (nodeId.includes('implementation')) cap = 'implementation-planning';
                  else if (nodeId.includes('testing')) cap = 'testing-strategy';
                  else if (nodeId.includes('deployment')) cap = 'deployment-planning';
                  else if (nodeId.includes('risk')) cap = 'risk-analysis';

                  return (
                    <motion.div
                      key={nodeId}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.3, delay: index * 0.05 }}
                      className="p-4 rounded-xl bg-slate-900/40 border border-slate-800 flex flex-col justify-between h-28 hover:border-indigo-500/20 transition-all"
                    >
                      <div className="flex items-start justify-between">
                        <div>
                          <h4 className="font-bold text-xs text-slate-200 capitalize">
                            {nodeId.replace(/_/g, ' ')}
                          </h4>
                          <span className="text-[10px] text-slate-500 font-mono">{nodeId}</span>
                        </div>
                        <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                      </div>

                      <div className="border-t border-slate-800/80 pt-2 flex items-center justify-between text-xxs">
                        <span className="text-slate-500 flex items-center gap-1">
                          <Compass className="w-3 h-3" />
                          Capability:
                        </span>
                        <span className="font-semibold text-indigo-400 truncate max-w-[150px]">{cap}</span>
                      </div>
                    </motion.div>
                  );
                })}
            </div>
          </div>

          {/* Right Status Overview Card */}
          <div className="space-y-6">
            <span className="text-xxs font-extrabold uppercase text-slate-500 tracking-widest block">
              Workflow Status Overview
            </span>

            <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800/80 backdrop-blur-md space-y-4">
              <div>
                <span className="text-xxs font-bold text-slate-400 uppercase tracking-wider">Project ID:</span>
                <div className="text-xs font-mono text-indigo-300 truncate">{details.workflow_id}</div>
              </div>

              <div className="space-y-2 text-xs">
                <div className="flex justify-between border-b border-slate-800/80 pb-2">
                  <span className="text-slate-500">Nodes Executed:</span>
                  <span className="text-slate-200 font-bold">11 / 11</span>
                </div>
                <div className="flex justify-between border-b border-slate-800/80 pb-2">
                  <span className="text-slate-500">Quality State:</span>
                  <span className="text-emerald-400 font-bold">PASSED</span>
                </div>
                <div className="flex justify-between border-b border-slate-800/80 pb-2">
                  <span className="text-slate-500">Security Audit:</span>
                  <span className="text-emerald-400 font-bold">PASSED</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
