---
name: "literature-search"
description: "Multi-database literature search, PDF download, citation analysis, and author tracking. Integrates paper-search MCP and semantic-scholar MCP tools. Triggers on: search papers, download paper, citation analysis, author tracking, find literature, 论文搜索, 下载论文, 引用分析, 作者追踪."
---

# Literature Search Skill

Multi-database literature search and acquisition skill with PDF download, citation analysis, and author tracking capabilities.

## Core Features

### 1. Multi-Database Parallel Search
- Search across arXiv, Semantic Scholar, Google Scholar, Crossref, Web of Science, and more
- Automatic deduplication and result merging
- Sort by relevance or citation count
- Advanced filtering (year, field, open access)

### 2. PDF Download
- Multi-source priority download (Open Access → SciHub → Institutional)
- SciHub mirror health check
- Download status tracking
- Batch download support

### 3. Citation Analysis
- Citation network visualization
- High-impact paper identification
- Citation chain tracing
- Research lineage analysis

### 4. Author Tracking
- Author search
- Author publication list
- High-productivity author identification
- Collaboration network analysis

## Trigger Conditions

Invoke this skill when:
- User wants to search academic papers ("search papers about...", "find literature on...", "论文搜索")
- User needs to download paper PDF ("download this paper", "get PDF for...", "下载论文")
- User wants to analyze citations ("citation analysis for...", "who cited this paper", "引用分析")
- User wants to track authors ("track author...", "find papers by...", "作者追踪")
- User needs paper recommendations ("recommend similar papers", "related work")

## Modes

| Mode | Trigger | Output |
|------|---------|--------|
| **search** | "search papers on [topic]" | Search report with ranked results |
| **download** | "download paper [DOI/title]" | Download status + local path |
| **citation** | "citation analysis for [paper]" | Citation network + key influencers |
| **author** | "track author [name]" | Author profile + publication list |
| **recommend** | "recommend similar to [paper]" | Related papers ranked by relevance |

## MCP Tools Integration

### paper-search MCP Tools
- `mcp_paper-search_search_arxiv` — arXiv search
- `mcp_paper-search_search_semantic_scholar` — Semantic Scholar search
- `mcp_paper-search_search_google_scholar` — Google Scholar search
- `mcp_paper-search_search_crossref` — Crossref search
- `mcp_paper-search_search_webofscience` — Web of Science search
- `mcp_paper-search_search_sciencedirect` — ScienceDirect search
- `mcp_paper-search_search_springer` — Springer search
- `mcp_paper-search_search_wiley` — Wiley search
- `mcp_paper-search_search_scopus` — Scopus search
- `mcp_paper-search_download_paper` — Paper download
- `mcp_paper-search_search_scihub` — SciHub search
- `mcp_paper-search_check_scihub_mirrors` — SciHub mirror check

### semantic-scholar MCP Tools
- `mcp_semantic-scholar_search_papers` — Paper search
- `mcp_semantic-scholar_get_paper` — Paper details
- `mcp_semantic-scholar_get_paper_citations` — Citations
- `mcp_semantic-scholar_get_paper_references` — References
- `mcp_semantic-scholar_get_paper_authors` — Authors
- `mcp_semantic-scholar_get_author` — Author details
- `mcp_semantic-scholar_get_author_papers` — Author papers
- `mcp_semantic-scholar_search_authors` — Author search
- `mcp_semantic-scholar_get_recommendations_for_paper` — Recommendations
- `mcp_semantic-scholar_batch_get_papers` — Batch paper retrieval
- `mcp_semantic-scholar_bulk_search_papers` — Bulk search

## Workflow

### Search Mode
```
1. Parse query → extract keywords, filters, year range
2. Execute parallel search across configured databases
3. Merge results → deduplicate by DOI/title
4. Rank by relevance + citation count
5. Apply filters (year, open access, field)
6. Generate search report
```

### Download Mode
```
1. Identify paper (DOI → title fallback)
2. Check open access availability first
3. If unavailable, check SciHub mirrors
4. Execute download with retry logic
5. Verify download integrity
6. Report status + local path
```

### Citation Mode
```
1. Get paper citations (forward)
2. Get paper references (backward)
3. Build citation network
4. Identify high-impact nodes
5. Trace citation chains
6. Generate network visualization
```

### Author Mode
```
1. Search author by name
2. Get author profile (h-index, citation count)
3. Get author publications
4. Identify collaboration network
5. Rank by productivity/impact
```

## Output Formats

### Search Report
```markdown
## Literature Search Report

### Query
**Keywords**: [extracted keywords]
**Databases**: [searched databases]
**Filters**: [applied filters]

### Results Summary
- Total unique papers: N
- After filtering: M
- Open access available: K

### Top Results (by relevance)

#### 1. [Title]
- **Authors**: [Author list]
- **Venue**: [Journal/Conference]
- **Year**: [Year]
- **Citations**: [Count]
- **DOI**: [DOI]
- **Abstract**: [Brief abstract]
- **Access**: [Open Access / Paywalled]

#### 2. ...
```

### Citation Network
```markdown
## Citation Network for [Paper Title]

### Forward Citations (N papers cite this)
| Paper | Year | Citations | Key Finding |
|-------|------|-----------|-------------|
| ... | ... | ... | ... |

### Backward References (M papers cited)
| Paper | Year | Why Cited |
|-------|------|-----------|
| ... | ... | ... |

### Citation Network Metrics
- **h-index**: X
- **Citation velocity**: Y/year
- **Field-weighted citation impact**: Z

### Key Influencers
[Top cited-by papers that shape this research line]
```

## Integration with academic-research-skills

This skill complements `academic-research-skills` by providing:

| academic-research-skills | literature-search |
|-------------------------|-------------------|
| Bibliography agent (strategy) | Search agent (execution) |
| Source verification | PDF download + verification |
| Synthesis | Citation network analysis |

### Data Flow
```
bibliography_agent (planning)
        ↓
literature-search (execution)
        ↓
source_verification_agent (validation)
        ↓
synthesis_agent (integration)
```

## Agent References

| Agent | Definition File |
|-------|----------------|
| search_agent | `agents/search_agent.md` |
| download_agent | `agents/download_agent.md` |
| citation_agent | `agents/citation_agent.md` |
| author_agent | `agents/author_agent.md` |

## Reference Files

| Reference | Purpose |
|-----------|---------|
| `references/database_protocols.md` | Database-specific search strategies |
| `references/download_sources.md` | Download source priority and reliability |
| `references/citation_metrics.md` | Citation metric interpretations |

## Templates

| Template | Purpose |
|----------|---------|
| `templates/search_report.md` | Search report format |
| `templates/citation_network.md` | Citation network visualization |

## Quality Standards

1. **Deduplication first** — Never show duplicate papers in results
2. **Source attribution** — Always show which database each result came from
3. **Download transparency** — Report download source and status
4. **Citation context** — When showing citations, explain why each paper is relevant
5. **Author disambiguation** — Handle author name conflicts carefully

## Anti-Patterns

| # | Anti-Pattern | Correct Behavior |
|---|-------------|-----------------|
| 1 | Single database search | Always search multiple databases for comprehensive coverage |
| 2 | Skip deduplication | Deduplicate by DOI and title similarity |
| 3 | Ignore access status | Clearly mark open access vs paywalled |
| 4 | Blind download | Check mirror health before SciHub download |
| 5 | Isolated citation list | Show citation context and relationship |

## Language Support

- Follows user's language
- Academic terminology kept in English
- Search queries adapted to database language requirements
