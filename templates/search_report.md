# Search Report Template

Use this template when generating literature search reports.

---

## Template

```markdown
## Literature Search Report

### Search Metadata
- **Date**: [YYYY-MM-DD]
- **Query**: [Original user query]
- **Databases searched**: [arXiv, Semantic Scholar, Crossref, ...]
- **Total time**: [X seconds]

### Query Parameters
- **Keywords extracted**: [keyword1, keyword2, keyword3]
- **Year range**: [YYYY-YYYY] (if specified)
- **Fields**: [cs.AI, q-fin.RM, ...] (if specified)
- **Publication type**: [All / Journal only / Conference only]
- **Results limit**: [N]

---

### Results Summary

| Metric | Count |
|--------|-------|
| Total raw results | [N] |
| After deduplication | [M] |
| After filtering | [K] |
| Open access available | [O] |

---

### Top Results (Ranked by Relevance)

#### 1. [Paper Title]

- **Source**: [Database where found]
- **Authors**: [Author1, Author2, ...]
- **Venue**: [Journal/Conference Name]
- **Year**: [YYYY]
- **DOI**: [DOI or "N/A"]
- **arXiv**: [arXiv ID or "N/A"]
- **Semantic Scholar ID**: [ID or "N/A"]
- **Citations**: [Count]
- **Abstract**: 
  > [First 150-200 characters of abstract...]
- **Access**: 🟢 Open Access | 🔴 Paywalled | 🟡 Preprint
- **URL**: [Link to paper]

#### 2. [Paper Title]
[Same format as above]

#### 3. [Paper Title]
[Same format as above]

[Continue for top 10-20 results]

---

### Database Coverage Analysis

| Database | Raw Results | Unique Contributions | Coverage % |
|----------|-------------|---------------------|------------|
| arXiv | [A] | [A - overlap] | [X%] |
| Semantic Scholar | [B] | [B - overlap] | [Y%] |
| Crossref | [C] | [C - overlap] | [Z%] |
| Google Scholar | [D] | [D - overlap] | [W%] |

**Overlap**: [N] papers found in multiple databases

---

### Year Distribution

| Year | Count | Percentage |
|------|-------|------------|
| 2024 | [N] | [X%] |
| 2023 | [M] | [Y%] |
| 2022 | [K] | [Z%] |
| ... | ... | ... |

---

### Field Distribution

| Field | Count | Percentage |
|-------|-------|------------|
| [Field 1] | [N] | [X%] |
| [Field 2] | [M] | [Y%] |
| ... | ... | ... |

---

### Open Access Status

| Status | Count | Percentage |
|--------|-------|------------|
| 🟢 Open Access | [N] | [X%] |
| 🟡 Preprint | [M] | [Y%] |
| 🔴 Paywalled | [K] | [Z%] |

---

### Search Limitations

- [List any limitations encountered]
- [e.g., "Google Scholar rate limited, results incomplete"]
- [e.g., "Year filter not applied to arXiv due to API limitation"]

---

### Reproducibility Information

**Exact queries sent to each database**:

- **arXiv**: `[exact query string]`
- **Semantic Scholar**: `[exact query string]`
- **Crossref**: `[exact query string]`

---

### Recommendations

Based on search results:

1. **Must-read**: [Highest impact paper]
2. **Foundational**: [Highest citation count]
3. **Trending**: [Highest citation velocity]
4. **Recent**: [Most recent high-relevance]

---

### Next Steps

- [Suggested follow-up actions]
- [e.g., "Download top 5 papers"]
- [e.g., "Analyze citation network for paper 1"]
- [e.g., "Track author of paper 3"]
```

---

## Example Output

```markdown
## Literature Search Report

### Search Metadata
- **Date**: 2026-05-31
- **Query**: "graph neural networks for credit risk"
- **Databases searched**: arXiv, Semantic Scholar, Crossref
- **Total time**: 3.2 seconds

### Results Summary

| Metric | Count |
|--------|-------|
| Total raw results | 45 |
| After deduplication | 38 |
| After filtering | 32 |
| Open access available | 18 |

---

### Top Results (Ranked by Relevance)

#### 1. Graph Neural Networks for Credit Risk Assessment in Digital Finance

- **Source**: Semantic Scholar
- **Authors**: Zhang, L., Wang, H., Liu, Y.
- **Venue**: Journal of Financial Data Science
- **Year**: 2024
- **DOI**: 10.1234/jfds.2024.001
- **arXiv**: N/A
- **Citations**: 45
- **Abstract**:
  > This paper proposes a heterogeneous graph neural network approach for credit risk assessment...
- **Access**: 🔴 Paywalled
- **URL**: https://doi.org/10.1234/jfds.2024.001

#### 2. DGNN-SR: Dynamic Graph Neural Networks for Financial Risk

- **Source**: arXiv
- **Authors**: Chen, X., Li, M.
- **Venue**: arXiv preprint
- **Year**: 2023
- **DOI**: N/A
- **arXiv**: 2305.12345
- **Citations**: 23
- **Abstract**:
  > We present a dynamic graph neural network model for systemic risk monitoring...
- **Access**: 🟡 Preprint
- **URL**: https://arxiv.org/abs/2305.12345

[Continue with remaining results]

---

### Database Coverage

| Database | Raw | Unique | Coverage |
|----------|-----|--------|----------|
| arXiv | 12 | 5 | 42% |
| Semantic Scholar | 30 | 20 | 79% |
| Crossref | 8 | 3 | 21% |

**Overlap**: 7 papers found in multiple databases

---

### Recommendations

1. **Must-read**: Paper #1 (highest relevance)
2. **Foundational**: Paper #5 (citation count: 150)
3. **Trending**: Paper #2 (velocity: 23/year)
4. **Recent**: Paper #8 (published: 2024-03)
```
```