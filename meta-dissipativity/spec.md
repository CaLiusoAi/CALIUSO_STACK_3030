# Meta — Dissipativity Backbone Specification

## Scope

Global contraction law applied to all layers to prevent hidden complexity regeneration.

## Invariants

1. R must not increase under valid transitions
2. If H == 0, then H' remains 0
3. Any violating transition is rejected

## Dependency Contract

- None (root/meta layer).

## Exit Criteria

- All required artifacts exist and are non-empty.
- Invariants above are represented in implementation and documentation.
- Validation tooling reports no errors.
