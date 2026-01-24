# Mechanics-Aware Query CLI

**Script:** `scripts/query_mechanics.py`
**Created:** 2025-01-23

---

## What This CLI Does

The query CLI provides **behavior-first retrieval** over the segment × primitive index:

1. **Structural Filtering** — Filter segments by interaction mechanics:
   - Model family (GPT or Claude)
   - Required primitive tags (must have all)
   - Excluded primitive tags (must have none)
   - Signature substring matching

2. **Semantic Ranking** — Within filtered candidates:
   - Embed query text using the same model as the index (intfloat/e5-small-v2)
   - Rank by cosine similarity
   - Return top-k results

3. **Human-Readable Output** — For each result:
   - Provenance (corpus, session, segment)
   - Structural metadata (type, signature, terminal status)
   - Text excerpt (first 300 characters)

---

## What This CLI Does NOT Do

- Does NOT modify indices or registry files
- Does NOT use GPU (CPU-only, respects existing GPU workloads)
- Does NOT provide full-text search (only semantic similarity)
- Does NOT make capability or quality claims about segments
- Does NOT interpret or analyze segment content
- Does NOT connect to external services or web APIs

---

## Behavior-First Retrieval

Traditional semantic search finds content similar to a query string. **Behavior-first retrieval** adds a structural filtering layer:

1. First, filter by *interaction mechanics* — the structural primitives that characterize how the exchange unfolds
2. Then, rank by *semantic content* — what the exchange is about

This allows queries like:
- "Find correction cycles about permissions" (CORRECT primitive + semantic query)
- "Find synthesis triggers in Claude sessions" (SYNTHESIZE + model filter)
- "Find exploration that isn't derailed" (EXPLORE required, DERAIL excluded)

---

## Usage

```bash
python scripts/query_mechanics.py [OPTIONS]
```

### Options

| Flag | Description |
|------|-------------|
| `--model_family {GPT,Claude,ALL}` | Filter by model family (default: ALL) |
| `--require PRIMITIVE` | Require primitive tag (repeatable) |
| `--exclude PRIMITIVE` | Exclude primitive tag (repeatable) |
| `--signature_contains STRING` | Filter signatures containing substring |
| `--text_query STRING` | Semantic query for ranking |
| `--top_k INT` | Number of results (default: 5) |
| `--list_primitives` | List known primitives and exit |
| `--no_text` | Suppress text excerpt (compact output mode) |

### Known Primitives

| Category | Primitives |
|----------|------------|
| Shared | INITIATE, CORRECT, SEQUENCE, REFERENCE |
| Claude-only | SYNTHESIZE, ELEVATE, EXTEND |
| GPT-only | EXPLORE, DERAIL, RESYNC, OVERFLOW, TRUNCATE |
| Reference variants | REFERENCE_INTERNAL (GPT), REFERENCE_EXTERNAL (Claude) |

---

## Example Commands

### Example 1: Find Claude Synthesis Triggers

Find segments where minimal input triggers extended output in Claude sessions:

```bash
python scripts/query_mechanics.py \
  --model_family Claude \
  --require SYNTHESIZE \
  --top_k 5
```

### Example 2: Semantic Search Within Correction Cycles

Find correction cycles related to permission issues:

```bash
python scripts/query_mechanics.py \
  --require CORRECT \
  --text_query "permission denied" \
  --top_k 3
```

### Example 3: GPT Exploration Without Derailment

Find exploratory questioning segments in GPT that don't include derailment:

```bash
python scripts/query_mechanics.py \
  --model_family GPT \
  --require EXPLORE \
  --exclude DERAIL \
  --top_k 5
```

### Example 4: Terminal Blocks with Security Content

Find terminal blocks that discuss security topics:

```bash
python scripts/query_mechanics.py \
  --require EXTEND \
  --text_query "security audit credentials" \
  --top_k 3
```

### Example 5: Signature Substring Match

Find all segments whose signature contains "SEQUENCE":

```bash
python scripts/query_mechanics.py \
  --signature_contains SEQUENCE \
  --top_k 10
```

### Example 6: Compact Output (No Text)

List Claude SYNTHESIZE segments without text excerpts:

```bash
python scripts/query_mechanics.py \
  --model_family Claude \
  --require SYNTHESIZE \
  --no_text \
  --top_k 5
```

---

## Output Format

Each result is printed in the following format:

```
──────────────────────────────────────────────────
Rank: 1
Score: 0.8234
Corpus: old_claude_v2
Model: Claude
Session: session_004
Segment: seg_003
Segment Type: Correction Cycle
Primitive Signature: CORRECT
Terminal: false
Excerpt: HUMAN[5]: The command still fails with permission denied...
──────────────────────────────────────────────────
```

| Field | Description |
|-------|-------------|
| Rank | Result position (1 = best match) |
| Score | Cosine similarity (N/A if no text_query) |
| Corpus | Source corpus identifier |
| Model | Model family (GPT or Claude) |
| Session | Session identifier |
| Segment | Segment identifier |
| Segment Type | Grammar type from typology |
| Primitive Signature | Structural signature string |
| Terminal | Whether segment is session-terminal |
| Excerpt | First 300 characters of segment text |

---

## Dependencies

- Python 3.8+
- faiss-cpu
- sentence-transformers
- numpy

Install with:
```bash
pip install faiss-cpu sentence-transformers numpy
```

---

## Non-Claims Statement

This query interface is a structural retrieval tool only. It does NOT:
- Evaluate segment quality or correctness
- Make claims about model capabilities
- Interpret segment meaning or intent
- Assess interaction success or failure

All results reflect structural metadata and semantic similarity scores only.

---

**END OF README**
