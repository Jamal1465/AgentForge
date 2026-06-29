import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { Sparkles, Terminal, ArrowRight, CheckCircle2 } from 'lucide-react';

type WorkflowEvent = {
  event_type?: string;
  message?: string;
  node_id?: string | null;
};

function normalizeEvents(rawEvents: unknown): WorkflowEvent[] {
  if (!Array.isArray(rawEvents)) {
    return [];
  }

  return rawEvents
    .filter((event): event is Record<string, unknown> => {
      return Boolean(event) && typeof event === 'object';
    })
    .map((event) => ({
      event_type:
        typeof event.event_type === 'string'
          ? event.event_type
          : 'unknown.event',
      message:
        typeof event.message === 'string'
          ? event.message
          : 'No event message available.',
      node_id:
        typeof event.node_id === 'string'
          ? event.node_id
          : null,
    }));
}

type GenerationResult = {
  workflow_id: string;
  output_path: string | null;
};


function getEventColor(eventType: string): string {
  if (eventType.startsWith('evaluation')) {
    return 'text-emerald-400';
  }

  if (eventType.startsWith('security')) {
    return 'text-amber-400';
  }

  if (eventType === 'error') {
    return 'text-rose-400';
  }

  if (eventType.endsWith('completed') || eventType.endsWith('finished')) {
    return 'text-indigo-400';
  }

  if (eventType.includes('started')) {
    return 'text-sky-400';
  }

  return 'text-slate-400';
}

export const Dashboard: React.FC = () => {
  const navigate = useNavigate();

  const [idea, setIdea] = useState(
    'Build a secure FastAPI task manager with PostgreSQL, Docker, tests, and documentation',
  );

  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [activeLogs, setActiveLogs] = useState<WorkflowEvent[]>([]);
  const [result, setResult] = useState<GenerationResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const startGeneration = async () => {
    setLoading(true);
    setProgress(5);
    setActiveLogs([]);
    setResult(null);
    setError(null);

    const API_BASE =
      (import.meta.env.VITE_API_BASE_URL as string | undefined) ||
      (import.meta.env.VITE_API_URL as string | undefined) ||
      'http://localhost:8080';

    try {
      const response = await fetch(`${API_BASE}/projects`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ description: idea }),
      });

      if (!response.ok) {
        throw new Error(`Server returned error status: ${response.status}`);
      }

      const data = await response.json();
      const events = normalizeEvents(data.events);

      if (events.length === 0) {
        setActiveLogs([
          {
            event_type: 'workflow.warning',
            message: 'Workflow completed, but no telemetry events were returned.',
            node_id: null,
          },
        ]);
        setProgress(100);
        setResult({
          workflow_id:
            typeof data.workflow_id === 'string' ? data.workflow_id : 'unknown-workflow',
          output_path:
            typeof data.output_path === 'string' ? data.output_path : null,
        });
        setLoading(false);
        return;
      }

      let idx = 0;

      const interval = window.setInterval(() => {
        if (idx < events.length) {
          const nextEvent = events[idx];

          if (nextEvent) {
            setActiveLogs((prev) => [...prev, nextEvent]);
          }

          setProgress(Math.round(((idx + 1) / Math.max(events.length, 1)) * 95));
          idx += 1;
          return;
        }

        window.clearInterval(interval);
        setProgress(100);
        setResult({
          workflow_id:
            typeof data.workflow_id === 'string' ? data.workflow_id : 'unknown-workflow',
          output_path:
            typeof data.output_path === 'string' ? data.output_path : null,
        });
        setLoading(false);
      }, 150);
    } catch (err) {
      console.error(err);
      const errMsg =
        err instanceof Error
          ? err.message
          : 'Failed to establish connection to the orchestrator backend.';
      setError(errMsg);

      setActiveLogs((prev) => [
        ...prev,
        {
          event_type: 'error',
          message: errMsg,
          node_id: null,
        },
      ]);

      setProgress(0);
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8 relative">
      <div className="flex flex-col gap-2">
        <h2 className="text-3xl font-extrabold tracking-tight text-white flex items-center gap-3">
          <Sparkles className="w-8 h-8 text-indigo-400" />
          Project Blueprint Generator
        </h2>

        <p className="text-slate-400 text-sm">
          Submit a project description. The capability router will invoke agent plugins to
          construct project briefs, C4 architectures, NFR profiles, and risk tables.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Input Console */}
        <div className="lg:col-span-2 space-y-6">
          <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800/80 backdrop-blur-md space-y-4">
            <label className="text-sm font-semibold tracking-wider text-slate-300 uppercase">
              Project Specification
            </label>

            <textarea
              value={idea}
              onChange={(e) => setIdea(e.target.value)}
              disabled={loading}
              rows={4}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl p-4 text-slate-200 placeholder-slate-600 focus:outline-none focus:border-indigo-500 transition-colors text-sm"
              placeholder="e.g. Build a secure microservice task manager..."
            />

            <div className="flex justify-end">
              <button
                onClick={startGeneration}
                disabled={loading || !idea.trim()}
                className="flex items-center gap-2 px-6 py-3 bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-800 disabled:text-slate-600 disabled:border-slate-900 text-white font-bold rounded-xl border border-indigo-400/20 shadow-lg transition-all"
              >
                {loading ? 'Orchestrating Agents...' : 'Initiate Synthesis'}
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Telemetry Console Output */}
          <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800/80 backdrop-blur-md space-y-4 flex flex-col min-h-[300px]">
            <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
              <div className="flex items-center gap-2 text-slate-300 font-semibold text-sm">
                <Terminal className="w-4 h-4 text-indigo-400" />
                Live Telemetry Log
              </div>

              {loading && (
                <span className="flex h-2 w-2 relative">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75" />
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-indigo-500" />
                </span>
              )}
            </div>

            <div className="flex-1 bg-slate-950/80 border border-slate-900 rounded-xl p-4 font-mono text-xs overflow-y-auto max-h-[320px] space-y-2">
              {error && (
                <div className="p-3 bg-rose-950/30 border border-rose-800/50 rounded-lg text-rose-300 text-xxs flex flex-col gap-1 mb-2">
                  <span className="font-bold flex items-center gap-1.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-rose-500 animate-pulse"></span>
                    Connection Failure
                  </span>
                  <p>{error}</p>
                </div>
              )}

              {(() => {
                const safeEvents = normalizeEvents(activeLogs);
                if (safeEvents.length === 0) {
                  return (
                    <div className="text-slate-600 italic">
                      No workflow events available yet.
                    </div>
                  );
                }

                return safeEvents.map((log, index) => {
                  const eventType = log.event_type ?? 'unknown.event';
                  const message = log.message ?? 'No event message available.';
                  const nodeId = log.node_id ?? 'system';
                  const color = getEventColor(eventType);

                  return (
                    <motion.div
                      key={`${eventType}-${index}`}
                      initial={{ opacity: 0, x: -5 }}
                      animate={{ opacity: 1, x: 0 }}
                      className="flex gap-2"
                    >
                      <span className="text-slate-600 font-semibold shrink-0">
                        [{nodeId}]
                      </span>
                      <span className={color}>{message}</span>
                    </motion.div>
                  );
                });
              })()}
            </div>
          </div>
        </div>

        {/* Right Status Panel */}
        <div className="space-y-6">
          {/* Progress / Status Block */}
          <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800/80 backdrop-blur-md flex flex-col items-center justify-center text-center space-y-4">
            <span className="text-sm font-semibold tracking-wider text-slate-400 uppercase">
              Orchestration Phase
            </span>

            <div className="relative w-36 h-36 flex items-center justify-center">
              <svg className="w-full h-full transform -rotate-90">
                <circle
                  cx="72"
                  cy="72"
                  r="60"
                  className="stroke-slate-800"
                  strokeWidth="6"
                  fill="transparent"
                />
                <circle
                  cx="72"
                  cy="72"
                  r="60"
                  className="stroke-indigo-500 transition-all duration-300"
                  strokeWidth="6"
                  fill="transparent"
                  strokeDasharray={377}
                  strokeDashoffset={377 - (377 * progress) / 100}
                />
              </svg>

              <div className="absolute flex flex-col items-center justify-center">
                <span className="text-3xl font-extrabold text-white">{progress}%</span>
                <span className="text-xxs text-slate-500 uppercase tracking-widest">
                  Progress
                </span>
              </div>
            </div>

            <div className="text-sm text-slate-300 font-medium">
              {loading && 'Routing capabilities to plugins...'}

              {!loading && progress === 0 && 'System Ready'}

              {!loading && progress === 100 && (
                <div className="flex items-center gap-1.5 text-emerald-400">
                  <CheckCircle2 className="w-4 h-4" />
                  Synthesis Complete
                </div>
              )}
            </div>
          </div>

          {/* Execution Result Actions */}
          <AnimatePresence>
            {result && (
              <motion.div
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 15 }}
                className="p-6 rounded-2xl bg-slate-900/60 border border-indigo-500/20 backdrop-blur-md space-y-4 shadow-[0_0_20px_rgba(99,102,241,0.1)]"
              >
                <div className="text-slate-200 font-bold text-sm">
                  Orchestrated Package Details
                </div>

                <div className="space-y-2 text-xs">
                  <div className="flex justify-between border-b border-slate-800/80 pb-2">
                    <span className="text-slate-500">Workflow ID:</span>
                    <span className="text-slate-300 font-semibold truncate max-w-[150px]">
                      {result.workflow_id}
                    </span>
                  </div>

                  <div className="flex justify-between border-b border-slate-800/80 pb-2">
                    <span className="text-slate-500">Disk Location:</span>
                    <span className="text-slate-300 font-semibold truncate max-w-[150px]">
                      {result.output_path ?? 'Not available'}
                    </span>
                  </div>
                </div>

                <div className="flex flex-col gap-2 pt-2">
                  <button
                    onClick={() => navigate(`/viewer/${result.workflow_id}`)}
                    className="w-full py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded-lg text-xs tracking-wider uppercase transition-all shadow-md"
                  >
                    Open Document Viewer
                  </button>

                  <button
                    onClick={() => navigate(`/workflow/${result.workflow_id}`)}
                    className="w-full py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold rounded-lg text-xs tracking-wider uppercase transition-all"
                  >
                    View Node Timeline
                  </button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
};