from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from llm_autoresearch.cli import build_parser, main  # noqa: E402


class CLISmokeTest(unittest.TestCase):
    def test_init_and_iterate_with_mock_provider(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "example-run"

            init_code = main(["init", str(run_dir), "--example"])
            self.assertEqual(init_code, 0)
            self.assertTrue((run_dir / "run.json").exists())
            self.assertTrue((run_dir / "sources" / "source-1.md").exists())

            iterate_code = main(["iterate", str(run_dir), "--provider", "mock"])
            self.assertEqual(iterate_code, 0)
            second_iterate = main(["iterate", str(run_dir), "--provider", "mock"])
            self.assertEqual(second_iterate, 0)
            third_iterate = main(["iterate", str(run_dir), "--provider", "mock"])
            self.assertEqual(third_iterate, 0)

            results_tsv = (run_dir / "results.tsv").read_text(encoding="utf-8")
            self.assertIn("status", results_tsv)
            self.assertIn("keep", results_tsv)
            self.assertIn("discard", results_tsv)

            knowledge_base = (run_dir / "knowledge_base.md").read_text(encoding="utf-8")
            self.assertIn("Roman concrete", knowledge_base)
            self.assertTrue((run_dir / "artifacts" / "iteration-0001" / "evaluation.json").exists())
            self.assertTrue((run_dir / "artifacts" / "iteration-0003" / "evaluation.json").exists())


class CLIParserTest(unittest.TestCase):
    def test_status_subcommand_parses(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["status", "/tmp/run", "--session", "main", "--json"])
        self.assertEqual(args.subcommand, "status")
        self.assertEqual(args.run_dir, "/tmp/run")
        self.assertEqual(args.session, "main")
        self.assertTrue(args.json_output)

    def test_supervise_subcommand_parses(self) -> None:
        parser = build_parser()
        args = parser.parse_args(
            [
                "supervise",
                "/tmp/run",
                "--tag",
                "run-tag",
                "--main-session",
                "main-session",
                "--producer",
                "codex",
                "--judge",
                "claude",
                "--interval",
                "120",
            ]
        )
        self.assertEqual(args.subcommand, "supervise")
        self.assertEqual(args.tag, "run-tag")
        self.assertEqual(args.main_session, "main-session")
        self.assertEqual(args.producer, "codex")
        self.assertEqual(args.judge, "claude")
        self.assertEqual(args.interval, 120)


if __name__ == "__main__":
    unittest.main()
