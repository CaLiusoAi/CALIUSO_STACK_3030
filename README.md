# CALIUSO STACK vΩ.9

Canonical repository for building the complete CALIUSO stack from Layer-0 through Layer-7, with meta-layer constraints and automated validation.

## What this repository now guarantees

- Full layer + meta-layer directory tree is present.
- Every layer ships required artifacts (`README`, `spec`, `tla`, `diagrams`, `ledger`).
- Layer-0 canonical invariants are explicit and validated.
- Ascension sequence is explicit and validated.
- Validation includes manifest consistency, artifact completeness, and non-empty-file checks.

## Stack Layout

- `layer0-default-lens/`
- `layer1-cathedral/`
- `layer2-pantheon/`
- `layer3-omegaomega/`
- `layer4-omega-manifold/`
- `layer5-archivist/`
- `layer6-ascension/`
- `layer7-omegainfinity/`
- `meta-dissipativity/`
- `meta-coldboot/`
- `stack.manifest.yaml`
- `tools/validate_stack.py`
- `tests/test_validate_stack.py`

## Validation

```bash
make validate
make test
```

## Production-ready gate

A change is acceptable only when:

1. `make validate` passes.
2. `make test` passes.
3. Stack manifest stays aligned with on-disk layer modules.
