# Growth Engine Run Initialization (Path B) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Land all artifacts the LLM Auto Research framework needs to start iter-1 of the growth-engine-from-scratch run — minus the §6.10 provisional anchors and §8.6 OS sandbox, which Path B explicitly defers per the design spec.

**Architecture:** Two parallel deliverables: (1) **run-init artifacts** mechanically extracted/derived from the design spec at `docs/superpowers/specs/2026-05-01-growth-engine-from-scratch-design.md` (topic.md, program.md, benchmark.json, run.json, knowledge_base.md seed); (2) **source set** — a deterministic Python extractor that walks `~/dev/getuai/`, dumps per-repo raw markdown extracts under `sources/_raw/`, then a deterministic composer that produces the 10 `source-*.md` digest files specified in spec §3 by structured concatenation (no LLM in the composition path — per Path B's "fast to iter-1" choice). Iter-1 verifies the run shape with `--provider mock`.

**Tech Stack:** Python 3.11+, `pytest`, the existing `llm_autoresearch` package CLI (`uv run autoresearch ...`), filesystem walks via `pathlib`.

---

## File Structure

**Files to create:**

| Path                                                                      | Responsibility                                                              |
| ------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| `runs/growth-engine-from-scratch/run.json`                                | Run config (provider/judge CLIs, evaluation thresholds, slug, topic title)  |
| `runs/growth-engine-from-scratch/topic.md`                                | Topic brief — derived from spec §1, §2, §4                                  |
| `runs/growth-engine-from-scratch/program.md`                              | Research lanes + hard rules — derived from spec §5 + §6 highlights          |
| `runs/growth-engine-from-scratch/benchmark.json`                          | The 15-question benchmark — extracted from spec §5 JSON blocks              |
| `runs/growth-engine-from-scratch/knowledge_base.md`                       | Empty seed with TOC                                                         |
| `runs/growth-engine-from-scratch/source_mapping.json`                     | Which repos feed which `source-*.md` (encodes spec §3 table)                |
| `runs/growth-engine-from-scratch/sources/_raw/<repo>.md` (×64)            | Per-repo raw extracts — output of `extract_sources.py`                      |
| `runs/growth-engine-from-scratch/sources/source-*.md` (×10)               | The 10 digests — output of `compose_sources.py`                             |
| `scripts/extract_benchmark.py`                                            | Parses spec markdown, emits `benchmark.json`                                |
| `scripts/extract_sources.py`                                              | Walks `~/dev/getuai/`, emits `sources/_raw/<repo>.md`                       |
| `scripts/compose_sources.py`                                              | Reads `_raw/` + `source_mapping.json`, emits `sources/source-*.md`          |
| `tests/test_extract_benchmark.py`                                         | Unit tests for benchmark extraction                                         |
| `tests/test_extract_sources.py`                                           | Unit tests for repo extraction (uses fixtures)                              |
| `tests/test_compose_sources.py`                                           | Unit tests for digest composition                                           |
| `tests/fixtures/fake_getuai/`                                             | Tiny fake repo tree for testing extraction                                  |

**Files NOT created (deferred per Path B):**

- `judge_calibration.md` (provisional anchors — §6.10 progressive crystallization handles this)
- The OS sandbox + point-verify tool (§8.6 — accept some honor-system risk for early iterations)

---

## Task 1: Initialize run directory and run.json

**Files:**
- Create: `runs/growth-engine-from-scratch/run.json`
- Create: `runs/growth-engine-from-scratch/knowledge_base.md` (empty seed)
- Create: `runs/growth-engine-from-scratch/sources/` (empty dir; populated later)
- Create: `runs/growth-engine-from-scratch/sources/_raw/` (empty dir)

- [ ] **Step 1: Create directory structure**

```bash
mkdir -p runs/growth-engine-from-scratch/sources/_raw
mkdir -p runs/growth-engine-from-scratch/artifacts
ls -d runs/growth-engine-from-scratch/*/
```

Expected: `artifacts/`, `sources/` listed.

- [ ] **Step 2: Write `runs/growth-engine-from-scratch/run.json`**

```json
{
  "topic": "Growth Engine From Scratch — synthesizing architecture, skills, and practitioner cognition from ~64 getuai/ repos",
  "slug": "growth-engine-from-scratch",
  "provider": {
    "kind": "command",
    "command": ""
  },
  "evaluation": {
    "minimum_improvement": 0.01,
    "allow_tie_if_shorter": true,
    "gate_threshold": 0.55
  },
  "producer": {
    "cli": "codex",
    "flags": "",
    "timeout_seconds": 3600
  },
  "judge": {
    "cli": "claude",
    "flags": "",
    "timeout_seconds": 1800
  }
}
```

- [ ] **Step 3: Write `runs/growth-engine-from-scratch/knowledge_base.md` seed**

```markdown
# Growth Engine From Scratch — Knowledge Base

Status: seed (iter-0). Producer fills in subsequent iterations.

## Q1 — A1: SEO/GEO Architecture
*To be drafted.*

## Q2 — A2: Content Writing Architecture
*To be drafted.*

## Q3 — A3: Ads Architecture
*To be drafted.*

## Q4 — A4: Social Architecture
*To be drafted.*

## Q5 — S1: SEO/GEO Skills
*To be drafted.*

## Q6 — S2: Content Writing Skills
*To be drafted.*

## Q7 — S3: Ads Skills
*To be drafted.*

## Q8 — S4: Social Skills
*To be drafted.*

## Q9 — C1: SEO/GEO Cognition
*To be drafted.*

## Q10 — C2: Content Writing Cognition
*To be drafted.*

## Q11 — C3: Ads Cognition
*To be drafted.*

## Q12 — C4: Social Cognition
*To be drafted.*

## Q13 — I1: Shared Foundations
*To be drafted.*

## Q14 — I2: Build Sequence (Day-1 → Month-3)
*To be drafted.*

## Q15 — I3: Cross-Domain Failure Modes
*To be drafted.*
```

- [ ] **Step 4: Verify**

```bash
test -f runs/growth-engine-from-scratch/run.json && python3 -c "import json; json.load(open('runs/growth-engine-from-scratch/run.json'))" && echo OK
test -f runs/growth-engine-from-scratch/knowledge_base.md && echo OK
test -d runs/growth-engine-from-scratch/sources/_raw && echo OK
test -d runs/growth-engine-from-scratch/artifacts && echo OK
```

Expected: 4× `OK`.

- [ ] **Step 5: Commit**

```bash
git add runs/growth-engine-from-scratch/run.json \
        runs/growth-engine-from-scratch/knowledge_base.md
git commit -m "feat(run): scaffold growth-engine-from-scratch run config and KB seed"
```

---

## Task 2: Extract benchmark.json from the design spec

**Files:**
- Create: `scripts/extract_benchmark.py`
- Create: `tests/test_extract_benchmark.py`
- Create: `runs/growth-engine-from-scratch/benchmark.json` (output of running the script)

- [ ] **Step 1: Write the failing test `tests/test_extract_benchmark.py`**

```python
"""Tests for extract_benchmark.py — parses the design spec into benchmark.json."""
from pathlib import Path
import json
import subprocess
import sys


SPEC = Path("docs/superpowers/specs/2026-05-01-growth-engine-from-scratch-design.md")
SCRIPT = Path("scripts/extract_benchmark.py")
OUTPUT = Path("runs/growth-engine-from-scratch/benchmark.json")


def test_script_exists():
    assert SCRIPT.exists(), f"{SCRIPT} must exist"


def test_extracts_15_questions(tmp_path):
    """Running the script against the real spec produces a benchmark.json with 15 questions."""
    out = tmp_path / "benchmark.json"
    subprocess.run(
        [sys.executable, str(SCRIPT), str(SPEC), str(out)],
        check=True,
        cwd=Path.cwd(),
    )
    questions = json.loads(out.read_text())
    assert len(questions) == 15, f"expected 15 questions, got {len(questions)}"


def test_each_question_has_required_fields(tmp_path):
    out = tmp_path / "benchmark.json"
    subprocess.run(
        [sys.executable, str(SCRIPT), str(SPEC), str(out)],
        check=True,
        cwd=Path.cwd(),
    )
    questions = json.loads(out.read_text())
    required_top = {"id", "question", "rubric", "rubric_criteria", "penalty_criteria", "must_include", "required_sources"}
    for q in questions:
        missing = required_top - set(q.keys())
        assert not missing, f"{q.get('id')} missing fields: {missing}"


def test_question_ids_q1_through_q15(tmp_path):
    out = tmp_path / "benchmark.json"
    subprocess.run(
        [sys.executable, str(SCRIPT), str(SPEC), str(out)],
        check=True,
        cwd=Path.cwd(),
    )
    questions = json.loads(out.read_text())
    ids = [q["id"] for q in questions]
    assert ids == [f"q{i}" for i in range(1, 16)], f"unexpected ids: {ids}"


def test_rubric_criteria_have_stable_ids(tmp_path):
    out = tmp_path / "benchmark.json"
    subprocess.run(
        [sys.executable, str(SCRIPT), str(SPEC), str(out)],
        check=True,
        cwd=Path.cwd(),
    )
    questions = json.loads(out.read_text())
    for q in questions:
        for c in q["rubric_criteria"]:
            assert c["id"].startswith(f"{q['id']}.r"), f"bad criterion id {c['id']} in {q['id']}"
            assert "weight" in c and "criterion" in c
        for p in q["penalty_criteria"]:
            assert p["id"].startswith(f"{q['id']}.p"), f"bad penalty id {p['id']} in {q['id']}"
            assert "deduction" in p and "trigger" in p
```

- [ ] **Step 2: Run test to verify it fails**

```bash
uv run pytest tests/test_extract_benchmark.py -v
```

Expected: FAIL — `scripts/extract_benchmark.py` does not exist.

- [ ] **Step 3: Write `scripts/extract_benchmark.py`**

```python
#!/usr/bin/env python3
"""Parse the design spec and emit benchmark.json.

Usage: python scripts/extract_benchmark.py <spec.md> <output.json>

Reads ```json``` blocks from the spec, keeps those that look like benchmark
question objects (have id/question/rubric), validates them, and writes a
JSON array.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


JSON_BLOCK_RE = re.compile(r"```json\n(\{[^`]+?\})\n```", re.DOTALL)


def extract_questions(spec_text: str) -> list[dict]:
    """Return all JSON blocks in the spec that look like benchmark questions."""
    questions: list[dict] = []
    for match in JSON_BLOCK_RE.finditer(spec_text):
        try:
            obj = json.loads(match.group(1))
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and {"id", "question", "rubric"}.issubset(obj.keys()):
            questions.append(obj)
    return questions


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: extract_benchmark.py <spec.md> <output.json>", file=sys.stderr)
        return 2
    spec_path = Path(argv[1])
    out_path = Path(argv[2])
    spec_text = spec_path.read_text()
    questions = extract_questions(spec_text)
    if len(questions) != 15:
        print(f"ERROR: expected 15 questions, found {len(questions)}", file=sys.stderr)
        return 1
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(questions, indent=2))
    print(f"wrote {len(questions)} questions to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
```

- [ ] **Step 4: Run tests to verify pass**

```bash
uv run pytest tests/test_extract_benchmark.py -v
```

Expected: 4 passed.

- [ ] **Step 5: Run the script for real, generate the benchmark.json**

```bash
python3 scripts/extract_benchmark.py \
  docs/superpowers/specs/2026-05-01-growth-engine-from-scratch-design.md \
  runs/growth-engine-from-scratch/benchmark.json
```

Expected: `wrote 15 questions to runs/growth-engine-from-scratch/benchmark.json`

- [ ] **Step 6: Verify benchmark.json is well-formed**

```bash
python3 -c "import json; data = json.load(open('runs/growth-engine-from-scratch/benchmark.json')); assert len(data) == 15; print(f'OK: {len(data)} questions')"
```

Expected: `OK: 15 questions`

- [ ] **Step 7: Commit**

```bash
git add scripts/extract_benchmark.py tests/test_extract_benchmark.py runs/growth-engine-from-scratch/benchmark.json
git commit -m "feat(run): extract 15-question benchmark.json from design spec"
```

---

## Task 3: Write topic.md from spec §1, §2, §4

**Files:**
- Create: `runs/growth-engine-from-scratch/topic.md`

This is a hand-derivation from the spec; no script needed. The format mirrors `runs/polymarket-deep-research/topic.md`.

- [ ] **Step 1: Write `runs/growth-engine-from-scratch/topic.md`**

````markdown
# Topic Brief

Topic: Growth Engine From Scratch — Architecture, Reusable Skills, and Practitioner Cognition Synthesized from the getuai/ Corpus

## Scope

This run synthesizes from the ~64 repositories under `~/dev/getuai/` a from-scratch
playbook for building a growth engine: the architecture (how the system is wired),
the reusable skills (what units of work exist, how they are invoked and maintained),
and the practitioner cognitive models (what mental frames the people who built these
repos applied).

The deliverable is a `knowledge_base.md` that gives a small team starting Day 1 a
defensible build sequence and decision frame across four growth domains — SEO/GEO,
Content Writing, Ads management, Social media — plus the cross-cutting infrastructure
and failure-mode discipline that ties them together.

## Goal State

"Good understanding" means being able to:

- State the from-scratch architecture of each domain subsystem (SEO/GEO, Content,
  Ads, Social), grounded in repo evidence and acknowledging where repos disagree.
- Enumerate the reusable skills per domain with their invocation surface, input/output
  contract, state persistence, and maintenance signals.
- Name the practitioner cognitive models per domain with worked-here / failed-here
  evidence pairs.
- Specify the cross-domain shared infrastructure (identity, data, queue, observability,
  LLM gateway, human-in-loop) with explicit decision rule for shared-vs-isolated.
- Produce a Day-1 → Month-3 build sequence with explicit deferrals.
- Catalog cross-domain failure modes with per-domain evidence and prophylactic measures.
- Carry three structured artifacts embedded in `knowledge_base.md`:
  - `skill-catalog` table (≥32 rows, 8 columns) split across Q5/Q6/Q7/Q8 answers
  - `build-sequence` table (≥6 rows, 6 columns) embedded in Q14 answer
  - `failure-modes` table (≥8 rows, 7 columns) embedded in Q15 answer

## Non-Goals

- Code-from-scratch implementation. The KB is design knowledge, not code.
- Coverage of repos outside `~/dev/getuai/`.
- Treating any single existing project (including `getuai/growth-engine` and
  `getuai/growth-engine-legacy`) as the canonical answer. They are peer evidence
  among 64.
- Generic growth-marketing advice not grounded in the corpus.
- Live experimentation. The corpus IS the empirical evidence; this run does not run
  campaigns or A/B tests.

## Quality Dimensions

- **Architecture grounding**: Every architectural claim cites repo:file:line per §6.3
  citation tier.
- **Skill enumeration completeness**: ≥8 skills per domain in the embedded skill-catalog
  with all 8 columns populated.
- **Cognition evidence pairing**: Every named mental model has a worked-here AND a
  failed-here citation; unsupported models score 0.0 per §6.7.
- **Cross-domain integration discipline**: Q13/Q14/Q15 use cross-question hooks to
  Q1-Q12; Q15 cross-domain claims have per-domain evidence.
- **Citation discipline**: Tiered per §6.3 — Strong (file:line), Acceptable for B/A
  (digest with transitive file:line), Required for S band (direct file:line).
- **Cross-model evaluability**: Per-criterion scoring (§6.2) with stable IDs makes
  judge divergence diagnosable at the clause level.

## Ambiguities Resolved (Per Spec §8)

- §8.1: single 15-question run (cross-question consistency requires it).
- §8.2: Content Writing kept as separate domain.
- §8.3: three artifacts EMBEDDED in `knowledge_base.md`.
- §8.4: provisional anchors deferred for Path B; progressive crystallization per §6.10.
- §8.5: `growth-engine-legacy` stays in `source-failure-modes.md`, origin-tagged.
- §8.6 (deferred for Path B): OS sandbox + point-verify tool; honor-system risk accepted
  for early iterations until the harness lands the wrapper.

## Research Frame

Every iteration should improve `knowledge_base.md` along the 15-question matrix:

```
Architecture (Q1-Q4) → Skills (Q5-Q8) → Cognition (Q9-Q12) → Integration (Q13-Q15)
```

Per §7 layer-iteration grouping, iter-1 to iter-10 prioritize architecture; iter-11
to iter-20 prioritize skills; iter-21 to iter-30 prioritize cognition; iter-31 to
iter-40 prioritize integration. Producer is free to revise earlier-layer answers
when integration questions reveal contradictions (§6.6).

## Control Frame

The control loop: producer proposes a `knowledge_base.md` revision, judge scores
against §5 benchmark using §6 calibration rules, only score-improving changes are
kept. Per §7, cross-model validation runs at iter-1 anchor crystallization, every
threshold crossing, iters 5/15/30, and the final iteration.
````

- [ ] **Step 2: Verify it exists and is non-empty**

```bash
test -s runs/growth-engine-from-scratch/topic.md && wc -l runs/growth-engine-from-scratch/topic.md
```

Expected: ≥80 lines.

- [ ] **Step 3: Commit**

```bash
git add runs/growth-engine-from-scratch/topic.md
git commit -m "docs(run): topic.md derived from spec §1, §2, §4"
```

---

## Task 4: Write program.md from spec §5 (lanes) + §6 (hard rules subset)

**Files:**
- Create: `runs/growth-engine-from-scratch/program.md`

- [ ] **Step 1: Write `runs/growth-engine-from-scratch/program.md`**

````markdown
# LLM Auto Research Program

You are running a bounded research loop for this topic:

**Growth Engine From Scratch — Architecture, Reusable Skills, and Practitioner Cognition Synthesized from the getuai/ Corpus**

## Primary Research Lanes (3 layers × 4 domains + 3 integration = 15 questions)

### Architecture Layer (Q1-Q4)

- **Q1 (A1) SEO/GEO**: components, data flow, external dependencies, human-in-loop
  control points; converged pattern across `geo-aeo`, `geo-seo-v2`, `geowriter`,
  `getuai-seo`, `rankgale`, `rankncompare*`, `seo-poster`.
- **Q2 (A2) Content Writing**: pipeline stages (ideation → outline → draft → edit →
  publish → post-publish), LLM role per stage, human-review hooks, load-bearing vs
  stylistic choices.
- **Q3 (A3) Ads**: closed loop campaign feed → bidding → reporting → attribution →
  optimization; data model; platform-specific vs platform-agnostic boundary.
- **Q4 (A4) Social**: listen / post / schedule / engage / monitor decomposition;
  multi-platform abstraction (or honest "no abstraction"); rate-limit + credit
  accounting; content moderation insertion point.

### Skill Layer (Q5-Q8)

- **Q5 (S1) SEO/GEO Skills**: ≥8 skills with 8-column table (skill_name,
  originating_repo, path_reference, invocation_surface, input_schema, output_schema,
  state_persistence, maintenance_signals); duplicates identified with canonical pick.
- **Q6 (S2) Content Writing Skills**: same 8-column table; brittleness problem +
  mitigation technique per skill.
- **Q7 (S3) Ads Skills**: same 8-column table; platform-bound vs platform-agnostic
  per skill; abstraction contract; kill criteria.
- **Q8 (S4) Social Skills**: same 8-column table; cross-platform vs per-platform;
  parameterization; failure mode on platform API change.

### Cognition Layer (Q9-Q12)

- **Q9 (C1) SEO/GEO Cognition**: ≥3 mental models with worked-here + failed-here
  pairs; ≥2 anti-patterns.
- **Q10 (C2) Content Writing Cognition**: ≥3 frames with cross-question hooks to
  Q2/Q6.
- **Q11 (C3) Ads Cognition**: ≥3 models with platform-change survival/failure pairs;
  kill-vs-scale criteria.
- **Q12 (C4) Social Cognition**: ≥3 models including automation visibility cost;
  per-platform repo evidence required.

### Integration Layer (Q13-Q15)

- **Q13 (I1) Shared Foundations**: ≥6 shared foundations with corpus evidence from
  ≥2 repos each; explicit decision rule for shared-vs-domain-isolated.
- **Q14 (I2) Build Sequence**: ≥6 milestones (Day-1 / Week-1 / Week-2 / Week-4 /
  Week-8 / Week-12) with scope + dependencies + done_criteria + next_trigger;
  cross-references Q1-Q13; ≥3 explicit deferrals; embedded `build-sequence` table
  artifact.
- **Q15 (I3) Failure Modes**: ≥8 failure modes; per-domain evidence for cross-domain
  claims (q15.r3 weight 1.5); ≥3 modes from `growth-engine-legacy`; embedded
  `failure-modes` table artifact.

## Hard Rules (from spec §6 calibration)

- Treat `knowledge_base.md` as the primary artifact you are improving. The 3 embedded
  artifact tables (skill-catalog quadrants, build-sequence, failure-modes) are part
  of `knowledge_base.md`, not separate files.
- Citations follow §6.3 tiered system: Strong (`repo/path:LINE`), Acceptable for B/A
  (`source-*.md§<section>` ONLY when the digest section transitively contains
  `file:line`), Required for S band per `must_include` (direct `repo/path:LINE`).
- Every `must_include` term must be used in its rubric meaning, not just present —
  per §6.4 anti-keyword-gaming.
- All 15 questions' `required_sources` MUST be cited; missing 1 caps at C/0.69,
  missing 2+ caps at D/0.49 (§6.5).
- For Q9-Q12 cognition, mental models without worked-AND-failed evidence pairs score
  0.0 in their slot (§6.7). ≥1 unsupported model present caps at B (0.84); 0 paired
  models caps at D (0.49).
- Cross-question contradictions reduce both implicated questions by 0.05 (§6.6).
- Per-criterion scoring (§6.2) is mandatory; emit per-criterion vector keyed by stable
  IDs (`q<N>.r<M>`, `q<N>.p<M>`, `a<N>.c<M>`) in `judge_feedback.md`. Holistic gestalt
  scoring is forbidden.
- For each strategy or pattern claim, use this skeleton:

  1. Pattern hypothesis
  2. Repos that exhibit it (≥2 with file:line evidence)
  3. Where it disagrees with other repos (if any)
  4. Why it converged (or didn't) — structural cause
  5. Failure modes when this pattern is applied wrongly
  6. Recommendation: keep / question / reject for from-scratch design

## Workflow Per Iteration

1. Read `judge_feedback.md` from prior iteration to identify lowest-scoring criteria.
2. Focus the iteration's `knowledge_base.md` revision on those criteria first.
3. Maintain the 3 embedded artifact tables — every iteration that updates KB content
   for Q5-Q8 / Q14 / Q15 MUST update the corresponding table.
4. Cite every claim with §6.3-tier-appropriate citations.
5. Mark each citation's tier in KB (`tier: digest` or `tier: file:line`) for §8.6
   citation provenance audit.
6. After iteration, judge scores per §5 rubric_criteria + §6.11 artifact criteria,
   emits per-criterion vector.
7. Per §7 cross-model validation: at iters 5/15/30, the OTHER model re-judges; at any
   `dimension_threshold` first crossing, the OTHER model confirms; final iteration
   requires fresh-session both-model consensus.
````

- [ ] **Step 2: Verify**

```bash
test -s runs/growth-engine-from-scratch/program.md && wc -l runs/growth-engine-from-scratch/program.md
```

Expected: ≥70 lines.

- [ ] **Step 3: Commit**

```bash
git add runs/growth-engine-from-scratch/program.md
git commit -m "docs(run): program.md with 15-question lanes and §6 hard rules"
```

---

## Task 5: Write source_mapping.json (which repos feed which source-*.md)

**Files:**
- Create: `runs/growth-engine-from-scratch/source_mapping.json`

This encodes the spec §3 table as machine-readable mapping consumed by `compose_sources.py` in Task 8.

- [ ] **Step 1: Write `runs/growth-engine-from-scratch/source_mapping.json`**

```json
{
  "source-seo-geo": [
    "geo-aeo", "geo-seo-v2", "geowriter", "getuai-seo",
    "rankgale", "rankncompare", "rankncompare_v2", "seo-poster"
  ],
  "source-content-writing": [
    "geowriter", "seo-poster", "getuai-email-2.0",
    "openclaw-marketing", "OpenBox-Marketing", "Vibe-marketing", "LLMRush"
  ],
  "source-ads": [
    "getuai-ads", "getuai-ads-attribution", "getuai-ads-attribution-sdk",
    "getuai-ads-data", "getuai-ads-sdk", "getu_ads_v2",
    "attribution_v2", "Fast-Attribution", "ads-library", "facebook-ads-library-api-demo"
  ],
  "source-social": [
    "reddit-scount", "x-api-credit-monitor", "youtube-api-demo",
    "openclaw-marketing"
  ],
  "source-shared-infra": [
    "getuai-api", "getuai-console", "getuai-ui", "getuai-auth-center",
    "getuai-mvp", "getuai-plugin", "Pi", "Visionary", "clawcloud",
    "cloud-claw-k", "valuecell", "project-base",
    "optiminds-org-config", "optiminds-repo-template"
  ],
  "source-skills-catalog": [
    "*"
  ],
  "source-cognitive-models": [
    "*"
  ],
  "source-failure-modes": [
    "growth-engine-legacy", "growth-engine"
  ],
  "source-vertical-cases": [
    "lawyer_marketing", "lawyer_finder", "law-intake", "cuilawgroup"
  ],
  "source-platform-prototypes": [
    "0407-prototype", "0408-prototype", "getuai-2.0", "getuai-mvp",
    "gmi-prototype", "getuai-comp-analysis-demo", "getuai-competitor-analysis"
  ]
}
```

The `"*"` wildcard in `source-skills-catalog` and `source-cognitive-models` means
"all 64 repos contribute" — the composer pulls skill manifests / CLAUDE.md /
AGENTS.md / READMEs from every repo.

- [ ] **Step 2: Verify JSON parses and references real repos**

```bash
python3 - <<'EOF'
import json
from pathlib import Path
mapping = json.loads(Path("runs/growth-engine-from-scratch/source_mapping.json").read_text())
getuai = Path.home() / "dev" / "getuai"
all_repos = {p.name for p in getuai.iterdir() if p.is_dir() and not p.name.startswith(".")}
for source, repos in mapping.items():
    if repos == ["*"]:
        continue
    missing = [r for r in repos if r not in all_repos]
    if missing:
        print(f"WARNING {source} references missing repos: {missing}")
    else:
        print(f"OK {source}: {len(repos)} repos all present")
EOF
```

Expected: 8 lines of `OK ...`, 0 `WARNING ...` lines.

- [ ] **Step 3: Commit**

```bash
git add runs/growth-engine-from-scratch/source_mapping.json
git commit -m "feat(run): source_mapping.json — repo → source-*.md routing"
```

---

## Task 6: Write `extract_sources.py` with TDD

**Files:**
- Create: `scripts/extract_sources.py`
- Create: `tests/test_extract_sources.py`
- Create: `tests/fixtures/fake_getuai/repo-a/README.md`
- Create: `tests/fixtures/fake_getuai/repo-a/CLAUDE.md`
- Create: `tests/fixtures/fake_getuai/repo-a/skills/skill-1/SKILL.md`
- Create: `tests/fixtures/fake_getuai/repo-b/README.md`

The script walks one repo and emits one markdown file with all the relevant content
(README, CLAUDE.md, AGENTS.md, every `.md` under `skills/` / `.claude/skills/` /
`.cursor/skills/` / `.agents/skills/` directories). Each file becomes a section
prefixed with the path. The output is structured raw material — NO LLM in the
pipeline.

- [ ] **Step 1: Create test fixtures**

```bash
mkdir -p tests/fixtures/fake_getuai/repo-a/skills/skill-1
mkdir -p tests/fixtures/fake_getuai/repo-b
```

Write `tests/fixtures/fake_getuai/repo-a/README.md`:

```markdown
# Repo A

This is repo-a's README. It does growth-related things.
```

Write `tests/fixtures/fake_getuai/repo-a/CLAUDE.md`:

```markdown
# CLAUDE.md for repo-a

Hard rule: address the user as Tester.
```

Write `tests/fixtures/fake_getuai/repo-a/skills/skill-1/SKILL.md`:

```markdown
---
name: skill-1
description: a test skill
---

This skill does something.
```

Write `tests/fixtures/fake_getuai/repo-b/README.md`:

```markdown
# Repo B

Repo-b is similar but different.
```

- [ ] **Step 2: Write the failing test `tests/test_extract_sources.py`**

```python
"""Tests for extract_sources.py."""
from pathlib import Path
import subprocess
import sys


SCRIPT = Path("scripts/extract_sources.py")
FIXTURES = Path("tests/fixtures/fake_getuai")


def test_script_exists():
    assert SCRIPT.exists()


def test_extracts_readme_and_claude_and_skill(tmp_path):
    """Running extract on the fixture tree produces one markdown file per repo containing all relevant content."""
    out_dir = tmp_path / "_raw"
    subprocess.run(
        [sys.executable, str(SCRIPT), str(FIXTURES), str(out_dir)],
        check=True,
        cwd=Path.cwd(),
    )
    # one .md per repo
    files = sorted(out_dir.glob("*.md"))
    assert {p.stem for p in files} == {"repo-a", "repo-b"}, [p.stem for p in files]

    # repo-a content checks
    repo_a = (out_dir / "repo-a.md").read_text()
    assert "# Repo: repo-a" in repo_a
    assert "## README.md" in repo_a
    assert "This is repo-a's README" in repo_a
    assert "## CLAUDE.md" in repo_a
    assert "address the user as Tester" in repo_a
    assert "## skills/skill-1/SKILL.md" in repo_a
    assert "name: skill-1" in repo_a

    # repo-b minimal content
    repo_b = (out_dir / "repo-b.md").read_text()
    assert "# Repo: repo-b" in repo_b
    assert "Repo-b is similar but different" in repo_b


def test_skips_dotfile_repos(tmp_path):
    """A directory starting with '.' is not treated as a repo."""
    fake = tmp_path / "fake_getuai"
    (fake / ".cache" / "skills").mkdir(parents=True)
    (fake / ".cache" / "skills" / "S.md").write_text("not a repo")
    (fake / "real-repo").mkdir()
    (fake / "real-repo" / "README.md").write_text("# real")
    out = tmp_path / "out"
    subprocess.run(
        [sys.executable, str(SCRIPT), str(fake), str(out)],
        check=True,
        cwd=Path.cwd(),
    )
    assert (out / "real-repo.md").exists()
    assert not (out / ".cache.md").exists()
```

- [ ] **Step 3: Run test, verify fail**

```bash
uv run pytest tests/test_extract_sources.py -v
```

Expected: FAIL — script does not exist.

- [ ] **Step 4: Write `scripts/extract_sources.py`**

```python
#!/usr/bin/env python3
"""Walk a getuai-like directory tree and emit per-repo raw markdown extracts.

Usage: python scripts/extract_sources.py <getuai_root> <output_dir>

For each subdirectory of <getuai_root> not starting with '.', extract:
- README.md (top level)
- CLAUDE.md / AGENTS.md / agents.md (top level)
- Every *.md under skills/, .claude/skills/, .cursor/skills/, .agents/skills/

Emit one markdown file per repo with structured sections.
"""
from __future__ import annotations

import sys
from pathlib import Path


SKILL_DIR_PATTERNS = [
    "skills",
    ".claude/skills",
    ".cursor/skills",
    ".agents/skills",
]
TOP_LEVEL_DOCS = ["README.md", "CLAUDE.md", "AGENTS.md", "agents.md"]
MAX_SKILL_BYTES = 8000  # truncate huge skill files to keep extracts manageable


def safe_read(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None


def extract_repo(repo_path: Path) -> str:
    """Return a markdown string for one repo."""
    sections: list[str] = [f"# Repo: {repo_path.name}\n"]

    for fname in TOP_LEVEL_DOCS:
        f = repo_path / fname
        if f.is_file():
            content = safe_read(f)
            if content is not None:
                sections.append(f"\n## {fname}\n```markdown\n{content}\n```\n")

    for pattern in SKILL_DIR_PATTERNS:
        skill_dir = repo_path / pattern
        if not skill_dir.is_dir():
            continue
        for skill_md in sorted(skill_dir.rglob("*.md")):
            try:
                rel = skill_md.relative_to(repo_path)
            except ValueError:
                continue
            content = safe_read(skill_md)
            if content is None:
                continue
            if len(content) > MAX_SKILL_BYTES:
                content = content[:MAX_SKILL_BYTES] + "\n\n[... truncated to 8KB ...]\n"
            sections.append(f"\n## {rel}\n```markdown\n{content}\n```\n")

    return "".join(sections)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: extract_sources.py <getuai_root> <output_dir>", file=sys.stderr)
        return 2
    root = Path(argv[1])
    out_dir = Path(argv[2])
    if not root.is_dir():
        print(f"ERROR: {root} is not a directory", file=sys.stderr)
        return 1
    out_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    for child in sorted(root.iterdir()):
        if not child.is_dir() or child.name.startswith("."):
            continue
        markdown = extract_repo(child)
        out = out_dir / f"{child.name}.md"
        out.write_text(markdown, encoding="utf-8")
        count += 1
        print(f"wrote {out}")

    print(f"\ntotal: {count} repos extracted")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
```

- [ ] **Step 5: Run tests, verify pass**

```bash
uv run pytest tests/test_extract_sources.py -v
```

Expected: 3 passed.

- [ ] **Step 6: Commit**

```bash
git add scripts/extract_sources.py tests/test_extract_sources.py tests/fixtures/fake_getuai/
git commit -m "feat(run): extract_sources.py walks getuai/ and emits per-repo raw markdown"
```

---

## Task 7: Run extract_sources.py against ~/dev/getuai/

**Files:**
- Output: `runs/growth-engine-from-scratch/sources/_raw/<repo>.md` (×64)

This step runs the script for real and produces the 64 raw extracts.

- [ ] **Step 1: Run the extractor**

```bash
python3 scripts/extract_sources.py \
  ~/dev/getuai \
  runs/growth-engine-from-scratch/sources/_raw
```

Expected: ~64 `wrote ...` lines, then `total: 64 repos extracted` (count may vary slightly).

- [ ] **Step 2: Sanity check the output**

```bash
ls runs/growth-engine-from-scratch/sources/_raw | wc -l
echo "---"
du -sh runs/growth-engine-from-scratch/sources/_raw
echo "---"
# spot check three big ones
for repo in growth-engine growth-engine-legacy lawyer_marketing; do
  echo "=== $repo ==="
  head -20 runs/growth-engine-from-scratch/sources/_raw/${repo}.md 2>/dev/null
done
```

Expected: 60-70 files; total size 5-50 MB; the `head -20` output shows real content for each.

- [ ] **Step 3: Commit**

```bash
git add runs/growth-engine-from-scratch/sources/_raw/
git commit -m "feat(run): generate per-repo raw extracts from ~/dev/getuai/ (64 repos)"
```

---

## Task 8: Write `compose_sources.py` with TDD — produces the 10 source-*.md digests

**Files:**
- Create: `scripts/compose_sources.py`
- Create: `tests/test_compose_sources.py`

The composer reads `source_mapping.json` and the per-repo `_raw/<repo>.md` files,
concatenating them into 10 `source-*.md` digests with TOC and per-repo section
headings. For wildcard sources (`source-skills-catalog`, `source-cognitive-models`),
it uses ALL repos in `_raw/`. The output is deterministic raw-material concatenation
— spec §3 calls for "structured digests, not raw dumps" but Path B accepts the
structured-concatenation interpretation for speed; LLM-driven re-summarization is
out of scope for this plan and can be a separate enhancement after iter-1.

- [ ] **Step 1: Write the failing test**

```python
"""Tests for compose_sources.py."""
from pathlib import Path
import json
import subprocess
import sys


SCRIPT = Path("scripts/compose_sources.py")


def setup_inputs(tmp_path: Path) -> tuple[Path, Path, Path]:
    raw = tmp_path / "_raw"
    raw.mkdir()
    (raw / "alpha.md").write_text("# Repo: alpha\n## README.md\n```markdown\nALPHA-CONTENT\n```\n")
    (raw / "beta.md").write_text("# Repo: beta\n## README.md\n```markdown\nBETA-CONTENT\n```\n")
    (raw / "gamma.md").write_text("# Repo: gamma\n## README.md\n```markdown\nGAMMA-CONTENT\n```\n")
    mapping = tmp_path / "source_mapping.json"
    mapping.write_text(json.dumps({
        "source-foo": ["alpha", "beta"],
        "source-bar": ["*"],
    }))
    out_dir = tmp_path / "out"
    return raw, mapping, out_dir


def test_named_repos_are_concatenated(tmp_path):
    raw, mapping, out = setup_inputs(tmp_path)
    subprocess.run(
        [sys.executable, str(SCRIPT), str(raw), str(mapping), str(out)],
        check=True, cwd=Path.cwd(),
    )
    foo = (out / "source-foo.md").read_text()
    assert "ALPHA-CONTENT" in foo
    assert "BETA-CONTENT" in foo
    assert "GAMMA-CONTENT" not in foo  # not in source-foo's mapping


def test_wildcard_includes_all_repos(tmp_path):
    raw, mapping, out = setup_inputs(tmp_path)
    subprocess.run(
        [sys.executable, str(SCRIPT), str(raw), str(mapping), str(out)],
        check=True, cwd=Path.cwd(),
    )
    bar = (out / "source-bar.md").read_text()
    assert "ALPHA-CONTENT" in bar
    assert "BETA-CONTENT" in bar
    assert "GAMMA-CONTENT" in bar


def test_outputs_have_toc(tmp_path):
    raw, mapping, out = setup_inputs(tmp_path)
    subprocess.run(
        [sys.executable, str(SCRIPT), str(raw), str(mapping), str(out)],
        check=True, cwd=Path.cwd(),
    )
    foo = (out / "source-foo.md").read_text()
    assert "## Table of Contents" in foo
    assert "- alpha" in foo
    assert "- beta" in foo


def test_missing_repo_in_mapping_warns_but_succeeds(tmp_path):
    raw, mapping, out = setup_inputs(tmp_path)
    # add a mapping entry for a repo whose _raw file doesn't exist
    data = json.loads(mapping.read_text())
    data["source-foo"].append("nonexistent")
    mapping.write_text(json.dumps(data))
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(raw), str(mapping), str(out)],
        capture_output=True, text=True, cwd=Path.cwd(),
    )
    assert result.returncode == 0  # graceful
    assert "WARNING" in result.stdout or "WARNING" in result.stderr
```

- [ ] **Step 2: Run test, verify fail**

```bash
uv run pytest tests/test_compose_sources.py -v
```

Expected: FAIL — script does not exist.

- [ ] **Step 3: Write `scripts/compose_sources.py`**

```python
#!/usr/bin/env python3
"""Compose 10 source-*.md digests from per-repo raw extracts and a mapping.

Usage: python scripts/compose_sources.py <raw_dir> <mapping.json> <out_dir>

Reads source_mapping.json. For each named source file, concatenates the relevant
per-repo extracts under <raw_dir>/<repo>.md with a TOC and per-repo section
headings. The wildcard mapping value ["*"] expands to all repos found under
<raw_dir>.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def list_all_repos(raw_dir: Path) -> list[str]:
    return sorted(p.stem for p in raw_dir.glob("*.md"))


def compose_one(source_name: str, repos: list[str], raw_dir: Path) -> str:
    sections: list[str] = []
    sections.append(f"# {source_name}\n")
    sections.append(
        f"\nSource digest auto-composed from {len(repos)} per-repo raw extracts under "
        f"`runs/growth-engine-from-scratch/sources/_raw/`. Producer cites sections "
        f"using `source-*.md§Repo: <name>` per §6.3.\n"
    )
    sections.append("\n## Table of Contents\n")
    for r in repos:
        sections.append(f"- {r}\n")

    sections.append("\n---\n")

    for repo in repos:
        raw_file = raw_dir / f"{repo}.md"
        if not raw_file.exists():
            print(f"WARNING: {raw_file} missing for {source_name}", file=sys.stderr)
            sections.append(f"\n## Repo: {repo}\n\n*Raw extract not found.*\n")
            continue
        sections.append(f"\n{raw_file.read_text(encoding='utf-8')}\n")

    return "".join(sections)


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print("usage: compose_sources.py <raw_dir> <mapping.json> <out_dir>", file=sys.stderr)
        return 2
    raw_dir = Path(argv[1])
    mapping_path = Path(argv[2])
    out_dir = Path(argv[3])

    if not raw_dir.is_dir():
        print(f"ERROR: {raw_dir} not a directory", file=sys.stderr)
        return 1

    mapping = json.loads(mapping_path.read_text())
    out_dir.mkdir(parents=True, exist_ok=True)

    all_repos = list_all_repos(raw_dir)

    for source_name, repos in mapping.items():
        if repos == ["*"]:
            repos = all_repos
        out = out_dir / f"{source_name}.md"
        out.write_text(compose_one(source_name, repos, raw_dir), encoding="utf-8")
        print(f"wrote {out} ({len(repos)} repos)")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
```

- [ ] **Step 4: Run tests, verify pass**

```bash
uv run pytest tests/test_compose_sources.py -v
```

Expected: 4 passed.

- [ ] **Step 5: Commit**

```bash
git add scripts/compose_sources.py tests/test_compose_sources.py
git commit -m "feat(run): compose_sources.py composes 10 digests from raw extracts + mapping"
```

---

## Task 9: Run compose_sources.py to generate the 10 source-*.md digests

**Files:**
- Output: `runs/growth-engine-from-scratch/sources/source-*.md` (×10)

- [ ] **Step 1: Run the composer**

```bash
python3 scripts/compose_sources.py \
  runs/growth-engine-from-scratch/sources/_raw \
  runs/growth-engine-from-scratch/source_mapping.json \
  runs/growth-engine-from-scratch/sources
```

Expected: 10 lines like `wrote runs/growth-engine-from-scratch/sources/source-XXX.md (N repos)`.

- [ ] **Step 2: Verify the 10 digests exist and have content**

```bash
ls runs/growth-engine-from-scratch/sources/source-*.md
echo "---"
wc -l runs/growth-engine-from-scratch/sources/source-*.md
echo "---"
du -sh runs/growth-engine-from-scratch/sources/source-*.md
```

Expected: 10 files; sizes vary widely (skills-catalog and cognitive-models will be
multi-MB since they include all 64 repos; others are smaller).

- [ ] **Step 3: Spot-check that key markers are present**

```bash
grep -l "growth-engine-legacy" runs/growth-engine-from-scratch/sources/source-failure-modes.md && echo "OK: failure-modes references growth-engine-legacy"
grep -l "lawyer_marketing" runs/growth-engine-from-scratch/sources/source-vertical-cases.md && echo "OK: vertical-cases references lawyer_marketing"
grep -l "Repo: geo-aeo" runs/growth-engine-from-scratch/sources/source-seo-geo.md && echo "OK: seo-geo references geo-aeo"
```

Expected: 3× `OK: ...`.

- [ ] **Step 4: Commit**

```bash
git add runs/growth-engine-from-scratch/sources/source-*.md
git commit -m "feat(run): compose 10 source-*.md digests from getuai/ corpus"
```

---

## Task 10: Mock-iterate to verify run shape

**Files:**
- No new files (the framework writes its own outputs).

This is the smoke test. Running `autoresearch iterate ... --provider mock` exercises
the full read path: framework loads `run.json`, parses `topic.md` / `program.md` /
`benchmark.json`, lists `sources/`, and runs ONE iteration with the mock provider
(which produces a deterministic placeholder change). If the run is malformed, this
will fail loudly.

- [ ] **Step 1: Run a single mock iteration**

```bash
uv run autoresearch iterate runs/growth-engine-from-scratch --provider mock
```

Expected: succeeds with a 0 exit code; framework prints something like
`iteration 1 complete, score: <number>`.

- [ ] **Step 2: Inspect the iteration artifacts**

```bash
ls runs/growth-engine-from-scratch/artifacts/
echo "---"
cat runs/growth-engine-from-scratch/results.tsv 2>/dev/null
echo "---"
cat runs/growth-engine-from-scratch/state.json 2>/dev/null
```

Expected: `artifacts/iteration-1/` exists; `results.tsv` has one data row;
`state.json` is non-empty.

- [ ] **Step 3: Verify the run is in a clean state for iter-1 with real producer**

```bash
uv run autoresearch status runs/growth-engine-from-scratch --json
```

Expected: JSON output showing run is initialized, `last_iteration: 1` (the mock
iteration), benchmark count: 15, source count: 10.

- [ ] **Step 4: Commit any artifacts the framework wrote**

```bash
git add runs/growth-engine-from-scratch/artifacts \
        runs/growth-engine-from-scratch/results.tsv \
        runs/growth-engine-from-scratch/state.json \
        runs/growth-engine-from-scratch/judge_feedback.md \
        runs/growth-engine-from-scratch/human_feedback.md 2>/dev/null
git commit -m "chore(run): record mock iter-1 verification artifacts" --allow-empty
```

---

## Task 11: Final verification + handoff doc

**Files:**
- Modify: `runs/growth-engine-from-scratch/topic.md` — append "Run-init verification" section

- [ ] **Step 1: Append a short verification section to `topic.md`**

```markdown

---

## Run-Init Verification (Path B, 2026-05-02)

- ✅ All 10 `sources/source-*.md` digests composed from 64-repo `_raw/` extracts
- ✅ `benchmark.json` contains 15 questions extracted from spec §5
- ✅ `topic.md`, `program.md`, `run.json`, `knowledge_base.md` seeded
- ✅ Mock iteration completed; framework reads run cleanly
- ⏸ DEFERRED: provisional anchors (§6.10 — progressive crystallization)
- ⏸ DEFERRED: §8.6 OS sandbox + point-verify tool (honor-system risk accepted for early iters)
- ⏭ NEXT: trigger iter-1 with real producer/judge:

  ```bash
  uv run autoresearch loop runs/growth-engine-from-scratch \
    --producer codex --judge claude \
    --tag growth-v1 \
    --max-total-iterations 40 \
    --dimension-threshold 0.80
  ```
```

- [ ] **Step 2: Commit**

```bash
git add runs/growth-engine-from-scratch/topic.md
git commit -m "docs(run): record Path B run-init verification status"
```

---

## Self-Review Notes

**Spec coverage:** Each spec §1–§9 element is addressed:
- §1 Goal → Task 3 topic.md scope/goal sections.
- §2 Non-Goals → Task 3 topic.md non-goals.
- §3 Source Set Strategy → Tasks 5, 6, 7, 8, 9 (mapping + extract + compose).
- §4 Benchmark Structure → Task 2 benchmark.json + Task 4 program.md lanes.
- §5 Benchmark Questions → Task 2 benchmark.json (the 15 question objects with rubric_criteria + penalty_criteria).
- §6 Calibration → Task 4 program.md hard-rules section.
- §7 Run Configuration → Task 1 run.json (provider/judge/threshold) + Task 11 next-step loop command.
- §8 Resolved Decisions → Task 3 topic.md ambiguities-resolved section.
- §8.4 anchors deferred (Path B) → Task 11 explicit DEFERRED note.
- §8.6 sandbox deferred (Path B) → Task 11 explicit DEFERRED note.
- §9 Definition of Done → Task 10 mock iteration + Task 11 verification section.

**Placeholder scan:** No `TBD` / `TODO` / `fill in later` / "similar to Task N" patterns. Every code block contains the actual content.

**Type consistency:** Filenames stable (`extract_benchmark.py`, `extract_sources.py`, `compose_sources.py`); `source_mapping.json` location stable across Tasks 5, 8, 9; `_raw/` directory location stable across Tasks 6, 7, 8, 9.

**Path-B contract honored:** Plan does NOT create `judge_calibration.md` or `point-verify` tool — these are deferred per the user's decision. Task 11 makes the deferral explicit so the next person in the workflow knows what's pending.
