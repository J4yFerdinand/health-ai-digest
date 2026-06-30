# ADR-008 - Weighted Scoring Engine

## Status

Accepted

## Context

Ranking requires combing multiple signals into a single comparable score.

Different signals contribute differently to article quality.

Examples include:

- publication recency
- topic relevance
- article quality
- citation count

A scoring strategy was needed to combine these signals into one ranking metric.

## Decision

Use a weighted scoring model.

Each article receives a final score based on a weighted sum of individual signals.

Formula:

```
final_score = 
(relevance_score * relevance_weight)
+ (recency_score * recency_weight)
+ (quality_score * quality_weight)
```

Weights are centralized in configuration via `settings.py`.

Initial signals:

- `recency_score` → implemented
- `relevance_score` → placeholder
- `quality_score` → placeholder

## Rationale

Weighted scoring was selected because it is:

- simple
- explainable
- easy to tune
- easy to extend

Alternative approaches considered:

- rule-based ranking
- machine learning ranking
- pairwise ranking models

These were rejected for now due to unnecessary complexity at the current project stage.

## Consequences

Positive

- transparent ranking logic
- configurable weighting
- easy experimentation
- low implementation complexity

Negative

- weights are heuristic initially
- may require calibration later
- limited sophistication compared to ML ranking
