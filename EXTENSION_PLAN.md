# Extension Plan — Interaction Mechanics Index

**Document Type:** Scaffold (no execution)
**Created:** 2025-01-23
**Status:** Planning only

---

## Purpose

This document defines preconditions, phases, and isolation rules for extending the interaction mechanics index to:
- New model families
- New temporal eras
- New operators (non-Wade users)

No extension should be executed without completing the relevant checklist (see EXTENSION_CHECKLIST.md).

---

## A. New Model Family

### A.1 Preconditions

Before ingesting a new model family (e.g., Gemini, Llama, Mistral):

| Precondition | Requirement |
|--------------|-------------|
| Closed grammar | Model family must have independently derived segment typology |
| Segmentation rules | Must define segment boundary markers specific to model |
| Export format | Must have documented conversation export structure |
| Minimum corpus | ≥5 sessions recommended for typology stability |
| Operator consistency | Same operator OR explicit operator isolation |

**Critical:** Do NOT reuse GPT or Claude typologies. Each model family requires independent grammar discovery.

### A.2 Required Phases

Extension follows the established phase sequence:

| Phase | Name | Purpose | Outputs |
|-------|------|---------|---------|
| 3A | Seed Ingestion | First session, discover initial patterns | raw_transcript.md, structural_segmentation.md |
| 3B | Boundary Discovery | Identify segment boundary markers | Provisional markers list |
| 3C | Type Emergence | Name and document segment types | Provisional typology |
| 3D | Typology Refinement | Stress-test types with edge cases | Refined typology |
| 4A | Segment-Diverse Ingestion | Expand corpus for type validation | 4-5 additional sessions |
| 4A′ | Targeted Ingestion | Resolve underrepresented types | 1-3 targeted sessions |
| 4B | Typology Validation | Validate all types across corpus | phase_4b_typology_validation.md |

**Minimum for GREEN status:** Complete through Phase 4B with VALIDATED status.

### A.3 Isolation Rules

| Rule | Requirement |
|------|-------------|
| Separate corpus directory | `/home/wade/professional_clear/research-corpus-v3-<model>/` |
| Independent typology map | `segment_typology_map.md` derived without reference to other models |
| Separate registry emission | New JSONL with `corpus_id: "old_<model>_v3"` |
| No index merging | Separate FAISS indices until crosswalk validated |
| Explicit comparison phase | Only compare grammars AFTER both are independently validated |

**Cross-contamination prevention:**
- Do NOT consult existing typologies during Phases 3A-3D
- Do NOT import segment type names from other grammars
- Do NOT assume primitives transfer across model families

---

## B. New Temporal Era

### B.1 Definition

A new temporal era occurs when:
- Model undergoes significant update (e.g., GPT-4 → GPT-4.5)
- Export format changes
- Interaction patterns show systematic drift
- >6 months elapsed since prior corpus

### B.2 Drift Detection Checklist

Before ingesting a new era of an existing model family:

| Check | Method | Threshold |
|-------|--------|-----------|
| Type distribution shift | Compare segment type frequencies | >20% shift in any type |
| New boundary markers | Scan for unrecognized patterns | Any new pattern |
| Message structure change | Compare export JSON schema | Any schema change |
| Turn length distribution | Compare message lengths | >30% mean shift |
| Empty message rate | Compare empty/minimal rates | >15% shift |

### B.3 Grammar Revalidation Criteria

If drift detected, the grammar requires revalidation:

| Condition | Action |
|-----------|--------|
| Minor drift (<20% type shift) | Extend existing grammar with notes |
| Moderate drift (20-40% type shift) | Phase 4A′ targeted ingestion for affected types |
| Major drift (>40% type shift) | Full grammar rediscovery (Phases 3A-4B) |
| New boundary markers | Document and integrate into segmentation rules |
| Export format change | Update parsing scripts before ingestion |

### B.4 Primitive Stability Test

Before merging new-era data into existing indices:

| Test | Requirement |
|------|-------------|
| Type → Primitive mapping | All new-era types must map to existing primitives |
| New primitive candidates | Must be justified by structural markers |
| Signature distribution | New era should not introduce >3 new signatures |
| Crosswalk validity | Existing crosswalk mappings must hold |

**If primitives unstable:** Create separate era-specific index until resolved.

---

## C. New Operator (Non-Wade User)

### C.1 Definition

A new operator is any user other than the original corpus operator (Wade).

Operator change introduces:
- Different interaction style
- Different task domains
- Different turn patterns
- Potential cultural/linguistic variation

### C.2 Required Metadata Changes

| Field | Change |
|-------|--------|
| `corpus_id` | Include operator identifier: `old_gpt_v1_op2` |
| `operator_id` | New field: string identifier (anonymized) |
| `source_paths` | Separate directory tree per operator |

### C.3 Segment Normalization Rules

To enable cross-operator comparison:

| Aspect | Normalization |
|--------|---------------|
| Turn labels | Standardize to HUMAN/ASSISTANT (not USER/AI/etc.) |
| Message indices | Always 1-based, sequential |
| Empty detection | Use consistent minimal confirmation list |
| Text encoding | UTF-8, strip BOM, normalize whitespace |

### C.4 Bias Controls

| Control | Implementation |
|---------|----------------|
| Operator isolation | Separate indices until grammar validated |
| Style neutralization | Segment types based on structure, not content |
| Domain independence | Do not create domain-specific types |
| Comparison gating | Only compare operators AFTER both grammars validated |

**Cross-operator claims prohibited:**
- No claims about operator skill or quality
- No claims about interaction success rates
- No claims about model preference by operator
- Comparison limited to structural patterns only

### C.5 Privacy Requirements

| Requirement | Implementation |
|-------------|----------------|
| Operator anonymization | Use opaque identifiers (op1, op2, ...) |
| PII removal | Strip names, emails, identifiers from transcripts |
| Content redaction | Redact sensitive content before segmentation |
| Consent documentation | Document consent for corpus inclusion |

---

## Non-Claims Boundary

This extension plan does NOT claim:
- Optimal extension procedures
- Completeness of preconditions
- Applicability to all model families
- Transferability of primitives across contexts

All extensions require independent validation before GREEN status.

---

**END OF EXTENSION PLAN**
