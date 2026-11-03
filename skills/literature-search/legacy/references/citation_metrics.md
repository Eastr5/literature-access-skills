# Citation Metrics Interpretation

This document explains the meaning and interpretation of common citation metrics.

## Common Citation Metrics

| Metric | Definition | Range | Best Use |
|--------|------------|-------|----------|
| **Citation Count** | Total citations received | 0 to thousands | Overall impact |
| **h-index** | h papers with ≥ h citations | 0 to 100+ | Sustained productivity |
| **i10-index** | Papers with ≥ 10 citations | 0 to hundreds | Google Scholar metric |
| **Citation Velocity** | Citations per year | 0 to hundreds | Current relevance |
| **Field-Weighted Citation Impact** | Citations normalized by field | 0 to 5+ | Cross-field comparison |

---

## h-index

### Definition

A researcher has h-index **h** if they have **h** papers with at least **h** citations each.

### Interpretation

| h-index Range | Career Stage (Approximate) |
|---------------|---------------------------|
| 1-5 | Early career / Graduate student |
| 6-10 | Postdoc / Assistant professor |
| 11-20 | Associate professor |
| 21-40 | Full professor |
| 41-60 | Distinguished professor |
| >60 | Highly influential researcher |

**Note**: These ranges vary significantly by field.

### Field Variations

| Field | Typical h-index for Professor |
|-------|------------------------------|
| Physics | 15-30 |
| Biology | 30-50 |
| Computer Science | 10-25 |
| Mathematics | 5-15 |
| Social Science | 10-25 |

**Important**: h-index is field-dependent. Never compare h-index across fields directly.

### Limitations

- Does not account for author position
- Penalizes recent work (needs time to accumulate)
- Does not distinguish self-citations
- Inflated by highly cited single paper

---

## i10-index

### Definition

Number of papers with at least 10 citations.

### Interpretation

| i10-index | Meaning |
|-----------|---------|
| 0-5 | Few impactful papers |
| 6-20 | Moderate productivity |
| 21-50 | Significant contribution |
| >50 | Highly productive |

**Note**: This is a Google Scholar-specific metric.

---

## Citation Velocity

### Definition

Average citations received per year since publication.

### Interpretation

| Velocity | Interpretation |
|----------|---------------|
| <1 | Slowly accumulating impact |
| 1-5 | Normal accumulation |
| 5-10 | Hot topic |
| >10 | Very high current interest |

### Use Cases

- Identify trending papers
- Assess current relevance
- Find emerging research directions

---

## Field-Weighted Citation Impact (FWCI)

### Definition

Ratio of paper's citations to average citations for similar papers in same field and year.

### Interpretation

| FWCI | Interpretation |
|------|---------------|
| <1 | Below field average |
| 1 | At field average |
| 1-2 | Above average |
| >2 | Well above average |

**Use**: Cross-field comparison (e.g., comparing a physics paper to a biology paper).

---

## Paper-Level Metrics

### Citation Count Interpretation

| Citations | Impact Level |
|-----------|-------------|
| 0-10 | Limited impact or very recent |
| 11-50 | Moderate impact |
| 51-100 | Good impact |
| 101-500 | High impact |
| >500 | Very high impact / seminal work |

### Context Factors

Consider:

- **Field**: Some fields cite more heavily
- **Age**: Older papers have more citation opportunity
- **Type**: Review papers often cited more
- **Venue**: High-impact journals get more visibility

---

## Journal-Level Metrics

### Impact Factor (IF)

Average citations per paper in past 2 years.

| IF Range | Journal Tier |
|----------|-------------|
| <2 | Regional/specialized |
| 2-5 | Good |
| 5-10 | High impact |
| >10 | Top-tier |

**Limitations**: Subject to field variation, manipulation, and does not reflect individual paper quality.

### CiteScore

Scopus metric, similar to IF but 4-year window.

---

## Author-Level Metrics

### Total Citation Count

Sum of all citations to author's papers.

### h-index

As defined above.

### Citation Distribution

How citations are spread across papers:

| Pattern | Interpretation |
|---------|---------------|
| Concentrated (few highly cited) | Specialized impact |
| Distributed (many moderately cited) | Broad productivity |
| Single spike | One seminal paper |

---

## Citation Types

### Quality Considerations

Not all citations are equal:

| Citation Type | Weight |
|---------------|--------|
| **Substantive** (uses methods/results) | High |
| **Perfunctory** (general mention) | Low |
| **Negative** (criticizes) | Variable |
| **Self-citation** | Low (exclude) |

---

## Network-Level Metrics

### Citation Network Analysis

| Metric | Definition |
|--------|------------|
| **Node degree** | Number of citations/references |
| **Clustering** | How connected is network |
| **Betweenness** | How much paper connects communities |
| **PageRank** | Influence in network |

### Research Lineage

Trace methodological or theoretical lineage through citation chains:

```
Foundational Paper → Intermediary → Current Paper
```

---

## Practical Recommendations

### For Finding High-Impact Papers

1. Look for papers with citation velocity > 5
2. Check if paper has > 100 citations (adjust by field)
3. Consider recency vs. accumulation time

### For Evaluating Authors

1. Use h-index for field-relative comparison
2. Check citation distribution (not just total)
3. Look at recent work, not just historical

### For Research Planning

1. Identify trending papers (high velocity)
2. Trace citation lineage to find foundations
3. Find bridge papers connecting fields

---

## Metric Sources

| Metric | Primary Source |
|--------|---------------|
| Citation count | Semantic Scholar, Google Scholar |
| h-index | Google Scholar, Scopus |
| FWCI | Scopus |
| Impact Factor | Web of Science (JCR) |
| CiteScore | Scopus |