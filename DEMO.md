# Demo: Query the Interaction Mechanics Index

Query dialogue segments by semantic content, structural primitive, or both.

## Prerequisites

```bash
pip install faiss-cpu sentence-transformers numpy
```

All scripts run CPU-only (no GPU required for querying).

## Available Indices

| Index | File | Content |
|-------|------|---------|
| Semantic | `indices/semantic.index` | Embeddings of segment text content |
| Structural | `indices/structural.index` | Embeddings of primitive signature strings |

Both indices share aligned metadata via segment UID in `segment_registry.jsonl`.

---

## Build the Indices (If Not Present)

```bash
# Step 1: Build segment registry from dialogue corpora
CUDA_VISIBLE_DEVICES="" python3 scripts/build_segment_registry.py

# Step 2: Compile primitive signatures
CUDA_VISIBLE_DEVICES="" python3 scripts/compile_primitive_signatures.py

# Step 3: Build dual FAISS indices (dry-run first)
CUDA_VISIBLE_DEVICES="" python3 scripts/build_dual_faiss_indices.py --dry_run

# Step 4: Build indices (real embeddings, CPU-only)
CUDA_VISIBLE_DEVICES="" python3 scripts/build_dual_faiss_indices.py --model intfloat/e5-small-v2
```

---

## Query Examples

### Semantic Query (Find by Meaning)

Search for segments whose text content is semantically similar to a natural-language query:

```bash
CUDA_VISIBLE_DEVICES="" python3 scripts/query_index.py \
    --index indices/semantic.index \
    --registry segment_registry.jsonl \
    --query "managing disagreement between participants"
```

**Example output:**
```
Query: managing disagreement between participants
Results: 5

==================================================
[1]  Score: 0.8724
  Segment: seg_0142
  Primitive: CORRECT
  Model: Claude
  Session: session_07

  "That's an important distinction. The framing I used earlier
  doesn't quite capture the dynamic you're describing. Let me
  revise: rather than a binary outcome, the interaction produces..."
```

### Structural Query (Find by Primitive)

Search for segments tagged with a specific interaction primitive:

```bash
CUDA_VISIBLE_DEVICES="" python3 scripts/query_index.py \
    --index indices/structural.index \
    --registry segment_registry.jsonl \
    --query "SYNTHESIZE"
```

**Example output:**
```
Query: SYNTHESIZE
Results: 5

==================================================
[1]  Score: 0.9103
  Segment: seg_0287
  Primitive: SYNTHESIZE
  Model: GPT
  Session: session_12

  "Bringing these threads together: the structural pattern we've
  identified operates at three levels — turn-level adjacency,
  sequence-level coherence, and session-level arc..."
```

### Try These Queries

**Semantic (find by meaning):**
```
"reaching consensus after disagreement"
"introducing a new analytical framework"
"summarizing multiple discussion threads"
"correcting a prior claim with evidence"
```

**Structural (find by primitive):**
```
"SYNTHESIZE"    — Moments where threads are combined
"CORRECT"       — Self-corrections or partner corrections
"EXTEND"        — Building on a prior contribution
"RESYNC"        — Re-aligning after a tangent
"SCAFFOLD"      — Providing structure for the partner
```

---

## Understanding Results

- **Score:** Cosine similarity (0.0-1.0). Higher = more relevant.
- **Segment:** Unique segment ID from the registry.
- **Primitive:** The interaction primitive tagged to this segment.
- **Model:** Which LLM produced this segment (GPT or Claude).
- **Session:** Source dialogue session.

The semantic index finds segments by what they say.
The structural index finds segments by how they function in the dialogue.

---

## Related

- [comparative-grammar-gpt-vs-claude](https://github.com/whmatrix/comparative-grammar-gpt-vs-claude) — Source grammar comparison providing segment typologies
- [structural-collaboration-primitives](https://github.com/whmatrix/structural-collaboration-primitives) — Primitive definitions used in the structural index
