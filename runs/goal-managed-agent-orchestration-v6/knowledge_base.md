# Knowledge Base

Topic: Goal-Managed Agent Orchestration with Conversational Planning, Governance, Pluggable Subagent Protocols, and Correctness Strategy

## Working thesis
- There is a real need here, but it is narrower than autonomy marketing. The user is asking to manage goals with less task babysitting while local agents handle bounded execution, and to escalate only when ambiguity, risk, or missing context appears [source-1-user-brief] [source-8-user-followup].
- The product is technically feasible now as a local-first control plane around existing local coding agents because the current surfaces already expose the core primitives we need: Codex SDK thread control through `startThread()`, `run(...)`, and `resumeThread(...)`; repo-local hook config in `.codex/hooks.json`; Claude Code `permissionDecision: defer` plus `claude -p --resume <session-id>`; and daemon-mediated local execution with isolated workspaces, heartbeats, and task polling [source-3-codex-capabilities] [source-4-claude-capabilities] [source-6-multica-daemon].
- The skeptical boundary remains: humans do not disappear. The system can reduce task micromanagement only if it owns clarification, approval, evidence review, and recovery semantics. It still needs humans for ambiguous goal formation, policy exceptions, destructive authority, and final acceptance when evidence is incomplete or conflicting [source-11-claudecode-permission-governance] [source-17-goal-managed-agent-testing-strategy] [source-18-user-priority-correctness].
- Larger organizations also matter. The same problem becomes more severe when coordination overhead, compliance, workspace scope, and auditability become harder. The first wedge can still be narrower, but the control-plane abstractions should be designed for a single accountable owner per objective in both small and large settings [source-5-multica-platform] [source-8-user-followup] [source-11-claudecode-permission-governance].

## 1. Demand reality
- Prompt-centric tooling breaks when work spans multiple dependent steps, approvals, and runtime interruptions. The user is not asking for better prompt authoring; they want preserved intent, local execution continuity, daemon-style routing, structured logs, and human escalation only when needed [source-1-user-brief].
- The local auto-research framework is evidence that once work becomes iterative, control-plane behavior matters as much as model output. The README-centered design uses a bounded `sources/` set, a mutable `knowledge_base.md`, fixed benchmark questions, `results.tsv`, keep or discard ratcheting, human feedback hot reload, and supervisor stop conditions. That is already a productized control loop, not just prompt text [source-2-auto-research-framework].
- Multica is the strongest comparable in the source set because it already exposes a managed-agent work surface with a Next.js frontend, Go backend, PostgreSQL plus pgvector, a local daemon, issue assignment, blockers, workspaces, execution history, and incremental run-message fetching. That does not prove goal-only management, but it does prove real demand for governed agent execution rather than raw chat [source-5-multica-platform] [source-6-multica-daemon].
- Decision: the need is real for local-agent power users and likely becomes more valuable, not less, as work requires approvals, blockers, and state continuity. What is not yet proven is a universal fully autonomous manager product.

## 2. Organization fit: solo, small team, larger organization
- Solo builders are the cleanest initial wedge because one person can act as the single accountable owner, answer clarifications quickly, and judge whether evidence is sufficient. The product saves them from turning each milestone into a pile of ad hoc prompts and manual follow-up [source-1-user-brief] [source-8-user-followup].
- Small teams benefit when an objective owner can mix human and agent work on the same board, see blockers, and review shared evidence. Multica's emphasis on assignments, blockers, reusable skills, and multi-workspace isolation is a signal that this middle layer is real product terrain already [source-5-multica-platform] [source-6-multica-daemon].
- Larger organizations matter because the same structure becomes more necessary under coordination overhead and compliance. Claude Code's permission model already implies the kind of maturity needed here: `PermissionRuleList` has distinct panels for recent denials, allow rules, ask rules, deny rules, and workspace directories; some rules are user-owned and deletable, others are managed and immutable. That is exactly the shape a larger-organization deployment would need [source-11-claudecode-permission-governance].
- The user is likely right that the durable unit is still one single accountable owner per objective. The difference is not whether large organizations need objective-driven execution; it is that they need stronger scoping, auditability, and policy layering before they can trust it [source-8-user-followup] [source-11-claudecode-permission-governance].

## 3. Conversational planning and SMART KR design
The system should turn ambiguity into executable work through a staged conversation, not a rigid form [source-8-user-followup] [source-9-claudecode-source-inspection] [source-10-claudecode-broader-product-inspection].

Suggested flow:
1. Capture the raw goal, why it matters, the deadline, and the operator of record.
2. Run a clarification pass on outcome, constraints, current assets, risk tolerance, permissions, dependencies, and what would count as proof.
3. Draft a short objective with owner, scope, success window, and excluded work.
4. Draft candidate SMART KRs. The local protocol spec already gives the right storage shape: each `KeyResult` carries `specific`, `measurable`, `attainable`, `relevant`, `time_bound`, `dependency_ids`, `evidence_contract_id`, and `version` [source-16-goal-managed-agent-protocol-spec].
5. Highlight gaps instead of pretending the first draft is ready. Ask follow-up questions until each KR is reasonably independent, permission-aware, and reviewable.
6. Show an execution-readiness preview with expected tools, workspaces, approvals, and evidence checks.
7. Require explicit approval before any runtime starts.

Claude Code is strong evidence that this has to be a first-class interaction design. `AskUserQuestionTool` is not plain chat text: it supports structured multiple-choice questions, preview mode, side-by-side option rendering, pasted images, and `shouldDefer: true` behavior when live user input is required. `EnterPlanModeTool` is a dedicated read-only stage that explicitly says to use `AskUserQuestion`, present the plan for approval, and avoid file edits until the plan is approved [source-9-claudecode-source-inspection].

After approval, work should become explicit runtime artifacts. `TaskCreateTool` creates tasks with `subject`, `description`, optional `activeForm`, and arbitrary `metadata`; `TaskGetTool` surfaces `status`, `blocks`, and `blockedBy`; `TaskUpdateTool` can update status, `addBlocks`, `addBlockedBy`, owner, and metadata. That is direct evidence that planning must feed a structured dependency-aware execution layer, not dissolve back into transcripts [source-9-claudecode-source-inspection].

## 4. Recursive KR to Objective structure and dependency rules
- A higher-level KR should become a child `Objective` only when satisfying it requires multiple subordinate KRs with their own evidence and review path. The object model in the local spec supports this explicitly through `parent_key_result_id`, per-KR `dependency_ids`, and independent `version` fields [source-8-user-followup] [source-16-goal-managed-agent-protocol-spec].
- Keep the hierarchy shallow and legible. Every child objective still needs one accountable owner, bounded scope, inherited intent from the parent KR, and a clear completion contract [source-15-goal-managed-agent-framework] [source-16-goal-managed-agent-protocol-spec].
- KRs should be independent by default. A dependency must be explicit, sparse, and reviewable. If many sibling KRs share mutable state or block one another, the plan is wrong and should be redrawn before execution [source-8-user-followup] [source-9-claudecode-source-inspection].
- When a parent objective or KR version changes, child executions should not silently merge back. The local spec's failure rules explicitly say a parent edit after spawn should mark work `stale_context`, and a late child `complete` after parent rescope becomes `orphaned` rather than mutating current state [source-16-goal-managed-agent-protocol-spec] [source-17-goal-managed-agent-testing-strategy].

## 5. What is technically feasible now
- Local execution is already real. Codex CLI runs locally, and the Codex SDK exposes `startThread()`, `run(...)`, and `resumeThread(...)`. Codex hooks are configured through `config.toml`, repo-local hooks can live in `.codex/hooks.json`, matching hooks receive JSON on stdin, and `Stop` hooks can continue the agent with a new prompt. The limitation is also concrete: current `PreToolUse` and `PostToolUse` interception is still Bash-focused and incomplete [source-3-codex-capabilities].
- Claude Code also exposes useful orchestration surfaces rather than only chat. `SessionStart` hooks can inject context, `CLAUDE_ENV_FILE` can persist environment variables for later Bash commands, `PreToolUse` can block or defer a tool call, `agent` hooks can spawn a subagent that returns a structured decision, `async` command hooks can run long tasks in the background, and non-interactive flows can pause with `permissionDecision: defer` and resume with `claude -p --resume <session-id>` [source-4-claude-capabilities].
- The current machine already has `codex-cli 0.118.0` and `Claude Code 2.1.100` installed, so the local runtime precondition is satisfied for a prototype [source-7-local-environment].
- Multica documents the clearest daemon pattern in the corpus. Its local daemon detects installed `claude` and `codex` CLIs, registers runtimes for watched workspaces, polls for claimed tasks, creates an isolated workspace directory for each task, spawns the agent CLI, streams results back, sends heartbeats, and deregisters runtimes on shutdown. The documented defaults are specific: poll interval `3s`, heartbeat interval `15s`, agent timeout `2h`, max concurrent tasks `20` [source-6-multica-daemon].
- Claude Code source inspection adds the missing product-state evidence. The system traces a dedicated `tool.blocked_on_user` span, treats plan approval as a distinct stage, models tasks and dependencies explicitly, and includes runtime recovery for blocked shell commands through a watchdog that checks every `5` seconds and uses a `45` second stall threshold before telling the model to kill and rerun a command non-interactively [source-9-claudecode-source-inspection].
- Build-from-scratch constraint: these are patterns to absorb, not framework dependencies to import. The runtime should use our own control-plane objects, event log, and protocol contracts even if adapters call existing CLIs [source-13-build-from-scratch-constraint].

Feasible now:
- conversational planning,
- local daemon plus local CLI execution,
- isolated workspace leasing,
- blocked on user and resume semantics,
- typed hooks,
- structured task and evidence state,
- human approval and evaluation loops.

Still speculative or risky:
- broad unattended cross-system automation,
- low-friction org-wide GitHub write authority,
- reliable business-judgment closure without human review,
- and large-scale multi-agent coordination without strong acceptance checks.

## 6. Why managing goals alone is still incomplete
A person cannot mostly manage goals unless the system also owns the layers underneath the goals [source-1-user-brief] [source-2-auto-research-framework] [source-15-goal-managed-agent-framework].

Those layers are:
- clarification and KR drafting,
- execution routing and workspace isolation,
- policy and approval,
- blocked-state handling,
- evaluation and evidence review,
- decision recording in an append-only event log.

The local protocol spec makes the gap concrete. `TaskExecution` has states such as `queued`, `starting`, `running`, `blocked`, `completed_claimed`, `failed`, `cancelled`, and `orphaned`. `completed_claimed` is deliberately not the same thing as done. `EvidenceCheck` can require `test`, `artifact`, `benchmark`, `human_review`, or `policy_review`, and a KR can close only after those checks pass or are explicitly waived [source-16-goal-managed-agent-protocol-spec].

Without those layers, goal management collapses back into prompt babysitting with better labels.

Human judgment remains essential for:
- ambiguous goal formation and tradeoffs,
- risky or destructive authority,
- credential provisioning and policy exceptions,
- evaluator disagreement,
- final acceptance when evidence is incomplete or conflicting [source-4-claude-capabilities] [source-11-claudecode-permission-governance] [source-17-goal-managed-agent-testing-strategy] [source-18-user-priority-correctness].

## 7. MVP architecture
The MVP should separate control plane, execution runtime, governance, evaluation, and operator surfaces from day one [source-15-goal-managed-agent-framework] [source-16-goal-managed-agent-protocol-spec].

Control plane:
- Owned objects: `Goal`, `Objective`, `KeyResult`, `EvidenceCheck`, `DecisionRecord`.
- Runtime objects: `TaskExecution`, `AgentSession`, `ApprovalRequest`, `WorkspaceLease`.
- `KeyResult` already has the right SMART and dependency fields in the local spec: `specific`, `measurable`, `attainable`, `relevant`, `time_bound`, `dependency_ids`, `evidence_contract_id`, `version` [source-16-goal-managed-agent-protocol-spec].

Execution runtime:
- `RuntimeAdapter` for Codex CLI and Claude CLI or SDK.
- `runtime-manager` to launch sessions, allocate workspaces, monitor liveness, and own `ResumeHandle` state [source-15-goal-managed-agent-framework].
- isolated workspace or worktree mode per task [source-6-multica-daemon] [source-12-claudecode-subagent-hooks-pluggability].

Governance:
- `PolicyEngine`, `PermissionRule`, `ApprovalRequest`, `HookRegistry` [source-15-goal-managed-agent-framework].
- explicit `allow`, `ask`, `deny` policy with scope by workspace, repo, path, branch, action, or tool [source-11-claudecode-permission-governance].

Evaluation:
- `EvaluatorRegistry`, `VerificationRun`, `CompletionDecision`, and evidence-backed closure [source-15-goal-managed-agent-framework] [source-17-goal-managed-agent-testing-strategy].

Storage:
- local structured store for owned objects,
- append-only event log for replay and audit,
- markdown export for knowledge capture,
- later adapters for GitHub and Obsidian, but not as core dependencies [source-1-user-brief] [source-13-build-from-scratch-constraint].

Operator API and UI:
- goal conversation,
- plan preview and approval,
- task board,
- session detail,
- approval inbox,
- evidence review,
- policy panel.

The event log should be explicit, not implied. The local spec already defines an `EventEnvelope` with `event_id`, `event_type`, `object_type`, `object_id`, optional `run_id`, `causation_id`, `correlation_id`, a stable `dedupe_key`, `actor`, `occurred_at`, and structured `payload`. That is the right source of truth for replay, audit, and recovery [source-16-goal-managed-agent-protocol-spec].

## 8. Why the center of gravity is UI and UX
Claude Code is strong evidence that the hard product work is not hidden backend scheduling. `AskUserQuestionTool` has previewable clarification, side-by-side options, and richer answer context. `EnterPlanModeTool` is a staged approval flow. `TaskCreateTool`, `TaskGetTool`, and `TaskUpdateTool` make dependencies explicit. `tool.blocked_on_user` is a traced runtime state. `LocalShellTask` ships a stall watchdog that looks for patterns such as `(y/n)`, `Press Enter`, `Continue?`, or directed questions and converts them into product-level recovery instructions [source-9-claudecode-source-inspection].

The broader product inspection strengthens the point. `TaskListV2` and `useTasksV2` sort tasks by status, keep blocked tasks behind unblocked pending work, surface active teammate ownership and recent activity, and hide recently completed tasks only after a short delay. `RemoteAgentTask` stores session IDs, titles, commands, logs, todo lists, remote metadata, review progress, and special phases such as `needs_input` and `plan_ready`. `scheduleRemoteAgents.ts` uses `AskUserQuestion` as the required first step unless explicit arguments are already present [source-10-claudecode-broader-product-inspection].

Therefore the MVP needs primary screens for:
- goal conversation with preview,
- objective and KR approval,
- dependency-aware task list,
- session detail with current tool activity and spawned agents,
- blocked on user inbox,
- approval and rule management,
- evidence review and verifier status.

If the operator must reconstruct system state from transcripts or raw logs, the product has failed at its main job.

## 9. Permission governance and approval UX
Permission governance should look like an operator product, not a hidden ACL file [source-11-claudecode-permission-governance].

Concrete source evidence:
- `PermissionRuleList` has tabs for recent denials, allow rules, ask rules, deny rules, and workspace directories.
- `interactiveHandler.ts` races approval sources from the local user, bridge or web surface, channel-based callbacks, and automated classifier checks, while recording decision source and timing.
- `BashPermissionRequest.tsx` includes destructive-command warnings, sandbox considerations, classifier-based auto-approval attempts, rule suggestions, and special handling for command patterns such as sed-based edits.
- `FilesystemPermissionRequest.tsx` extracts a concrete path when possible, routes the request through a dedicated file permission dialog, and distinguishes read versus write operations [source-11-claudecode-permission-governance].

Required model for our product:
- `allow`, `ask`, `deny` rules,
- scope by workspace, repo, branch, path, tool, and action,
- separate capability profiles for GitHub and filesystem authority,
- recent denials view so the system can learn from refusals and avoid repetitive prompts,
- immutable policy layers when rules come from managed settings, plus user-owned local exceptions [source-11-claudecode-permission-governance] [source-15-goal-managed-agent-framework].

Approval UX should show:
- exact requested action,
- reason code,
- affected workspace or path,
- blast radius,
- expiry,
- related objective or KR,
- whether this can become a reusable rule.

Default stance:
- discovery can be broader,
- write actions should usually be `ask`,
- destructive actions should lean `deny` unless explicitly elevated,
- denials should force replanning or a narrower request rather than silent retries [source-6-multica-daemon] [source-7-local-environment] [source-11-claudecode-permission-governance].

## 10. Subagent protocol
Subagents must be a protocol, not a convenience helper [source-12-claudecode-subagent-hooks-pluggability] [source-16-goal-managed-agent-protocol-spec].

Required pieces:
- mode: `fork`, `fresh`, `worktree`, `remote`, `teammate`.
- context contract: immutable goal scope, filtered or summarized history, cloned mutable runtime state by default, explicitly shared callbacks only when required.
- communication contract: typed channels for notification, direct message, approval, resume, and event streaming.
- lifecycle policy: timeout, retry budget, stall policy, orphan policy.
- protocol actions: `spawn`, `ack`, `block`, `resume`, `complete`, `cancel`.

Important Claude Code lessons:
- `AgentTool.tsx` routes into regular subagents, implicit forks, background local agents, worktree-isolated agents, remote agents, and teammate or squad-style agents [source-12-claudecode-subagent-hooks-pluggability].
- `runAgent.ts` and `forkedAgent.ts` build child context deliberately. Normal subagents are seeded with `forkContextMessages + promptMessages`; incomplete parent tool calls are filtered out; `createSubagentContext()` clones mutable state by default; `readFileState` is cloned; content-replacement state is cloned for prompt-cache stability; a fresh async-local `agentContext` is created; only selected callbacks are shared back [source-12-claudecode-subagent-hooks-pluggability].
- `forkSubagent.ts` is not just generic inheritance. It can trigger an implicit fork when `subagent_type` is omitted, the child inherits the parent's rendered system prompt bytes, reuses the parent's tool pool and thinking config, and uses a byte-stable conversation prefix for prompt-cache reuse [source-12-claudecode-subagent-hooks-pluggability].
- Parent and child communication already uses multiple explicit paths. `LocalAgentTask` writes task output, records messages, and enqueues task notifications; `resumeAgent.ts` reconstructs transcript state, content-replacement state, and worktree path; `SendMessageTool.ts` and `teammateMailbox.ts` implement file-backed inboxes for direct, broadcast, structured, and control messages such as plan approval or task assignment [source-12-claudecode-subagent-hooks-pluggability].

Our protocol should formalize those lessons. The local spec's `SpawnRequest` already names the right fields: `protocol_id`, `task_execution_id`, `mode`, `context_contract`, `capability_profile`, `communication_contract.channels`, and `lifecycle_policy` with `timeout_seconds`, `max_retries`, `stall_policy`, and `orphan_policy` [source-16-goal-managed-agent-protocol-spec].

Design rule: parent-child coordination should ride a typed message bus and event log. Transcript text may be inspectable evidence, but never the source of truth.

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

Hook outputs are concrete, not metaphorical. Claude Code's hook types can block or approve, change tool input, inject additional context, retry denied operations, alter MCP tool output, request or answer permission decisions, add watched paths, and stop continuation with an explicit reason. Codex adds another useful signal: matching hooks can run concurrently, commands receive JSON on stdin, and `Stop` hooks can continue the agent with a new prompt [source-3-codex-capabilities] [source-12-claudecode-subagent-hooks-pluggability].

The local protocol spec gives the right deterministic wrapper around those capabilities. `HookRegistration` includes `scope`, `event`, `order`, `timeout_ms`, `failure_policy`, `mode`, `input_schema_ref`, and `output_schema_ref`. Merge rules are explicit: `block` overrides `approve`; `stop_continuation` is terminal for that boundary; `updated_input` is valid only before execution starts; retries consume budget and must emit an event [source-16-goal-managed-agent-protocol-spec].

Critical caveat: hooks are not enough on their own. Source-3 states that current Codex `PreToolUse` and `PostToolUse` interception is still incomplete and Bash-focused, so the control plane still needs its own policy engine and approval state. Hooks should be treated as typed lifecycle boundaries, not the whole governance story [source-3-codex-capabilities].

## 12. Pluggability model
The framework should expose scoped, typed extension surfaces rather than one global callback table [source-12-claudecode-subagent-hooks-pluggability] [source-15-goal-managed-agent-framework].

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
- Claude Code's permission model implies that plugin authority also needs governance. Rules can be user-owned or managed, so plugins should declare the permissions they require and which rules they expect to interact with [source-11-claudecode-permission-governance].

Each plugin should declare:
- scope and lifecycle,
- schemas,
- permissions it requires,
- conflict rules,
- failure policy,
- cleanup behavior.

Session-scoped registration is the key pattern to copy. It keeps a skill or agent extension alive only for the owning session or workflow, which prevents silent global callback chaos [source-12-claudecode-subagent-hooks-pluggability].

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

Source-level best practices are specific:
- every state transition should have positive and forbidden-transition tests,
- duplicate `complete` must not double-close a KR,
- late approval cannot silently resume superseded work,
- `block` must override `approve` when hook outputs conflict [source-17-goal-managed-agent-testing-strategy].
- datasets should start small but real, roughly `20-50` high-signal tasks, each with input context, exact goal, success conditions, constraints, expected evidence, grader instructions, and a reference solution when possible [source-17-goal-managed-agent-testing-strategy].
- graders should prefer deterministic assertions first, structural assertions second, model-graded rubrics only when necessary, and human review for ambiguous cases [source-17-goal-managed-agent-testing-strategy].
- the pattern memo adds another important constraint: turn real failures into future tests, keep versioned datasets, and measure consistency across reruns rather than celebrating one-off hero runs [source-14-pattern-extraction-memo] [source-17-goal-managed-agent-testing-strategy].

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
- if a tool or shell appears interactive, detect the stall, kill it, and rerun with piped input or a non-interactive flag. Claude Code's watchdog evidence is unusually concrete: it checks every `5` seconds, uses a `45` second threshold, inspects the tail of output, and looks for patterns such as `(y/n)`, `Press Enter`, `Continue?`, or directed questions [source-9-claudecode-source-inspection].
- if permissions are denied, move the task to blocked or superseded, surface the denial, and either narrow the request or wait for explicit operator change [source-11-claudecode-permission-governance].

Cross-agent mistakes:
- dedupe duplicate `complete` or `block` events,
- treat late results as orphaned if parent state moved on,
- prevent auto-merge after parent version change,
- reconstruct from the event log after restart,
- fail closed when lease, policy, or protocol state cannot be revalidated [source-16-goal-managed-agent-protocol-spec] [source-17-goal-managed-agent-testing-strategy].

The local protocol spec already names the exact recovery rules:
- `resume` is valid only for blocked or disconnected child state,
- late `complete` after KR supersession becomes `orphaned`,
- duplicate events are accepted once and later duplicates are recorded without replaying side effects,
- late approvals require explicit reattachment before resuming work,
- restart recovery must reconstruct from objects plus event log rather than transcript tailing [source-16-goal-managed-agent-protocol-spec].

Evaluator mistakes:
- a passed test suite does not equal KR completion,
- machine-human disagreement routes to review,
- the KR stays in `verifying` or `failed` until evidence and decisions align [source-15-goal-managed-agent-framework] [source-17-goal-managed-agent-testing-strategy].

## 15. Expansion path
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

## 16. Key risks and open questions
- Demand risk: the pain is real, but usage frequency at the full goal-managed level is not yet proven.
- UX risk: SMART KR authoring can turn into bureaucracy if clarification is not fast and preview-driven.
- Governance risk: approval fatigue can destroy flow if rules do not ratchet intelligently.
- Runtime risk: different agent runtimes expose different hook and resume guarantees.
- Eval risk: measuring true completion may be expensive or ambiguous outside code-heavy tasks.
- Org risk: larger organizations may want the audit and permission model but move more slowly than the early wedge.

## 17. Recommendation
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

The product is worth building if it is framed as a governed goal-to-execution control plane, not as a magic manager replacement.
