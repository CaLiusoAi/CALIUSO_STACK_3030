# Layer-0 — DEFAULT LENS (Foundation)

## Purpose

Structural filter that enforces maximal observability and zero hidden complexity before any higher-layer reasoning is allowed.

## Required Invariants

1. O = 10
2. H = 0
3. R = -∞
4. StyleStep -> H' = 0
5. All 10 observable predicates are present
6. All 5 hidden predicates are absent

## Dependencies

- `meta-dissipativity`
- `meta-coldboot`

## Artifacts

- `spec.md`
- `tla/module.tla`
- `diagrams/README.md`
- `ledger/ledger-template.md`
