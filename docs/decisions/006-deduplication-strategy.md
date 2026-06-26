# ADR-006 - Use Multi-Strategy Article Deduplication

## Status

Accepted

## Context

Once multiple ingestion sources are aggregated, duplicate articles become inevitable.

The same research article may appear across different providers with variations such as:

- Different URLs
- Different title formatting
- Missing metadata in one source
- Presence or absence of DOI

Examples:

A PubMed article and an arXiv paper may refer to the same research but expose metadata differently.

Using a single deduplication strategy is insufficient because:

- DOI may be missing
- URL may differ between providers
- Titles may contain formatting differences

A robust deduplication strategy must tolerate incomplete or inconsistent metadata.

## Decision

Adopt a multi-strategy deduplication process with ordered priority.

Duplicate detection priority:

1. DOI
2. URL
3. Normalized title

Normalization rules for title comparison:

- Convert to lowercase
- Trim leading/trailing spaces
- Normalize whitespace

Implementation resides in:

- `Deduplicator`

Example:

These titles should be treated as duplicates:

```
AI Diagnosis Study
 ai diagnosis study 
```

because normalization produces equivalent strings.

## Rationale

The chosen priority reflects identifier reliability.

### DOI

Strongest identifier.

Properties:

- Globally unique
- Stable
- Research-standard identifier

Preferred whenever available.

---

### URL

Good fallback.

Useful when:

- DOI missing
- Provider exposes canonical article URL

Lees reliable than DOI because URLs may differ across sources.

---

### Normalized Title

Weakest heuristic but userful fallback.

Allows duplicate detection when:

- DOI missing
- URLs differ
- Only title overlaps

This improves recall but carries higher false-positive risk.

Ordered strategy minimizes incorrect duplicate removal while maintaining robustness.

## Consequences

Positive:

- Improved duplicate detection across heterogeneous sources
- Better dataset quality before ranking
- Reduced duplicate entries in final digest

Negative:

- Additional processing cost during aggregation
- Title-based matching may occacionally produce false positives

Long-term impact:

This strategy provides a pragmatic balance between precision and recall and can later evolve into more advanced semantic deduplication if required.
