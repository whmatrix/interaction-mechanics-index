# Interaction Mechanics Index

**Created:** 2025-01-23
**Status:** Build infrastructure for mechanics-aware retrieval

---

## Purpose

Mechanics-aware retrieval over segment × primitive units.

This project builds two aligned indices:
1. **Semantic index** — embeddings of segment text content
2. **Structural index** — embeddings of primitive signature strings

Both indices share aligned metadata rows by segment UID, enabling queries that combine semantic similarity with structural pattern matching.

---

## Input Corpora

This repository builds indices from two dialogue corpora:

| Corpus | Model Family | Segments |
|--------|-------------|----------|
| Research Corpus v1 (GPT) | GPT | 37 segments across 6 sessions |
| Research Corpus v2 (Claude) | Claude | 80 segments across 8 sessions |

Source dialogue transcripts are private research material. This repo contains the derived indices, segment registry, and query infrastructure.

For the grammar analysis these corpora produced, see:
- [comparative-grammar-gpt-vs-claude](https://github.com/whmatrix/comparative-grammar-gpt-vs-claude) — Structural comparison of GPT and Claude dialogue grammars
- [structural-collaboration-primitives](https://github.com/whmatrix/structural-collaboration-primitives) — Interaction primitives derived from these grammars

---

## Output Artifacts

| File | Description |
|------|-------------|
| `SCHEMA_segment_registry.md` | Schema definition for segment records |
| `segment_registry.jsonl` | One JSON record per segment |
| `primitive_signatures.jsonl` | Primitive tags and signatures per segment |
| `indices/semantic.index` | FAISS index over segment text |
| `indices/structural.index` | FAISS index over primitive signatures |
| `reports/build_report.md` | Registry build summary |
| `reports/index_build_report.md` | Index build summary |

---

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/build_segment_registry.py` | Parse corpora, emit segment_registry.jsonl |
| `scripts/compile_primitive_signatures.py` | Map segment types to primitives |
| `scripts/build_dual_faiss_indices.py` | Build semantic + structural FAISS indices |

---

## Execution (CPU-Only)

All scripts must run CPU-only to respect existing GPU workloads.

```bash
# Build registry
nice -n 15 ionice -c2 -n7 python3 ./scripts/build_segment_registry.py

# Compile primitives
nice -n 15 ionice -c2 -n7 python3 ./scripts/compile_primitive_signatures.py

# Build indices (dry-run first)
nice -n 15 ionice -c2 -n7 python3 ./scripts/build_dual_faiss_indices.py --dry_run

# Build indices (real embeddings, CPU-only)
nice -n 15 ionice -c2 -n7 CUDA_VISIBLE_DEVICES="" python3 ./scripts/build_dual_faiss_indices.py --model intfloat/e5-small-v2
```

---

## Non-Claims Statement

This index infrastructure does NOT claim:

- Semantic or cognitive meaning of segments
- Capability or quality assessment of models
- Representativeness beyond sampled corpora
- Correctness of primitive mappings beyond documented rules
- Applicability to other systems or timeframes

**Structure-only analysis.** All mappings traceable to typology documents.

---

## CPU-Only Constraint

This build respects existing GPU workloads:
- All Python execution uses `CUDA_VISIBLE_DEVICES=""`
- Commands wrapped with `nice -n 15 ionice -c2 -n7`
- Embedding model defaults to CPU-feasible `intfloat/e5-small-v2`
- Dry-run mode available for testing without heavy embedding

---

## Related

- [comparative-grammar-gpt-vs-claude](https://github.com/whmatrix/comparative-grammar-gpt-vs-claude) — Source grammar comparison providing the segment typologies
- [structural-collaboration-primitives](https://github.com/whmatrix/structural-collaboration-primitives) — Primitive definitions used in the structural index
