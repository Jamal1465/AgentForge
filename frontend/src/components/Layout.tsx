import React from 'react';
import { Link, useLocation, useParams } from 'react-router-dom';
import {
  Shield,
  Settings,
  Activity,
  Compass,
  Terminal,
  FileText,
  Download,
  Play,
  Home,
  Database
} from 'lucide-react';

interface LayoutProps {
  children: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  const location = useLocation();
  const { workflowId } = useParams<{ workflowId?: string }>();

  // Determine current active page
  const isActive = (path: string) => location.pathname === path;

  return (
    <div className="min-h-screen flex bg-slate-950 text-slate-100 font-sans">
      {/* Sidebar */}
      <aside className="w-64 border-r border-slate-800 bg-slate-900/60 backdrop-blur-md flex flex-col justify-between p-4 sticky top-0 h-screen">
        <div>
          {/* Logo / Header */}
          <div className="flex items-center gap-3 px-2 py-4 mb-6 border-b border-slate-800/80">
            <div className="p-2 bg-indigo-600/20 text-indigo-400 rounded-lg border border-indigo-500/30 shadow-[0_0_15px_rgba(99,102,241,0.2)]">
              <Database className="w-6 h-6 animate-pulse" />
            </div>
            <div>
              <h1 className="font-extrabold tracking-wide text-lg text-white">AgentForge</h1>
              <span className="text-xs text-indigo-400 font-semibold uppercase tracking-widest">Orchestrator</span>
            </div>
          </div>

          {/* Navigation Group 1: Global */}
          <div className="space-y-1 mb-6">
            <span className="px-3 text-xxs font-extrabold uppercase text-slate-500 tracking-widest block mb-2">
              System Control
            </span>
            <Link
              to="/"
              className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                isActive('/') 
                  ? 'bg-indigo-600/20 text-indigo-300 border-l-2 border-indigo-500' 
                  : 'text-slate-400 hover:bg-slate-800/40 hover:text-slate-200'
              }`}
            >
              <Home className="w-4 h-4" />
              <span>Portal Entry</span>
            </Link>
            <Link
              to="/dashboard"
              className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                isActive('/dashboard') 
                  ? 'bg-indigo-600/20 text-indigo-300 border-l-2 border-indigo-500' 
                  : 'text-slate-400 hover:bg-slate-800/40 hover:text-slate-200'
              }`}
            >
              <Play className="w-4 h-4" />
              <span>Generator Console</span>
            </Link>
            <Link
              to="/registry"
              className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                isActive('/registry') 
                  ? 'bg-indigo-600/20 text-indigo-300 border-l-2 border-indigo-500' 
                  : 'text-slate-400 hover:bg-slate-800/40 hover:text-slate-200'
              }`}
            >
              <Settings className="w-4 h-4" />
              <span>Agent Registry</span>
            </Link>
            <Link
              to="/capabilities"
              className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                isActive('/capabilities') 
                  ? 'bg-indigo-600/20 text-indigo-300 border-l-2 border-indigo-500' 
                  : 'text-slate-400 hover:bg-slate-800/40 hover:text-slate-200'
              }`}
            >
              <Compass className="w-4 h-4" />
              <span>Capability Map</span>
            </Link>
          </div>

          {/* Navigation Group 2: Active Run Context */}
          {workflowId && (
            <div className="space-y-1 pt-4 border-t border-slate-800/80">
              <span className="px-3 text-xxs font-extrabold uppercase text-slate-500 tracking-widest block mb-2">
                Active Project Run
              </span>
              <Link
                to={`/workflow/${workflowId}`}
                className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                  isActive(`/workflow/${workflowId}`) 
                    ? 'bg-indigo-600/20 text-indigo-300 border-l-2 border-indigo-500' 
                    : 'text-slate-400 hover:bg-slate-800/40 hover:text-slate-200'
                }`}
              >
                <Activity className="w-4 h-4" />
                <span>Workflow Status</span>
              </Link>
              <Link
                to={`/viewer/${workflowId}`}
                className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                  isActive(`/viewer/${workflowId}`) 
                    ? 'bg-indigo-600/20 text-indigo-300 border-l-2 border-indigo-500' 
                    : 'text-slate-400 hover:bg-slate-800/40 hover:text-slate-200'
                }`}
              >
                <FileText className="w-4 h-4" />
                <span>Document Viewer</span>
              </Link>
              <Link
                to={`/reports/${workflowId}`}
                className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                  isActive(`/reports/${workflowId}`) 
                    ? 'bg-indigo-600/20 text-indigo-300 border-l-2 border-indigo-500' 
                    : 'text-slate-400 hover:bg-slate-800/40 hover:text-slate-200'
                }`}
              >
                <Shield className="w-4 h-4" />
                <span>Security / Eval</span>
              </Link>
              <Link
                to={`/observability/${workflowId}`}
                className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                  isActive(`/observability/${workflowId}`) 
                    ? 'bg-indigo-600/20 text-indigo-300 border-l-2 border-indigo-500' 
                    : 'text-slate-400 hover:bg-slate-800/40 hover:text-slate-200'
                }`}
              >
                <Terminal className="w-4 h-4" />
                <span>Telemetry logs</span>
              </Link>
              <Link
                to={`/export/${workflowId}`}
                className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                  isActive(`/export/${workflowId}`) 
                    ? 'bg-indigo-600/20 text-indigo-300 border-l-2 border-indigo-500' 
                    : 'text-slate-400 hover:bg-slate-800/40 hover:text-slate-200'
                }`}
              >
                <Download className="w-4 h-4" />
                <span>Export Package</span>
              </Link>
            </div>
          )}
        </div>

        {/* Footer info */}
        <div className="px-2 py-4 border-t border-slate-800/80 text-xxs text-slate-500">
          <div className="flex justify-between mb-1">
            <span>Server:</span>
            <span className="text-indigo-400 font-semibold">Online</span>
          </div>
          <div>Capability Routed Engine</div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto max-h-screen">
        <div className="p-8 max-w-7xl mx-auto">
          {children}
        </div>
      </main>
    </div>
  );
};
