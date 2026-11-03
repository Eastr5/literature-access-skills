# Database Search Protocols

This document describes the search strategies and protocols for each academic database integrated into this skill.

## Database Overview

| Database | Coverage | Strengths | MCP Tool |
|----------|----------|-----------|----------|
| **arXiv** | Preprints (CS, physics, math) | Fast, open, CS-focused | `mcp_paper-search_search_arxiv` |
| **Semantic Scholar** | All fields, 200M+ papers | Citation data, AI-powered | `mcp_semantic-scholar_search_papers` |
| **Google Scholar** | Broad web coverage | Comprehensive, includes grey lit | `mcp_paper-search_search_google_scholar` |
| **Crossref** | DOI-registered works | Metadata quality, DOI lookup | `mcp_paper-search_search_crossref` |
| **Web of Science** | Curated academic content | Quality control, citation index | `mcp_paper-search_search_webofscience` |
| **Scopus** | Science, social science | Author profiles, metrics | `mcp_paper-search_search_scopus` |

---

## arXiv

### Characteristics
- **Type**: Preprint server
- **Fields**: Computer Science, Physics, Mathematics, Statistics, Quantitative Finance
- **Access**: Fully open access
- **Update speed**: Immediate (often days before publication)

### Search Strategy

```yaml
arXiv:
  best_for:
    - CS/ML/AI papers
    - Physics/mathematical papers
    - Recent work (pre-publication)
  
  limitations:
    - No citation counts (unless via Semantic Scholar)
    - Quality varies (unreviewed)
    - Limited to certain fields
  
  query_format:
    - title search: "ti:machine learning"
    - author search: "au:Smith"
    - abstract search: "abs:neural network"
    - category filter: "cat:cs.AI"
```

### arXiv Categories Reference

| Code | Field |
|------|-------|
| `cs.AI` | Artificial Intelligence |
| `cs.LG` | Machine Learning |
| `cs.CL` | Computational Linguistics |
| `cs.CV` | Computer Vision |
| `cs.NE` | Neural and Evolutionary Computing |
| `stat.ML` | Machine Learning (Statistics) |
| `q-fin.RM` | Risk Management |
| `physics.data-an` | Data Analysis |

---

## Semantic Scholar

### Characteristics
- **Type**: Academic search engine with AI
- **Coverage**: 200M+ papers across all fields
- **Access**: Free API, some full text
- **Strengths**: Citation network, paper recommendations

### Search Strategy

```yaml
Semantic_Scholar:
  best_for:
    - Citation analysis
    - Paper recommendations
    - All academic fields
  
  limitations:
    - API rate limits (unauth: 1 req/s, auth: 10 req/s)
    - Some papers lack full metadata
  
  query_format:
    - Natural language queries
    - Boolean operators supported
    - Year range filtering
    - Field of study filtering
  
  api_key: S2_API_KEY environment variable
```

### Semantic Scholar API Features

| Feature | Tool | Use Case |
|---------|------|----------|
| Paper search | `search_papers` | Find papers by topic |
| Paper details | `get_paper` | Get full metadata |
| Citations | `get_paper_citations` | Forward citation analysis |
| References | `get_paper_references` | Backward reference analysis |
| Recommendations | `get_recommendations_for_paper` | Find related papers |
| Author papers | `get_author_papers` | Track author output |

---

## Google Scholar

### Characteristics
- **Type**: Web search engine for academic content
- **Coverage**: Broadest, includes grey literature
- **Access**: Free (with rate limiting concerns)
- **Strengths**: Comprehensive coverage

### Search Strategy

```yaml
Google_Scholar:
  best_for:
    - Grey literature
    - Broad coverage
    - Finding obscure papers
  
  limitations:
    - No official API (scraping)
    - Rate limiting strict
    - Many duplicates
    - Metadata often incomplete
  
  query_format:
    - Natural language
    - Exact phrase: "quoted terms"
    - Author: author:Smith
    - Year: after:2020 before:2024
  
  usage_note: Use sparingly, prefer Semantic Scholar for primary search
```

---

## Crossref

### Characteristics
- **Type**: DOI registration agency
- **Coverage**: All DOI-registered works
- **Access**: Free API
- **Strengths**: DOI metadata quality

### Search Strategy

```yaml
Crossref:
  best_for:
    - DOI validation
    - Metadata lookup
    - Publisher information
  
  limitations:
    - Limited full-text
    - Abstract often missing
  
  query_format:
    - DOI lookup: query.bibliographic
    - Title search
    - Author filter
  
  special_features:
    - DOI validation
    - Reference linking
    - Publisher metadata
```

---

## Web of Science

### Characteristics
- **Type**: Curated citation index
- **Coverage**: High-quality academic journals
- **Access**: Subscription required (often via institution)
- **Strengths**: Quality control, citation metrics

### Search Strategy

```yaml
Web_of_Science:
  best_for:
    - High-quality curated results
    - Citation metrics (Impact Factor)
    - Journal quality assessment
  
  limitations:
    - Subscription required
    - Limited to indexed journals
    - No preprints
  
  query_format:
    - Boolean operators
    - Field-specific search
    - Year range
    - Document type filter
```

---

## Scopus

### Characteristics
- **Type**: Abstract and citation database
- **Coverage**: Science, technology, medicine, social sciences
- **Access**: Subscription required
- **Strengths**: Author profiles, comprehensive metrics

### Search Strategy

```yaml
Scopus:
  best_for:
    - Author disambiguation
    - Institution analysis
    - Citation metrics
  
  limitations:
    - Subscription required
    - Coverage gaps in humanities
  
  query_format:
    - Boolean operators
    - Author ID search
    - Affiliation search
    - Source title filter
```

---

## ScienceDirect

### Characteristics
- **Type**: Elsevier journal platform
- **Coverage**: Elsevier journals
- **Access**: Subscription for full text
- **Strengths**: High-quality journal content

### Search Strategy

```yaml
ScienceDirect:
  best_for:
    - Elsevier journal articles
    - STM fields
    - Full text when subscribed
  
  limitations:
    - Limited to Elsevier content
    - Paywall for unsubscribed
  
  query_format:
    - Natural language
    - Boolean operators
    - Journal filter
```

---

## Springer Nature

### Characteristics
- **Type**: Publisher platform
- **Coverage**: Springer and Nature journals
- **Access**: Mix of OA and paywalled
- **Strengths**: High-impact journals (Nature)

### Search Strategy

```yaml
Springer:
  best_for:
    - Nature journal articles
    - Springer books/journals
    - Some open access
  
  limitations:
    - Publisher-specific
    - Many paywalled
  
  query_format:
    - Natural language
    - DOI lookup
    - Journal filter
```

---

## Database Selection Guide

### By Field

| Field | Primary | Secondary |
|-------|---------|-----------|
| CS/AI/ML | arXiv, Semantic Scholar | Google Scholar |
| Physics | arXiv, Web of Science | Semantic Scholar |
| Biomedical | Semantic Scholar, PubMed* | Google Scholar |
| Social Science | Web of Science, Scopus | Google Scholar |
| Finance | Semantic Scholar, SSRN* | Google Scholar |
| All fields | Semantic Scholar | Crossref |

*PubMed and SSRN are available through dedicated MCP tools if configured.

### By Need

| Need | Recommended Database |
|------|---------------------|
| Latest preprints | arXiv |
| Citation analysis | Semantic Scholar |
| DOI validation | Crossref |
| Grey literature | Google Scholar |
| High-quality curated | Web of Science |
| Author tracking | Semantic Scholar, Scopus |

---

## Parallel Search Protocol

When executing parallel searches:

```yaml
parallel_search:
  default_databases:
    - arXiv (for CS/ML topics)
    - Semantic Scholar
    - Crossref
  
  optional_additions:
    - Google Scholar (if broad coverage needed)
    - Web of Science (if quality filter needed)
  
  deduplication:
    primary_key: DOI
    fallback: Title similarity (>= 0.85)
  
  rate_limits:
    respect_each_database: true
    batch_delay: 0.5s
```

---

## Error Handling by Database

| Database | Common Error | Handling |
|----------|--------------|----------|
| arXiv | Timeout | Retry with smaller query |
| Semantic Scholar | 429 Rate Limit | Wait 1s, retry |
| Google Scholar | Blocked | Use Semantic Scholar instead |
| Crossref | Missing metadata | Accept incomplete record |
| Web of Science | Auth failed | Fall back to Semantic Scholar |