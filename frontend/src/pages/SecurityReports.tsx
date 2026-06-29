import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Shield, CheckCircle2, AlertTriangle, XCircle, RefreshCw } from 'lucide-react';
import type { ProjectDetails } from '../types';

export const SecurityReports: React.FC = () => {
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
            <Shield className="w-8 h-8 text-indigo-400" />
            Security & Evaluation Reports
          </h2>
          <p className="text-slate-400 text-sm">
            Review security audit guardrail decisons and evaluation score reports generated per artifact.
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
        <div className="space-y-6 animate-pulse">
          <div className="h-40 rounded-2xl bg-slate-900/40 border border-slate-800" />
          <div className="h-40 rounded-2xl bg-slate-900/40 border border-slate-800" />
        </div>
      )}

      {!loading && details && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Section 1: Quality Gate Evaluations */}
          <div className="space-y-4">
            <span className="text-xxs font-extrabold uppercase text-slate-500 tracking-widest block">
              Quality Gate Evaluations
            </span>

            {details.evaluations.length === 0 && (
              <div className="p-6 rounded-2xl bg-slate-900/20 border border-slate-850 text-slate-500 italic text-sm text-center">
                No evaluation reports attached to this run.
              </div>
            )}

            <div className="space-y-4 max-h-[550px] overflow-y-auto pr-2">
              {details.evaluations.map((report) => {
                const isPassed = report.status === 'passed';
                return (
                  <div
                    key={report.report_id}
                    className="p-5 rounded-2xl bg-slate-900/40 border border-slate-800/80 backdrop-blur-md space-y-3"
                  >
                    <div className="flex justify-between items-start">
                      <div>
                        <h4 className="font-bold text-sm text-slate-200">Evaluation Report</h4>
                        <span className="text-xxs text-slate-500 font-mono">{report.report_id}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className="px-2 py-0.5 rounded bg-slate-950 border border-slate-800 font-mono text-xxs text-indigo-400 font-semibold">
                          Score: {Math.round(report.score * 100)}%
                        </span>
                        <span className={`px-2.5 py-0.5 rounded-full text-xxs font-bold uppercase tracking-wider ${
                          isPassed 
                            ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/15' 
                            : 'bg-amber-500/10 text-amber-400 border border-amber-500/15'
                        }`}>
                          {report.status}
                        </span>
                      </div>
                    </div>

                    {report.findings.length > 0 && (
                      <div className="border-t border-slate-800/80 pt-3 space-y-2">
                        <span className="text-xxs font-bold text-slate-400 uppercase tracking-widest block">
                          Evaluation Findings:
                        </span>
                        {report.findings.map((f, fIdx) => (
                          <div
                            key={fIdx}
                            className="p-3 rounded-lg bg-slate-950/80 border border-slate-900 flex items-start gap-2.5 text-xs text-slate-350"
                          >
                            <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
                            <div>
                              <div className="font-mono text-xxs text-slate-500">{f.criterion_id}</div>
                              <div>{f.message}</div>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>

          {/* Section 2: Security Audit Events */}
          <div className="space-y-4">
            <span className="text-xxs font-extrabold uppercase text-slate-500 tracking-widest block">
              Security Guardrail Audit log
            </span>

            {details.security_events.length === 0 && (
              <div className="p-6 rounded-2xl bg-slate-900/20 border border-slate-850 text-slate-500 italic text-sm text-center">
                No security audit events recorded.
              </div>
            )}

            <div className="space-y-4 max-h-[550px] overflow-y-auto pr-2">
              {details.security_events.map((e, index) => {
                const isAllow = e.decision_status === 'allow';
                return (
                  <div
                    key={index}
                    className="p-5 rounded-2xl bg-slate-900/40 border border-slate-800/80 backdrop-blur-md flex gap-4"
                  >
                    <div className="mt-1">
                      {isAllow ? (
                        <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                      ) : (
                        <XCircle className="w-5 h-5 text-rose-400" />
                      )}
                    </div>

                    <div className="flex-1 space-y-2">
                      <div className="flex justify-between items-start">
                        <div>
                          <h4 className="font-bold text-xs text-slate-200 capitalize">
                            {e.event_type.replace(/_/g, ' ')}
                          </h4>
                          <span className="text-xxs text-slate-500 font-mono">Subject: {e.subject_id}</span>
                        </div>
                        <span className={`px-2 py-0.5 rounded text-[10px] uppercase font-bold tracking-wider ${
                          isAllow 
                            ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/15' 
                            : 'bg-rose-500/10 text-rose-400 border border-rose-500/15'
                        }`}>
                          {e.decision_status}
                        </span>
                      </div>
                      <p className="text-slate-400 text-xs">{e.message}</p>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
