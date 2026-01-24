# Extension Checklist — Interaction Mechanics Index

**Document Type:** Gate checklist
**Created:** 2025-01-23
**Status:** Required before any extension

---

## Purpose

This checklist must be completed before extending the interaction mechanics index to new model families, temporal eras, or operators.

**All items must be YES or N/A before proceeding.**

---

## Pre-Extension Gate

### 1. Population Boundary

- [ ] **Population boundary defined?**
  - Source corpus clearly identified
  - Session selection criteria documented
  - Inclusion/exclusion rules explicit
  - Sample size justified (≥5 sessions recommended)

### 2. Protocol Version

- [ ] **Protocol version locked?**
  - Current protocol version recorded (v4.23)
  - Schema version documented
  - No mid-extension version changes planned
  - Backwards compatibility assessed

### 3. Grammar Discovery

- [ ] **Grammar discovery isolated?**
  - No reference to existing typologies during discovery
  - Independent segment type naming
  - No imported primitive assumptions
  - Boundary markers derived from new corpus only

### 4. Validation Threshold

- [ ] **Validation threshold met?**
  - All segment types observed in ≥2 sessions
  - Hybrid classification rate <15%
  - Forced classification rate = 0%
  - Coverage = 100% for all sessions

### 5. Comparison Justification

- [ ] **Comparison justified?**
  - Both grammars independently validated (if comparing)
  - Crosswalk methodology documented
  - Non-claims boundary explicit
  - No capability or quality claims

---

## Extension-Specific Checks

### A. New Model Family

- [ ] Export format documented
- [ ] Segmentation rules defined
- [ ] Corpus directory isolated
- [ ] Typology derived independently
- [ ] Phases 3A-4B completed

### B. New Temporal Era

- [ ] Drift detection completed
- [ ] Type distribution compared
- [ ] Grammar revalidation status determined
- [ ] Primitive stability tested
- [ ] Era identifier assigned

### C. New Operator

- [ ] Operator identifier assigned
- [ ] Privacy requirements met
- [ ] Metadata fields updated
- [ ] Normalization rules applied
- [ ] Bias controls documented

---

## Post-Extension Verification

- [ ] Registry JSONL validates against schema
- [ ] Signature compilation succeeds
- [ ] Index alignment verified (n_semantic == n_structural)
- [ ] Query CLI returns expected results
- [ ] Build report shows no errors
- [ ] PROTOCOL_DATASET_MANIFEST.json updated
- [ ] PROTOCOL_ARTIFACTS_REGISTRY.md entry added

---

## Sign-Off

| Role | Name | Date | Status |
|------|------|------|--------|
| Extension Author | | | PENDING |
| Validation Review | | | PENDING |

**Extension may proceed only when both sign-offs complete.**

---

## Failure Modes

If any checklist item fails:

| Failure | Resolution |
|---------|------------|
| Population boundary unclear | Document before proceeding |
| Grammar not isolated | Restart discovery without reference |
| Validation threshold not met | Continue ingestion (Phase 4A′) |
| Comparison unjustified | Defer comparison until both validated |
| Privacy requirements unmet | Redact/anonymize before ingestion |

---

**END OF EXTENSION CHECKLIST**
