# ADR-007 - Ranking Layer Architecture

## Status

Accepted

## Context

After Phase 2, the system could successfully ingest and aggregate healthcare AI articles from external sources.

At that point, the pipeline produced a clean deduplicated list of `Article` objects.

However, all articles were treated equally.

This created a limitation:

- recent articles were not prioritized
- highly relevant articles were not distinguishable
- there was no mechanism to select the best candidates for digest generation

A dedicated ranking stage became necessary before digest generation.

## Decision

Introduce a dedicated **Ranking Layer** between aggregation and digest generation.

The Ranking Layer is composed of three main components:

- `SignalCalculator`
- `ScoringEngine`
- `Ranker`

Responsibilities:

- compute ranking signals
- calculate weighted scores
- sort articles by importance

Pipeline update:

```
Aggregation Layer
	↓
Ranking Layer
	↓
Digest Generation
```

## Rationale

Introducing a separate ranking layer improves architectural clarity.

Benefits:

- preserves separation of concerns
- avoids mixing ranking logic with aggregation
- enables independent testing
- supports future ranking signals

The ranking system is expected to evolve significantly over time, so isolating this logic improves maintainability.

## Consequences

Positive

- cleaner pipeline architecture
- easier future enhancements
- modulat scoring system
- improved testability

Negative

- additional architectural complexity
- more domain object and abstractions
