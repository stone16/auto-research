# Knowledge Base

Topic: Goal-Managed Agent Orchestration with Conversational Planning, Governance, Pluggable Subagent Protocols, and Correctness Strategy

## Working thesis
- There is a real operator need here, but it is narrower than autonomy marketing. The user is asking to manage goals with less task babysitting while local agents handle bounded execution, and to escalate only when ambiguity, risk, or missing context appears [source-1-user-brief] [source-8-user-followup].
- The product is technically feasible now as a local-first control plane around existing local coding agents, with conversational planning, approved SMART Key Results, daemon-managed execution, rule-based permissions, typed hooks, resumable sessions, and evaluation-backed closure [source-3-codex-capabilities] [source-4-claude-capabilities] [source-6-multica-daemon] [source-9-claudecode-source-inspection] [source-12-claudecode-subagent-hooks-pluggability].
- Skeptical call: do not promise that humans disappear from execution. The system can reduce task micromanagement only if it owns blocked-state handling, permissions, evidence review, and recovery semantics. It cannot safely remove humans from ambiguous planning, destructive authority, or final acceptance [source-11-claudecode-permission-governance] [source-17-goal-managed-agent-testing-strategy] [source-18-user-priority-correctness].
- Larger organizations matter because the same problems intensify under coordination overhead and compliance, but the first wedge is still narrower. Design the contracts for scale, while shipping a product that works for one accountable owner first [source-5-multica-platform] [source-8-user-followup].

## 1. Demand reality
- Prompt-centric tooling breaks when work spans multiple dependent steps, approvals, and runtime interruptions. The user does not want better prompting alone; they want a system that preserves intent, routes execution, and requests help only when needed [source-1-user-brief].
- The local auto-research framework is a strong product signal: bounded sources, a mutable knowledge base, fixed benchmarks, human feedback hot-reload, and supervisor stop reasons all show that once work becomes iterative, control-plane behavior matters as much as model output [source-2-auto-research-framework].
- Multica is the clearest comparable in the frozen corpus. Its emphasis on assignments, blockers, workspaces, local daemon execution, and reusable skills suggests there is already demand for managed-agent infrastructure. It does not prove goal-only management, but it does prove that coordination and governance are already product surfaces [source-5-multica-platform] [source-6-multica-daemon].
- Decision: the need is real for local-agent power users and plausibly stronger in governed environments. The category is not yet proven as a universal autonomy platform.

## 2. Organization fit: solo, small team, larger organization
- Solo builders are the fastest wedge because one person is already the single accountable owner, can answer clarifications quickly, and can judge whether evidence is good enough. The product saves them from turning each milestone into a pile of ad hoc prompts and manual follow-up [source-1-user-brief] [source-8-user-followup].
- Small teams add value when an objective owner can mix human and agent work on the same board, see blockers, and review shared evidence. This is close to the work-management model already implied by Multica [source-5-multica-platform] [source-15-goal-managed-agent-framework].
- Larger organizations matter because the same structure becomes more necessary, not less, as coordination overhead, compliance, workspace scoping, approval routing, and auditability become harder. The user is likely right that the enduring unit is still one single accountable owner per objective, with delegated human and agent execution beneath that layer [source-8-user-followup] [source-11-claudecode-permission-governance].
- Skeptical caveat: larger organizations only fit if permission rules, decision provenance, approval UX, and audit exports are first-class. Otherwise the product becomes either unsafe shadow automation or a new coordination tax [source-11-claudecode-permission-governance] [source-15-goal-managed-agent-framework].

## 3. Conversational planning and SMART KR design
The system should turn ambiguity into executable work through a staged conversation, not a rigid schema [source-8-user-followup] [source-9-claudecode-source-inspection] [source-10-claudecode-broader-product-inspection].

Suggested flow:
1. Capture the raw goal, why it matters, the deadline, and the operator of record.
2. Run a clarification pass on outcome, constraints, current assets, risk tolerance, permissions, dependencies, and what would count as proof.
3. Draft a short objective with owner, scope, success window, and excluded work.
4. Draft candidate SMART KRs. Each KR needs Specific, Measurable, Attainable, Relevant, and Time-bound fields plus an evidence contract [source-8-user-followup] [source-16-goal-managed-agent-protocol-spec].
5. Highlight gaps instead of pretending the first draft is ready. Ask follow-up questions until each KR is reasonably independent, permission-aware, and reviewable.
6. Show an execution-readiness preview with expected tools, workspaces, approvals, and evidence checks.
7. Require explicit approval before any runtime starts.

Claude Code evidence is strong here. AskUserQuestion is a rich clarification surface with previews, side-by-side option rendering, and deferred user interaction. Plan Mode is an explicit read-only stage before edits. Verifier setup and remote scheduling are also dialog-driven rather than being hidden backend steps [source-9-claudecode-source-inspection] [source-10-claudecode-broader-product-inspection].

## 4. Recursive KR to Objective structure and dependency rules
- A higher-level KR may become a child Objective only when satisfying it requires multiple subordinate KRs with their own evidence and review path [source-8-user-followup] [source-15-goal-managed-agent-framework].
- Keep the hierarchy shallow and legible. Every child objective still needs one accountable owner, bounded scope, inherited context from the parent KR, and a clear completion contract [source-16-goal-managed-agent-protocol-spec].
- KRs should be independent by default. A dependency must be explicit, sparse, and reviewable. If many sibling KRs share mutable state or block one another, the plan is wrong and should be redrawn before execution [source-8-user-followup] [source-9-claudecode-source-inspection].
- When a parent objective or KR version changes, child executions should be marked stale_context or orphaned rather than silently merged back. Recursive decomposition is only safe if versioning and revalidation are first-class [source-16-goal-managed-agent-protocol-spec] [source-17-goal-managed-agent-testing-strategy].

## 5. What is technically feasible now
- Local execution is already real. Codex CLI runs locally, exposes thread control through `startThread()`, `run(...)`, and `resumeThread(...)`, and supports repo-local hooks that receive JSON on stdin. Codex hooks are useful control surfaces, though current PreToolUse and PostToolUse interception is still Bash-focused and incomplete [source-3-codex-capabilities].
- Claude Code also exposes hooks, programmatic control, and a `permissionDecision: defer` plus `--resume <session-id>` path that fits human escalation well [source-4-claude-capabilities].
- The current machine already has `codex-cli 0.118.0` and `Claude Code 2.1.100` installed, so a prototype can orchestrate real local agents now [source-7-local-environment].
- Multica documents the strongest concrete daemon pattern in the corpus: detect local CLIs, watch workspaces, claim tasks, create an isolated workspace per task, stream results, poll every 3 seconds, heartbeat every 15 seconds, and deregister on shutdown [source-6-multica-daemon].
- Claude Code source inspection shows the underlying mechanisms we need: blocked-on-user tracing, task and dependency state, plan approval, remote session supervision, context construction for child agents, and typed lifecycle hooks [source-9-claudecode-source-inspection] [source-10-claudecode-broader-product-inspection] [source-12-claudecode-subagent-hooks-pluggability].
- Build-from-scratch constraint: absorb these mechanisms, but do not depend on an external agent framework as the product core [source-13-build-from-scratch-constraint].

Feasible now:
- conversational planning,
- local daemon plus local CLI execution,
- isolated workspace leasing,
- blocked and resume semantics,
- typed hooks,
- structured task and evidence state,
- human approval and evaluation loops.

Still speculative or risky:
- broad unattended cross-system automation,
- low-friction org-wide GitHub write authority,
- reliable business-judgment closure without human review,
- and large-scale multi-agent coordination without strong acceptance checks.

## 6. Why managing goals alone is still incomplete
A user cannot mostly manage goals unless the system also owns the layers underneath the goals [source-1-user-brief] [source-2-auto-research-framework] [source-15-goal-managed-agent-framework].

Those layers are:
- clarification and KR drafting,
- execution routing and workspace isolation,
- policy and approval,
- blocked-state handling,
- evaluation and evidence review,
- decision recording in an event log.

Without them, goal management collapses back into prompt babysitting with better labels.

Human judgment remains essential for:
- ambiguous goal formation and tradeoffs,
- risky or destructive authority,
- credential provisioning and policy exceptions,
- evaluator disagreement,
- and final acceptance when evidence is incomplete or conflicting [source-4-claude-capabilities] [source-11-claudecode-permission-governance] [source-17-goal-managed-agent-testing-strategy] [source-18-user-priority-correctness].

## 7. MVP architecture
The MVP should separate control plane, execution runtime, governance, evaluation, and operator surfaces from day one [source-15-goal-managed-agent-framework] [source-16-goal-managed-agent-protocol-spec].

Control plane:
- `Goal`, `Objective`, `KeyResult`, `EvidenceCheck`, `DecisionRecord`
- `PlanningSession`, `PlanPreview`, `ExecutionReadinessCheck`
- append-only event log as source of truth

Execution runtime:
- local daemon
- `RuntimeAdapter` for Codex CLI and Claude CLI or SDK
- `TaskExecution`, `AgentSession`, `WorkspaceLease`
- isolated workspace or worktree mode per task
- `ResumeHandle` for paused or disconnected sessions

Governance:
- `PolicyEngine`
- `PermissionRule`
- `ApprovalRequest`
- `HookRegistry`

Evaluation:
- `EvaluatorRegistry`
- tests, artifact checks, benchmarks, human review
- completion claims accepted only after evaluation

Operator API and UI:
- goal conversation
- plan preview and approval
- task board
- session detail
- approval inbox
- evidence review
- policy panel

Storage:
- local structured store for owned objects
- append-only event log for replay and audit
- markdown exports for knowledge capture
- later adapters for GitHub and Obsidian, but not as core dependencies [source-1-user-brief] [source-13-build-from-scratch-constraint].

## 8. Why the center of gravity is UI and UX
Claude Code is strong evidence that the hard product work is not hidden backend scheduling. AskUserQuestion is a previewable clarification surface. Plan Mode is a staged approval flow. TaskCreate, TaskGet, and TaskUpdate make dependencies explicit. Blocked-on-user is a traced runtime state. LocalShellTask ships a stall watchdog that checks every 5 seconds, uses a 45 second threshold, detects interactive prompts, and pushes recovery back into the product workflow [source-9-claudecode-source-inspection]. TaskListV2 and RemoteAgentTask show a persistent operator cockpit with status, ownership, active agents, and plan phases [source-10-claudecode-broader-product-inspection].

Therefore the MVP needs primary screens for:
- goal conversation with alternative previews,
- objective and KR approval,
- dependency-aware task list,
- session detail with current tool activity and spawned agents,
- blocked-on-user inbox,
- approval and rule management,
- evidence review and verifier status.

If the operator must reconstruct state from transcripts or logs, the product has failed at its main job.

## 9. Permission governance and approval UX
Permission governance should look like an operator product, not a hidden ACL file [source-11-claudecode-permission-governance].

Required model:
- `allow`, `ask`, `deny` rules
- scope by workspace, repo, branch, path, tool, and action
- separate capability profiles for GitHub and filesystem authority
- recent denials view so the system can learn from refusals and avoid repetitive prompts
- immutable policy layers when rules come from managed settings, plus user-owned local exceptions [source-11-claudecode-permission-governance] [source-15-goal-managed-agent-framework]

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
- and denials should force replanning or a narrower request rather than silent retries [source-6-multica-daemon] [source-7-local-environment] [source-11-claudecode-permission-governance].

## 10. Subagent protocol
Subagents must be a protocol, not a convenience helper [source-12-claudecode-subagent-hooks-pluggability] [source-16-goal-managed-agent-protocol-spec].

Required pieces:
- mode: `fork`, `fresh`, `worktree`, `remote`, `teammate`
- context contract: immutable goal scope, filtered or summarized history, cloned mutable runtime state by default, explicitly shared callbacks only when required
- communication contract: typed channels for notification, direct message, approval, resume, and event streaming
- lifecycle policy: timeout, retry budget, stall policy, orphan policy
- protocol actions: `spawn`, `ack`, `block`, `resume`, `complete`, `cancel`

Important Claude Code lessons:
- child context is explicitly constructed,
- incomplete parent tool calls are filtered,
- cloned mutable state is the default,
- fork mode optimizes stronger context inheritance,
- background completion returns through notifications,
- mailbox-style direct messaging exists for teammate patterns,
- resume reconstructs execution from saved state rather than parent transcript scraping [source-12-claudecode-subagent-hooks-pluggability].

Design rule: parent-child coordination should ride a typed message bus and event log. Transcript text may be inspectable evidence, but never the source of truth.

## 11. Hooks as deterministic control surfaces
Hooks matter because they actively change control flow [source-3-codex-capabilities] [source-4-claude-capabilities] [source-12-claudecode-subagent-hooks-pluggability].

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

Useful hook outputs:
- approve,
- block,
- updated input,
- additional context,
- updated output,
- retry,
- escalation request,
- stop continuation [source-12-claudecode-subagent-hooks-pluggability].

Determinism comes from:
- typed input and output schemas,
- deterministic order within a scope,
- explicit precedence rules such as block beats approve,
- timeouts and fail-open or fail-closed policy,
- retry budgets and event emission,
- scope ownership and cleanup.

Critical caveat: Codex hook interception is still incomplete, so hooks are strong guardrails but not the only governance mechanism. The control plane still needs its own policy engine and approval state [source-3-codex-capabilities].

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

Each plugin should declare:
- scope and lifecycle,
- schemas,
- permissions it requires,
- conflict rules,
- failure policy,
- cleanup behavior.

Session-scoped registration is the key pattern to copy from Claude Code. It keeps a skill or agent extension alive only for the owning session or workflow, which prevents hidden global mutation [source-12-claudecode-subagent-hooks-pluggability].

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
- Layer 1: deterministic control-plane tests
- Layer 2: protocol and recovery tests
- Layer 3: offline evals on a versioned dataset
- Layer 4: adversarial and fault-injection tests
- Layer 5: online monitoring plus regular human review [source-17-goal-managed-agent-testing-strategy]

Best-practice commitments:
- deterministic assertions first,
- versioned datasets,
- narrow graders,
- consistency measurement across reruns,
- human calibration,
- and turning real failures into new tests [source-14-pattern-extraction-memo] [source-17-goal-managed-agent-testing-strategy].

## 14. Recovery and error-correction model
The system should correct mistakes by explicit state transitions, not by optimistic narration [source-16-goal-managed-agent-protocol-spec] [source-17-goal-managed-agent-testing-strategy].

Planning mistakes:
- if clarifications are missing, `block` and ask the user rather than launching work,
- if the objective changes, mark dependent tasks `stale_context` and require revalidation.

Execution mistakes:
- if a tool or shell appears interactive, detect the stall, kill it, and rerun with non-interactive input or a different flag. Claude Code's watchdog is strong evidence that this belongs in runtime product behavior [source-9-claudecode-source-inspection].
- if permissions are denied, move the task to blocked or superseded, surface the denial, and either narrow the request or wait for explicit operator change [source-11-claudecode-permission-governance].

Cross-agent mistakes:
- dedupe duplicate `complete` or `block` events,
- treat late results as orphaned if parent state moved on,
- prevent auto-merge after parent version change,
- reconstruct from the event log after restart,
- fail closed when lease, policy, or protocol state cannot be revalidated [source-16-goal-managed-agent-protocol-spec] [source-17-goal-managed-agent-testing-strategy].

Evaluator mistakes:
- a passed test suite does not equal KR completion,
- machine-human disagreement routes to review,
- the KR stays in verifying or failed until evidence and decisions align [source-15-goal-managed-agent-framework] [source-17-goal-managed-agent-testing-strategy].

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
- richer exporter support such as Obsidian markdown sync [source-1-user-brief] [source-11-claudecode-permission-governance].

Phase 3:
- org-managed policy layers,
- remote runtimes,
- compliance exports,
- multi-workspace governance,
- richer audit and portfolio views [source-5-multica-platform] [source-6-multica-daemon] [source-10-claudecode-broader-product-inspection].

Invariant across phases:
- the event log remains the source of truth,
- plugins remain scoped,
- completion remains evidence-backed.

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
