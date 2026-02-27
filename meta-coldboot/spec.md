# Meta — Cold-Boot Reconstruction Specification

## Scope

Substrate-independent recovery protocol ensuring the entire stack can be reconstructed from repository artifacts.

## Invariants

1. Artifacts are readable in isolation
2. No external hidden dependencies
3. Reconstruction order is deterministic

## Dependency Contract

- None (root/meta layer).

## Exit Criteria

- All required artifacts exist and are non-empty.
- Invariants above are represented in implementation and documentation.
- Validation tooling reports no errors.
