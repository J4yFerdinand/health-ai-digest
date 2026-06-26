# Architecture - health-ai-digest

## 1. Overview

`health-ai-digest` is a Python-based system designed to automatically collect, process, rank, and summarize the most relevant AI-related healthcare research articles.

The goal of the project is to reduce information overload by transforming large volumes of medical research into concise, high-value digest focused on artificial intelligence in healthcare.

The system is being built incrementally using a layered architecture that prioritizes modularity, testability, and extensibility.

---

## 2. Core Problem

Healthcare AI research grows at a pace that makes manual tracking increasingly difficult.

Researchers, engineers, clinicians, and decision-makers face several challenges:

- Too many papers published daily
- Multiple data sources with overlapping content
- Difficult manual filtering of relevant research
- Limited time to read long technical papers

Health AI Digest addresses this problem by automating:

1. Article ingestion
2. Multi-source aggregation
3. Deduplication
4. Relevance ranking
5. Digest generation

---

## 3. High-Level Architecture

Health AI Digest follows a pipeline architecture.

```
External Sources
		↓
Ingestion Layer
		↓
Aggregation Layer
		↓
Clean Article Collection
		↓
Ranking Layer
		↓
Digest Generator Layer
		↓
Newsletter Output
```

Each layer has a single responsibility and transforms data into a more refined form.

### Current Pipeline State

Implemented:

```
External Sources
	↓
Ingestion Layer
	↓
Aggregation Layer
```

Planned:

```
Ranking Layer
	↓
Digest Generation Layer
```
---

## 4. Architectural Layers

### 4.1 Ingestion Layer

The Ingestion Layer is responsible for interacting with external article providers and converting source-specific responses into normalized internal objects.

Responsibilities:

- Query external APIs
- Parse raw provider responses
- Normalize metadata
- Map data into `Article` objects

Current sources:

- PubMed

Main components:

- `BaseIngestionClient`
- `PubMedClient`

Output:

`list[Article]`

Status

✅ Implemented

---

### 4.2 Aggregation Layer

The Aggregation Layer combines results from multiple ingestion clients into a unified collection.

Responsibilities:

- Merge article collections from multiple sources
- Remove duplicates
- Prepare a clean article set for ranking

Main components:

- `AggregationService`
- `Deduplicator`

Current deduplication strategy:

Priority order:

1. DOI
2. URL
3. Normalize title

Example:

Two articles are considered duplicates if any of these identifiers match according to the priority strategy.

Output:

`list[Article]`

Status:

✅ Implement

---

### 4.3 Ranking Layer

The Ranking Layer will determine which articles are most relevant for the final digest.

Responsibilities:

- Score articles
- Prioritize high-value research
- Sort by relevance

Potential ranking signals:

- Publication recency
- AI relevance
- Clinical relevance
- Citation count
- Journal reputation

Possible output:

`list[Article]`

Status:

🔜 Planned (Phase 3)

---

### 4.4 Digest Generation Layer

The Digest Generation Layer will transform ranked articles into readable summaries.

Responsibilities:

- Summarize papers
- Generate digest section
- Export formatted digest

Potential output formats:

- Markdown
- HTML
- Email newsletter
- API Response

Status:

🔜 Planned (Phase 4)

---

## 5. Current Project Structure

```
health-ai-digest/
|
├─ docs/
|  ├─ decisions/
|  |	├─ 001-src-layout.md
|  |	├─ 002-pydantic-models.md
|  |    ├─ 003-adapter-architecture.md
|  |	└─ 004-pubmed-first-source.md
|  ├─ architecture.md
|  └─ roadmap.md
|
├─ src/
|	└─ health_ai_digest/
|	|	├─ aggregation/
|	|	|	├─ __init__.py
|	|	|	├─ aggregator.py
|	|	|	└─ deduplicator.py
|	|	|
|	|	├─ ingestion/
|	|	|	├─ __init__.py
|	|	|	├─ base.py
|	|	|	└─ pubmed.py
|	|	|
|	|	├─ models/
|	|	|	├─ __init__.py
|	|	|	├─ article.py
|	|	|	└─ enums.py
|	|	|
|	| 	├─ __init__.py
|	|	├─ main.py
|   |	|
|	|
├─ tests/
|	├─ aggregation/
|	|	├─ test_aggregator.py
|	|	└─ test_deduplicator.py
|	|
|	├─ ingestion/
|	|	└─ test_pubmed.py
|	|
|	├─ models/
|	|	└─ test_article.py
|	|
|	├─ __init__.py
|	├─ conftest.py
|	|
├─ .gitignore
├─ pyproject.toml
├─ README.md
├─ requirements.txt	
```

---

## 6. Domain Model

### Article

`Article` is the core domain object and currently acts as the central aggregate root across all layers.

Structure:

```
Article( 
	title: str 
	source: SourceType 
	url: str 
	abstract: str | None 
	authors: list[str] 
	published_at: datetime | None 
	keywords: list[str] 
	doi: str | None 
)
```

Responsibilities:

- Represent normalized research data
- Decouple domain logic from source-specific formats
- Serve as the shared contract between layers

The `Article` model ensures all providers expose a consistent internal interface.

---

## 7. Phase Status

### Phase 1 ─ Ingestion Foundation

Status:

✅ Completed

Implmented:

- Initial project structure
- Article domain model
- Source enum
- Base ingestion abstraction
- PubMed adapter
- XML parsing
- Metadata normalization

Deliverable:

Fetch normalized healthcare AI research articles from PubMed.

---

### Phase 2 ─ Aggregation Layer

Status:

✅ Completed

Implmented:

- AggregationService
- Deduplicator
- Multi-client aggregation
- Duplicate detection heuristics
- Unit tests
- Shared pytest fixtures via `conftest.py`

Deliverable:

Merge multiple article streams into a clean deduplicated datatest.

---

### Phase 3 ─ Ranking Engine

Status:

🔜 Next

Planned:

- Scoring system
- Relevance heuristics
- Ranking algorithm
- Sorting strategies

Goal:

Determine the most important articles.

---

### Phase 4 ─ Digest Generation

Status:

Planned

Goal:

Generate readable AI healthcare digests.

---

## 8. Design Principles

### Separation of Concerns

Each layer has one responsibility.

Examples:

- Ingestion fetches data
- Aggregation merges data
- Ranking scores data
- Digest formats output

---

### Extensibility

The architecture supports easy addition of new sources.

Example future sources:

- arXiv
- bioRxiv
- Semantic Scholar

New providers should integrate without changing existing domain logic.

---

### Strong Domain Modeling

The system is built around explicit domain objects rather than raw dictionaries.

Benefits:

- Better validation
- Stronger typing
- Easier refactors
- Clearer contracts

---

### Incremental Evolution

The project evolves phase-by-phase.

This allows:

- Fast iteration
- Continuous testing
- Low-risk refactors
- Better architecture decisions over time

---

## 9. Roadmap

### Phase 1 ─ Ingestion Foundation

- [x] PubMed adapter
- [x] Domain models
- [x] Manual testing

### Phase 2 ─ Aggregation Layer

- [x] Multi-source ingestion
- [x] Aggregation service
- [x] Deduplication logic

### Phase 3 ─ Ranking Engine 

- [ ] Relevance scoring
- [ ] Clinical priority scoring

### Phase 4 ─ Digest Generation

- [ ] Summaries
- [ ] Newsletter formatting
- [ ] AI-assisted digest generation

---

## 10. Future Refactors

Potential future improvements:

### Configuration Management

Move environment/config settings into dedicated configuration objects.

Example:

- API URLs
- Timeouts
- Limits
- Ranking weights

---

### Logging and Observability

Add structured logging and metrics.

Examples:

- Articles fetched
- Duplicates removed
- Ranking scores
- Pipeline latency

---

### Multi-Source Expansion

Add additional providers:

- arXiv
- bioRxiv
- WHO

---

### Persistence Layer

Potential storage options:

- SQLite
- PostgreSQL
- Vector database

Useful for:

- Historical digests
- Trend analysis
- Search
