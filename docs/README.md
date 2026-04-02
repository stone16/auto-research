# Approach And Operating Insights

`LLM Auto Research` treats research as an iterative optimization problem, not a one-shot prompting problem.

The core idea is simple:

1. pick a bounded topic
2. freeze the source set
3. define what good looks like with benchmark questions and quality dimensions
4. let a producer propose revisions
5. let evaluation and a judge decide whether to keep or discard them

That structure changes the behavior of the system in useful ways.

## What It Can Reliably Do

When the topic and evidence boundary are clear, this framework is good at:

- synthesizing a source set into a cleaner and denser knowledge base
- improving benchmark-grounded answers across multiple iterations
- preserving a clean history of accepted improvements
- giving operators a controllable overnight or long-running loop
- separating generation from judgment so quality feedback compounds over time

In practice, this means it can help produce internal briefs, cited explainers, research memos, and other bounded knowledge artifacts that should improve incrementally instead of being regenerated from scratch.

## What It Does Not Automatically Solve

This framework does not remove the need for clear problem framing.

It is weaker when:

- the source set is incomplete or constantly changing
- the task has no benchmarkable notion of "better"
- the output quality depends on live web discovery rather than a bounded corpus
- the topic requires genuinely new empirical discovery, not synthesis and refinement

You can extend the system with a custom `command` provider, but the default framework is optimized for bounded, auditable loops.

## Why The Design Looks Like This

Several design choices matter more than they might seem at first:

### 1. A mutable artifact beats chat transcripts

The loop is centered on `knowledge_base.md`, not on the conversation history. That gives the system a stable object to improve and a stable thing for humans to inspect.

### 2. A fixed benchmark beats vague prompting

Without `benchmark.json`, agents can produce text that sounds better without actually being more complete or better grounded. Benchmarks force the loop to prove that it improved.

### 3. Keep/discard beats endless accumulation

Many agent loops drift because every iteration appends more text. The ratchet does the opposite: it keeps the improved state and throws away the weaker state.

### 4. Separate producer and judge roles matter

Using one model to produce and another to judge often gives better directional feedback. Even when the same provider is used for both roles, the separation in protocol still helps.

### 5. Human feedback is highest leverage when it is live

Operators do not need to restart the run to steer it. Editing `human_feedback.md` between iterations is cheap, and that makes the system more usable in practice.

### 6. Reliability features are part of the product

`status`, `provider_status.json`, `loop_status.json`, and `supervise` are not just operator extras. They are what turns a demo loop into something you can leave running overnight.

## Practical Insights We Have Found

These are the main operating lessons reflected in the current codebase:

- missing judge dimensions must count as zero, otherwise partial judge payloads inflate scores
- benchmark answers need non-empty citations, otherwise the loop rewards fluent but weak outputs
- large prompts and task payloads should go through stdin or temp files, not argv
- supervisor logic must distinguish clean terminal stops from unhealthy crashes
- local run state should stay local; the framework is the product, not the contents of `runs/`

These constraints look operational, but they are really quality controls. If you ignore them, the loop quickly becomes hard to trust.

## How To Think About Scope

A good first run has:

- one clear topic
- a small, frozen source set
- two to five benchmark questions
- explicit quality dimensions
- a clear idea of what a "better" knowledge base looks like

Do not start with a giant open-ended domain. Start with a topic that can converge.

## Suggested Reading Order

- Start with the root [README.md](../README.md) for positioning and usage
- Then read [../examples/README.md](../examples/README.md) for what a run produces
- Then adapt the example run into your own topic
