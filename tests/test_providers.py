from __future__ import annotations

import json
import os
import signal
import stat
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from llm_autoresearch.providers import (  # noqa: E402
    CliAgentProvider,
    ProviderError,
    ProviderTask,
    create_provider,
)


def _make_mock_cli_script(script_path: Path, json_output: dict) -> None:
    """Create a Python script that outputs the given JSON to stdout."""
    json_str = json.dumps(json_output)
    script_path.write_text(
        f"""#!/usr/bin/env python3
import sys
# Read the prompt file path from -p argument
args = sys.argv[1:]
# Output JSON
print({json_str!r})
""",
        encoding="utf-8",
    )
    script_path.chmod(script_path.stat().st_mode | stat.S_IEXEC)


def _make_preamble_cli_script(script_path: Path, json_output: dict) -> None:
    """Create a script that outputs non-JSON preamble before JSON."""
    json_str = json.dumps(json_output)
    script_path.write_text(
        f"""#!/usr/bin/env python3
import sys
print("Loading model...")
print("Ready.")
print({json_str!r})
""",
        encoding="utf-8",
    )
    script_path.chmod(script_path.stat().st_mode | stat.S_IEXEC)


def _make_slow_cli_script(script_path: Path) -> None:
    """Create a script that sleeps for a long time (for timeout testing)."""
    script_path.write_text(
        """#!/usr/bin/env python3
import time
import signal
signal.signal(signal.SIGTERM, signal.SIG_DFL)
time.sleep(300)
print('{"result": "should not reach here"}')
""",
        encoding="utf-8",
    )
    script_path.chmod(script_path.stat().st_mode | stat.S_IEXEC)


def _make_failing_cli_script(script_path: Path) -> None:
    """Create a script that exits with error."""
    script_path.write_text(
        """#!/usr/bin/env python3
import sys
print("Error: something went wrong", file=sys.stderr)
sys.exit(1)
""",
        encoding="utf-8",
    )
    script_path.chmod(script_path.stat().st_mode | stat.S_IEXEC)


def _sample_task() -> ProviderTask:
    return ProviderTask(
        task_type="research_iteration",
        instructions="Test instructions",
        payload={"topic": "test-topic", "state": {"iteration": 0}},
    )


class TestCliAgentProviderSpawn(unittest.TestCase):
    """Test that CliAgentProvider spawns a CLI subprocess and parses JSON output."""

    def test_basic_invocation(self) -> None:
        expected = {"experiment_title": "test", "result": "ok"}
        with tempfile.TemporaryDirectory() as tmp:
            script = Path(tmp) / "mock_cli.py"
            _make_mock_cli_script(script, expected)

            provider = CliAgentProvider(
                cli_binary=sys.executable,
                cli_flags=str(script) + " -p",
                role="producer",
            )
            result = provider.invoke(_sample_task())
            self.assertEqual(result["experiment_title"], "test")
            self.assertEqual(result["result"], "ok")

    def test_prompt_written_to_temp_file(self) -> None:
        """Verify the provider writes the task JSON to a temp file."""
        with tempfile.TemporaryDirectory() as tmp:
            # Script that reads the prompt file and echoes its content in JSON
            script = Path(tmp) / "echo_prompt.py"
            script.write_text(
                """#!/usr/bin/env python3
import sys
import json

# Find the -p argument and read the file
args = sys.argv[1:]
prompt_content = None
for i, arg in enumerate(args):
    if arg == "-p" and i + 1 < len(args):
        prompt_content = args[i + 1]
        break

print(json.dumps({"prompt_received": prompt_content is not None, "prompt_length": len(prompt_content) if prompt_content else 0}))
""",
                encoding="utf-8",
            )
            script.chmod(script.stat().st_mode | stat.S_IEXEC)

            provider = CliAgentProvider(
                cli_binary=sys.executable,
                cli_flags=str(script) + " -p",
                role="producer",
            )
            result = provider.invoke(_sample_task())
            self.assertTrue(result["prompt_received"])
            self.assertGreater(result["prompt_length"], 0)


class TestCliAgentProviderJsonParsing(unittest.TestCase):
    """Test JSON extraction from mixed stdout."""

    def test_json_with_preamble(self) -> None:
        """Provider should find first { and parse JSON from there."""
        expected = {"experiment_title": "preamble-test", "status": "ok"}
        with tempfile.TemporaryDirectory() as tmp:
            script = Path(tmp) / "preamble_cli.py"
            _make_preamble_cli_script(script, expected)

            provider = CliAgentProvider(
                cli_binary=sys.executable,
                cli_flags=str(script) + " -p",
                role="producer",
            )
            result = provider.invoke(_sample_task())
            self.assertEqual(result["experiment_title"], "preamble-test")
            self.assertEqual(result["status"], "ok")

    def test_no_json_in_output(self) -> None:
        """Should raise ProviderError when stdout has no JSON."""
        with tempfile.TemporaryDirectory() as tmp:
            script = Path(tmp) / "no_json.py"
            script.write_text(
                """#!/usr/bin/env python3
print("no json here")
""",
                encoding="utf-8",
            )
            script.chmod(script.stat().st_mode | stat.S_IEXEC)

            provider = CliAgentProvider(
                cli_binary=sys.executable,
                cli_flags=str(script) + " -p",
                role="producer",
            )
            with self.assertRaises(ProviderError):
                provider.invoke(_sample_task())

    def test_extracts_json_from_result_array(self) -> None:
        """Claude-style JSON envelopes should yield the final structured result."""
        payload = [
            {"type": "assistant", "message": {"content": [{"type": "text", "text": "ignore me"}]}},
            {
                "type": "result",
                "result": '{"experiment_title":"array-test","status":"ok"}',
            },
        ]

        result = CliAgentProvider._extract_json(json.dumps(payload))
        self.assertEqual(result["experiment_title"], "array-test")
        self.assertEqual(result["status"], "ok")

    def test_extracts_first_json_object_with_trailing_text(self) -> None:
        stdout = (
            '{"dimension_scores":{"quality":8},"priority_dimension":"quality",'
            '"review_markdown":"good","improvement_suggestion":"none"}\n'
            "```"
        )

        result = CliAgentProvider._extract_json(stdout)
        self.assertEqual(result["priority_dimension"], "quality")
        self.assertEqual(result["dimension_scores"]["quality"], 8)

    def test_invalid_json_after_brace(self) -> None:
        """Should raise ProviderError when JSON after { is malformed."""
        with tempfile.TemporaryDirectory() as tmp:
            script = Path(tmp) / "bad_json.py"
            script.write_text(
                """#!/usr/bin/env python3
print("{not valid json at all")
""",
                encoding="utf-8",
            )
            script.chmod(script.stat().st_mode | stat.S_IEXEC)

            provider = CliAgentProvider(
                cli_binary=sys.executable,
                cli_flags=str(script) + " -p",
                role="producer",
            )
            with self.assertRaises(ProviderError):
                provider.invoke(_sample_task())


class TestCliAgentProviderTimeout(unittest.TestCase):
    """Test timeout handling with process group killing."""

    def test_timeout_kills_process(self) -> None:
        """Provider should kill slow process and raise ProviderError."""
        with tempfile.TemporaryDirectory() as tmp:
            script = Path(tmp) / "slow_cli.py"
            _make_slow_cli_script(script)

            provider = CliAgentProvider(
                cli_binary=sys.executable,
                cli_flags=str(script) + " -p",
                role="producer",
                timeout=2,  # 2 second timeout
            )
            with self.assertRaises(ProviderError) as ctx:
                provider.invoke(_sample_task())
            self.assertIn("timeout", str(ctx.exception).lower())


class TestCliAgentProviderErrors(unittest.TestCase):
    """Test error handling."""

    def test_nonzero_exit_code(self) -> None:
        """Should raise ProviderError on non-zero exit."""
        with tempfile.TemporaryDirectory() as tmp:
            script = Path(tmp) / "fail_cli.py"
            _make_failing_cli_script(script)

            provider = CliAgentProvider(
                cli_binary=sys.executable,
                cli_flags=str(script) + " -p",
                role="producer",
            )
            with self.assertRaises(ProviderError):
                provider.invoke(_sample_task())

    def test_missing_binary(self) -> None:
        """Should raise ProviderError when binary doesn't exist."""
        provider = CliAgentProvider(
            cli_binary="/nonexistent/binary",
            cli_flags="-p",
            role="producer",
        )
        with self.assertRaises(ProviderError):
            provider.invoke(_sample_task())


class TestCreateProviderCli(unittest.TestCase):
    """Test create_provider with kind='cli'."""

    def test_create_cli_provider(self) -> None:
        provider = create_provider(
            kind="cli",
            cli_binary="codex",
            cli_flags="-q --json --approval-mode full-auto",
        )
        self.assertIsInstance(provider, CliAgentProvider)

    def test_create_cli_provider_default_flags(self) -> None:
        provider = create_provider(kind="cli", cli_binary="claude")
        self.assertIsInstance(provider, CliAgentProvider)

    def test_create_mock_still_works(self) -> None:
        """Backwards compatibility: mock provider still works."""
        from llm_autoresearch.providers import MockProvider

        provider = create_provider(kind="mock")
        self.assertIsInstance(provider, MockProvider)

    def test_create_command_still_works(self) -> None:
        """Backwards compatibility: command provider still works."""
        from llm_autoresearch.providers import CommandProvider

        provider = create_provider(kind="command", command="echo test")
        self.assertIsInstance(provider, CommandProvider)


class TestCliAgentConfig(unittest.TestCase):
    """Test CliAgentConfig model and RunConfig role configs."""

    def test_cli_agent_config_from_dict(self) -> None:
        from llm_autoresearch.models import CliAgentConfig

        data = {"cli": "codex", "flags": "-q --json --approval-mode full-auto"}
        config = CliAgentConfig.from_dict(data)
        self.assertEqual(config.cli, "codex")
        self.assertEqual(config.flags, "-q --json --approval-mode full-auto")

    def test_cli_agent_config_defaults(self) -> None:
        from llm_autoresearch.models import CliAgentConfig

        config = CliAgentConfig()
        self.assertEqual(config.cli, "")
        self.assertEqual(config.flags, "")

    def test_run_config_with_roles(self) -> None:
        from llm_autoresearch.models import CliAgentConfig, RunConfig

        data = {
            "topic": "test",
            "slug": "test-slug",
            "producer": {
                "cli": "codex",
                "flags": "-q --json --approval-mode full-auto",
            },
            "judge": {
                "cli": "claude",
                "flags": "--output-format json --dangerously-skip-permissions",
            },
        }
        config = RunConfig.from_dict(data)
        self.assertEqual(config.producer.cli, "codex")
        self.assertEqual(config.producer.flags, "-q --json --approval-mode full-auto")
        self.assertEqual(config.judge.cli, "claude")
        self.assertEqual(
            config.judge.flags,
            "--output-format json --dangerously-skip-permissions",
        )

    def test_run_config_roles_default_empty(self) -> None:
        from llm_autoresearch.models import RunConfig

        data = {"topic": "test", "slug": "test-slug"}
        config = RunConfig.from_dict(data)
        self.assertEqual(config.producer.cli, "")
        self.assertEqual(config.producer.flags, "")
        self.assertEqual(config.judge.cli, "")
        self.assertEqual(config.judge.flags, "")

    def test_run_config_to_dict_includes_roles(self) -> None:
        from llm_autoresearch.models import CliAgentConfig, RunConfig

        config = RunConfig(
            topic="test",
            slug="test-slug",
            producer=CliAgentConfig(cli="codex", flags="-q --json"),
            judge=CliAgentConfig(cli="claude", flags="--output-format json"),
        )
        d = config.to_dict()
        self.assertIn("producer", d)
        self.assertIn("judge", d)
        self.assertEqual(d["producer"]["cli"], "codex")
        self.assertEqual(d["judge"]["cli"], "claude")

    def test_run_config_roundtrip(self) -> None:
        from llm_autoresearch.models import CliAgentConfig, RunConfig

        original = RunConfig(
            topic="test",
            slug="test-slug",
            producer=CliAgentConfig(cli="codex", flags="-q --json"),
            judge=CliAgentConfig(cli="claude", flags="--output-format json"),
        )
        d = original.to_dict()
        restored = RunConfig.from_dict(d)
        self.assertEqual(restored.producer.cli, original.producer.cli)
        self.assertEqual(restored.producer.flags, original.producer.flags)
        self.assertEqual(restored.judge.cli, original.judge.cli)
        self.assertEqual(restored.judge.flags, original.judge.flags)


if __name__ == "__main__":
    unittest.main()
