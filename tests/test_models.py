from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


class TestResearchResponseParsing(unittest.TestCase):
    def test_accepts_benchmark_answer_map(self) -> None:
        from llm_autoresearch.models import ResearchResponse

        raw = {
            "experiment_title": "map-shape",
            "change_summary": ["First change", "Second change"],
            "knowledge_base_markdown": "# KB",
            "benchmark_answers": {
                "q1": {
                    "answer": "Answer 1",
                    "citations": "source-a, source-b",
                },
                "q2": "Answer 2",
            },
            "notes": '["note-1", "note-2"]',
        }

        response = ResearchResponse.from_dict(raw)

        self.assertEqual(response.experiment_title, "map-shape")
        self.assertIn("First change", response.change_summary)
        self.assertEqual(len(response.benchmark_answers), 2)
        self.assertEqual(response.benchmark_answers[0].id, "q1")
        self.assertEqual(response.benchmark_answers[0].citations, ["source-a", "source-b"])
        self.assertEqual(response.benchmark_answers[1].id, "q2")
        self.assertEqual(response.benchmark_answers[1].answer, "Answer 2")
        self.assertEqual(response.notes, ["note-1", "note-2"])

    def test_accepts_stringified_benchmark_answers_json(self) -> None:
        from llm_autoresearch.models import ResearchResponse

        raw = {
            "experiment_title": "string-json",
            "change_summary": "",
            "knowledge_base_markdown": "# KB",
            "benchmark_answers": (
                '{"q1":{"answer":"Answer 1","citations":["source-a"]},'
                '"q2":{"text":"Answer 2","citations":"source-b"}}'
            ),
        }

        response = ResearchResponse.from_dict(raw)

        self.assertEqual(len(response.benchmark_answers), 2)
        self.assertEqual(response.benchmark_answers[0].id, "q1")
        self.assertEqual(response.benchmark_answers[1].id, "q2")
        self.assertEqual(response.benchmark_answers[1].citations, ["source-b"])

    def test_accepts_python_literal_strings(self) -> None:
        from llm_autoresearch.models import ResearchResponse

        raw = {
            "experiment_title": "python-literal",
            "change_summary": "['First change', 'Second change']",
            "knowledge_base_markdown": "# KB",
            "benchmark_answers": (
                "{'q1': {'answer': 'Answer 1', 'citations': ['source-a']}, "
                "'q2': {'answer': 'Answer 2', 'citations': 'source-b'}}"
            ),
        }

        response = ResearchResponse.from_dict(raw)

        self.assertEqual(len(response.benchmark_answers), 2)
        self.assertIn("First change", response.change_summary)
        self.assertEqual(response.benchmark_answers[1].citations, ["source-b"])

    def test_backfills_citations_from_inline_source_tags(self) -> None:
        from llm_autoresearch.models import ResearchResponse

        raw = {
            "experiment_title": "inline-citations",
            "change_summary": "",
            "knowledge_base_markdown": "# KB",
            "benchmark_answers": [
                {
                    "id": "q1",
                    "answer": "Answer with evidence [source-a] and more evidence [source-b].",
                    "citations": [],
                }
            ],
        }

        response = ResearchResponse.from_dict(raw)

        self.assertEqual(response.benchmark_answers[0].citations, ["source-a", "source-b"])

    def test_merges_explicit_and_inline_citations_without_duplicates(self) -> None:
        from llm_autoresearch.models import ResearchResponse

        raw = {
            "experiment_title": "merged-citations",
            "change_summary": "",
            "knowledge_base_markdown": "# KB",
            "benchmark_answers": [
                {
                    "id": "q1",
                    "answer": "Answer with evidence [source-b] and [source-c].",
                    "citations": ["source-a", "[source-b]", "source-a"],
                }
            ],
        }

        response = ResearchResponse.from_dict(raw)

        self.assertEqual(
            response.benchmark_answers[0].citations,
            ["source-a", "source-b", "source-c"],
        )


if __name__ == "__main__":
    unittest.main()
