# ADR-003 — Use Adapter-Based Ingestion Architecture

## Status

Accepted

## Context

The system needs to ingest content from multiple heterogeneous sources.

Planned sources include:

* PubMed
* arXiv
* WHO
* Nature
* Other scientific sources

Each source exposes data differently:

* REST APIs
* XML
* JSON
* RSS
* HTML scraping

The project required a design that isolates source-specific logic.

## Decision

Adopt an adapter-based ingestion architecture.

Each source implements a dedicated client.

Example:

```text
Source
   ↓
Adapter Client
   ↓
Normalized Article
```

Current implementation:

* `PubMedClient`

Base abstraction:

* `BaseIngestionClient`

## Rationale

Benefits:

* Loose coupling
* Clear responsibilities
* Easier testing
* Extensibility

New sources can be added without modifying core business logic.

Example:

```python
class ArxivClient(BaseIngestionClient):
    ...
```

## Consequences

Positive:

* Scalable architecture
* Independent source implementations
* Easier maintenance

Tradeoffs:

* More abstractions
* Slightly more boilerplate per source
