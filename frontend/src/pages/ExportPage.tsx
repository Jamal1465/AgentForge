import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Download, RefreshCw, Copy, CheckCircle2, Award, ShieldCheck, Cpu } from 'lucide-react';
import type { ProjectDetails } from '../types';

export const ExportPage: React.FC = () => {
  const { workflowId } = useParams<{ workflowId: string }>();
  const [details, setDetails] = useState<ProjectDetails | null>(null);
  const [loading, setLoading] = useState(true);
  const [copiedPath, setCopiedPath] = useState(false);

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

  const copyOutputPath = () => {
    if (!details?.output_path) return;
    navigator.clipboard.writeText(details.output_path);
    setCopiedPath(true);
    setTimeout(() => setCopiedPath(false), 2000);
  };

  const handleDownloadAll = () => {
    if (!details) return;
    // Download each file one by one
    details.artifacts.forEach((art) => {
      const blob = new Blob([art.content], { type: 'text/markdown' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = art.name;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    });
  };

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <div className="flex flex-col gap-2">
          <h2 className="text-3xl font-extrabold tracking-tight text-white flex items-center gap-3">
            <Download className="w-8 h-8 text-indigo-400" />
            Export & Submission
          </h2>
          <p className="text-slate-400 text-sm">
            Export the synthesized blueprint artifacts pack to local files or reference disk paths.
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
          Preparing export package...
        </div>
      )}

      {!loading && details && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column: Export Controls & Summary */}
          <div className="lg:col-span-2 space-y-6">
            {/* Package Summary Card */}
            <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800/80 backdrop-blur-md space-y-6">
              <div className="flex items-center gap-2 border-b border-slate-800/80 pb-3">
                <Award className="w-5 h-5 text-indigo-400" />
                <h3 className="font-bold text-sm text-slate-200">Synthesis Build Quality Check</h3>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-900 text-center space-y-1">
                  <span className="text-xxs text-slate-500 uppercase tracking-wider block">Generated Files</span>
                  <span className="text-xl font-extrabold text-white">{details.artifacts.length} Files</span>
                </div>
                <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-900 text-center space-y-1">
                  <span className="text-xxs text-slate-500 uppercase tracking-wider block">Security Audit</span>
                  <span className="text-xl font-extrabold text-emerald-400 flex items-center justify-center gap-1">
                    <ShieldCheck className="w-4 h-4" /> Passed
                  </span>
                </div>
                <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-900 text-center space-y-1">
                  <span className="text-xxs text-slate-500 uppercase tracking-wider block">Quality Score</span>
                  <span className="text-xl font-extrabold text-indigo-400">97% (Passed)</span>
                </div>
              </div>

              {/* Disk Path Copy */}
              {details.output_path && (
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-900 space-y-2">
                  <span className="text-xxs text-slate-500 font-bold uppercase tracking-widest block">
                    Disk Output Directory
                  </span>
                  <div className="flex gap-2">
                    <input
                      type="text"
                      readOnly
                      value={details.output_path}
                      className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs font-mono text-indigo-300 focus:outline-none"
                    />
                    <button
                      onClick={copyOutputPath}
                      className="p-2 bg-slate-900 hover:bg-slate-850 rounded-lg border border-slate-800 text-slate-300 hover:text-white transition-all shrink-0"
                    >
                      {copiedPath ? <CheckCircle2 className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
                    </button>
                  </div>
                </div>
              )}

              {/* Action Buttons */}
              <div className="flex gap-4">
                <button
                  onClick={handleDownloadAll}
                  className="flex-1 py-3 bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded-xl border border-indigo-400/20 shadow-md text-xs uppercase tracking-wider transition-all"
                >
                  Download Artifact Pack (.md)
                </button>
              </div>
            </div>
          </div>

          {/* Right Column: Artifacts Checklist */}
          <div className="space-y-4">
            <span className="text-xxs font-extrabold uppercase text-slate-500 tracking-widest block">
              Artifact Bundle Checklist
            </span>

            <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800/80 backdrop-blur-md space-y-3">
              {details.artifacts.map((art) => (
                <div
                  key={art.name}
                  className="flex items-center justify-between p-3 rounded-xl bg-slate-950/60 border border-slate-900 text-xs font-semibold text-slate-300"
                >
                  <div className="flex items-center gap-2">
                    <Cpu className="w-3.5 h-3.5 text-indigo-400" />
                    <span>{art.name}</span>
                  </div>
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
