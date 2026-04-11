# Knowledge Base

Topic: Goal-Managed Agent Orchestration with Conversational Planning, Governance, Pluggable Subagent Protocols, and Correctness Strategy

## Executive Decision Brief
- Build this as a local-first governed control plane: conversational planning turns vague goals into SMART KRs, typed runtimes execute bounded work, an operator cockpit handles approvals and blocked states, and completion stays evidence-backed from day one. Do not sell this as full autonomy [source-1-user-brief] [source-8-user-followup] [source-15-goal-managed-agent-framework] [source-17-goal-managed-agent-testing-strategy].
- Solo builders are the cleanest first wedge, but larger organizations also matter because coordination overhead, compliance, and authority scoping get worse as more repos, workspaces, reviewers, and policy layers enter the loop. Keep one single accountable owner per objective as the invariant across both [source-5-multica-platform] [source-8-user-followup] [source-11-claudecode-permission-governance].
- The next proof burden is not more topical coverage. It is proving that one real KR can move cleanly through clarification, readiness preview, governed launch, permission denial, replan, resume, completion claim, evaluator verification, operator acceptance, and recovery or audit without state ambiguity [source-8-user-followup] [source-9-claudecode-source-inspection] [source-16-goal-managed-agent-protocol-spec] [source-17-goal-managed-agent-testing-strategy].
- Authority should expand only behind metric gates: approval precision, false-approve rate, false-block rate, resume success, orphaned-completion rate, evaluator disagreement, and cost or latency baselines should decide when GitHub or filesystem authority widens [source-11-claudecode-permission-governance] [source-17-goal-managed-agent-testing-strategy] [source-18-user-priority-correctness].

## Working thesis
- There is a real need here, but it is narrower than autonomy marketing. The pain is not merely poor prompting; it is the burden of carrying intent, approvals, blockers, and evaluation across multi-step work [source-1-user-brief] [source-2-auto-research-framework].
- The product is technically feasible now because the current local-agent stack already exposes the core surfaces needed for orchestration: Codex SDK thread control through `startThread()`, `run(...)`, and `resumeThread(...)`; repo-local hook config in `.codex/hooks.json`; Claude Code `permissionDecision: defer` plus `claude -p --resume <session-id>`; and daemon-mediated local execution with workspaces, heartbeats, and task polling [source-3-codex-capabilities] [source-4-claude-capabilities] [source-6-multica-daemon].
- Humans do not disappear. They remain necessary for ambiguous goal formation, policy exceptions, destructive authority, and final acceptance when evidence is incomplete or evaluators disagree [source-11-claudecode-permission-governance] [source-17-goal-managed-agent-testing-strategy] [source-18-user-priority-correctness].

## 1. Demand reality
- Prompt-centric tooling breaks down when work spans dependent steps, approvals, runtime interruptions, and evidence review. The user is asking to manage goals with less task babysitting, not to type better prompts [source-1-user-brief].
- The local auto-research framework is direct evidence that once work becomes iterative, control-plane behavior matters as much as model output. Its bounded `sources/`, mutable `knowledge_base.md`, fixed benchmark questions, `results.tsv`, keep-or-discard ratchet, human feedback hot reload, and supervisor stop conditions are already product behavior, not prompt craft [source-2-auto-research-framework].
- Multica is the strongest comparable in the corpus because it already exposes a managed-agent surface with assignments, blockers, multi-workspace isolation, a daemon, execution history, and incremental run-message fetching. That proves demand for governed agent execution, even if it does not prove people can live at goal level alone [source-5-multica-platform] [source-6-multica-daemon].
- Decision: the need is real for local-agent power users and likely grows with coordination complexity. What remains unproven is a universal mostly-goal-management workflow; that is why the next proof burden is one end-to-end KR, not more breadth.

## 2. Organization fit: solo, small team, larger organization
- Solo builders are the cleanest initial wedge because one person can answer clarifications quickly, approve work with low latency, and judge whether evidence is sufficient [source-1-user-brief] [source-8-user-followup].
- Small teams benefit when one objective owner can mix human and agent work on the same board, see blockers, and review shared evidence. Multica's emphasis on assignments, blockers, reusable skills, and workspace isolation is evidence that this middle layer is real product terrain [source-5-multica-platform] [source-6-multica-daemon].
- Larger organizations also matter because the exact same workflow becomes more valuable when coordination overhead, compliance, and permission governance get harder. Claude Code's `PermissionRuleList` already implies the right maturity model: separate recent denials, allow rules, ask rules, deny rules, and workspace directories, with user-owned versus managed rules [source-8-user-followup] [source-11-claudecode-permission-governance].
- The invariant across all three is one single accountable owner per objective. The difference is not whether objective-driven execution matters; it is how much governance, auditability, and policy layering must sit around it [source-8-user-followup] [source-11-claudecode-permission-governance].

## 3. Conversational planning and SMART KR design
The system should turn ambiguity into executable work through a staged conversation, not a rigid form [source-8-user-followup] [source-9-claudecode-source-inspection] [source-10-claudecode-broader-product-inspection].

Planning flow:
1. Capture the raw goal, why it matters, deadline, owner, and excluded work.
2. Ask clarifying questions about outcome, constraints, current assets, permissions, dependencies, risk tolerance, and what would count as proof.
3. Draft a short objective with scope, owner, success window, and non-goals.
4. Draft candidate SMART KRs. The local protocol spec already gives the right storage shape: each `KeyResult` carries `specific`, `measurable`, `attainable`, `relevant`, `time_bound`, `dependency_ids`, `evidence_contract_id`, and `version` [source-16-goal-managed-agent-protocol-spec].
5. Mark missing SMART properties or hidden coupling explicitly. A KR should not progress while it is vague, unmeasurable, or too entangled with siblings.
6. Show an execution-readiness preview listing likely runtimes, workspace scope, approvals, evidence checks, and known blockers.
7. Require explicit approval before any runtime starts.

### Worked OAuth2 planning example
Raw goal: `Move the app from ad hoc session middleware to OAuth2 before launch` [source-8-user-followup].

Clarifying questions the system should ask before execution:
- Which surfaces are in scope: API only, admin UI, mobile clients, or all three?
- What counts as done: staging only, production cutover, or production plus rollback readiness?
- Which identity provider is fixed, and which repo or directories may the agent modify?
- What deadline is binding?
- What evidence is required: contract tests, login video, docs, security review, migration runbook?
- What blast radius is acceptable if credentials or callback URLs are missing?

A first-pass KR such as `switch auth to OAuth2` should be rejected as not Specific, not Measurable, and not Time-bound. The planning UI should mark those SMART gaps and ask follow-ups rather than pretending a rewrite is execution-ready [source-8-user-followup] [source-9-claudecode-source-inspection].

A revised objective and KR set could be:
- Objective: `Ship OAuth2-based authentication for API and admin routes without breaking existing user access before launch review.`
- KR1: `By April 30, API and admin routes authenticate through provider X in staging; contract tests for login, token refresh, and logout pass; legacy middleware remains only in the documented compatibility shim.`
- KR2: `By April 30, secrets, callback URLs, and environment variables are present in staging; a rollback runbook and migration checklist are approved by the objective owner.`
- KR3: `Before production rollout, the operator reviews an evidence bundle containing test output, changed files, remaining risk, and the exact approvals required for production credentials.`

The readiness preview should then show expected runtime choice, workspace scope, likely GitHub or filesystem approvals, required `EvidenceCheck` types, and known blockers such as missing client credentials. The approval surface should preview the plan, show the dependency graph, flag any KR that is not reasonably independent, and name who must accept the evidence bundle [source-9-claudecode-source-inspection] [source-16-goal-managed-agent-protocol-spec].

Claude Code is strong evidence that this must be a first-class interaction design problem. `AskUserQuestionTool` supports structured multiple-choice questions, preview mode, side-by-side option rendering, and `shouldDefer: true`; `EnterPlanModeTool` is a dedicated read-only stage that says to use `AskUserQuestion`, present the plan for approval, and avoid file edits until approval; `TaskCreateTool`, `TaskGetTool`, and `TaskUpdateTool` make dependency-aware work tracking explicit instead of burying it in transcript text [source-9-claudecode-source-inspection].

## 4. Recursive KR to Objective decomposition and dependency rules
- A higher-level `KeyResult` should become a child `Objective` only when satisfying it requires multiple subordinate KRs with their own evidence and review path. The object model supports this explicitly through `parent_key_result_id`, per-KR `dependency_ids`, and independent `version` fields [source-8-user-followup] [source-16-goal-managed-agent-protocol-spec].
- Keep the hierarchy shallow and legible. Every child objective still needs one accountable owner, bounded scope, inherited intent from the parent KR, and a clear completion contract [source-15-goal-managed-agent-framework] [source-16-goal-managed-agent-protocol-spec].
- KRs should be independent by default. Dependencies must be sparse, explicit, and reviewable. If many sibling KRs block one another or mutate the same state, the plan is wrong and should be redrawn before execution [source-8-user-followup] [source-9-claudecode-source-inspection].
- Parent edits must not silently merge back into child work. The spec's failure rules say a parent edit after spawn should mark work `stale_context`, and a late child `complete` after parent rescope becomes `orphaned` rather than mutating current state [source-16-goal-managed-agent-protocol-spec] [source-17-goal-managed-agent-testing-strategy].

## 5. What is technically feasible now
- Codex already supports the core local-execution path: local CLI execution, SDK thread control through `startThread()`, `run(...)`, and `resumeThread(...)`, hook config in `config.toml`, repo-local hooks in `.codex/hooks.json`, concurrent hook matching, JSON on stdin, and `Stop` hooks that can continue the agent with a new prompt. The important limitation is explicit: current `PreToolUse` and `PostToolUse` interception is still Bash-focused and incomplete [source-3-codex-capabilities].
- Claude Code exposes the missing human-escalation surfaces: `SessionStart` hooks for context injection, `CLAUDE_ENV_FILE` for persisted environment variables, `PreToolUse` hooks that can block or defer, `agent` hooks that can spawn a subagent and return a structured decision, `async` command hooks for long tasks, and non-interactive pause or resume through `permissionDecision: defer` plus `claude -p --resume <session-id>` [source-4-claude-capabilities].
- The current machine already has `codex-cli 0.118.0` and `Claude Code 2.1.100`, so the local runtime precondition is satisfied for a prototype [source-7-local-environment].
- Multica documents the clearest daemon pattern in the corpus: detect installed `claude` and `codex` CLIs, register runtimes for watched workspaces, poll for claimed tasks, create an isolated workspace directory for each task, spawn the agent CLI, stream results, send heartbeats, and deregister on shutdown. The documented defaults are concrete: `3s` poll, `15s` heartbeat, `2h` timeout, `20` max concurrent tasks [source-6-multica-daemon].
- Claude Code source inspection adds the product-state evidence missing from docs alone: a dedicated `tool.blocked_on_user` span, task and dependency objects, and blocked-shell recovery through a watchdog that checks every `5` seconds, uses a `45` second stall threshold, and tells the model to kill and rerun interactive commands non-interactively [source-9-claudecode-source-inspection].
- Build-from-scratch constraint: these are patterns to absorb, not frameworks to depend on. The runtime should use our own object model, event log, and protocol contracts even if adapters call existing CLIs [source-13-build-from-scratch-constraint].

Feasible now:
- conversational planning,
- local daemon plus local CLI execution,
- isolated workspace leasing,
- blocked-on-user and resume semantics,
- typed hooks,
- structured task and evidence state,
- human approval and evaluation loops.

Still speculative or risky:
- broad unattended cross-system automation,
- low-friction org-wide GitHub write authority,
- reliable business-judgment closure without human review,
- and large-scale multi-agent coordination without strong acceptance checks.

## 6. Why managing goals alone is still incomplete
A person cannot mostly manage goals unless the system also owns the layers underneath the goals: clarification, runtime routing, policy and approval, blocked-state handling, evaluation, and decision recording in an append-only event log [source-1-user-brief] [source-2-auto-research-framework] [source-15-goal-managed-agent-framework].

The local protocol spec makes the gap concrete. `TaskExecution` has states such as `queued`, `starting`, `running`, `blocked`, `completed_claimed`, `failed`, `cancelled`, and `orphaned`. `completed_claimed` is deliberately not the same thing as done. `EvidenceCheck` can require `test`, `artifact`, `benchmark`, `human_review`, or `policy_review`, and a KR can close only after those checks pass or are explicitly waived [source-16-goal-managed-agent-protocol-spec].

Without those layers, goal management collapses back into prompt babysitting with better labels. Humans remain essential for ambiguous goal formation, risky authority, credential provisioning, evaluator disagreement, and final acceptance when evidence is incomplete or conflicting [source-4-claude-capabilities] [source-11-claudecode-permission-governance] [source-17-goal-managed-agent-testing-strategy] [source-18-user-priority-correctness].

## 7. MVP architecture
The MVP should separate control plane, execution runtime, governance, evaluation, storage, and operator surfaces from day one [source-15-goal-managed-agent-framework] [source-16-goal-managed-agent-protocol-spec].

Control plane:
- `Goal`, `Objective`, `KeyResult`, `EvidenceCheck`, `DecisionRecord`.
- `KeyResult` should store `specific`, `measurable`, `attainable`, `relevant`, `time_bound`, `dependency_ids`, `evidence_contract_id`, and `version` [source-16-goal-managed-agent-protocol-spec].

Execution runtime:
- `RuntimeAdapter` for Codex CLI and Claude CLI or SDK.
- `runtime-manager` to launch sessions, allocate workspaces, monitor liveness, and own `ResumeHandle` state [source-15-goal-managed-agent-framework].
- isolated workspace or worktree mode per task [source-6-multica-daemon] [source-12-claudecode-subagent-hooks-pluggability].

Governance:
- `PolicyEngine`, `PermissionRule`, `ApprovalRequest`, `HookRegistry` [source-15-goal-managed-agent-framework].
- explicit `allow`, `ask`, `deny` policy with scope by workspace, repo, path, branch, action, or tool [source-11-claudecode-permission-governance].

Evaluation:
- `EvaluatorRegistry`, `VerificationRun`, `CompletionDecision`, and evidence-backed closure, with evaluator-provider plugins bound to workflow or evaluator scope rather than global callbacks [source-15-goal-managed-agent-framework] [source-17-goal-managed-agent-testing-strategy].

Storage:
- local structured store for owned objects,
- append-only event log for replay and audit,
- markdown export for knowledge capture,
- later adapters for GitHub and Obsidian, but not as core dependencies [source-1-user-brief] [source-13-build-from-scratch-constraint].

Operator surfaces:
- goal conversation,
- plan preview and approval,
- task board,
- session detail,
- approval inbox,
- evidence review,
- policy panel.

The event log should be explicit, not implied. The spec's `EventEnvelope` with `event_id`, `event_type`, `object_type`, `object_id`, optional `run_id`, `causation_id`, `correlation_id`, stable `dedupe_key`, `actor`, `occurred_at`, and structured `payload` is the right source of truth for replay, audit, and recovery [source-16-goal-managed-agent-protocol-spec].

## 8. Why the center of gravity is UI and UX
Claude Code is strong evidence that the hard product work is not hidden backend scheduling. `AskUserQuestionTool` gives previewable clarification, `EnterPlanModeTool` creates a staged approval flow, `TaskCreateTool` or `TaskGetTool` or `TaskUpdateTool` make dependencies explicit, `tool.blocked_on_user` is traced as a first-class runtime state, and `LocalShellTask` ships a stall watchdog for interactive command recovery [source-9-claudecode-source-inspection].

The broader product inspection strengthens the point. `TaskListV2` and `useTasksV2` sort tasks by status and visible blockers; `RemoteAgentTask` stores session IDs, logs, todo lists, remote metadata, and phases such as `needs_input` and `plan_ready`; `scheduleRemoteAgents.ts` uses `AskUserQuestion` as the required first step unless explicit arguments are already present [source-10-claudecode-broader-product-inspection].

Therefore the MVP needs primary screens for:
- goal conversation with preview,
- objective and KR approval,
- dependency-aware task list,
- session detail with current tool activity and spawned agents,
- blocked-on-user inbox,
- approval and rule management,
- evidence review and verifier status.

If the operator must reconstruct state from transcripts or raw logs, the product has failed at its main job.

## 9. Permission governance and approval UX
Permission governance should look like an operator product, not a hidden ACL file [source-11-claudecode-permission-governance].

Concrete source evidence:
- `PermissionRuleList` has tabs for recent denials, allow rules, ask rules, deny rules, and workspace directories.
- `interactiveHandler.ts` races approval sources from the local user, bridge or web surface, channel-based callbacks, and automated classifier checks while recording decision source and timing.
- `BashPermissionRequest.tsx` includes destructive-command warnings, sandbox considerations, classifier-based auto-approval attempts, and reusable rule suggestions.
- `FilesystemPermissionRequest.tsx` extracts a concrete path when possible, routes the request through a dedicated file permission dialog, and distinguishes read versus write operations [source-11-claudecode-permission-governance].

Required model for our product:
- `allow`, `ask`, `deny` rules,
- scope by workspace, repo, branch, path, tool, and action,
- separate capability profiles for GitHub and filesystem authority,
- recent-denials view so the system can learn from refusals and avoid repetitive prompts,
- immutable policy layers for managed settings plus user-owned local exceptions [source-11-claudecode-permission-governance] [source-15-goal-managed-agent-framework].

Approval UX should show the exact requested action, reason code, affected workspace or path, blast radius, expiry, related objective or KR, and whether the decision can become a reusable rule. Discovery can be broader, write actions should usually be `ask`, destructive actions should lean `deny` unless explicitly elevated, and denials should force replanning or a narrower request rather than silent retries [source-6-multica-daemon] [source-7-local-environment] [source-11-claudecode-permission-governance].

## 10. Subagent protocol
Subagents must be a protocol, not a convenience helper [source-12-claudecode-subagent-hooks-pluggability] [source-16-goal-managed-agent-protocol-spec].

Required contract:
- mode: `fork`, `fresh`, `worktree`, `remote`, `teammate`.
- context contract: immutable goal scope, filtered or summarized history, cloned mutable runtime state by default, explicitly shared callbacks only when required.
- communication contract: typed channels for notification, direct message, approval, resume, and event streaming.
- lifecycle policy: timeout, retry budget, stall policy, orphan policy.
- protocol actions: `spawn`, `ack`, `block`, `resume`, `complete`, `cancel`.

Claude Code lessons that should become design rules:
- `AgentTool.tsx` routes into regular subagents, implicit forks, background local agents, worktree-isolated agents, remote agents, and teammate or squad-style agents. The product surface says launch an agent, but the runtime is selecting among multiple isolation modes [source-12-claudecode-subagent-hooks-pluggability].
- `runAgent.ts` and `forkedAgent.ts` construct child context deliberately: normal subagents are seeded with `forkContextMessages + promptMessages`; incomplete parent tool calls are filtered out; `createSubagentContext()` clones mutable state; `readFileState` is cloned; content-replacement state is cloned for prompt-cache stability; only selected callbacks are shared back [source-12-claudecode-subagent-hooks-pluggability].
- `forkSubagent.ts` is a special inheritance path: omitting `subagent_type` can trigger an implicit `fork`; the child inherits the rendered system prompt bytes, reuses the parent's tool pool and thinking config, and uses a byte-stable prefix for prompt-cache reuse [source-12-claudecode-subagent-hooks-pluggability].
- Parent and child communication already uses multiple explicit paths: `LocalAgentTask` writes output and notifications, `resumeAgent.ts` reconstructs transcript and worktree state, and `SendMessageTool.ts` plus `teammateMailbox.ts` implement file-backed inboxes for direct, broadcast, structured, and control messages such as plan approval or task assignment [source-12-claudecode-subagent-hooks-pluggability].

The local spec's `SpawnRequest` already names the right fields: `protocol_id`, `task_execution_id`, `mode`, `context_contract`, `capability_profile`, `communication_contract.channels`, and `lifecycle_policy` with `timeout_seconds`, `max_retries`, `stall_policy`, and `orphan_policy` [source-16-goal-managed-agent-protocol-spec]. Design rule: parent-child coordination should ride a typed message bus and event log. Transcript text may be inspectable evidence, but never the source of truth.

## 11. Hooks as deterministic control surfaces
Hooks matter because they actively change control flow, not because they add logs [source-3-codex-capabilities] [source-4-claude-capabilities] [source-12-claudecode-subagent-hooks-pluggability].

Relevant lifecycle boundaries already evidenced:
- `SessionStart`
- `UserPromptSubmit`
- `PreToolUse`
- `PostToolUse`
- `PostToolUseFailure`
- `PermissionRequest`
- `PermissionDenied`
- `SubagentStart`
- `SubagentStop`
- `TaskCreated`
- `TaskCompleted`
- `Stop`

Hook outputs are concrete, not metaphorical. Claude Code's hook types can block or approve, change tool input, inject additional context, retry denied operations, alter MCP tool output, request or answer permission decisions, add watched paths, and stop continuation with an explicit reason. Codex adds two useful constraints: matching hooks can run concurrently, and `Stop` hooks can continue the agent with a new prompt [source-3-codex-capabilities] [source-12-claudecode-subagent-hooks-pluggability].

The local protocol spec gives the right deterministic wrapper: `HookRegistration` includes `scope`, `event`, `order`, `timeout_ms`, `failure_policy`, `mode`, `input_schema_ref`, and `output_schema_ref`. Merge rules are explicit: `block` overrides `approve`; `stop_continuation` is terminal for that boundary; `updated_input` is valid only before execution starts; retries consume budget and must emit an event [source-16-goal-managed-agent-protocol-spec].

Critical caveat: hooks are not enough on their own. Source 3 states that current Codex `PreToolUse` and `PostToolUse` interception is still incomplete and Bash-focused, so the control plane still needs its own policy engine and approval state. Hooks should be treated as typed lifecycle boundaries, not the whole governance story [source-3-codex-capabilities].

## 12. Pluggability model
The framework should expose scoped, typed extension surfaces rather than one global callback table, and the same manifest plus lifecycle skeleton should govern both runtime launch plugins and evaluator plugins [source-12-claudecode-subagent-hooks-pluggability] [source-15-goal-managed-agent-framework] [source-16-goal-managed-agent-protocol-spec].

Recommended plugin types:
- runtime adapters,
- hook packages,
- evaluator providers,
- context assemblers,
- policy providers,
- export sinks,
- skill packs for planning or execution templates.

Recommended scopes:
- session,
- workflow,
- agent,
- runtime,
- evaluator.

Concrete source evidence:
- `registerFrontmatterHooks.ts` registers frontmatter hooks into session-scoped hooks and cleans them up with the session or subagent lifecycle, which is the right antidote to global mutation [source-12-claudecode-subagent-hooks-pluggability].
- The auto-research framework is another signal for explicit scoped surfaces: bounded source sets, benchmark definitions, producer and judge loops, supervisor state, and human feedback are all discrete extension points rather than hidden global behavior [source-2-auto-research-framework].
- Claude Code's permission model implies plugin authority also needs governance. Rules can be user-owned or managed, so plugins should declare the permissions they require and which rules they expect to interact with [source-11-claudecode-permission-governance].

Each plugin should declare scope and lifecycle, schemas, required permissions, conflict rules, failure policy, and cleanup behavior.

### Concrete contract example: `RuntimeAdapterPlugin`
The exact shape below is a recommended from-scratch contract inferred from the framework, protocol, and Claude Code session-scoped hook patterns; it is not claimed as a direct existing API [source-11-claudecode-permission-governance] [source-12-claudecode-subagent-hooks-pluggability] [source-15-goal-managed-agent-framework] [source-16-goal-managed-agent-protocol-spec].

```ts
type PermissionManifest = {
  filesystem?: Array<{
    workspace_ref: string;
    path_globs: string[];
    actions: Array<'read' | 'write' | 'delete' | 'exec'>;
  }>;
  github?: Array<{
    repo: string;
    branches?: string[];
    actions: Array<'read' | 'issue_write' | 'pr_write' | 'content_write'>;
  }>;
  tools?: Array<{
    tool_name: string;
    actions: string[];
  }>;
  escalation_required_for: string[];
};

type PluginManifest = {
  id: string;
  version: string;
  kind: 'runtime_adapter' | 'evaluator_provider';
  scopes: Array<'session' | 'workflow' | 'agent' | 'runtime' | 'evaluator'>;
  activation_events: string[];
  dispose_events: string[];
  input_schema_ref: string;
  output_schema_ref: string;
  permission_manifest: PermissionManifest;
  cleanup_contract: {
    idempotent: boolean;
    timeout_ms: number;
    emits_event: 'plugin.cleaned_up';
    failure_policy: 'fail_closed' | 'fail_open';
  };
};

type RuntimeAdapterPlugin = {
  manifest: PluginManifest & { kind: 'runtime_adapter' };
  register(ctx: RuntimePluginContext): Promise<{
    adapter_name: string;
    hook_registrations: HookRegistration[];
  }>;
  launch(req: LaunchRequest): Promise<{
    session_id: string;
    resume_handle?: ResumeHandle;
  }>;
  resume(handle: ResumeHandle): Promise<{
    session_id: string;
    resumed: boolean;
  }>;
  stop(session_id: string, reason_code: string): Promise<void>;
  collectArtifacts(session_id: string): Promise<ArtifactRef[]>;
  cleanup(scope_id: string): Promise<{
    released_hooks: string[];
    released_leases: string[];
  }>;
};
```

Why this matters:
- `permission_manifest` lets the policy engine and approval UI show requested authority before activation, which matches allow or ask or deny rule-driven governance [source-11-claudecode-permission-governance].
- `input_schema_ref` and `output_schema_ref` force typed contracts so runtime adapters, hooks, and evaluator providers compose through declared schemas instead of hidden payload assumptions [source-15-goal-managed-agent-framework] [source-16-goal-managed-agent-protocol-spec].
- `activation_events` and `dispose_events` make lifecycle scope explicit. The plugin is alive only for its owning session, workflow, agent, runtime, or evaluator scope [source-12-claudecode-subagent-hooks-pluggability].
- `cleanup()` is part of the contract, not an afterthought. A plugin must unregister hooks, release leases or watchers, emit a cleanup event, and do so idempotently [source-12-claudecode-subagent-hooks-pluggability] [source-16-goal-managed-agent-protocol-spec].

### Concrete contract example: `EvaluatorProviderPlugin`
Evaluator providers should use the same `PermissionManifest`, `PluginManifest`, lifecycle, and cleanup skeleton so pluggability generalizes beyond runtime adapters. This is again a recommended from-scratch contract inferred from the framework, protocol, and testing strategy rather than a claimed existing API [source-15-goal-managed-agent-framework] [source-16-goal-managed-agent-protocol-spec] [source-17-goal-managed-agent-testing-strategy].

```ts
type EvaluatorProviderPlugin = {
  manifest: PluginManifest & {
    kind: 'evaluator_provider';
    scopes: Array<'workflow' | 'evaluator'>;
  };
  register(ctx: EvaluatorPluginContext): Promise<{
    evaluator_name: string;
    supported_check_types: Array<
      'test' | 'artifact' | 'benchmark' | 'human_review' | 'policy_review'
    >;
    hook_registrations: HookRegistration[];
  }>;
  createVerificationRun(req: VerificationRunRequest): Promise<{
    verification_run_id: string;
    planned_checks: EvidenceCheck[];
  }>;
  executeCheck(req: EvidenceCheckExecutionRequest): Promise<{
    check_id: string;
    status: 'passed' | 'failed' | 'waived' | 'needs_review';
    artifact_refs: ArtifactRef[];
    rationale?: string;
    metrics?: Record<string, number>;
  }>;
  summarize(run_id: string): Promise<{
    decision: 'accept' | 'reject' | 'needs_human_review';
    evidence_refs: ArtifactRef[];
    rationale: string;
  }>;
  cleanup(scope_id: string): Promise<{
    released_hooks: string[];
    released_temp_artifacts: string[];
  }>;
};
```

Why this matters:
- It proves the same typed plugin, lifecycle, permission, and cleanup model can govern evaluation, not just runtime launch.
- An evaluator plugin can request read-only filesystem, tool execution, or benchmark access through `permission_manifest` instead of receiving hidden carte blanche [source-11-claudecode-permission-governance] [source-17-goal-managed-agent-testing-strategy].
- `createVerificationRun()` and `executeCheck()` line up with the existing `EvidenceCheck` and `VerificationRun` concepts, so verification logic stays attached to explicit objects and evented state rather than ad hoc post-run callbacks [source-15-goal-managed-agent-framework] [source-16-goal-managed-agent-protocol-spec].
- `summarize()` can recommend acceptance or rejection, but it still stops short of silently closing a KR. Machine success alone is not enough when evaluator disagreement or missing evidence remains [source-17-goal-managed-agent-testing-strategy] [source-18-user-priority-correctness].
- `cleanup()` matters here too: temporary artifacts, watchers, and hook registrations must die with the evaluator scope so repeated verification runs do not leak state across workflows.

At the protocol level, plugin activation should also be evented: `plugin.register_requested`, `plugin.registered`, `plugin.activation_denied`, and `plugin.cleaned_up`. Conflict rules should be explicit: a plugin cannot register overlapping hook order inside the same scope without a priority decision; a broader-scope plugin may not override a narrower-scope `block`; activation should fail closed if required schemas are missing or if the permission manifest exceeds the current capability profile [source-11-claudecode-permission-governance] [source-16-goal-managed-agent-protocol-spec].

## 13. Correctness strategy
Correctness splits into two different problems [source-17-goal-managed-agent-testing-strategy] [source-18-user-priority-correctness].

1. Deterministic system correctness
- state transitions,
- hook precedence,
- permission policy,
- event-log replay,
- dedupe and orphan handling,
- approval semantics.

2. Probabilistic agent effectiveness
- clarification quality,
- KR drafting quality,
- task success,
- tool use,
- evidence sufficiency,
- cross-agent coordination.

The assurance stack should be:
- Layer 1: deterministic control-plane tests.
- Layer 2: protocol and recovery tests.
- Layer 3: offline evals on a versioned dataset.
- Layer 4: adversarial and fault-injection tests.
- Layer 5: online monitoring plus regular human review [source-17-goal-managed-agent-testing-strategy].

Best practices that matter most:
- every state transition should have positive and forbidden-transition tests,
- duplicate `complete` must not double-close a KR,
- late approval cannot silently resume superseded work,
- `block` must override `approve` when hook outputs conflict,
- datasets should start small but real, roughly `20-50` high-signal tasks,
- graders should prefer deterministic assertions first, structural assertions second, model-graded rubrics only when necessary, and human review for ambiguous cases,
- and real failures should be turned into future regression tests [source-14-pattern-extraction-memo] [source-17-goal-managed-agent-testing-strategy].

Operational cadence should also be explicit:
- per-commit: control-plane unit tests, protocol contract tests, hook precedence tests, policy-engine tests, and a tiny smoke eval suite,
- nightly: full offline eval suite, repeated reruns for consistency, adversarial subset, chaos tests for restart and recovery,
- pre-release: long-running scenario and soak tests, human transcript review sample, policy and audit export verification,
- post-release: production monitoring, canary rollout for runtime or model changes, and continuous failure harvesting back into the dataset [source-17-goal-managed-agent-testing-strategy].

## 14. Recovery and error-correction model
The system should correct mistakes by explicit state transitions, not by optimistic narration [source-16-goal-managed-agent-protocol-spec] [source-17-goal-managed-agent-testing-strategy].

Planning mistakes:
- if clarifications are missing, `block` and ask the user rather than launching work,
- if the objective changes, mark dependent tasks `stale_context` and require revalidation.

Execution mistakes:
- if a tool or shell appears interactive, detect the stall, kill it, and rerun with piped input or a non-interactive flag. Claude Code's watchdog evidence is concrete: it checks every `5` seconds, uses a `45` second threshold, inspects the tail of output, and looks for patterns such as `(y/n)`, `Press Enter`, `Continue?`, or directed questions [source-9-claudecode-source-inspection].
- if permissions are denied, move the task to blocked or superseded, surface the denial, and either narrow the request or wait for explicit operator change [source-11-claudecode-permission-governance].

Cross-agent mistakes:
- dedupe duplicate `complete` or `block` events,
- treat late results as `orphaned` if parent state moved on,
- prevent auto-merge after parent version change,
- reconstruct from the event log after restart,
- fail closed when lease, policy, or protocol state cannot be revalidated [source-16-goal-managed-agent-protocol-spec] [source-17-goal-managed-agent-testing-strategy].

Evaluator mistakes:
- a passed test suite does not equal KR completion,
- machine-human disagreement routes to review,
- the KR stays in `verifying` or `failed` until evidence and decisions align [source-15-goal-managed-agent-framework] [source-17-goal-managed-agent-testing-strategy].

## 15. End-to-end walkthrough: one OAuth2 KR through the full lifecycle
This is the proof burden the MVP must clear: can one real KR move through the entire governed loop without state ambiguity or hand-wavy recovery [source-8-user-followup] [source-9-claudecode-source-inspection] [source-16-goal-managed-agent-protocol-spec] [source-17-goal-managed-agent-testing-strategy].

1. Drafting: the user states the OAuth2 goal, the planning layer asks clarifying questions, and the KR is rejected until it becomes Specific, Measurable, Attainable, Relevant, and Time-bound.
2. Readiness preview: the system shows likely runtime, workspace scope, expected GitHub or filesystem approvals, evidence checks, and known blockers before any task is created.
3. Governed launch: once approved, the control plane creates `TaskExecution`, leases an isolated workspace, and launches the chosen runtime adapter under the declared capability profile.
4. Permission denial: the runtime hits a blocked credential or write action, emits an approval request, and the operator denies it. The system records the denial, moves the task to `blocked`, and avoids silent retry.
5. Replan: the planning layer narrows scope, perhaps keeping staging-only work active while production credential work becomes a separate approval-bearing KR. Parent and child versions are updated so stale work cannot auto-merge.
6. Resume: after the operator supplies the missing credential path or broader approval, the same child session is resumed through the runtime's `resume` path rather than restarted from scratch.
7. Completion claim: the child emits `complete` with artifact references, but the task moves only to `completed_claimed`; it is not yet done.
8. Evaluator verification: tests, artifact checks, and any required human or policy review run through `VerificationRun` and `EvidenceCheck` objects. Missing docs, failing logout tests, or policy review can still reject the claim.
9. Operator acceptance: the operator reviews the evidence bundle, remaining risk, and decision history, then accepts or rejects the KR. Objective progress updates only after this acceptance, not after agent self-report.
10. Recovery and audit: every transition is reconstructable from the event log. A restart, duplicate `complete`, or late approval can be replayed and resolved deterministically, with `orphaned` or `stale_context` states used instead of transcript guesswork.

If the product cannot make this single lifecycle legible, resumable, and reviewable, then more topic coverage or more agents will not save it.

## 16. Expansion path
Phase 1:
- one accountable owner,
- local structured store,
- append-only event log,
- markdown knowledge capture,
- local Codex and Claude adapters,
- plan approval, task board, approval inbox, evidence review [source-1-user-brief] [source-7-local-environment] [source-15-goal-managed-agent-framework].

Phase 2:
- GitHub read and limited write adapters with repo and branch scopes,
- filesystem authority with workspace and path scopes,
- worktree isolation,
- markdown export plus richer Obsidian sync [source-1-user-brief] [source-11-claudecode-permission-governance] [source-15-goal-managed-agent-framework].

Phase 3:
- org-managed policy layers,
- remote runtimes,
- compliance exports,
- multi-workspace governance,
- richer audit and portfolio views [source-5-multica-platform] [source-6-multica-daemon] [source-10-claudecode-broader-product-inspection].

Invariant across phases:
- the event log remains the source of truth,
- plugins remain scoped,
- completion remains evidence-backed,
- open source remains a pattern library rather than the product core [source-13-build-from-scratch-constraint].

## 17. Key risks and open questions
- Demand risk: the pain is real, but usage frequency at the full goal-managed level is not yet proven.
- UX risk: SMART KR authoring can turn into bureaucracy if clarification is not fast and preview-driven.
- Governance risk: approval fatigue can destroy flow if rules do not ratchet intelligently.
- Runtime risk: different agent runtimes expose different hook and resume guarantees.
- Eval risk: measuring true completion may be expensive or ambiguous outside code-heavy tasks.
- Org risk: larger organizations may want the audit and permission model but adopt more slowly than the early wedge.

## 18. Recommendation and rollout gates
Build the MVP, but keep the claim narrow:
- local-first,
- one accountable owner per objective,
- conversational planning into SMART KRs,
- daemon-backed execution with isolated workspaces,
- typed hooks and rule-based permissions,
- event-log-backed recovery,
- evidence-backed completion with an eval harness [source-8-user-followup] [source-12-claudecode-subagent-hooks-pluggability] [source-17-goal-managed-agent-testing-strategy] [source-18-user-priority-correctness].

Do not promise:
- full autonomy,
- org-wide deployment first,
- or correctness through a second judge model alone.

Phase-promotion criteria should stay metric-gated, not vibe-gated [source-17-goal-managed-agent-testing-strategy] [source-18-user-priority-correctness].

- Prototype -> pilot: deterministic state-machine, replay, policy, and protocol suites are green; approval precision and false-approve rate are measured on a versioned dataset; resume success and orphaned-completion rate are instrumented; cost or latency baselines exist for the top workflows.
- Pilot -> beta: offline eval consistency is stable across reruns; permission-request precision and false-block rate are tolerable; evaluator disagreement is low enough to review manually; blocked-on-user recovery plus stale-context handling behave correctly under restart and retry.
- Beta -> higher-authority rollout: canary monitoring shows no regression in approval precision, false-approve rate, resume success, orphaned-completion rate, evaluator disagreement, or cost or latency; audit exports and recent-denial recovery work; and managed rule layers are proven for GitHub and filesystem authority.

The product is worth building if it is framed as a governed goal-to-execution control plane, not as a magic manager replacement.
