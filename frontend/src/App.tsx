import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Layout } from './components/Layout';
import { LandingPage } from './pages/LandingPage';
import { Dashboard } from './pages/Dashboard';
import { PluginRegistry } from './pages/PluginRegistry';
import { CapabilityMap } from './pages/CapabilityMap';
import { WorkflowTimeline } from './pages/WorkflowTimeline';
import { DocumentViewer } from './pages/DocumentViewer';
import { SecurityReports } from './pages/SecurityReports';
import { ObservabilityEvents } from './pages/ObservabilityEvents';
import { ExportPage } from './pages/ExportPage';
import './App.css';

const queryClient = new QueryClient();

const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/registry" element={<PluginRegistry />} />
            <Route path="/capabilities" element={<CapabilityMap />} />
            <Route path="/workflow/:workflowId" element={<WorkflowTimeline />} />
            <Route path="/viewer/:workflowId" element={<DocumentViewer />} />
            <Route path="/reports/:workflowId" element={<SecurityReports />} />
            <Route path="/observability/:workflowId" element={<ObservabilityEvents />} />
            <Route path="/export/:workflowId" element={<ExportPage />} />
          </Routes>
        </Layout>
      </Router>
    </QueryClientProvider>
  );
};

export default App;
