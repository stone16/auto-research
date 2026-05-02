"""Tests for extract_benchmark.py — parses the design spec into benchmark.json."""
from pathlib import Path
import json
import subprocess
import sys


SPEC = Path("docs/superpowers/specs/2026-05-01-growth-engine-from-scratch-design.md")
SCRIPT = Path("scripts/extract_benchmark.py")


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
