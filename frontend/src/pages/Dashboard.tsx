import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Sparkles,
  Terminal,
  ArrowRight,
  CheckCircle2,
  FileText,
  Copy,
  Download,
  RefreshCw,
  Search,
  Archive,
  Eye,
  Activity,
  ArrowUpRight,
  Shield,
} from 'lucide-react';
import type { Artifact, ProjectDetails } from '../types';

type WorkflowEvent = {
  event_type?: string;
  message?: string;
  node_id?: string | null;
};

interface ProjectItem {
  workflow_id: string;
  project_name: string;
  status: string;
  files: { name: string; size_bytes: number }[];
  timestamp: string;
}

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

  // Tab State
  const [activeTab, setActiveTab] = useState<'generate' | 'archive'>('generate');

  // API base url resolver
  const API_BASE =
    (import.meta.env.VITE_API_BASE_URL as string | undefined) ||
    (import.meta.env.VITE_API_URL as string | undefined) ||
    'http://localhost:8080';

  // --- Tab 1: Project Blueprint Generator state ---
  const [idea, setIdea] = useState(
    'Build a library Management System',
  );
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [activeLogs, setActiveLogs] = useState<WorkflowEvent[]>([]);
  const [result, setResult] = useState<GenerationResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  // --- Tab 2: Generated Documents Archive state ---
  const [projectsList, setProjectsList] = useState<ProjectItem[]>([]);
  const [fetchingProjects, setFetchingProjects] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedProjectId, setSelectedProjectId] = useState<string | null>(null);
  const [selectedProject, setSelectedProject] = useState<ProjectDetails | null>(null);
  const [fetchingProjectDetails, setFetchingProjectDetails] = useState(false);
  const [selectedDoc, setSelectedDoc] = useState<Artifact | null>(null);
  const [copiedDoc, setCopiedDoc] = useState(false);

  // Fetch all projects list
  const fetchProjects = async () => {
    setFetchingProjects(true);
    try {
      const response = await fetch(`${API_BASE}/api/workflows`);
      if (response.ok) {
        const data = await response.json();
        setProjectsList(data.projects || []);
      }
    } catch (err) {
      console.error('Failed to fetch projects list:', err);
    } finally {
      setFetchingProjects(false);
    }
  };

  // Fetch project detailed artifacts
  const fetchProjectDetails = async (workflowId: string) => {
    setFetchingProjectDetails(true);
    setSelectedProjectId(workflowId);
    setSelectedProject(null);
    setSelectedDoc(null);
    try {
      const response = await fetch(`${API_BASE}/projects/${workflowId}`);
      if (response.ok) {
        const data = (await response.json()) as ProjectDetails;
        setSelectedProject(data);
        if (data.artifacts && data.artifacts.length > 0) {
          setSelectedDoc(data.artifacts[0]);
        }
      }
    } catch (err) {
      console.error('Failed to fetch project details:', err);
    } finally {
      setFetchingProjectDetails(false);
    }
  };

  // Trigger loading projects when mounting or switching tab
  useEffect(() => {
    if (activeTab === 'archive') {
      fetchProjects();
    }
  }, [activeTab]);

  const handleCopyDoc = () => {
    if (!selectedDoc) return;
    navigator.clipboard.writeText(selectedDoc.content);
    setCopiedDoc(true);
    setTimeout(() => setCopiedDoc(false), 2000);
  };

  const handleDownloadDoc = () => {
    if (!selectedDoc) return;
    const blob = new Blob([selectedDoc.content], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = selectedDoc.name;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const startGeneration = async () => {
    setLoading(true);
    setProgress(5);
    setActiveLogs([]);
    setResult(null);
    setError(null);

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

  const renderMarkdown = (text: string) => {
    const lines = text.split('\n');
    let tableHeaders: string[] = [];
    const elements: React.ReactNode[] = [];

    lines.forEach((line, idx) => {
      const trimmed = line.trim();

      // Table formatting
      if (trimmed.startsWith('|') && trimmed.endsWith('|')) {
        const cells = trimmed.split('|').slice(1, -1).map((c) => c.trim());

        if (cells.every((c) => c.startsWith('-'))) {
          return;
        }

        if (tableHeaders.length === 0) {
          tableHeaders = cells;
          elements.push(
            <table
              key={`table-${idx}`}
              className="min-w-full border border-slate-800 bg-slate-950/40 text-xs rounded-lg overflow-hidden my-4"
            >
              <thead>
                <tr className="bg-slate-900 border-b border-slate-800 text-slate-350">
                  {cells.map((cell, cIdx) => (
                    <th key={cIdx} className="px-4 py-2 text-left font-bold">
                      {cell}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody></tbody>
            </table>
          );
        } else {
          elements.push(
            <div
              key={`tr-${idx}`}
              className="grid grid-cols-5 gap-4 px-4 py-2 border-b border-slate-800 bg-slate-950/20 text-slate-350 font-mono text-xxs"
            >
              {cells.map((cell, cIdx) => (
                <div key={cIdx} className="truncate">
                  {cell}
                </div>
              ))}
            </div>
          );
        }
        return;
      } else {
        tableHeaders = [];
      }

      if (trimmed.startsWith('# ')) {
        elements.push(
          <h1
            key={idx}
            className="text-2xl font-black text-white tracking-tight mt-6 mb-4 border-b border-slate-850 pb-2"
          >
            {trimmed.substring(2)}
          </h1>
        );
      } else if (trimmed.startsWith('## ')) {
        elements.push(
          <h2
            key={idx}
            className="text-lg font-extrabold text-slate-200 tracking-wide mt-6 mb-3"
          >
            {trimmed.substring(3)}
          </h2>
        );
      } else if (trimmed.startsWith('### ')) {
        elements.push(
          <h3 key={idx} className="text-sm font-bold text-indigo-400 mt-4 mb-2">
            {trimmed.substring(4)}
          </h3>
        );
      } else if (trimmed.startsWith('- ')) {
        elements.push(
          <div
            key={idx}
            className="flex gap-2 text-sm text-slate-350 leading-relaxed ml-2 my-1"
          >
            <span className="text-indigo-500">•</span>
            <span>{trimmed.substring(2)}</span>
          </div>
        );
      } else if (trimmed === '---') {
        elements.push(<hr key={idx} className="border-slate-800/80 my-4" />);
      } else if (trimmed) {
        const isMetadataLine = trimmed.includes(':') && !trimmed.startsWith('http');
        if (isMetadataLine) {
          const parts = trimmed.split(':');
          const key = parts[0];
          const val = parts.slice(1).join(':');
          elements.push(
            <div
              key={idx}
              className="text-xs font-semibold text-slate-400 my-1 font-mono"
            >
              <span className="text-indigo-400">{key}:</span> {val}
            </div>
          );
        } else {
          elements.push(
            <p key={idx} className="text-sm text-slate-350 leading-relaxed my-2">
              {trimmed}
            </p>
          );
        }
      }
    });

    return <div className="space-y-1">{elements}</div>;
  };

  // Filter projects by search query
  const filteredProjects = projectsList.filter((p) => {
    const q = searchQuery.toLowerCase();
    return (
      p.project_name.toLowerCase().includes(q) ||
      p.workflow_id.toLowerCase().includes(q)
    );
  });

  return (
    <div className="space-y-8 relative">
      <div className="flex flex-col gap-2">
        <h2 className="text-3xl font-extrabold tracking-tight text-white flex items-center gap-3">
          <Sparkles className="w-8 h-8 text-indigo-400" />
          Project Blueprint Dashboard
        </h2>

        <p className="text-slate-400 text-sm">
          Route specifications dynamically to specialized capability agents, construct custom architectures, and view generated blueprints.
        </p>
      </div>

      {/* Tab Swapping Header */}
      <div className="flex border-b border-slate-800/80 gap-6">
        <button
          onClick={() => setActiveTab('generate')}
          className={`pb-3 font-bold text-sm tracking-wider uppercase border-b-2 transition-all ${
            activeTab === 'generate'
              ? 'border-indigo-500 text-indigo-400 font-extrabold'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          Synthesize New Project
        </button>
        <button
          onClick={() => setActiveTab('archive')}
          className={`pb-3 font-bold text-sm tracking-wider uppercase border-b-2 transition-all ${
            activeTab === 'archive'
              ? 'border-indigo-500 text-indigo-400 font-extrabold'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          Generated Documents Archive
        </button>
      </div>

      {activeTab === 'generate' ? (
        // --- Synthesize New Project Tab ---
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
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

            {/* Telemetry Log */}
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

          {/* Right Phase / Status Card */}
          <div className="space-y-6">
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
      ) : (
        // --- Tab 2: Generated Documents Archive Tab ---
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Left Columns - Projects Listing List (4 cols) */}
          <div className="lg:col-span-4 space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-widest">
                Blueprints Archive
              </span>
              <button
                onClick={fetchProjects}
                disabled={fetchingProjects}
                className="p-1.5 hover:bg-slate-800/80 border border-slate-800/60 rounded-lg text-slate-400 hover:text-slate-200 transition-colors"
              >
                <RefreshCw className={`w-3.5 h-3.5 ${fetchingProjects ? 'animate-spin' : ''}`} />
              </button>
            </div>

            <div className="relative">
              <Search className="w-4 h-4 text-slate-500 absolute left-3 top-3" />
              <input
                type="text"
                placeholder="Search projects..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full bg-slate-905 border border-slate-800/85 rounded-xl py-2 px-10 text-xs text-slate-200 placeholder-slate-650 focus:outline-none focus:border-indigo-500 transition-colors"
              />
            </div>

            {fetchingProjects ? (
              <div className="h-64 flex items-center justify-center text-slate-500 font-semibold text-xs border border-slate-850 rounded-2xl bg-slate-900/10">
                Fetching projects archive...
              </div>
            ) : filteredProjects.length === 0 ? (
              <div className="h-64 flex flex-col gap-2 items-center justify-center text-slate-500 font-semibold text-xs border border-slate-850/60 rounded-2xl bg-slate-900/10 p-6 text-center">
                <Archive className="w-8 h-8 text-slate-600 mb-1" />
                No generated blueprints found matching your filter.
              </div>
            ) : (
              <div className="space-y-2 max-h-[580px] overflow-y-auto pr-1">
                {filteredProjects.map((p) => {
                  const isSelected = selectedProjectId === p.workflow_id;
                  const dateStr = p.timestamp
                    ? new Date(p.timestamp).toLocaleDateString('en-US', {
                        month: 'short',
                        day: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit',
                      })
                    : 'Unknown date';

                  return (
                    <button
                      key={p.workflow_id}
                      onClick={() => fetchProjectDetails(p.workflow_id)}
                      className={`w-full p-4 rounded-xl border text-left flex flex-col gap-2.5 transition-all ${
                        isSelected
                          ? 'bg-indigo-600/10 border-indigo-500/50 text-indigo-300 shadow-[0_0_15px_rgba(99,102,241,0.08)]'
                          : 'bg-slate-900/30 border-slate-800/60 text-slate-400 hover:bg-slate-800/30 hover:text-slate-200'
                      }`}
                    >
                      <div className="flex justify-between items-start gap-2 w-full">
                        <span className="font-bold text-slate-200 text-xs line-clamp-1">
                          {p.project_name}
                        </span>
                        <span className="text-xxs px-2 py-0.5 rounded-full bg-slate-950 text-slate-500 shrink-0 font-mono">
                          {p.files.length} doc{p.files.length !== 1 ? 's' : ''}
                        </span>
                      </div>

                      <div className="text-xxs text-slate-500 font-mono flex items-center justify-between w-full">
                        <span className="truncate max-w-[140px]">{p.workflow_id}</span>
                        <span>{dateStr}</span>
                      </div>
                    </button>
                  );
                })}
              </div>
            )}
          </div>

          {/* Right Columns - Project Workspace Preview (8 cols) */}
          <div className="lg:col-span-8">
            {selectedProjectId === null ? (
              <div className="h-full min-h-[500px] flex flex-col gap-3 items-center justify-center text-slate-500 border border-slate-850/60 rounded-2xl bg-slate-900/10 p-8 text-center">
                <Archive className="w-12 h-12 text-slate-700" />
                <span className="font-extrabold text-sm text-slate-400">Project Workspace</span>
                <p className="text-xs text-slate-500 max-w-sm">
                  Select a generated blueprint from the sidebar to list and inspect its requirements, architectures, and implementation documents inline.
                </p>
              </div>
            ) : fetchingProjectDetails ? (
              <div className="h-full min-h-[500px] flex items-center justify-center text-slate-500 font-bold text-xs border border-slate-850/60 rounded-2xl bg-slate-900/20 animate-pulse">
                Loading project workspace artifacts...
              </div>
            ) : selectedProject ? (
              <div className="space-y-4">
                {/* Selected Project Header Bar */}
                <div className="p-4 rounded-xl border border-slate-800/80 bg-slate-900/40 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                  <div className="space-y-1">
                    <span className="text-xxs font-extrabold text-indigo-400 uppercase tracking-widest block">
                      Active Workspace
                    </span>
                    <h3 className="text-lg font-bold text-slate-100">
                      {selectedProject.workflow_id ? projectsList.find(p => p.workflow_id === selectedProject.workflow_id)?.project_name || 'Generated Project' : 'Generated Project'}
                    </h3>
                    <span className="text-xxs font-mono text-slate-500 block truncate max-w-[320px]">
                      Workflow ID: {selectedProject.workflow_id}
                    </span>
                  </div>

                  {/* Quick Action Navigation links */}
                  <div className="flex flex-wrap gap-1.5">
                    <button
                      onClick={() => navigate(`/viewer/${selectedProject.workflow_id}`)}
                      title="Open Full Document Viewer"
                      className="p-2 bg-slate-950 border border-slate-800/80 hover:bg-slate-800 hover:text-indigo-400 rounded-lg text-slate-400 text-xs font-semibold flex items-center gap-1.5 transition-all"
                    >
                      <Eye className="w-3.5 h-3.5" />
                      <span>Viewer</span>
                    </button>
                    <button
                      onClick={() => navigate(`/workflow/${selectedProject.workflow_id}`)}
                      title="Open Workflow node timeline"
                      className="p-2 bg-slate-950 border border-slate-800/80 hover:bg-slate-800 hover:text-indigo-400 rounded-lg text-slate-400 text-xs font-semibold flex items-center gap-1.5 transition-all"
                    >
                      <Activity className="w-3.5 h-3.5" />
                      <span>Timeline</span>
                    </button>
                    <button
                      onClick={() => navigate(`/reports/${selectedProject.workflow_id}`)}
                      title="Open Security Reports"
                      className="p-2 bg-slate-950 border border-slate-800/80 hover:bg-slate-800 hover:text-indigo-400 rounded-lg text-slate-400 text-xs font-semibold flex items-center gap-1.5 transition-all"
                    >
                      <Shield className="w-3.5 h-3.5" />
                      <span>Security</span>
                    </button>
                    <button
                      onClick={() => navigate(`/export/${selectedProject.workflow_id}`)}
                      title="Export compiled assets"
                      className="p-2 bg-slate-950 border border-slate-800/80 hover:bg-slate-800 hover:text-indigo-400 rounded-lg text-slate-400 text-xs font-semibold flex items-center gap-1.5 transition-all"
                    >
                      <ArrowUpRight className="w-3.5 h-3.5" />
                      <span>Export</span>
                    </button>
                  </div>
                </div>

                {/* Left Listing / Right Markdown Preview split */}
                <div className="grid grid-cols-1 md:grid-cols-12 gap-6 items-start">
                  {/* Left Column Documents Index (4 cols) */}
                  <div className="md:col-span-4 space-y-1.5">
                    <span className="text-xxs font-extrabold uppercase text-slate-500 tracking-wider block mb-2 pl-1">
                      Artifacts Index
                    </span>
                    <div className="space-y-1 max-h-[460px] overflow-y-auto pr-1">
                      {selectedProject.artifacts && selectedProject.artifacts.map((doc) => {
                        const isSelected = selectedDoc?.name === doc.name;
                        return (
                          <button
                            key={doc.name}
                            onClick={() => setSelectedDoc(doc)}
                            className={`w-full flex items-center gap-2.5 px-3 py-2.5 rounded-lg text-left text-xxs font-semibold border transition-all ${
                              isSelected
                                ? 'bg-indigo-600/10 border-indigo-500/50 text-indigo-300'
                                : 'bg-slate-900/30 border-slate-800/40 text-slate-400 hover:bg-slate-800/30 hover:text-slate-200'
                            }`}
                          >
                            <FileText className="w-3.5 h-3.5 shrink-0" />
                            <span className="truncate">{doc.name.replace(/_/g, ' ')}</span>
                          </button>
                        );
                      })}
                    </div>
                  </div>

                  {/* Right Column Markdown Renderer (8 cols) */}
                  <div className="md:col-span-8">
                    {selectedDoc ? (
                      <div className="rounded-xl border border-slate-800/80 bg-slate-900/30 overflow-hidden flex flex-col min-h-[460px] max-h-[520px]">
                        {/* File Action Bar */}
                        <div className="flex justify-between items-center px-4 py-2.5 border-b border-slate-800 bg-slate-950/30">
                          <span className="font-mono text-xxs text-slate-300 truncate max-w-[180px]">
                            {selectedDoc.name}
                          </span>
                          <div className="flex items-center gap-1.5 shrink-0">
                            <button
                              onClick={handleCopyDoc}
                              className="flex items-center gap-1 px-2.5 py-1 bg-slate-900 hover:bg-slate-800 text-slate-350 rounded border border-slate-800 text-xxs font-bold transition-all"
                            >
                              {copiedDoc ? (
                                <CheckCircle2 className="w-3 h-3 text-emerald-400" />
                              ) : (
                                <Copy className="w-3 h-3" />
                              )}
                              <span>{copiedDoc ? 'Copied' : 'Copy'}</span>
                            </button>
                            <button
                              onClick={handleDownloadDoc}
                              className="flex items-center gap-1 px-2.5 py-1 bg-indigo-600 hover:bg-indigo-500 text-white rounded border border-indigo-500/20 text-xxs font-bold transition-all shadow-sm"
                            >
                              <Download className="w-3 h-3" />
                              <span>Download</span>
                            </button>
                          </div>
                        </div>

                        {/* File Preview Content */}
                        <div className="flex-1 p-6 overflow-y-auto max-h-[450px]">
                          {renderMarkdown(selectedDoc.content)}
                        </div>
                      </div>
                    ) : (
                      <div className="h-[460px] flex items-center justify-center text-slate-650 bg-slate-900/10 rounded-xl border border-slate-800 border-dashed">
                        Select a file to inspect content.
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ) : (
              <div className="h-full min-h-[500px] flex items-center justify-center text-slate-600 bg-slate-900/10 border border-slate-800 rounded-2xl">
                Could not retrieve project workspace details.
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};