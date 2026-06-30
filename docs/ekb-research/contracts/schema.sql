/*
EKB Postgres Contract Schema
Status: CP16 contract artifact
Date: 2026-06-28

Design source: docs/enterprise-knowledge-base-design.md:300-352 for tables and
docs/enterprise-knowledge-base-design.md:358-360 for tenant_id plus RLS.
Extraction source: docs/ekb-research/extraction-map.md.

Table map:
- tenants: design 302-314; extraction F-AUTHZ-001, F-AUTHZ-002.
- workspaces: design 302-314; extraction F-AUTHZ-001, F-AUTHZ-002.
- users: design 302-314; extraction F-AUTHZ-001, F-AUTHZ-002.
- tenant_memberships: design 302-314; extraction F-AUTHZ-001.
- workspace_memberships: design 302-314; extraction F-AUTHZ-001.
- groups: design 302-314; extraction F-AUTHZ-001.
- group_members: design 302-314; extraction F-AUTHZ-001.
- service_accounts: design 302-314; extraction F-AUTHZ-001.
- api_keys: design 302-314; extraction F-AUTHZ-002.
- knowledge_bases: design 316-328; extraction F-AUTHZ-001, F-ANYTHINGLLM-004.
- kb_grants: design 316-328; extraction F-AUTHZ-001.
- source_connectors: design 316-328; extraction F-ANYTHINGLLM-004.
- documents: design 316-328; extraction F-ANYTHINGLLM-004.
- document_versions: design 316-328; extraction F-ANYTHINGLLM-004.
- chunks: design 316-328; extraction F-ANYTHINGLLM-004, F-OBS-003.
- index_versions: design 316-328; extraction F-OBS-001, F-OBS-003.
- chunk_embeddings: design 316-328; extraction F-OBS-003.
- resource_grants: design 329-337; extraction F-AUTHZ-001.
- policy_bindings: design 329-337; extraction F-AUTHZ-002.
- policy_decision_logs: design 329-337; extraction F-AUTHZ-002.
- audit_events: design 329-337; extraction F-AUTHZ-002, F-OBS-001.
- conversations: design 338-352; extraction F-OBS-001.
- messages: design 338-352; extraction F-OBS-001.
- retrieval_events: design 338-352; extraction F-OBS-001, F-OBS-003.
- answer_events: design 338-352; extraction F-OBS-001, F-OBS-003.
- tools: design 338-352; extraction F-FLOWISE-004, F-ANYTHINGLLM-004.
- tool_grants: design 338-352; extraction F-AUTHZ-001, F-FLOWISE-004.
- tool_calls: design 338-352; extraction F-OBS-001, F-FLOWISE-004.
- eval_datasets: design 338-352; extraction F-OBS-001, F-OBS-003.
- eval_cases: design 338-352; extraction F-OBS-003.
- eval_runs: design 338-352; extraction F-OBS-003, F-OBS-004.
- eval_scores: design 338-352; extraction F-OBS-002, F-OBS-003, F-OBS-004.

All tables are tenant-owned. The tenants table carries tenant_id as a generated
alias of id so the RLS pattern is mechanically consistent everywhere. Tenant
creation is a bootstrap operation: the caller supplies id equal to
ekb.current_tenant_id(), after which normal tenant RLS applies.
*/

CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE SCHEMA IF NOT EXISTS ekb;

CREATE OR REPLACE FUNCTION ekb.current_tenant_id()
RETURNS uuid
LANGUAGE sql
STABLE
AS $$
  SELECT NULLIF(current_setting('app.tenant_id', true), '')::uuid;
$$;

CREATE TABLE tenants (
  id uuid PRIMARY KEY,
  tenant_id uuid GENERATED ALWAYS AS (id) STORED UNIQUE,
  name text NOT NULL,
  status text NOT NULL CHECK (status IN ('active', 'suspended', 'deleted')),
  plan text NOT NULL,
  region text NOT NULL,
  retention_policy jsonb NOT NULL DEFAULT '{}'::jsonb,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE workspaces (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  name text NOT NULL,
  type text NOT NULL CHECK (type IN ('sales', 'hr', 'ops', 'engineering', 'general')),
  parent_id uuid REFERENCES workspaces(id) ON DELETE SET NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, name)
);

CREATE TABLE users (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  primary_email text NOT NULL,
  display_name text NOT NULL,
  status text NOT NULL CHECK (status IN ('active', 'disabled', 'deleted')),
  identity_provider_id text,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, primary_email)
);

CREATE TABLE tenant_memberships (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  user_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  role text NOT NULL CHECK (role IN ('owner', 'admin', 'member', 'viewer')),
  status text NOT NULL CHECK (status IN ('active', 'invited', 'disabled')),
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, user_id)
);

CREATE TABLE workspace_memberships (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  workspace_id uuid NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  user_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  role text NOT NULL CHECK (role IN ('owner', 'admin', 'editor', 'viewer')),
  status text NOT NULL CHECK (status IN ('active', 'invited', 'disabled')),
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, workspace_id, user_id)
);

CREATE TABLE groups (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  workspace_id uuid REFERENCES workspaces(id) ON DELETE CASCADE,
  name text NOT NULL,
  purpose text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, workspace_id, name)
);

CREATE TABLE group_members (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  group_id uuid NOT NULL REFERENCES groups(id) ON DELETE CASCADE,
  principal_type text NOT NULL CHECK (principal_type IN ('user', 'group', 'service_account')),
  principal_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, group_id, principal_type, principal_id)
);

CREATE TABLE service_accounts (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  workspace_id uuid REFERENCES workspaces(id) ON DELETE CASCADE,
  name text NOT NULL,
  owner_user_id uuid REFERENCES users(id) ON DELETE SET NULL,
  status text NOT NULL CHECK (status IN ('active', 'disabled', 'deleted')),
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, workspace_id, name)
);

CREATE TABLE api_keys (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  principal_id uuid NOT NULL,
  scopes text[] NOT NULL DEFAULT '{}'::text[],
  key_hash text NOT NULL,
  expires_at timestamptz,
  last_used_at timestamptz,
  created_at timestamptz NOT NULL DEFAULT now()
);
COMMENT ON COLUMN api_keys.key_hash IS 'Keyed HMAC-SHA256 over the API key using a server-side pepper; never store plaintext API keys.';

CREATE TABLE knowledge_bases (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  workspace_id uuid NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  name text NOT NULL,
  visibility text NOT NULL CHECK (visibility IN ('private', 'workspace', 'tenant')),
  owner_id uuid REFERENCES users(id) ON DELETE SET NULL,
  default_policy_id uuid,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, workspace_id, name)
);

CREATE TABLE kb_grants (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  kb_id uuid NOT NULL REFERENCES knowledge_bases(id) ON DELETE CASCADE,
  principal_type text NOT NULL CHECK (principal_type IN ('user', 'group', 'service_account')),
  principal_id uuid NOT NULL,
  permission text NOT NULL CHECK (permission IN ('read', 'write', 'grant', 'admin')),
  expires_at timestamptz,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, kb_id, principal_type, principal_id, permission)
);

CREATE TABLE source_connectors (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  workspace_id uuid REFERENCES workspaces(id) ON DELETE SET NULL,
  type text NOT NULL,
  credential_ref text NOT NULL,
  sync_policy jsonb NOT NULL DEFAULT '{}'::jsonb,
  status text NOT NULL CHECK (status IN ('active', 'paused', 'error', 'deleted')),
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE documents (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  kb_id uuid NOT NULL REFERENCES knowledge_bases(id) ON DELETE CASCADE,
  source_id uuid REFERENCES source_connectors(id) ON DELETE SET NULL,
  uri text NOT NULL,
  title text NOT NULL,
  version integer NOT NULL DEFAULT 1,
  acl_hash text NOT NULL,
  status text NOT NULL CHECK (status IN ('active', 'revoked', 'deleted')),
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, kb_id, uri, version)
);

CREATE TABLE document_versions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  document_id uuid NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
  content_hash text NOT NULL,
  parser_version text NOT NULL,
  metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, document_id, content_hash)
);

CREATE TABLE chunks (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  document_version_id uuid NOT NULL REFERENCES document_versions(id) ON DELETE CASCADE,
  text text NOT NULL,
  span jsonb NOT NULL DEFAULT '{}'::jsonb,
  metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
  acl_hash text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE index_versions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  kb_id uuid NOT NULL REFERENCES knowledge_bases(id) ON DELETE CASCADE,
  embedding_model text NOT NULL,
  chunker_version text NOT NULL,
  status text NOT NULL CHECK (status IN ('building', 'active', 'superseded', 'failed')),
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, kb_id, embedding_model, chunker_version, created_at)
);

CREATE TABLE chunk_embeddings (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  chunk_id uuid NOT NULL REFERENCES chunks(id) ON DELETE CASCADE,
  index_version_id uuid NOT NULL REFERENCES index_versions(id) ON DELETE CASCADE,
  vector_ref text NOT NULL,
  embedding_hash text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, chunk_id, index_version_id)
);

CREATE TABLE resource_grants (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  resource_type text NOT NULL,
  resource_id uuid NOT NULL,
  principal_type text NOT NULL CHECK (principal_type IN ('user', 'group', 'service_account')),
  principal_id uuid NOT NULL,
  permission text NOT NULL,
  expires_at timestamptz,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, resource_type, resource_id, principal_type, principal_id, permission)
);

CREATE TABLE policy_bindings (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  scope_type text NOT NULL CHECK (scope_type IN ('tenant', 'workspace', 'knowledge_base', 'document', 'tool')),
  scope_id uuid NOT NULL,
  policy_id text NOT NULL,
  version text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, scope_type, scope_id, policy_id, version)
);

CREATE TABLE policy_decision_logs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  request_id text NOT NULL,
  principal_id uuid NOT NULL,
  action text NOT NULL,
  resource jsonb NOT NULL,
  decision text NOT NULL CHECK (decision IN ('allow', 'deny')),
  reason text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE audit_events (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  actor_id uuid,
  action text NOT NULL,
  resource jsonb NOT NULL,
  ip inet,
  user_agent text,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE conversations (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  workspace_id uuid NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  user_id uuid REFERENCES users(id) ON DELETE SET NULL,
  app_id text,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE messages (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  conversation_id uuid NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
  role text NOT NULL CHECK (role IN ('system', 'user', 'assistant', 'tool')),
  content text NOT NULL,
  trace_id text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE retrieval_events (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  trace_id text NOT NULL,
  query text NOT NULL,
  kb_ids uuid[] NOT NULL DEFAULT '{}'::uuid[],
  chunk_ids uuid[] NOT NULL DEFAULT '{}'::uuid[],
  scores jsonb NOT NULL DEFAULT '{}'::jsonb,
  policy_version text NOT NULL,
  index_version_id uuid REFERENCES index_versions(id) ON DELETE SET NULL,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE answer_events (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  trace_id text NOT NULL,
  model text NOT NULL,
  prompt_version text NOT NULL,
  citations jsonb NOT NULL DEFAULT '[]'::jsonb,
  cost numeric(12, 6) NOT NULL DEFAULT 0,
  latency integer NOT NULL CHECK (latency >= 0),
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE tools (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  name text NOT NULL,
  type text NOT NULL CHECK (type IN ('mcp', 'rest', 'internal')),
  schema jsonb NOT NULL DEFAULT '{}'::jsonb,
  risk_level text NOT NULL CHECK (risk_level IN ('low', 'medium', 'high')),
  owner_id uuid REFERENCES users(id) ON DELETE SET NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, name)
);

CREATE TABLE tool_grants (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  tool_id uuid NOT NULL REFERENCES tools(id) ON DELETE CASCADE,
  principal_type text NOT NULL CHECK (principal_type IN ('user', 'group', 'service_account')),
  principal_id uuid NOT NULL,
  permission text NOT NULL CHECK (permission IN ('invoke', 'admin')),
  constraints jsonb NOT NULL DEFAULT '{}'::jsonb,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, tool_id, principal_type, principal_id, permission)
);

CREATE TABLE tool_calls (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  trace_id text NOT NULL,
  tool_id uuid NOT NULL REFERENCES tools(id) ON DELETE RESTRICT,
  input_hash text NOT NULL,
  output_hash text,
  decision text NOT NULL CHECK (decision IN ('allow', 'deny', 'error')),
  latency integer NOT NULL CHECK (latency >= 0),
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE eval_datasets (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  name text NOT NULL,
  scope jsonb NOT NULL DEFAULT '{}'::jsonb,
  version text NOT NULL,
  owner_id uuid REFERENCES users(id) ON DELETE SET NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, name, version)
);

CREATE TABLE eval_cases (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  dataset_id uuid NOT NULL REFERENCES eval_datasets(id) ON DELETE CASCADE,
  query text NOT NULL,
  expected_answer text,
  required_chunk_ids uuid[] NOT NULL DEFAULT '{}'::uuid[],
  forbidden_chunk_ids uuid[] NOT NULL DEFAULT '{}'::uuid[],
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE eval_runs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  dataset_id uuid NOT NULL REFERENCES eval_datasets(id) ON DELETE CASCADE,
  candidate_config jsonb NOT NULL DEFAULT '{}'::jsonb,
  expected_metrics text[] NOT NULL CHECK (COALESCE(array_length(expected_metrics, 1), 0) > 0),
  status text NOT NULL CHECK (status IN ('queued', 'running', 'passed', 'failed', 'error')),
  started_at timestamptz NOT NULL DEFAULT now(),
  completed_at timestamptz
);

CREATE TABLE eval_scores (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  eval_run_id uuid NOT NULL REFERENCES eval_runs(id) ON DELETE CASCADE,
  case_id uuid NOT NULL REFERENCES eval_cases(id) ON DELETE CASCADE,
  metric text NOT NULL,
  metric_status text NOT NULL DEFAULT 'scored' CHECK (metric_status IN ('scored', 'missing', 'skipped', 'error', 'absent')),
  score numeric(6, 5) NOT NULL CHECK (score >= 0 AND score <= 1),
  reason text NOT NULL,
  evidence jsonb NOT NULL DEFAULT '{}'::jsonb,
  created_at timestamptz NOT NULL DEFAULT now(),
  CHECK (metric_status = 'scored' OR score = 0),
  UNIQUE (tenant_id, eval_run_id, case_id, metric)
);

CREATE VIEW eval_score_facts WITH (security_invoker = true) AS
SELECT
  r.tenant_id,
  r.id AS eval_run_id,
  c.id AS case_id,
  expected.metric,
  COALESCE(s.score, 0.0::numeric(6, 5)) AS score,
  COALESCE(s.metric_status, 'absent') AS metric_status,
  COALESCE(s.reason, 'metric absent from producer output; zero-filled by contract') AS reason,
  COALESCE(s.evidence, '{}'::jsonb) AS evidence
FROM eval_runs r
JOIN eval_cases c
  ON c.tenant_id = r.tenant_id
 AND c.dataset_id = r.dataset_id
CROSS JOIN LATERAL unnest(r.expected_metrics) AS expected(metric)
LEFT JOIN eval_scores s
  ON s.tenant_id = r.tenant_id
 AND s.eval_run_id = r.id
 AND s.case_id = c.id
 AND s.metric = expected.metric
WHERE r.tenant_id = ekb.current_tenant_id();

CREATE INDEX workspaces_tenant_parent_idx ON workspaces (tenant_id, parent_id);
CREATE INDEX users_tenant_status_idx ON users (tenant_id, status);
CREATE INDEX groups_tenant_workspace_idx ON groups (tenant_id, workspace_id);
CREATE INDEX documents_tenant_kb_status_idx ON documents (tenant_id, kb_id, status);
CREATE INDEX chunks_tenant_acl_hash_idx ON chunks (tenant_id, acl_hash);
CREATE INDEX messages_tenant_trace_idx ON messages (tenant_id, trace_id);
CREATE INDEX retrieval_events_tenant_trace_idx ON retrieval_events (tenant_id, trace_id);
CREATE INDEX answer_events_tenant_trace_idx ON answer_events (tenant_id, trace_id);
CREATE INDEX tool_calls_tenant_trace_idx ON tool_calls (tenant_id, trace_id);
CREATE INDEX audit_events_tenant_created_idx ON audit_events (tenant_id, created_at);
CREATE INDEX policy_decision_logs_tenant_request_idx ON policy_decision_logs (tenant_id, request_id);

ALTER TABLE tenants ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenants_tenant_isolation ON tenants USING (tenant_id = ekb.current_tenant_id()) WITH CHECK (tenant_id = ekb.current_tenant_id());
ALTER TABLE workspaces ENABLE ROW LEVEL SECURITY;
CREATE POLICY workspaces_tenant_isolation ON workspaces USING (tenant_id = ekb.current_tenant_id()) WITH CHECK (tenant_id = ekb.current_tenant_id());
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
CREATE POLICY users_tenant_isolation ON users USING (tenant_id = ekb.current_tenant_id()) WITH CHECK (tenant_id = ekb.current_tenant_id());
ALTER TABLE tenant_memberships ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_memberships_tenant_isolation ON tenant_memberships USING (tenant_id = ekb.current_tenant_id()) WITH CHECK (tenant_id = ekb.current_tenant_id());
ALTER TABLE workspace_memberships ENABLE ROW LEVEL SECURITY;
CREATE POLICY workspace_memberships_tenant_isolation ON workspace_memberships USING (tenant_id = ekb.current_tenant_id()) WITH CHECK (tenant_id = ekb.current_tenant_id());
ALTER TABLE groups ENABLE ROW LEVEL SECURITY;
CREATE POLICY groups_tenant_isolation ON groups USING (tenant_id = ekb.current_tenant_id()) WITH CHECK (tenant_id = ekb.current_tenant_id());
ALTER TABLE group_members ENABLE ROW LEVEL SECURITY;
CREATE POLICY group_members_tenant_isolation ON group_members USING (tenant_id = ekb.current_tenant_id()) WITH CHECK (tenant_id = ekb.current_tenant_id());
ALTER TABLE service_accounts ENABLE ROW LEVEL SECURITY;
CREATE POLICY service_accounts_tenant_isolation ON service_accounts USING (tenant_id = ekb.current_tenant_id()) WITH CHECK (tenant_id = ekb.current_tenant_id());
ALTER TABLE api_keys ENABLE ROW LEVEL SECURITY;
CREATE POLICY api_keys_tenant_isolation ON api_keys USING (tenant_id = ekb.current_tenant_id()) WITH CHECK (tenant_id = ekb.current_tenant_id());
ALTER TABLE knowledge_bases ENABLE ROW LEVEL SECURITY;
CREATE POLICY knowledge_bases_tenant_isolation ON knowledge_bases USING (tenant_id = ekb.current_tenant_id()) WITH CHECK (tenant_id = ekb.current_tenant_id());
ALTER TABLE kb_grants ENABLE ROW LEVEL SECURITY;
CREATE POLICY kb_grants_tenant_isolation ON kb_grants USING (tenant_id = ekb.current_tenant_id()) WITH CHECK (tenant_id = ekb.current_tenant_id());
ALTER TABLE source_connectors ENABLE ROW LEVEL SECURITY;
CREATE POLICY source_connectors_tenant_isolation ON source_connectors USING (tenant_id = ekb.current_tenant_id()) WITH CHECK (tenant_id = ekb.current_tenant_id());
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
CREATE POLICY documents_tenant_isolation ON documents USING (tenant_id = ekb.current_tenant_id()) WITH CHECK (tenant_id = ekb.current_tenant_id());
ALTER TABLE document_versions ENABLE ROW LEVEL SECURITY;
CREATE POLICY document_versions_tenant_isolation ON document_versions USING (tenant_id = ekb.current_tenant_id()) WITH CHECK (tenant_id = ekb.current_tenant_id());
ALTER TABLE chunks ENABLE ROW LEVEL SECURITY;
CREATE POLICY chunks_tenant_isolation ON chunks USING (tenant_id = ekb.current_tenant_id()) WITH CHECK (tenant_id = ekb.current_tenant_id());
ALTER TABLE index_versions ENABLE ROW LEVEL SECURITY;
CREATE POLICY index_versions_tenant_isolation ON index_versions USING (tenant_id = ekb.current_tenant_id()) WITH CHECK (tenant_id = ekb.current_tenant_id());
ALTER TABLE chunk_embeddings ENABLE ROW LEVEL SECURITY;
CREATE POLICY chunk_embeddings_tenant_isolation ON chunk_embeddings USING (tenant_id = ekb.current_tenant_id()) WITH CHECK (tenant_id = ekb.current_tenant_id());
ALTER TABLE resource_grants ENABLE ROW LEVEL SECURITY;
CREATE POLICY resource_grants_tenant_isolation ON resource_grants USING (tenant_id = ekb.current_tenant_id()) WITH CHECK (tenant_id = ekb.current_tenant_id());
ALTER TABLE policy_bindings ENABLE ROW LEVEL SECURITY;
CREATE POLICY policy_bindings_tenant_isolation ON policy_bindings USING (tenant_id = ekb.current_tenant_id()) WITH CHECK (tenant_id = ekb.current_tenant_id());
ALTER TABLE policy_decision_logs ENABLE ROW LEVEL SECURITY;
CREATE POLICY policy_decision_logs_tenant_isolation ON policy_decision_logs USING (tenant_id = ekb.current_tenant_id()) WITH CHECK (tenant_id = ekb.current_tenant_id());
ALTER TABLE audit_events ENABLE ROW LEVEL SECURITY;
CREATE POLICY audit_events_tenant_isolation ON audit_events USING (tenant_id = ekb.current_tenant_id()) WITH CHECK (tenant_id = ekb.current_tenant_id());
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;
CREATE POLICY conversations_tenant_isolation ON conversations USING (tenant_id = ekb.current_tenant_id()) WITH CHECK (tenant_id = ekb.current_tenant_id());
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;
CREATE POLICY messages_tenant_isolation ON messages USING (tenant_id = ekb.current_tenant_id()) WITH CHECK (tenant_id = ekb.current_tenant_id());
ALTER TABLE retrieval_events ENABLE ROW LEVEL SECURITY;
CREATE POLICY retrieval_events_tenant_isolation ON retrieval_events USING (tenant_id = ekb.current_tenant_id()) WITH CHECK (tenant_id = ekb.current_tenant_id());
ALTER TABLE answer_events ENABLE ROW LEVEL SECURITY;
CREATE POLICY answer_events_tenant_isolation ON answer_events USING (tenant_id = ekb.current_tenant_id()) WITH CHECK (tenant_id = ekb.current_tenant_id());
ALTER TABLE tools ENABLE ROW LEVEL SECURITY;
CREATE POLICY tools_tenant_isolation ON tools USING (tenant_id = ekb.current_tenant_id()) WITH CHECK (tenant_id = ekb.current_tenant_id());
ALTER TABLE tool_grants ENABLE ROW LEVEL SECURITY;
CREATE POLICY tool_grants_tenant_isolation ON tool_grants USING (tenant_id = ekb.current_tenant_id()) WITH CHECK (tenant_id = ekb.current_tenant_id());
ALTER TABLE tool_calls ENABLE ROW LEVEL SECURITY;
CREATE POLICY tool_calls_tenant_isolation ON tool_calls USING (tenant_id = ekb.current_tenant_id()) WITH CHECK (tenant_id = ekb.current_tenant_id());
ALTER TABLE eval_datasets ENABLE ROW LEVEL SECURITY;
CREATE POLICY eval_datasets_tenant_isolation ON eval_datasets USING (tenant_id = ekb.current_tenant_id()) WITH CHECK (tenant_id = ekb.current_tenant_id());
ALTER TABLE eval_cases ENABLE ROW LEVEL SECURITY;
CREATE POLICY eval_cases_tenant_isolation ON eval_cases USING (tenant_id = ekb.current_tenant_id()) WITH CHECK (tenant_id = ekb.current_tenant_id());
ALTER TABLE eval_runs ENABLE ROW LEVEL SECURITY;
CREATE POLICY eval_runs_tenant_isolation ON eval_runs USING (tenant_id = ekb.current_tenant_id()) WITH CHECK (tenant_id = ekb.current_tenant_id());
ALTER TABLE eval_scores ENABLE ROW LEVEL SECURITY;
CREATE POLICY eval_scores_tenant_isolation ON eval_scores USING (tenant_id = ekb.current_tenant_id()) WITH CHECK (tenant_id = ekb.current_tenant_id());
