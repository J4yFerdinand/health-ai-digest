# ADR-001 — Use `src/` Layout

## Status

Accepted

## Context

The project required defining a Python package structure for long-term maintainability.

Two possible layouts were considered:

### Flat layout

```text
repo/
└── health_ai_digest/
```

### `src/` layout

```text
repo/
└── src/
    └── health_ai_digest/
```

The project is expected to grow into a multi-module system with:

* ingestion
* aggregation
* ranking
* digest generation

A scalable layout was required.

## Decision

Use the `src/` layout.

```text
health-ai-digest/
├── src/
│   └── health_ai_digest/
├── tests/
└── docs/
```

## Rationale

Benefits of `src/` layout:

* Prevents accidental imports from repository root
* Encourages proper package boundaries
* Improves packaging and distribution readiness
* Aligns with modern Python project conventions
* Reduces import-related issues during testing

## Consequences

Positive:

* Better project structure
* Easier scaling
* Cleaner imports

Tradeoffs:

* Requires awareness of execution context
* Commands must often be executed from repository root using module syntax

Example:

```bash
python -m health_ai_digest.main
```
