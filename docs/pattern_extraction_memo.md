# Pattern Extraction Memo

Goal: identify current OSS projects worth reading, the exact mechanism each teaches, why that mechanism exists, what not to copy, and what our framework must implement itself.

## Shortlist By Fit

1. `OpenHands` - closest end-to-end local agent runtime and operator surface.
2. `LangGraph` - best control-plane / state-machine pattern for planning and recovery.
3. `Temporal` - best durable execution / retry / resume substrate.
4. `AutoGen` - best multi-agent communication and handoff patterns.
5. `inspect_ai` - best evaluation harness and sandboxing patterns.
6. `Aider` - best local terminal-first coding-agent workflow.
7. `n8n` - best workflow/plugin/operator UI pattern for integrations.

Honorable mention: `openai-agents-python` for typed handoffs, tracing, and guardrails, but it is less local-first than the projects above.

## Planning UX

`LangGraph` and `OpenHands` are the strongest references here.

- `LangGraph` teaches explicit graph/state transitions, human-in-the-loop checkpoints, and conditional routing. It exists because linear prompts do not model re-entry, branching, or pause/resume cleanly. Do not copy the framework as a black box; copy the idea of typed states and explicit edges. Our framework should own planning UX, KR previews, dependency visualization, and approval states itself.
- `OpenHands` teaches the operator-facing planning surface for a coding agent: task context, repo-aware action, and visible workspace state. It exists because users need to see what the agent is doing and why. Do not copy its product scope or heavy runtime assumptions; copy the need for operator legibility and task-centric planning.
- `Aider` teaches the smallest useful loop for local code work: chat, patch, commit, repeat. It exists because many coding tasks are better served by a tight git-centered interaction loop than by a giant platform. Do not copy its single-agent limitation. Our framework should support guided goal clarification and KR authoring before any patch loop starts.

## Runtime/Orchestration

`OpenHands`, `Temporal`, and `AutoGen` are the main references.

- `OpenHands` teaches the local execution runtime pattern: shell, repo, browser, task state, and a UI around it. It exists because coding agents need real tools, not just chat. Do not copy the whole runtime stack; implement our own runtime adapter, claim/heartbeat logic, and workspace isolation.
- `Temporal` teaches durable workflow execution, retries, long-running tasks, and resume semantics. It exists because distributed work fails and must be replayable. Do not copy Temporal as our agent framework; copy durable state, retries, and explicit workflow boundaries.
- `AutoGen` teaches multi-agent handoffs and conversation-based cooperation. It exists because some tasks benefit from specialized agents talking to each other. Do not copy unconstrained chatty swarms; implement our own typed subagent protocol and explicit message bus.

## Governance/Policy

`OpenHands`, `n8n`, and `LangGraph` are the most useful references.

- `OpenHands` shows that permissions, tool use, and runtime guardrails need to be visible to the operator. It exists because local execution without policy is unsafe. Do not copy its implicit assumptions; build our own policy engine, scoped approvals, and workspace/path rules.
- `n8n` teaches credential scoping, workflow-level connectors, and an operator-friendly integration UI. It exists because automation is useful only when secrets and connectors are managed cleanly. Do not copy workflow sprawl; implement our own permission rules and connector scopes.
- `LangGraph` teaches that policy decisions can be encoded as graph branches and interrupt points. It exists because governance is often a workflow transition, not a static config. Do not copy generic graph abstractions; implement explicit approval states and policy transitions.

## Evaluation/Observability

`inspect_ai` and `openai-agents-python` are the strongest references.

- `inspect_ai` teaches benchmark definitions, task sandboxes, scorers, and evaluation runs. It exists because model outputs need repeatable measurement. Do not copy it as a production runtime; build our own evaluation contracts and keep evaluation separate from execution.
- `openai-agents-python` teaches tracing, guardrails, and structured handoffs. It exists because observability and safety need to be native to the agent API. Do not copy vendor coupling; implement our own event log, trace schema, and evaluator hooks.

## Agent UI / Operator Cockpit

`OpenHands`, `Aider`, and `n8n` are the strongest references.

- `OpenHands` teaches the operator cockpit: tasks, session state, tool activity, and visible progress. It exists because agent work is otherwise opaque. Do not copy the product shape wholesale; implement our own cockpit around objectives, KR state, approvals, and blocked reasons.
- `Aider` teaches the minimal cockpit for code edits: terminal feedback and git history. It exists because many users want low-friction control. Do not copy its narrow scope; our cockpit needs goal-level state and evidence, not just diffs.
- `n8n` teaches a visual control room for automation. It exists because integration flows need easy inspection and reruns. Do not copy workflow-node clutter; use similar legibility for approvals, connectors, and evaluator status only.

## What Our Framework Must Implement Itself

We should implement these primitives directly:

- goal / objective / KR modeling
- conversational planning UX
- subagent protocol and context contract
- workflow state machine and resume logic
- policy engine and approval inbox
- event log and observability schema
- evaluation contracts and evidence checks
- operator cockpit for blocked states and review

The rule is simple: read these projects for mechanisms, not as dependencies. The framework must own its core protocol if it is to remain local-first, governable, and composable.
