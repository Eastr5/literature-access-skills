# Literature Search Skill

[![License: CC BY-NC 4.0](https://img.shields.io/badge/license-CC%20BY--NC%204.0-lightgrey)](https://creativecommons.org/licenses/by-nc/4.0/)

Multi-database literature search skill with PDF download, citation analysis, and author tracking capabilities.

**Complements [academic-research-skills](https://github.com/Imbad0202/academic-research-skills)** by providing execution-level tools for the "search-download-analyze" pipeline.

---

## Features

### Multi-Database Parallel Search
- Search across arXiv, Semantic Scholar, Google Scholar, Crossref, Web of Science, and more
- Automatic deduplication by DOI and title similarity
- Results ranked by relevance and citation count
- Open access status detection

### PDF Download
- Priority: Open Access → SciHub → Institutional
- SciHub mirror health checking
- File integrity verification
- Batch download support

### Citation Analysis
- Forward citations (who cited this paper)
- Backward references (what this paper cites)
- Citation network visualization
- Research lineage tracing
- Key influencer identification

### Author Tracking
- Author search with disambiguation
- Publication lists sorted by impact
- Collaboration network analysis
- h-index and other metrics

---

## Installation

### As a Claude Code Skill

1. Clone or download this repository
2. Place in your `.trae/skills/` directory:
   ```
   ~/.trae/skills/literature-search/
   ```
3. Restart Claude Code

### Requirements

- Claude Code CLI with MCP support
- Configured `paper-search` MCP server (for search/download)
- Configured `semantic-scholar` MCP server (for citation analysis)

---

## Usage

### Search Mode

```
"Search for papers on graph neural networks for credit risk"
"论文搜索：深度学习在金融风险中的应用"
```

Output: Ranked search results with metadata, open access status, and recommendations.

### Download Mode

```
"Download paper 10.1234/example.2024.001"
"下载论文：[DOI or title]"
```

Output: PDF file saved locally with source attribution.

### Citation Mode

```
"Citation analysis for paper [DOI]"
"引用分析：[paper title]"
```

Output: Citation network with forward/backward analysis and key influencers.

### Author Mode

```
"Track author [name]"
"作者追踪：[name]"
```

Output: Author profile with publications, metrics, and collaboration network.

---

## Integration with academic-research-skills

This skill is designed to complement [academic-research-skills](https://github.com/Imbad0202/academic-research-skills):

| academic-research-skills | literature-search |
|-------------------------|-------------------|
| `bibliography_agent` (planning) | `search_agent` (execution) |
| `source_verification_agent` | `download_agent` (PDF acquisition) |
| `synthesis_agent` | `citation_agent` (network analysis) |

### Data Flow

```
bibliography_agent (search strategy)
         ↓
literature-search (execute search)
         ↓
download_agent (acquire PDFs)
         ↓
source_verification_agent (validate)
         ↓
synthesis_agent (integrate findings)
```

---

## MCP Tools Used

### paper-search MCP
- `search_arxiv`
- `search_semantic_scholar`
- `search_google_scholar`
- `search_crossref`
- `search_webofscience`
- `download_paper`
- `search_scihub`
- `check_scihub_mirrors`

### semantic-scholar MCP
- `search_papers`
- `get_paper`
- `get_paper_citations`
- `get_paper_references`
- `get_author`
- `get_author_papers`
- `search_authors`
- `get_recommendations_for_paper`

---

## Directory Structure

```
literature-search/
├── SKILL.md                    # Main skill definition
├── agents/
│   ├── search_agent.md         # Multi-database search
│   ├── download_agent.md       # PDF acquisition
│   ├── citation_agent.md       # Citation analysis
│   └── author_agent.md         # Author tracking
├── references/
│   ├── database_protocols.md   # Database strategies
│   ├── download_sources.md     # Download source priority
│   └── citation_metrics.md     # Metric interpretations
├── templates/
│   ├── search_report.md        # Search report format
│   └── citation_network.md     # Citation network format
└── README.md
```

---

## Quality Standards

1. **Deduplication first** — Never show duplicate results
2. **Source transparency** — Always report which database each result came from
3. **Download attribution** — Report download source and legal status
4. **Citation context** — Explain why papers cite each other
5. **Author disambiguation** — Handle name conflicts carefully

---

## License

This work is licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).

**Attribution format:**
```
Based on Literature Search Skill by [Your Name]
https://github.com/[username]/literature-search-skill
```

---

## Related Projects

- [academic-research-skills](https://github.com/Imbad0202/academic-research-skills) — Complete academic research skill package
- [paper-search MCP](https://github.com/[paper-search-mcp]) — Paper search MCP server
- [semantic-scholar MCP](https://github.com/[semantic-scholar-mcp]) — Semantic Scholar MCP server

---

## Changelog

### v1.0.0 (2026-05-31)

- Initial release
- Multi-database parallel search
- PDF download with SciHub fallback
- Citation network analysis
- Author tracking
