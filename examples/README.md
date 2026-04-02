# Example Outputs And Use Cases

This directory is for concrete, shareable examples of what an `LLM Auto Research` run can produce.

The bundled example run uses the topic _"Why Roman concrete remained durable in marine environments"_. You can create it locally with:

```bash
uv run autoresearch init runs/example --example
```

## What Goes In

The example run starts with:

- a topic brief that defines the desired understanding
- a `program.md` file that tells the producer how to improve the knowledge base
- two short source documents in `sources/`
- a benchmark with two fixed questions and required citations

That is enough for the loop to do real work: rewrite the knowledge base, answer benchmark questions, score the result, and keep or discard the change.

## What Comes Out

A successful run produces an improved `knowledge_base.md`, grounded benchmark answers, a score history, and a full artifact trail.

### Condensed `knowledge_base.md` example

```markdown
# Knowledge Base

## Roman concrete in marine environments

Roman concrete stayed durable in seawater because the material did not just resist damage.
It continued reacting over time. Seawater interacted with lime and volcanic ash, forming
new mineral phases such as aluminous tobermorite that strengthened the structure instead of
breaking it down.[source-1]

The key ingredients were lime, volcanic ash, and rock aggregate. The volcanic ash enabled
a pozzolanic reaction that contributed to long-term durability, especially in marine
conditions.[source-2]
```

### Condensed benchmark output example

```json
[
  {
    "id": "q1",
    "answer": "Roman concrete remained durable because seawater reacted with lime and volcanic ash to form strengthening mineral phases such as aluminous tobermorite.",
    "citations": ["source-1"]
  },
  {
    "id": "q2",
    "answer": "Its distinguishing ingredients were lime, volcanic ash, and rock aggregate, with volcanic ash enabling the pozzolanic reaction behind long-term durability.",
    "citations": ["source-2"]
  }
]
```

### Condensed `results.tsv` example

```tsv
iteration	status	score	experiment
1	discard	0.4200	initial rewrite
2	keep	0.7100	add seawater mechanism
3	keep	0.8300	strengthen benchmark citations
```

### Condensed `judge_feedback.md` example

```markdown
## Iteration 3

- Priority dimension: Evidence Density
- Improvement suggestion: Tie the mechanism section more explicitly to source-1 and keep source IDs in benchmark answers.
```

### Condensed git history example

```bash
$ git log --oneline autoresearch/example-run
3c1d2ab autoresearch: [0003] strengthen benchmark citations
8f17e4a autoresearch: [0002] add seawater mechanism
```

## What This Example Shows

The point of the framework is not just to generate a paragraph. It is to produce a research asset that is:

- grounded in an explicit evidence set
- evaluated against fixed questions
- improved iteratively instead of rewritten blindly
- auditable after the fact

## Use Cases This Pattern Fits

The Roman concrete example is tiny on purpose, but the same pattern fits larger workflows:

- scientific topic explainers built from a fixed paper set
- market or product briefs built from internal reports
- policy comparisons built from official source documents
- technical knowledge bases built from specs, transcripts, and notes

If you want the broader reasoning behind this design, see [../docs/README.md](../docs/README.md).
