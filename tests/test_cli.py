from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from llm_autoresearch.cli import main  # noqa: E402


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


if __name__ == "__main__":
    unittest.main()
