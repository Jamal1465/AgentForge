export interface WorkflowEvent {
  event_type: string;
  message: string;
  node_id: string | null;
}

export interface Artifact {
  name: string;
  content: string;
}

export interface EvaluationFinding {
  criterion_id: string;
  message: string;
  severity: string;
}

export interface EvaluationReport {
  report_id: string;
  status: string;
  score: number;
  findings: EvaluationFinding[];
}

export interface SecurityEvent {
  event_type: string;
  subject_id: string;
  actor_id: string;
  decision_status: string;
  message: string;
  finding_ids: string[];
}

export interface ProjectDetails {
  workflow_id: string;
  status: string;
  events: WorkflowEvent[];
  artifacts: Artifact[];
  evaluations: EvaluationReport[];
  security_events: SecurityEvent[];
  output_path: string | null;
}

export interface PluginInfo {
  agent_id: string;
  name: string;
  version: string;
  risk_level: string;
  capabilities: string[];
}

export interface PluginsRegistryData {
  plugins: PluginInfo[];
  capability_map: Record<string, string[]>;
}
