# Citation Network Template

Use this template when generating citation network analysis reports.

---

## Template

```markdown
## Citation Network Analysis

### Seed Paper

| Field | Value |
|-------|-------|
| **Title** | [Paper title] |
| **Authors** | [Author list] |
| **Year** | [YYYY] |
| **Venue** | [Journal/Conference] |
| **DOI** | [DOI] |
| **Semantic Scholar ID** | [ID] |
| **Total Citations** | [N] |
| **Total References** | [M] |
| **Citation Velocity** | [X/year] |

---

### Forward Citations (Cited By)

**Total papers citing this work**: [N]

#### High-Impact Citations (Top 10 by citation count)

| # | Paper | Year | Citations | Venue | Key Contribution |
|---|-------|------|-----------|-------|------------------|
| 1 | [Title] | [Year] | [Count] | [Venue] | [What they added] |
| 2 | [Title] | [Year] | [Count] | [Venue] | [What they added] |
| ... | ... | ... | ... | ... | ... |

#### Recent Citations (Last 2 Years)

| Paper | Year | Venue | Relevance |
|-------|------|-------|-----------|
| [Title] | [Year] | [Venue] | [Why relevant] |

#### Citation by Venue Distribution

| Venue Type | Count | Percentage |
|------------|-------|------------|
| Journal | [N] | [X%] |
| Conference | [M] | [Y%] |
| Preprint | [K] | [Z%] |

#### Citation Velocity Trend

| Year | Citations | Cumulative |
|------|-----------|------------|
| [Year 1] | [N] | [N] |
| [Year 2] | [M] | [N+M] |
| ... | ... | ... |

**Peak Year**: [Year with most citations]

---

### Backward References (Cited By This Paper)

**Total references**: [M]

#### Foundational Works

| # | Paper | Year | Why Cited | Citation Type |
|---|-------|------|-----------|---------------|
| 1 | [Title] | [Year] | [Theoretical basis] | Theoretical |
| 2 | [Title] | [Year] | [Method source] | Methodological |
| ... | ... | ... | ... | ... |

#### Method Lineage

```
[Original Method Paper]
         ↓
[Intermediate Paper]
         ↓
[Seed Paper]
```

#### Data Source References

| Paper | Year | Data Type | Access |
|-------|------|-----------|--------|
| [Title] | [Year] | [Dataset] | [Open/Closed] |

---

### Citation Network Metrics

| Metric | Value | Interpretation |
|--------|-------|----------------|
| **Network h-index** | [X] | [Interpretation] |
| **Average citation depth** | [Y] | [Interpretation] |
| **Field diversity** | [Z fields] | [Interpretation] |
| **Bridge papers** | [N] | [Papers connecting fields] |

---

### Key Influencers

Papers that have significantly shaped research following this work:

#### 1. [Paper Title]

- **Citations**: [Count]
- **Year**: [Year]
- **Why influential**: [Explanation]
- **Impact on field**: [Description]

#### 2. [Paper Title]

[Same format]

---

### Research Lineage

```
┌─────────────────────────────────────────────────┐
│                 FOUNDATIONAL                     │
│  [Paper A] (Year)                               │
│  ↓                                              │
│  [Paper B] (Year)                               │
│  ↓                                              │
│                 SEED PAPER                       │
│  [Current Paper] (Year)                         │
│  ↓         ↓         ↓                          │
│ [Cite 1]  [Cite 2]  [Cite 3]                    │
│ (Year)    (Year)    (Year)                      │
└─────────────────────────────────────────────────┘
```

---

### Citation Context Analysis

When available, the context of how papers cite each other:

| Citation Type | Count | Examples |
|---------------|-------|----------|
| **Methodological** | [N] | Papers extending methods |
| **Theoretical** | [M] | Papers building on theory |
| **Empirical** | [K] | Papers comparing results |
| **Contrasting** | [L] | Papers presenting alternatives |

---

### Related Papers (Recommendations)

Papers recommended based on citation network:

| # | Paper | Year | Relevance Score | Why Related |
|---|-------|------|-----------------|-------------|
| 1 | [Title] | [Year] | [Score] | [Explanation] |
| 2 | [Title] | [Year] | [Score] | [Explanation] |

---

### Recommended Reading Path

For understanding this research area, read in order:

1. **Foundation**: [Paper A] — Original theoretical work
2. **Development**: [Paper B] — Key intermediate work
3. **Current**: [Seed Paper] — State of the art
4. **Extension**: [Paper C] — Recent advancement
5. **Alternative**: [Paper D] — Contrasting approach

---

### Research Gap Analysis

Based on citation network:

- **Unexplored**: [Topic not covered in citations]
- **Contradicted**: [Topic with conflicting findings]
- **Extended**: [Topics well-covered in citations]

---

### Collaboration Network

Authors who frequently appear in citation network:

| Author | Papers in Network | Total Citations | Affiliation |
|--------|-------------------|-----------------|-------------|
| [Name] | [N] | [M] | [Institution] |

---

### Notes

- [Any additional observations about the citation network]
- [e.g., "High self-citation rate in forward citations"]
- [e.g., "Strong conference presence suggests active community"]
```

---

## Example Output

```markdown
## Citation Network Analysis

### Seed Paper

| Field | Value |
|-------|-------|
| **Title** | Graph Neural Networks for Credit Risk Assessment |
| **Authors** | Zhang, L., Wang, H., Liu, Y. |
| **Year** | 2024 |
| **Venue** | Journal of Financial Data Science |
| **DOI** | 10.1234/jfds.2024.001 |
| **Semantic Scholar ID** | abc123 |
| **Total Citations** | 45 |
| **Total References** | 32 |
| **Citation Velocity** | 22.5/year |

---

### Forward Citations (Cited By)

**Total papers citing this work**: 45

#### High-Impact Citations

| # | Paper | Year | Citations | Venue | Key Contribution |
|---|-------|------|-----------|-------|------------------|
| 1 | Heterogeneous GNN for Credit Scoring | 2024 | 18 | JFDS | Extended to heterogeneous graphs |
| 2 | Dynamic GNN Risk Models | 2024 | 12 | arXiv | Added temporal dynamics |
| 3 | Multi-task GNN Finance | 2024 | 8 | KDD | Multi-task learning extension |

#### Recent Citations

| Paper | Year | Venue | Relevance |
|-------|------|-------|-----------|
| Attention-based GNN Credit | 2024 | NeurIPS | Adds attention mechanism |

---

### Research Lineage

```
┌───────────────────────────────────────┐
│           FOUNDATIONAL                 │
│  "Graph Neural Networks" (2019)       │
│  ↓                                     │
│  "GNN for Finance" (2022)             │
│  ↓                                     │
│           SEED PAPER                   │
│  "GNN Credit Risk" (2024)             │
│  ↓         ↓                           │
│ [Hetero]  [Dynamic]                    │
└───────────────────────────────────────┘
```

---

### Recommended Reading

1. **Foundation**: GNN Survey (2019) — Original methods
2. **Application**: GNN Finance (2022) — First finance application
3. **Current**: GNN Credit Risk (2024) — This paper
4. **Extension**: Dynamic GNN (2024) — Temporal extension
```
```