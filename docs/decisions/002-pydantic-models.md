# ADR-002 — Use Pydantic for Domain Models

## Status

Accepted

## Context

The system ingests data from external scientific sources such as PubMed.

External data can be:

* incomplete
* inconsistent
* malformed
* partially missing

The project needed a reliable way to represent internal domain objects.

Options considered:

* dictionaries
* dataclasses
* attrs
* Pydantic

## Decision

Use Pydantic models for core domain entities.

Main example:

* `Article`

## Rationale

Pydantic provides:

* Runtime validation
* Strong typing
* Clear schemas
* Easy serialization
* Better developer ergonomics

Example:

```python
published_at: datetime | None
```

This guarantees normalized internal data.

## Consequences

Positive:

* Safer ingestion pipeline
* Early validation errors
* Better debugging
* Easier future API integration

Tradeoffs:

* Extra dependency
* Slight runtime overhead compared to plain dataclasses
