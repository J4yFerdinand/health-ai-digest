# ADR-009 ─ RankedArticle Domain Model

## Status

Accepted

## Context

During Phase 3, ranking introduced additional metadata not present in the base `Article` model.

Examples:

- final score
- recency score
- relevance score
- quality score

Adding these fields directly to `Article` would mix responsibilities.

`Article` is intended to represent normalized raw research data, not ranking state.

## Decision

Introduce a dedicated `RankedArticle` model.

Structure:

```python
RankedArticle(
  article: Article,
  score: float,
  relevance_score: float = 0.0,
  recency_score: float = 0.0,
  quality_score: float = 0.0,
)
```

This model wraps an `Article` and adds ranking metadata.

## Rationale

Separating ranked output from raw article data improves domain modeling.

Responsibilities become explicit:

- `Article` → normalized research metadata
- `RankedArticle` → ranked article with scoring metadata

This improves clarity accross the ranking and digest generation layers.

## Consequences

Positive

- stronger domain separation
- improved traceability
- explainable scoring
- easier future digest generation

Negative

- additional model complexity
- extra object creation during ranking
