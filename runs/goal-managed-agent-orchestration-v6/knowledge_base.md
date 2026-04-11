# Knowledge Base

Topic: Goal-Managed Agent Orchestration with Conversational Planning, Governance, Pluggable Subagent Protocols, and Correctness Strategy

## Executive Decision Brief
- Build this as a local-first governed control plane: conversational planning turns vague goals into SMART KRs, typed runtimes execute bounded work, an operator cockpit handles approvals and blocked states, and completion stays evidence-backed from day one. Do not sell it as full autonomy [source-1-user-brief] [source-8-user-followup] [source-15-goal-managed-agent-framework] [source-17-goal-managed-agent-testing-strategy].
- The real pain is not prompt quality. It is carrying intent, dependencies, approvals, blockers, and evidence across multi-step work without dropping state or replaying the same human judgment over and over [source-1-user-brief] [source-2-auto-research-framework].
- Larger organizations matter even if the first wedge is narrower, because coordination overhead, compliance, and authority scoping get worse as more repos, workspaces, reviewers, and policy layers enter the loop. The invariant across solo, small-team, and larger-organization use is a single accountable owner per objective [source-5-multica-platform] [source-8-user-followup] [source-11-claudecode-permission-governance].
- The next proof burden is not more topic coverage. It is proving that one real KR can move cleanly through clarification, readiness preview, governed launch, permission denial, replan, resume, completion claim, evaluator verification, operator acceptance, and recovery or audit without state ambiguity [source-8-user-followup] [source-9-claudecode-source-inspection] [source-16-goal-managed-agent-protocol-spec] [source-17-goal-managed-agent-testing-strategy].
- Authority should widen only behind metric gates: approval precision, false-approve rate, false-block rate, resume success, orphaned-completion rate, evaluator disagreement, and cost or latency baselines should decide when GitHub or filesystem authority expands [source-11-claudecode-permission-governance] [source-17-goal-managed-agent-testing-strategy] [source-18-user-priority-correctness].

## 1. Working thesis
- There is a real need here, but it is narrower than autonomy marketing. The product is valuable when work is too long-lived and stateful for prompt-by-prompt babysitting, not because users want humans removed from judgment entirely [source-1-user-brief] [source-2-auto-research-framework].
- The direction is technically feasible now because current local agents already expose the needed surfaces: Codex has local CLI execution, SDK thread control with `startThread()`, `run(...)`, and `resumeThread(...)`, plus repo-local hooks; Claude Code has `permissionDecision: defer`, `claude -p --resume`, typed hooks, and subagent or async hook patterns; Multica proves the daemon-mediated remote-to-local runtime shape [source-3-codex-capabilities] [source-4-claude-capabilities] [source-6-multica-daemon].
- Open source should be treated as a reference corpus for durable mechanisms and failure patterns, not as our runtime dependency. The control plane, protocol, policy engine, and evaluator model should be built from scratch around our own object model and event log [source-13-build-from-scratch-constraint] [source-14-pattern-extraction-memo] [source-15-goal-managed-agent-framework].
- Humans remain essential for ambiguous goal formation, risky authority, policy exceptions, and final acceptance when evidence is incomplete or evaluators disagree [source-11-claudecode-permission-governance] [source-17-goal-managed-agent-testing-strategy] [source-18-user-priority-correctness].

## 2. Demand reality
- Prompt-centric tooling fails when work spans multiple dependent steps, approvals, interruptions, and evidence review. The demand is to reduce task babysitting, not to make one-shot prompts more eloquent [source-1-user-brief].
- The local `auto-research` framework is direct evidence that once work becomes iterative, control-plane behavior becomes product behavior: bounded `sources/`, mutable `knowledge_base.md`, fixed benchmark questions, keep-or-discard ratchet, human feedback hot reload, supervisor stop conditions, and audit artifacts all matter as much as model output [source-2-auto-research-framework].
- Multica is the strongest comparable in the corpus because it already exposes assignments, blockers, multi-workspace isolation, a daemon, execution history, and incremental run-message fetching. That proves demand for governed agent execution, even though it does not prove people can live at goal level alone [source-5-multica-platform] [source-6-multica-daemon].
- Decision: the need is real for power users now and likely grows with coordination complexity. The unresolved question is not whether governed execution is useful; it is whether a mostly-goal-management workflow can stay legible and efficient enough to become habitual [source-1-user-brief] [source-5-multica-platform] [source-17-goal-managed-agent-testing-strategy].

## 3. Organization fit: solo wedge, larger-organization relevance
- Solo builders are the cleanest first wedge because one person can answer clarifications quickly, approve low-risk actions with low latency, and judge whether an evidence bundle is sufficient [source-1-user-brief] [source-8-user-followup].
- Small teams benefit when one objective owner can mix human and agent work on the same board, see blockers, and review shared evidence. Multica's emphasis on blockers, reusable skills, and workspace isolation is evidence that this middle layer is already real product terrain [source-5-multica-platform] [source-6-multica-daemon].
- Larger organizations also matter because the same workflow becomes more valuable when coordination overhead, compliance, and permission governance get harder. Claude Code's rule panels already imply the right maturity model: separate recent denials, allow rules, ask rules, deny rules, and workspace directories, with user-owned versus managed policy layers [source-8-user-followup] [source-11-claudecode-permission-governance].
- The invariant across all three is one single accountable owner per objective. The difference is not whether objective-driven execution matters; it is how much governance, auditability, and approval routing must sit around it [source-8-user-followup] [source-11-claudecode-permission-governance].

## 4. Conversational planning into SMART KRs
The system should turn ambiguity into executable work through a staged conversation, not a rigid form [source-8-user-followup] [source-9-claudecode-source-inspection] [source-10-claudecode-broader-product-inspection].

Planning flow:
1. Capture the raw goal, why it matters, deadline, owner, and excluded work.
2. Ask clarifying questions about outcome, constraints, current assets, permissions, dependencies, risk tolerance, and what would count as proof.
3. Draft a short objective with scope, owner, success window, and non-goals.
4. Draft candidate SMART KRs. The protocol draft gives the right storage shape: each `KeyResult` carries `specific`, `measurable`, `attainable`, `relevant`, `time_bound`, `dependency_ids`, `evidence_contract_id`, and `version` [source-16-goal-managed-agent-protocol-spec].
5. Mark missing SMART properties or hidden coupling explicitly. A KR should not progress while it is vague, unmeasurable, or too entangled with siblings.
6. Show an execution-readiness preview listing likely runtimes, workspace scope, approvals, evidence checks, and known blockers.
7. Require explicit approval before any runtime starts.

Worked OAuth2 example:
- Raw goal: `Move the app from ad hoc session middleware to OAuth2 before launch review` [source-8-user-followup].
- The system should reject `switch auth to OAuth2` as not Specific, not Measurable, and not Time-bound, then ask clarifying questions about scope, identity provider, deadline, rollback needs, and required evidence [source-8-user-followup] [source-9-claudecode-source-inspection].
- A stronger objective is: `Ship OAuth2-based authentication for API and admin routes without breaking existing user access before launch review.`
- A stronger KR set is: staging auth flow passes contract tests; secrets and callback URLs exist with rollback docs; operator reviews a final evidence bundle before production rollout. KRs should be reasonably independent by default [source-8-user-followup] [source-16-goal-managed-agent-protocol-spec].

Claude Code is strong evidence that this must be a first-class interaction design problem. `AskUserQuestionTool` supports structured choices, preview mode, side-by-side option rendering, and `shouldDefer: true`; `EnterPlanModeTool` is a dedicated read-only stage that says to clarify, present the plan for approval, and avoid file edits until approval [source-9-claudecode-source-inspection].

## 5. Recursive KR -> Objective decomposition and dependency rules
- A higher-level `KeyResult` should become a child `Objective` only when satisfying it requires multiple subordinate KRs with their own evidence and review path. The object model already supports this through `parent_key_result_id`, per-KR `dependency_ids`, and independent `version` fields [source-8-user-followup] [source-16-goal-managed-agent-protocol-spec].
- Keep the hierarchy shallow and legible. Every child objective still needs one accountable owner, bounded scope, inherited intent from the parent KR, and a clear completion contract [source-15-goal-managed-agent-framework] [source-16-goal-managed-agent-protocol-spec].
- KRs should be independent by default. Dependencies must be sparse, explicit, and reviewable. If many sibling KRs block one another or mutate the same state, the plan is wrong and should be redrawn before execution [source-8-user-followup] [source-9-claudecode-source-inspection].
- Parent edits must not silently merge back into child work. The protocol rules say a parent edit after spawn should mark work `stale_context`, and a late child `complete` after parent rescope becomes `orphaned` rather than mutating current state [source-16-goal-managed-agent-protocol-spec] [source-17-goal-managed-agent-testing-strategy].

## 6. What is technically feasible now
- Codex already supports the core local path: local CLI execution, SDK thread control through `startThread()`, `run(...)`, and `resumeThread(...)`, repo-local hooks in `.codex/hooks.json`, JSON over stdin, concurrent hook matching, and `Stop` hooks that can continue the agent with a new prompt. The limitation is explicit: current `PreToolUse` and `PostToolUse` interception is still Bash-focused and incomplete [source-3-codex-capabilities].
- Claude Code exposes the missing human-escalation surfaces: `SessionStart` hooks for context injection, `CLAUDE_ENV_FILE` for persisted environment, `PreToolUse` hooks that can block or defer, `agent` hooks that can spawn a subagent and return a structured decision, `async` command hooks for long tasks, and non-interactive pause or resume through `permissionDecision: defer` plus `claude -p --resume <session-id>` [source-4-claude-capabilities].
- The current machine already has `codex-cli 0.118.0` and `Claude Code 2.1.100`, so the local-runtime precondition is satisfied for a prototype [source-7-local-environment].
- Multica documents the clearest daemon pattern in the corpus: detect installed CLIs, register runtimes for watched workspaces, poll for claimed tasks, create an isolated workspace directory for each task, spawn the local CLI, stream results back, send heartbeats, and deregister on shutdown. Its defaults are concrete: `3s` poll, `15s` heartbeat, `2h` timeout, `20` max concurrent tasks [source-6-multica-daemon].
- Claude Code source inspection adds the product-state evidence missing from docs alone: a dedicated `tool.blocked_on_user` span, structured task and dependency objects, and blocked-shell recovery through a watchdog that checks every `5` seconds, uses a `45` second threshold, and tells the model to rerun interactive commands non-interactively [source-9-claudecode-source-inspection].

Feasible now:
- conversational planning,
- local daemon plus local CLI execution,
- isolated workspace or worktree leasing,
- blocked-on-user and resume semantics,
- typed hooks,
- structured task and evidence state,
- human approval and evaluation loops.

Still risky or speculative:
- broad unattended cross-system automation,
- low-friction org-wide GitHub write authority,
- reliable business-judgment closure without human review,
- and large-scale multi-agent coordination without strong acceptance checks [source-3-codex-capabilities] [source-4-claude-capabilities] [source-17-goal-managed-agent-testing-strategy].

## 7. MVP architecture
Goal management alone is incomplete. The MVP needs an explicit control plane, execution runtime, governance layer, evaluation loop, storage model, and operator surfaces from day one [source-2-auto-research-framework] [source-15-goal-managed-agent-framework] [source-16-goal-managed-agent-protocol-spec].

Owned objects:
- `Goal`
- `Objective`
- `KeyResult`
- `EvidenceCheck`
- `DecisionRecord`

Runtime objects:
- `TaskExecution`
- `AgentSession`
- `ApprovalRequest`
- `WorkspaceLease`

Control-plane services:
- planning service: `PlanningSession`, `ClarificationPrompt`, `PlanPreview`, `DependencyGraph`, `ExecutionReadinessCheck`
- runtime manager: `RuntimeAdapter`, `ResumeHandle`, workspace allocation, liveness, artifact collection
- governance: `PolicyEngine`, `PermissionRule`, `HookRegistry`, decision recording
- evaluation: `EvaluatorRegistry`, `VerificationRun`, `CompletionDecision`
- storage: local structured store plus append-only `EventEnvelope` log with `event_id`, `event_type`, `object_type`, `object_id`, `correlation_id`, `dedupe_key`, `actor`, `occurred_at`, and structured payload [source-15-goal-managed-agent-framework] [source-16-goal-managed-agent-protocol-spec].

Implementation rules:
- `TaskExecution` exists only to satisfy a `KeyResult`.
- `AgentSession` exists only to satisfy a `TaskExecution`.
- `completed_claimed` is not done; it must route into verification.
- transcripts may be stored, but they are never the primary state container [source-16-goal-managed-agent-protocol-spec].

## 8. Why the center of gravity is UI/UX
Claude Code is strong evidence that the hard product work is not hidden scheduling. `AskUserQuestionTool` gives previewable clarification, `EnterPlanModeTool` creates a staged approval flow, `TaskCreateTool`, `TaskGetTool`, and `TaskUpdateTool` make dependencies explicit, `tool.blocked_on_user` is traced as a first-class runtime state, and `LocalShellTask` ships a stall watchdog for blocked-command recovery [source-9-claudecode-source-inspection].

The broader product inspection strengthens the point. `TaskListV2` and `useTasksV2` surface persistent status and blockers; `RemoteAgentTask` stores session IDs, logs, todo lists, remote metadata, and phases such as `needs_input` and `plan_ready`; `scheduleRemoteAgents.ts` uses `AskUserQuestion` as the required first step unless explicit arguments are already present [source-10-claudecode-broader-product-inspection].

The MVP therefore needs primary screens for:
- goal conversation with preview,
- objective and KR approval,
- dependency-aware task list,
- session detail with current activity and spawned agents,
- blocked-on-user inbox,
- approval and rule management,
- evidence review and verifier status.

If the operator must reconstruct state from transcripts or raw logs, the product has failed at its main job [source-9-claudecode-source-inspection] [source-10-claudecode-broader-product-inspection].

## 9. Permission governance and approval UX
Permission governance should look like an operator product, not a hidden ACL file [source-11-claudecode-permission-governance].

Concrete source evidence:
- `PermissionRuleList` has tabs for recent denials, allow rules, ask rules, deny rules, and workspace directories.
- `interactiveHandler.ts` races approval sources from the local user, bridge or web surface, channel-based callbacks, and automated classifier checks while recording decision source and timing.
- `BashPermissionRequest.tsx` includes destructive-command warnings, sandbox considerations, classifier-based auto-approval attempts, and reusable rule suggestions.
- `FilesystemPermissionRequest.tsx` extracts a concrete path when possible, routes through a dedicated file dialog, and distinguishes read versus write operations [source-11-claudecode-permission-governance].

Required model for our product:
- `allow`, `ask`, `deny` rules,
- scope by workspace, repo, branch, path, tool, and action,
- separate capability profiles for GitHub and filesystem authority,
- recent-denials view so the system can learn from refusals and avoid repetitive prompts,
- immutable managed policy layers plus user-owned local exceptions [source-11-claudecode-permission-governance] [source-15-goal-managed-agent-framework].

Approval UX should show the requested action, reason code, affected workspace or path, blast radius, expiry, related objective or KR, and whether the decision can become a reusable rule. Discovery can be broader, write actions should usually be `ask`, destructive actions should lean `deny` unless explicitly elevated, and denials should force replanning or a narrower request rather than silent retry [source-6-multica-daemon] [source-7-local-environment] [source-11-claudecode-permission-governance].

## 10. Subagent protocol
Subagents must be a protocol, not a convenience helper [source-12-claudecode-subagent-hooks-pluggability] [source-16-goal-managed-agent-protocol-spec].

Required contract:
- modes: `fork`, `fresh`, `worktree`, `remote`, `teammate`
- context contract: immutable goal scope, filtered or summarized history, cloned mutable runtime state by default, explicitly shared callbacks only when required
- communication contract: typed channels for `notification`, `message`, `approval`, `resume`, and `event_stream`
- lifecycle policy: timeout, retry budget, stall policy, orphan policy
- protocol actions: `spawn`, `ack`, `block`, `resume`, `complete`, `cancel`

Claude Code lessons that should become design rules:
- `AgentTool.tsx` routes into regular subagents, implicit forks, background local agents, worktree-isolated agents, remote agents, and teammate-style agents. The product surface says `launch an agent`, but the runtime is selecting among multiple isolation modes [source-12-claudecode-subagent-hooks-pluggability].
- `runAgent.ts`, `forkedAgent.ts`, and `createSubagentContext()` show explicit context construction: filtered history, cloned `readFileState`, cloned mutable state, byte-stable fork prefixes, and only selected shared callbacks [source-12-claudecode-subagent-hooks-pluggability].
- Parent-child communication already uses multiple explicit paths: `LocalAgentTask` notifications, `resumeAgent.ts`, and file-backed inboxes through `SendMessageTool.ts` and `teammateMailbox.ts`. The right abstraction is a typed message bus, not transcript scraping [source-10-claudecode-broader-product-inspection] [source-12-claudecode-subagent-hooks-pluggability].
- The local spec's `SpawnRequest` already names the core fields: `protocol_id`, `task_execution_id`, `mode`, `context_contract`, `capability_profile`, `communication_contract.channels`, and `lifecycle_policy` [source-16-goal-managed-agent-protocol-spec].

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

Hook outputs are concrete, not metaphorical. Claude Code's hook types can `block` or approve, change tool input, inject `additional_context`, retry denied operations, alter MCP output, request permission decisions, add watched paths, and stop continuation with an explicit reason. Codex adds two useful constraints: matching hooks can run concurrently, and `Stop` hooks can continue the agent with a new prompt [source-3-codex-capabilities] [source-12-claudecode-subagent-hooks-pluggability].

The protocol draft gives the right deterministic wrapper: each `HookRegistration` needs `scope`, `event`, `order`, `timeout_ms`, `failure_policy`, `mode`, `input_schema_ref`, and `output_schema_ref`. Merge rules must be explicit: `block` overrides `approve`; `stop_continuation` is terminal; `updated_input` is valid only before execution; retries consume budget and emit events [source-16-goal-managed-agent-protocol-spec].

Critical caveat: hooks are not the whole governance story. Source 3 says current Codex `PreToolUse` and `PostToolUse` interception is incomplete and Bash-focused, so the control plane still needs its own policy engine and approval state [source-3-codex-capabilities].

## 12. Pluggability model
The framework should expose scoped, typed extension surfaces rather than one global callback table, and the same lifecycle skeleton should govern runtime launch plugins and evaluator plugins [source-12-claudecode-subagent-hooks-pluggability] [source-15-goal-managed-agent-framework] [source-16-goal-managed-agent-protocol-spec].

Recommended plugin kinds:
- runtime adapters
- hook packages
- evaluator providers
- context assemblers
- policy providers
- export sinks
- skill packs for planning or execution templates

Recommended scopes:
- `session`
- `workflow`
- `agent`
- `runtime`
- `evaluator`

Mandatory manifest fields:
- plugin id and version
- kind and supported scopes
- activation and disposal events
- typed input and output schema refs
- permission manifest for filesystem, GitHub, tools, and escalation-required actions
- cleanup contract with idempotency, timeout, emitted cleanup event, and failure policy [source-11-claudecode-permission-governance] [source-12-claudecode-subagent-hooks-pluggability] [source-16-goal-managed-agent-protocol-spec].

Minimum runtime-adapter plugin contract:
- `register()` returns adapter name and hook registrations
- `launch()` returns `session_id` and optional `resume_handle`
- `resume()` re-enters the same logical session
- `stop()` ends the session with a reason code
- `collectArtifacts()` returns reviewable outputs
- `cleanup()` unregisters hooks and releases leases

Minimum evaluator-provider plugin contract:
- `register()` declares supported check types
- `createVerificationRun()` plans checks against `EvidenceCheck`
- `executeCheck()` returns `passed`, `failed`, `waived`, or `needs_review` with artifacts and metrics
- `summarize()` recommends `accept`, `reject`, or `needs_human_review`
- `cleanup()` removes temp artifacts and scope-bound hooks [source-15-goal-managed-agent-framework] [source-16-goal-managed-agent-protocol-spec] [source-17-goal-managed-agent-testing-strategy].

Why lifecycle scoping matters: Claude Code's `registerFrontmatterHooks.ts` registers session-scoped hooks and cleans them up with the session or subagent lifecycle. That is the antidote to global callback chaos [source-12-claudecode-subagent-hooks-pluggability].

## 13. Correctness strategy, testing, and metrics
Correctness splits into two different problems [source-17-goal-managed-agent-testing-strategy] [source-18-user-priority-correctness].

1. Deterministic system correctness:
- state transitions,
- hook precedence,
- permission policy,
- event-log replay,
- dedupe and orphan handling,
- approval semantics.

2. Probabilistic agent effectiveness:
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
- prefer deterministic assertions first, structural assertions second, model-graded rubrics only when necessary, and human review for ambiguous cases
- make every state transition have positive and forbidden-transition tests
- version datasets and graders
- rerun critical cases to measure consistency, not just `pass@1`
- turn real failures into new regression tests [source-14-pattern-extraction-memo] [source-17-goal-managed-agent-testing-strategy] [source-18-user-priority-correctness].

Metrics that should gate rollout:
- task success rate
- consistency across reruns
- false-approve rate
- false-block rate
- permission-request precision
- retry rate
- resume success rate
- orphaned-completion rate
- evaluator disagreement rate
- cost per successful task
- latency to successful task [source-17-goal-managed-agent-testing-strategy].

## 14. Recovery and error-correction model
The system should correct mistakes by explicit state transitions, not optimistic narration [source-16-goal-managed-agent-protocol-spec] [source-17-goal-managed-agent-testing-strategy].

The local protocol spec should lock in five recovery rules clearly:
1. Resume validity: `resume` is valid only for blocked or disconnected child state.
2. Late complete -> `orphaned`: a `complete` that arrives after parent state moved on becomes an `orphaned` result, not a silent merge.
3. Duplicate event handling: accept the first transition, record later duplicates, and never replay side effects.
4. Late approval reattachment: a late approval is recorded, but it cannot silently reopen work; explicit reattachment to current state is required.
5. Restart reconstruction: rebuild state from owned objects plus the append-only event log; if lease or protocol state cannot be safely revalidated, fail closed [source-16-goal-managed-agent-protocol-spec].

Planning mistakes:
- if clarifications are missing, `block` and ask the user rather than launching work
- if the objective changes, mark dependent tasks `stale_context` and require revalidation [source-15-goal-managed-agent-framework] [source-16-goal-managed-agent-protocol-spec].

Execution mistakes:
- if a tool or shell appears interactive, detect the stall, kill it, and rerun with piped input or a non-interactive flag; Claude Code's watchdog evidence is concrete here [source-9-claudecode-source-inspection]
- if permissions are denied, move the task to blocked or superseded, surface the denial, and either narrow the request or wait for explicit operator change [source-11-claudecode-permission-governance].

Cross-agent mistakes:
- dedupe duplicate `complete` or `block` events
- route retries through an explicit retry budget
- prevent auto-merge after parent version change
- reconstruct from the event log after restart
- fail closed when lease, policy, or protocol state cannot be revalidated [source-16-goal-managed-agent-protocol-spec] [source-17-goal-managed-agent-testing-strategy].

Evaluator mistakes:
- a passed test suite does not equal KR completion
- machine-human disagreement routes to review
- the KR stays in `verifying` or moves to `failed` until evidence and decisions align [source-15-goal-managed-agent-framework] [source-17-goal-managed-agent-testing-strategy].

## 15. End-to-end walkthrough: one OAuth2 KR through the full lifecycle
This is the proof burden the MVP must clear: can one real KR move through the entire governed loop without state ambiguity or hand-wavy recovery [source-8-user-followup] [source-9-claudecode-source-inspection] [source-16-goal-managed-agent-protocol-spec] [source-17-goal-managed-agent-testing-strategy].

1. Drafting: the user states the OAuth2 goal; the planning layer asks clarifying questions; the KR is rejected until it becomes Specific, Measurable, Attainable, Relevant, and Time-bound.
2. Readiness preview: the system shows likely runtime, workspace scope, expected approvals, evidence checks, and known blockers before any task is created.
3. Governed launch: once approved, the control plane creates `TaskExecution`, leases an isolated workspace, and launches the runtime adapter under the declared capability profile.
4. Permission denial: the runtime hits a blocked credential or write action, emits an approval request, and the operator denies it. The system records the denial, moves the task to `blocked`, and avoids silent retry.
5. Replan: the planning layer narrows scope, perhaps keeping staging-only work active while production credential work becomes a separate approval-bearing KR. Parent and child versions are updated so stale work cannot auto-merge.
6. Resume: after the operator supplies the missing credential path or broader approval, the same child session resumes through the runtime's resume path rather than restarting from scratch.
7. Completion claim: the child emits `complete` with artifact references, but the task moves only to `completed_claimed`; it is not yet done.
8. Evaluator verification: tests, artifact checks, and any required human or policy review run through `VerificationRun` and `EvidenceCheck` objects. Missing docs, failing logout tests, or policy review can still reject the claim.
9. Operator acceptance: the operator reviews the evidence bundle, remaining risk, and decision history, then accepts or rejects the KR. Objective progress updates only after this acceptance, not after agent self-report.
10. Recovery and audit: every transition is reconstructable from the event log. A restart, duplicate `complete`, or late approval can be replayed and resolved deterministically, with `orphaned` or `stale_context` states used instead of transcript guesswork.

## 16. Expansion path
Phase 1:
- one accountable owner
- local structured store
- append-only event log
- markdown knowledge capture
- local Codex and Claude adapters
- plan approval, task board, approval inbox, evidence review [source-1-user-brief] [source-7-local-environment] [source-15-goal-managed-agent-framework].

Phase 2:
- GitHub read and limited write adapters with repo and branch scopes
- filesystem authority with workspace and path scopes
- worktree isolation
- markdown export plus richer Obsidian sync [source-1-user-brief] [source-11-claudecode-permission-governance] [source-15-goal-managed-agent-framework].

Phase 3:
- org-managed policy layers
- remote runtimes
- compliance exports
- multi-workspace governance
- richer audit and portfolio views [source-5-multica-platform] [source-6-multica-daemon] [source-10-claudecode-broader-product-inspection].

Invariant across phases:
- the event log remains the source of truth
- plugins remain scoped
- completion remains evidence-backed
- open source remains a pattern library rather than the product core [source-13-build-from-scratch-constraint].

## 17. Key risks and open questions
- Demand risk: the pain is real, but frequency at the full goal-managed level is not yet proven.
- UX risk: SMART KR authoring can become bureaucracy if clarification is not fast and preview-driven.
- Governance risk: approval fatigue can destroy flow if rules do not ratchet intelligently.
- Runtime risk: different agent runtimes expose different hook and resume guarantees.
- Eval risk: measuring true completion may be expensive or ambiguous outside code-heavy tasks.
- Org risk: larger organizations may want the audit and permission model but adopt more slowly than the early wedge [source-5-multica-platform] [source-11-claudecode-permission-governance] [source-17-goal-managed-agent-testing-strategy].

## 18. Recommendation and rollout gates
Build the MVP, but keep the claim narrow:
- local-first
- one accountable owner per objective
- conversational planning into SMART KRs
- daemon-backed execution with isolated workspaces
- typed hooks and rule-based permissions
- event-log-backed recovery
- evidence-backed completion with an eval harness [source-8-user-followup] [source-12-claudecode-subagent-hooks-pluggability] [source-17-goal-managed-agent-testing-strategy] [source-18-user-priority-correctness].

Do not promise:
- full autonomy
- org-wide deployment first
- or correctness through a second judge model alone [source-13-build-from-scratch-constraint] [source-17-goal-managed-agent-testing-strategy] [source-18-user-priority-correctness].

Phase-promotion criteria should stay metric-gated, not vibe-gated:
- Prototype -> pilot: deterministic state-machine, replay, policy, and protocol suites are green; approval precision and false-approve rate are measured on a versioned dataset; resume success and orphaned-completion rate are instrumented; cost or latency baselines exist for the top workflows.
- Pilot -> beta: offline eval consistency is stable across reruns; permission-request precision and false-block rate are tolerable; evaluator disagreement is low enough to review manually; blocked-on-user recovery plus stale-context handling behave correctly under restart and retry.
- Beta -> higher-authority rollout: canary monitoring shows no regression in approval precision, false-approve rate, resume success, orphaned-completion rate, evaluator disagreement, or cost or latency; audit exports and recent-denial recovery work; and managed rule layers are proven for GitHub and filesystem authority [source-17-goal-managed-agent-testing-strategy] [source-18-user-priority-correctness].

The product is worth building if it is framed as a governed goal-to-execution control plane, not as a magic manager replacement.
