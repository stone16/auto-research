from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from llm_autoresearch.models import GoalState, QualityDimension  # noqa: E402
from llm_autoresearch.run_files import (  # noqa: E402
    RunContext,
    init_run,
    load_run_context,
    parse_goal_state,
)
from llm_autoresearch.templates import default_topic  # noqa: E402


class TestQualityDimensionModel(unittest.TestCase):
    """Tests for the QualityDimension dataclass."""

    def test_quality_dimension_fields(self) -> None:
        dim = QualityDimension(name="Causal Completeness", description="Covers all causal links")
        self.assertEqual(dim.name, "Causal Completeness")
        self.assertEqual(dim.description, "Covers all causal links")

    def test_quality_dimension_no_max_score(self) -> None:
        """QualityDimension should NOT have a max_score field -- all dimensions are 0-10."""
        dim = QualityDimension(name="Test", description="Test desc")
        self.assertFalse(hasattr(dim, "max_score"))


class TestGoalStateModel(unittest.TestCase):
    """Tests for the GoalState dataclass."""

    def test_goal_state_fields(self) -> None:
        dims = [
            QualityDimension(name="A", description="Desc A"),
            QualityDimension(name="B", description="Desc B"),
        ]
        gs = GoalState(done_definition="The research is complete.", dimensions=dims)
        self.assertEqual(gs.done_definition, "The research is complete.")
        self.assertEqual(len(gs.dimensions), 2)
        self.assertEqual(gs.dimensions[0].name, "A")
        self.assertEqual(gs.dimensions[1].name, "B")


class TestParseGoalState(unittest.TestCase):
    """Tests for parse_goal_state from topic markdown."""

    def test_parse_valid_topic(self) -> None:
        """Parse a well-formed topic with goal state and quality dimensions."""
        md = """\
# Topic Brief

Topic: Some topic

## Goal State

A thorough understanding of causal mechanisms behind the phenomenon.

## Quality Dimensions

- **Causal Completeness**: All major causal pathways are identified and explained
- **Evidence Density**: Claims are backed by specific source references
- **Coverage Breadth**: All key sub-topics are addressed
- **Conciseness**: No redundant or filler content
"""
        gs = parse_goal_state(md)
        self.assertEqual(
            gs.done_definition,
            "A thorough understanding of causal mechanisms behind the phenomenon.",
        )
        self.assertEqual(len(gs.dimensions), 4)
        self.assertEqual(gs.dimensions[0].name, "Causal Completeness")
        self.assertEqual(
            gs.dimensions[0].description,
            "All major causal pathways are identified and explained",
        )
        self.assertEqual(gs.dimensions[1].name, "Evidence Density")
        self.assertEqual(gs.dimensions[2].name, "Coverage Breadth")
        self.assertEqual(gs.dimensions[3].name, "Conciseness")
        self.assertEqual(gs.dimensions[3].description, "No redundant or filler content")

    def test_parse_single_dimension(self) -> None:
        """Parse with exactly one dimension."""
        md = """\
# Topic

## Goal State

Done when we understand X.

## Quality Dimensions

- **Accuracy**: All facts are correct
"""
        gs = parse_goal_state(md)
        self.assertEqual(gs.done_definition, "Done when we understand X.")
        self.assertEqual(len(gs.dimensions), 1)
        self.assertEqual(gs.dimensions[0].name, "Accuracy")
        self.assertEqual(gs.dimensions[0].description, "All facts are correct")

    def test_parse_empty_dimensions_section_raises(self) -> None:
        """An empty quality dimensions section should raise a ValueError."""
        md = """\
# Topic

## Goal State

Done definition here.

## Quality Dimensions

"""
        with self.assertRaises(ValueError) as ctx:
            parse_goal_state(md)
        self.assertIn("dimension", str(ctx.exception).lower())

    def test_parse_malformed_entries_no_bold_raises(self) -> None:
        """Entries without bold name format should not parse as dimensions."""
        md = """\
# Topic

## Goal State

Done definition here.

## Quality Dimensions

- Causal Completeness: description without bold
- Another item: also no bold
"""
        with self.assertRaises(ValueError) as ctx:
            parse_goal_state(md)
        self.assertIn("dimension", str(ctx.exception).lower())

    def test_parse_malformed_entry_no_colon_raises(self) -> None:
        """Entries with bold but missing colon separator should not parse."""
        md = """\
# Topic

## Goal State

Done definition here.

## Quality Dimensions

- **NoColonHere** just some text
"""
        with self.assertRaises(ValueError) as ctx:
            parse_goal_state(md)
        self.assertIn("dimension", str(ctx.exception).lower())

    def test_parse_missing_goal_state_section(self) -> None:
        """If ## Goal State section is missing, done_definition should be empty."""
        md = """\
# Topic

## Quality Dimensions

- **Accuracy**: Facts are correct
"""
        gs = parse_goal_state(md)
        self.assertEqual(gs.done_definition, "")
        self.assertEqual(len(gs.dimensions), 1)

    def test_parse_missing_quality_dimensions_section(self) -> None:
        """If ## Quality Dimensions section is missing entirely, raise ValueError."""
        md = """\
# Topic

## Goal State

Done.
"""
        result = parse_goal_state(md)
        self.assertEqual(result.dimensions, [])
        self.assertEqual(result.done_definition, "Done.")

    def test_parse_multiline_done_definition(self) -> None:
        """Done definition can span multiple lines until next section."""
        md = """\
# Topic

## Goal State

First line of done definition.
Second line of done definition.

## Quality Dimensions

- **A**: Description A
"""
        gs = parse_goal_state(md)
        self.assertIn("First line", gs.done_definition)
        self.assertIn("Second line", gs.done_definition)

    def test_parse_dimensions_with_extra_whitespace(self) -> None:
        """Dimensions should be parsed even with extra whitespace."""
        md = """\
# Topic

## Goal State

Done.

## Quality Dimensions

-   **Spaced Out**:   Lots of extra spaces
"""
        gs = parse_goal_state(md)
        self.assertEqual(len(gs.dimensions), 1)
        self.assertEqual(gs.dimensions[0].name, "Spaced Out")
        self.assertEqual(gs.dimensions[0].description, "Lots of extra spaces")

    def test_parse_dimension_stops_at_next_section(self) -> None:
        """Parsing quality dimensions stops at the next ## heading."""
        md = """\
# Topic

## Goal State

Done.

## Quality Dimensions

- **A**: Desc A

## Another Section

Some other content.
"""
        gs = parse_goal_state(md)
        self.assertEqual(len(gs.dimensions), 1)
        self.assertEqual(gs.dimensions[0].name, "A")


class TestDefaultTopicTemplate(unittest.TestCase):
    """Tests that the default_topic template includes goal state and quality dimensions."""

    def test_topic_template_has_goal_state_section(self) -> None:
        topic_md = default_topic("Test topic")
        self.assertIn("## Goal State", topic_md)

    def test_topic_template_has_quality_dimensions_section(self) -> None:
        topic_md = default_topic("Test topic")
        self.assertIn("## Quality Dimensions", topic_md)

    def test_topic_template_has_four_dimensions(self) -> None:
        topic_md = default_topic("Test topic")
        self.assertIn("**Causal Completeness**", topic_md)
        self.assertIn("**Evidence Density**", topic_md)
        self.assertIn("**Coverage Breadth**", topic_md)
        self.assertIn("**Conciseness**", topic_md)

    def test_topic_template_parseable(self) -> None:
        """The default topic template should be parseable by parse_goal_state."""
        topic_md = default_topic("Test topic")
        gs = parse_goal_state(topic_md)
        self.assertEqual(len(gs.dimensions), 4)
        self.assertTrue(len(gs.done_definition) > 0)


class TestRunContextGoalState(unittest.TestCase):
    """Tests that RunContext includes goal_state after loading."""

    def test_run_context_has_goal_state_field(self) -> None:
        """RunContext should have a goal_state attribute."""
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "test-run"
            init_run(run_dir, topic=None, provider_kind="mock", example=True)
            ctx = load_run_context(run_dir)
            self.assertIsInstance(ctx.goal_state, GoalState)

    def test_run_context_goal_state_has_dimensions(self) -> None:
        """RunContext goal_state should have parsed dimensions from example topic."""
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "test-run"
            init_run(run_dir, topic=None, provider_kind="mock", example=True)
            ctx = load_run_context(run_dir)
            self.assertGreaterEqual(len(ctx.goal_state.dimensions), 1)

    def test_run_context_goal_state_done_definition(self) -> None:
        """RunContext goal_state should have a non-empty done_definition."""
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "test-run"
            init_run(run_dir, topic=None, provider_kind="mock", example=True)
            ctx = load_run_context(run_dir)
            self.assertTrue(len(ctx.goal_state.done_definition) > 0)


if __name__ == "__main__":
    unittest.main()
