# Rebuild Instructions — Interaction Mechanics Index

**Dataset:** interaction_mechanics_segments_v1
**Protocol Version:** v4.23
**Last Verified:** 2025-01-23

---

## Prerequisites

### Python Dependencies

```bash
pip install faiss-cpu sentence-transformers numpy
```

### Source Corpora (Read-Only)

The following corpora must exist and be unchanged:

| Corpus | Path |
|--------|------|
| OLD GPT v1 | `./corpus/old_gpt_v1/` (local source corpus) |
| OLD CLAUDE v2 | `./corpus/old_claude_v2/` (local source corpus) |

---

## Rebuild Commands

### Working Directory

All commands assume you are in the repository root:
```bash
cd <repo-root>/
```

### Step 1: Build Segment Registry

```bash
nice -n 15 ionice -c2 -n7 python3 scripts/build_segment_registry.py
```

**Outputs:**
- `segment_registry.jsonl` (119 records)
- `reports/build_report.md`

**Expected:**
- GPT: 6 sessions, 39 segments
- Claude: 8 sessions, 80 segments
- Total: 119 segments

### Step 2: Compile Primitive Signatures

```bash
nice -n 15 ionice -c2 -n7 python3 scripts/compile_primitive_signatures.py
```

**Outputs:**
- `primitive_signatures.jsonl` (119 records)
- `reports/primitive_compile_summary.md`

**Expected:**
- 15 unique signatures
- ~70% STRONG mapping strength

### Step 3: Build FAISS Indices

#### CPU-Only (Recommended)

```bash
CUDA_VISIBLE_DEVICES="" nice -n 15 ionice -c2 -n7 python3 scripts/build_dual_faiss_indices.py --model intfloat/e5-small-v2 --batch_size 16
```

#### Dry-Run Mode (No Embeddings)

```bash
nice -n 15 ionice -c2 -n7 python3 scripts/build_dual_faiss_indices.py --dry_run
```

**Outputs:**
- `indices/semantic/faiss.index`
- `indices/semantic/meta.jsonl`
- `indices/structural/faiss.index`
- `indices/structural/meta.jsonl`
- `reports/index_build_report.md`

**Expected:**
- 119 vectors in each index
- Embedding dimension: 384
- Index type: IndexFlatIP (normalized)

---

## GPU Usage Warning

**CRITICAL: GPU usage is NOT recommended for this dataset.**

Reasons:
1. Dataset is small (119 segments) — CPU is sufficient
2. Existing GPU workloads may be disrupted
3. CPU build completes in < 30 seconds

If GPU is required for larger datasets, use:
```bash
# GPU mode (NOT RECOMMENDED for this dataset)
python3 scripts/build_dual_faiss_indices.py --model intfloat/e5-small-v2 --batch_size 32
```

Always verify no critical GPU jobs are running before GPU builds.

---

## Determinism Verification

Rebuild is deterministic. Same inputs produce identical outputs.

### Checksum Expectations

After rebuild, verify with:
```bash
wc -l segment_registry.jsonl primitive_signatures.jsonl
# Expected: 119 119

wc -l indices/semantic/meta.jsonl indices/structural/meta.jsonl
# Expected: 119 119
```

### Segment Counts

```bash
jq -r '.corpus_id' segment_registry.jsonl | sort | uniq -c
# Expected:
#   80 old_claude_v2
#   39 old_gpt_v1
```

### Signature Distribution

```bash
jq -r '.primitive_signature' primitive_signatures.jsonl | sort | uniq -c | sort -rn | head -5
# Expected top signatures:
#   36 SEQUENCE
#   23 CORRECT
#   15 INITIATE
#   8 REFERENCE_EXTERNAL
#   7 SYNTHESIZE (or similar)
```

---

## Full Rebuild Script

For complete rebuild from scratch:

```bash
#!/bin/bash
set -e

cd <repo-root>/

echo "=== Step 1: Build Segment Registry ==="
nice -n 15 ionice -c2 -n7 python3 scripts/build_segment_registry.py

echo "=== Step 2: Compile Primitive Signatures ==="
nice -n 15 ionice -c2 -n7 python3 scripts/compile_primitive_signatures.py

echo "=== Step 3: Build FAISS Indices (CPU) ==="
CUDA_VISIBLE_DEVICES="" nice -n 15 ionice -c2 -n7 python3 scripts/build_dual_faiss_indices.py --model intfloat/e5-small-v2 --batch_size 16

echo "=== Verification ==="
wc -l segment_registry.jsonl primitive_signatures.jsonl
wc -l indices/semantic/meta.jsonl indices/structural/meta.jsonl
jq -r '.corpus_id' segment_registry.jsonl | sort | uniq -c

echo "=== Rebuild Complete ==="
```

---

## Troubleshooting

### Missing Dependencies

```bash
pip install faiss-cpu sentence-transformers numpy
```

### Model Download Fails

If `intfloat/e5-small-v2` download fails:
1. Check network connectivity
2. Try fallback model: `sentence-transformers/all-MiniLM-L6-v2`
3. Use `--dry_run` for hash-based indices (testing only)

### Corpus Not Found

Verify source paths exist:
```bash
ls -d ./corpus/old_gpt_v1/dialogues/session_*
ls -d ./corpus/old_claude_v2/dialogues/session_*
```

### FAISS Import Error

```bash
pip uninstall faiss-gpu faiss-cpu
pip install faiss-cpu
```

---

## Non-Claims Boundary

This rebuild produces structural retrieval indices only.
No claims are made about:
- Semantic meaning of segments
- Model capabilities or quality
- Interaction success or failure
- Representativeness beyond sampled data

---

**END OF REBUILD INSTRUCTIONS**
