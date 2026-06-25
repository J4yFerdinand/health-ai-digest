# ADR-004 — Use PubMed as First Ingestion Source

## Status

Accepted

## Context

The project required selecting the first scientific source to validate the ingestion pipeline.

Possible candidates included:

* PubMed
* arXiv
* Semantic Scholar
* Crossref

The project focuses on:

* AI in healthcare
* AI-assisted diagnosis
* Patient monitoring
* Clinical decision support

The first source needed to align strongly with this domain.

## Decision

Use PubMed as the first ingestion source.

## Rationale

PubMed offers:

* High-quality biomedical literature
* Strong domain relevance
* Stable public APIs
* Rich metadata
* Widespread scientific adoption

Important metadata available:

* title
* authors
* abstract
* publication date
* DOI

This makes PubMed ideal for validating:

* ingestion
* parsing
* normalization

## Consequences

Positive:

* Strong domain alignment
* High-quality test dataset
* Reliable metadata extraction

Tradeoffs:

* Limited to biomedical literature
* Does not cover all AI publications
* May need complementary sources later (e.g. arXiv)
