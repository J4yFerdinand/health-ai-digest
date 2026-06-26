# ADR-005 - Introduce a Dedicated Aggregation Layer

## Status

Accepted

## Context

Phase 1 introduced the ingestion foundation of the system, allowing external providers such as PubMed to fetch and normalize article data into internal `Article` objects.

At this stage, the system could ingest articles from a single source, but future roadmap phases require support for multiple providers such as:

- PubMed
- arXiv
- bioRxiv
- Semantic Scholar

As multiple sources are integrated, several challenges emerge:

- Articles from different providers must be merged
- Duplicate content across providers becomes likely
- Ranking logic should operate on a clean unified dataset
- Source-specific logic should remain isolated from downstream processing

Without an explicit aggregation stage, ingestion clients would need to manage merging and deduplication themselves, increasing coupling and reducing maintainability.

## Decision

Introduce a dedicated Aggregation Layer as a separate architectural stage between Ingestion and Ranking.

This layer is responsible for:

- Collecting articles from multiple ingestion clients
- Merging all article streams
- Producing a unified article collection
- Delegating duplicate removal to a dedicated component

The Aggregation Layer is implemented through:

- `AggregationService`
- `Deduplicator`

Pipeline:

```
External Sources
	↓
Ingestion Layer
	↓
Aggregation Layer
	↓
Ranking Layer
```

## Rationale

This design improves separation of concerns.

Responsibilities remain clearly isolated:

- Ingestion fetches and normalizes source-specific data
- Aggregation merges and cleans datasets
- Ranking evaluates article relevance

Benefits of this decision:

1. Better modularity
2. Easier support for multiple sources
3. Cleaner ranking pipeline
4. Improved testability
5. Reduced coupling between layers

Aggregation becomes a first-class architectural concern rather than utility logic scattered across clients.

## Consequences

Positive:

- New sources can be added without modifying aggregation logic
- Ranking receives a clean unified dataset
- Aggregation logic can evolve independently

Negative:

- Introduces additional layer complexity
- Slight increase in orchestration overhead

Long-term impact:

This decision enables scalable multi-source ingestion and prepares the system for ranking and digest generation phases.
