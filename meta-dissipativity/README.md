# Meta — Dissipativity Backbone

## Purpose

Global contraction law applied to all layers to prevent hidden complexity regeneration.

## Required Invariants

1. R must not increase under valid transitions
2. If H == 0, then H' remains 0
3. Any violating transition is rejected

## Dependencies

- None (root/meta layer).

## Artifacts

- `spec.md`
- `tla/module.tla`
- `diagrams/README.md`
- `ledger/ledger-template.md`
