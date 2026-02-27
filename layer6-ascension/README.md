# Layer-6 — ASCENSION ENGINE

## Purpose

Gatekeeper transition logic that permits layer promotion only when structural, dissipative, and ledger rules pass.

## Required Invariants

1. Gate checks are deterministic
2. Ascension is blocked on unresolved violations
3. Sequence progresses strictly forward

## Dependencies

- `layer5-archivist`

## Artifacts

- `spec.md`
- `tla/module.tla`
- `diagrams/README.md`
- `ledger/ledger-template.md`
