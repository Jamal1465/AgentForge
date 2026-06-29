import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { FileText, Copy, Download, RefreshCw, CheckCircle2 } from 'lucide-react';
import type { ProjectDetails, Artifact } from '../types';

export const DocumentViewer: React.FC = () => {
  const { workflowId } = useParams<{ workflowId: string }>();
  const [details, setDetails] = useState<ProjectDetails | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedDoc, setSelectedDoc] = useState<Artifact | null>(null);
  const [copied, setCopied] = useState(false);

  const fetchDetails = async () => {
    if (!workflowId) return;
    setLoading(true);
    const API_BASE = (import.meta.env.VITE_API_URL as string) || 'http://localhost:8080';
    try {
      const res = await fetch(`${API_BASE}/projects/${workflowId}`);
      if (res.ok) {
        const payload = await res.json();
        setDetails(payload);
        // Default to first doc if none selected
        if (payload.artifacts && payload.artifacts.length > 0) {
          setSelectedDoc(payload.artifacts[0]);
        }
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

  const handleCopy = () => {
    if (!selectedDoc) return;
    navigator.clipboard.writeText(selectedDoc.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
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

  // Simple, elegant custom markdown renderer
  const renderMarkdown = (text: string) => {
    const lines = text.split('\n');
    let tableHeaders: string[] = [];
    const elements: React.ReactNode[] = [];

    lines.forEach((line, idx) => {
      const trimmed = line.trim();

      // Table formatting
      if (trimmed.startsWith('|') && trimmed.endsWith('|')) {
        const cells = trimmed.split('|').slice(1, -1).map(c => c.trim());
        
        // Skip separator line e.g. |---|---|
        if (cells.every(c => c.startsWith('-'))) {
          return;
        }

        if (tableHeaders.length === 0) {
          tableHeaders = cells;
          elements.push(
            <table key={`table-${idx}`} className="min-w-full border border-slate-800 bg-slate-950/40 text-xs rounded-lg overflow-hidden my-4">
              <thead>
                <tr className="bg-slate-900 border-b border-slate-800 text-slate-300">
                  {cells.map((cell, cIdx) => (
                    <th key={cIdx} className="px-4 py-2 text-left font-bold">{cell}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {/* Rows will append here or parsed separately */}
              </tbody>
            </table>
          );
        } else {
          // Add row
          elements.push(
            <div key={`tr-${idx}`} className="grid grid-cols-5 gap-4 px-4 py-2 border-b border-slate-800 bg-slate-950/20 text-slate-300 font-mono text-xxs">
              {cells.map((cell, cIdx) => (
                <div key={cIdx} className="truncate">{cell}</div>
              ))}
            </div>
          );
        }
        return;
      } else {
        tableHeaders = [];
      }

      // Title header #
      if (trimmed.startsWith('# ')) {
        elements.push(
          <h1 key={idx} className="text-2xl font-black text-white tracking-tight mt-6 mb-4 border-b border-slate-850 pb-2">
            {trimmed.substring(2)}
          </h1>
        );
      }
      // Subheader ##
      else if (trimmed.startsWith('## ')) {
        elements.push(
          <h2 key={idx} className="text-lg font-extrabold text-slate-200 tracking-wide mt-6 mb-3">
            {trimmed.substring(3)}
          </h2>
        );
      }
      // Triple header ###
      else if (trimmed.startsWith('### ')) {
        elements.push(
          <h3 key={idx} className="text-sm font-bold text-indigo-400 mt-4 mb-2">
            {trimmed.substring(4)}
          </h3>
        );
      }
      // List item -
      else if (trimmed.startsWith('- ')) {
        elements.push(
          <div key={idx} className="flex gap-2 text-sm text-slate-350 leading-relaxed ml-2 my-1">
            <span className="text-indigo-500">•</span>
            <span>{trimmed.substring(2)}</span>
          </div>
        );
      }
      // Metadata separator ---
      else if (trimmed === '---') {
        elements.push(<hr key={idx} className="border-slate-800/80 my-4" />);
      }
      // Paragraph text
      else if (trimmed) {
        // Highlight keys if metadata metadata blocks
        const isMetadataLine = trimmed.includes(':') && !trimmed.startsWith('http');
        if (isMetadataLine) {
          const parts = trimmed.split(':');
          const key = parts[0];
          const val = parts.slice(1).join(':');
          elements.push(
            <div key={idx} className="text-xs font-semibold text-slate-400 my-1 font-mono">
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

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <div className="flex flex-col gap-2">
          <h2 className="text-3xl font-extrabold tracking-tight text-white flex items-center gap-3">
            <FileText className="w-8 h-8 text-indigo-400" />
            Generated Documents Viewer
          </h2>
          <p className="text-slate-400 text-sm">
            Browse and download the capability-routed architecture plans, functional tables, and risk metrics.
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
          Loading orchestrated artifacts...
        </div>
      )}

      {!loading && details && (
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Left Sidebar Document Listing */}
          <div className="space-y-2">
            <span className="text-xxs font-extrabold uppercase text-slate-500 tracking-widest block mb-4">
              Generated Artifact Files
            </span>
            <div className="space-y-1.5 max-h-[550px] overflow-y-auto pr-2">
              {details.artifacts.map((doc) => {
                const isSelected = selectedDoc?.name === doc.name;
                return (
                  <button
                    key={doc.name}
                    onClick={() => setSelectedDoc(doc)}
                    className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-left text-xs font-semibold border transition-all ${
                      isSelected
                        ? 'bg-indigo-600/10 border-indigo-500/50 text-indigo-300 shadow-md'
                        : 'bg-slate-900/40 border-slate-800/80 text-slate-400 hover:bg-slate-800/40 hover:text-slate-200'
                    }`}
                  >
                    <FileText className="w-4 h-4 shrink-0" />
                    <span className="truncate">{doc.name.replace(/_/g, ' ')}</span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Right Artifact Preview Panel */}
          <div className="lg:col-span-3 flex flex-col gap-4">
            {selectedDoc ? (
              <div className="rounded-2xl border border-slate-800/85 bg-slate-900/40 backdrop-blur-md overflow-hidden flex flex-col min-h-[550px]">
                {/* Document Header bar */}
                <div className="flex justify-between items-center px-6 py-4 border-b border-slate-800/80 bg-slate-950/30">
                  <div className="flex items-center gap-2">
                    <FileText className="w-4 h-4 text-indigo-400" />
                    <span className="font-bold text-sm text-slate-200">{selectedDoc.name}</span>
                  </div>
                  
                  <div className="flex items-center gap-2">
                    <button
                      onClick={handleCopy}
                      className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-900 hover:bg-slate-800 text-slate-300 rounded-lg border border-slate-800 text-xxs font-bold transition-all"
                    >
                      {copied ? <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                      <span>{copied ? 'Copied' : 'Copy'}</span>
                    </button>
                    <button
                      onClick={handleDownload}
                      className="flex items-center gap-1.5 px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg border border-indigo-500/20 text-xxs font-bold transition-all shadow-sm"
                    >
                      <Download className="w-3.5 h-3.5" />
                      <span>Download</span>
                    </button>
                  </div>
                </div>

                {/* Rendered markdown body */}
                <div className="flex-1 p-8 overflow-y-auto max-h-[500px]">
                  {renderMarkdown(selectedDoc.content)}
                </div>
              </div>
            ) : (
              <div className="h-full flex items-center justify-center text-slate-600 bg-slate-900/20 rounded-2xl border border-slate-800 border-dashed">
                Select an artifact file to preview content.
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
