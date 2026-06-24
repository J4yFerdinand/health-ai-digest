# Architecture - health-ai-digest

## 1. Overview

`health-ai-digest` is a Python-based system designed to generate personalized newsletters focused on:

- Artificial Intelligence in healthcare
- AI-assisted diagnosis
- Patient monitoring and patient support
- Emerging scientific research in health AI

The goal is to ingest scientific content from multiple trusted sources, process and rank that content by relevance, and generate concise digest summaries for fast consumption.

---
## 2. Core Problem

The health AI ecosystem evolves rapidly across:

- Scientific papers
- Medical journals
- Research databases
- Institutional publications

Keeping up with relevant advances manually is time-consuming.

This project solves that by automating:

1. Content ingestion
2. Metadata extraction
3. Relevance scoring
4. Digest generation

---
## 3. High-Level Architecture

Current target architecture:

```
Sources
├─ PubMed
├─ arXiv
├─ WHO
├─ Nature
└─ Other scientific sources
		↓
Ingestion Layer
		↓
Aggregation Layer
		↓
Ranking Engine
		↓
Digest Generator
		↓
Newsletter Output
```

Each layer has a clear responsibility and should remain loosely coupled.

---
## 4. Architectural Layers
### 4.1 Ingestion Layer

Responsible for retrieving raw data from external sources.

Responsibilities:

- Connect to APIs/websites
- Fetch raw content
- Parse responses
- Convert raw source data into internal domain objects

Current implementations:
- `PubMedClient`

Future implementations:
 - `ArxivClient`
 - `WHOClient`
 - `NatureClient`

---
### 4.2 Aggregation Layer

Responsible for consolidating content from multiple sources.

Responsibilities:

- Collect articles from all ingestion clients
- Merge results
- Normalize data
- Deduplicate entries

Example:

Multiple sources may reference the same paper. Aggregation ensures the system treats them as a single article.

---
### 4.3 Ranking Layer

Responsible for scoring article relevance.

Potential ranking criteria:

- Topic relevance
- Publication recency
- Clinical impact
- Novelty
- Source credibility

Example scoring formula:

```
score = 
	relevance * 0.40 +
	recency * 0.30 +
	credibility * 0.30
```

This layer determines which articles deserve attention.

---
### 4.4 Digest Generation Layer

Responsible for transforming ranked articles into digest-friendly summaries.

Responsibilities:

- Summarize papers
- Highlight key findings
- Generate human-readable output

Potential AI features:

- LLM summarization
- Semantic clustering
- Topic extraction
- Trend detection

Example digest output:

```
Morning Health AI Digest

1. New AI model improves early lung cancer detection.
2. LLM-assisted triage reduces emergency wait times.
3. Wearable AI improves atrial fibrillation screening.
```
---
## 5. Current Project Structure

```
health-ai-digest/
|
├─ docs/
|  └─ architecture.md
├─ src/
|	└─ health_ai_digest/
|	|	├─ ingestion/
|	|	|	├─ __init__.py
|	|	|	├─ base.py
|	|	|	└─ pubmed.py
|	|	├─ models/
|	|	|	├─ __init__.py
|	|	|	├─ article.py
|	|	|	└─ enums.py
|	|	|
|	|	└─ main.py
|	|	|
|	|
├─ tests/
├─ .gitignore
├─ pyproject.toml
├─ README.md
├─ requirements.txt	
```
---
## 6. Domain Model

### Article

`Article` is the main domain entity shared across the system.

Fields:

- `title`
- `source`
- `url`
- `abstract`
- `authors`
- `published_at`
- `keywords`
- `doi`

All ingestion sources must normalize their outputs into this model.

This guarantees consistency across the pipeline.

---
## 7. Phase 1 Status (Completed)

Phase 1 focused on building the ingestion foundation.

Completed components:

- Project structure
- Python package setup
- Pydantic domain models
- Base ingestion abstraction
- PubMed adapter
- Manual smoke testing

### PubMed Adapter Feature

Implemented:

- Search via PubMed E-utilities API
- Metadata retrieval
- XML parsing
- Article normalization

Parsed fields:

- Title
- Source
- URL
- Authors
- Publication date
- Abstract
- DOI

Current parsing pipeline:

```
Query
  ↓
PubMed Search API
  ↓
PMIDs
  ↓
PubMed Fetch API
  ↓
XML Response
  ↓
PubMed Parser
  ↓
Article objects
```
---
## 8. Design Principles

This project follows several architectural principles:

### Separation of Concerns

Each component should have one responsibility.

Examples:

- Networking
- Parsing
- Ranking
- Summarization

Should remain isolated.

---
### Extensibility

New sources should be easy to add.

Example:

Adding `ArxivClient` should require minimal changes to existing code.

---
### Strong Domain Modeling

Internal data should always be represented by typed models.

Benefits:

- Validation
- Predictability
- Easier debugging
---
### Incremental Evolution

Architecture will evolve phase by phase.

Avoid premature complexity.

---
## 9. Roadmap

### Phase 1 ─ Ingestion Foundation

- [x] PubMed adapter
- [x] Domain models
- [x] Manual testing

### Phase 2 ─ Aggregation Layer

- [ ] Multi-source ingestion
- [ ] Aggregation service
- [ ] Deduplication logic

### Phase 3 ─ Ranking Engine 

- [ ] Relevance scoring
- [ ] Clinical priority scoring

### Phase 4 ─ Digest Generation

- [ ] Summaries
- [ ] Newsletter formatting
- [ ] AI-assisted digest generation
---
## 10. Future Refactors

Potential future refactor for PubMed module:

```
ingestion/pubmed/
├─ client.py
├─ parser.py
├─ constants.py
└─ exceptions.py
```

This split may be useful as the PubMed adapter grows.

Not required yet.

Currente implementation remains intentionally simple.