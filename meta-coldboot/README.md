# Meta — Cold-Boot Reconstruction

## Purpose

Substrate-independent recovery protocol ensuring the entire stack can be reconstructed from repository artifacts.

## Required Invariants

1. Artifacts are readable in isolation
2. No external hidden dependencies
3. Reconstruction order is deterministic

## Dependencies

- None (root/meta layer).

## Artifacts

- `spec.md`
- `tla/module.tla`
- `diagrams/README.md`
- `ledger/ledger-template.md`
