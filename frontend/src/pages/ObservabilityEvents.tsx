import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Terminal, RefreshCw, Layers } from 'lucide-react';
import type { ProjectDetails } from '../types';

export const ObservabilityEvents: React.FC = () => {
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
            <Terminal className="w-8 h-8 text-indigo-400" />
            Observability events
          </h2>
          <p className="text-slate-400 text-sm">
            Terminal stream detailing internal orchestrator executions, quality checks, and database persistence logs.
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
        <div className="h-64 flex items-center justify-center text-slate-500 animate-pulse bg-slate-900/40 rounded-2xl border border-slate-800">
          Loading telemetry stream...
        </div>
      )}

      {!loading && details && (
        <div className="space-y-4">
          <div className="flex items-center gap-2 text-xxs font-extrabold uppercase text-slate-500 tracking-widest">
            <Layers className="w-3.5 h-3.5" />
            Telemetry event logs console
          </div>

          <div className="p-6 rounded-2xl border border-slate-850 bg-slate-950 font-mono text-xs text-slate-350 space-y-3 min-h-[450px] overflow-y-auto max-h-[500px]">
            {details.events.map((event, idx) => {
              let tagColor = 'text-indigo-400 border-indigo-500/20';
              if (event.event_type.startsWith('evaluation')) {
                tagColor = 'text-emerald-400 border-emerald-500/20';
              } else if (event.event_type.startsWith('security')) {
                tagColor = 'text-amber-400 border-amber-500/20';
              } else if (event.event_type === 'error') {
                tagColor = 'text-rose-400 border-rose-500/20';
              }

              return (
                <div key={idx} className="flex gap-4 items-start py-1 border-b border-slate-900/40">
                  <span className="text-slate-600 shrink-0 font-semibold select-none">
                    [Node: {event.node_id || 'SYSTEM'}]
                  </span>
                  <span className={`px-2 py-0.5 rounded border text-[9px] uppercase tracking-wider font-bold shrink-0 ${tagColor}`}>
                    {event.event_type}
                  </span>
                  <span className="text-slate-300">{event.message}</span>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};
