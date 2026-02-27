# Layer-0 — DEFAULT LENS (Foundation) Specification

## Scope

Structural filter that enforces maximal observability and zero hidden complexity before any higher-layer reasoning is allowed.

## Invariants

1. O = 10
2. H = 0
3. R = -∞
4. StyleStep -> H' = 0
5. All 10 observable predicates are present
6. All 5 hidden predicates are absent

## Dependency Contract

- `meta-dissipativity`
- `meta-coldboot`

## Exit Criteria

- All required artifacts exist and are non-empty.
- Invariants above are represented in implementation and documentation.
- Validation tooling reports no errors.
