# Layer-5 — ARCHIVIST (Ledger Engine)

## Purpose

Append-only reconstruction ledger preserving traceability, conflicts, and resolutions across the stack.

## Required Invariants

1. No deletions
2. No state rewrites
3. All conflicts logged and resolvable

## Dependencies

- `layer4-omega-manifold`

## Artifacts

- `spec.md`
- `tla/module.tla`
- `diagrams/README.md`
- `ledger/ledger-template.md`
