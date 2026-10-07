---
name: literature-search
description: >
  Searches and discovers academic papers across multiple sources (Semantic
  Scholar, arXiv, Tavily, Exa, Gemini deep research, AMiner, Google Scholar)
  with adaptive engine selection based on query type. Returns ranked,
  deduplicated results with metadata (authors, venue, year, citations, abstract,
  PDF link). Use when the user asks to find papers / literature / publications /
  preprints / references on a topic, search for related work, look up a specific
  paper by title or DOI or arXiv ID, find papers by an author, find recent SOTA
  / state-of-the-art work, survey a research area, or run a deep / comprehensive literature search with synthesis.
---

# Literature Search

Systematic, multi-engine academic paper search.

## When to Use

- User asks "find papers about X"
- User needs related work for a new project
- User wants to know the state of the art on a topic
- User asks for papers from a specific venue/author/year

## Engine Selection

Choose engines based on the search goal:

| Goal | Primary Engine | Supplementary |
|------|---------------|---------------|
| **Broad topic survey** | Semantic Scholar | arXiv, Tavily |
| **Latest preprints** | arXiv (sort by submittedDate) | Semantic Scholar |
| **Deep research / complex questions** | Gemini deep research | Tavily + Exa |
| **Specific paper by title** | Semantic Scholar | Google Scholar (via Tavily) |
| **Papers by author** | Semantic Scholar (author search) | AMiner |
| **Chinese research community** | AMiner | Semantic Scholar |
| **Industry/applied papers** | Tavily (deep) | Exa semantic search |
| **Social buzz / trending papers** | Twitter/X (xreach) | Reddit |
| **Code implementations** | GitHub (gh search) | Exa (get_code_context) |
| **Finding similar papers** | Exa (semantic) | Semantic Scholar (citations) |

## ⚠️ 先读这一段：本机脚本与 node 路径

本技能自带的 `scripts/search/*.mjs` 此前缺失，现已补齐三个（2026-09-29 重写并通过实测）。
**必须用 managed node 运行**（系统 node 也能跑，但统一用下面这个路径）：

```
~/.workbuddy\binaries\node\versions\22.22.2\node.exe
```

```bash
# OpenAlex：主力通道，无需 key，覆盖期刊论文最全
node scripts/search/openalex.mjs "guarantee network credit risk contagion firm" -n 10 --from 2015

# arXiv：找最新预印本，默认按相关度排序
node scripts/search/arxiv.mjs "corporate default prediction graph neural network" -n 8
node scripts/search/arxiv.mjs "credit risk" -n 10 --cat q-fin.RM --sort submittedDate

# Semantic Scholar：引用数最准，但极易 429；失败时请改用 openalex.mjs
node scripts/search/semantic-scholar.mjs "corporate default prediction" -n 15 --year 2018-2026
```

**三个已知坑（都踩过）**：
1. OpenAlex 限流很凶，连续请求之间要 sleep 10 秒以上；脚本已内置 429 退避重试。
2. arXiv 的 `search_query` 整句加引号会返回 0 条，按 `submittedDate` 排序会把当天无关预印本排在最前。
   脚本现在的做法是取前 5 个实词用 `+AND+` 连接，默认按相关度排序。
3. `.mjs` 是 ESM，里面不能用 `require()`。

**覆盖不到的部分（必须告诉用户）**：CNKI、万方、Web of Science 需要机构订阅与登录态，
本技能进不去。中文期刊（经济研究、管理世界、金融研究、会计研究）的检索必须用户手动做，
或由用户提供检索结果后由助手判读。

## Workflow

### Step 1: Understand the Query

Before searching, clarify:
- **Scope**: Broad survey vs. specific subtopic
- **Recency**: All time vs. last N years vs. latest only
- **Venue preference**: Top-tier only? Specific conference?
- **Quantity**: Top 5 vs. comprehensive survey
- **Depth**: Quick list vs. deep research with synthesis

### Step 2: Select Search Strategy

**Quick search (single engine):**
For simple, well-defined queries. Use Semantic Scholar or arXiv directly.

**Multi-engine search (2-3 engines in parallel):**
For broader topics. Run engines simultaneously, deduplicate results.

**Deep research (Gemini):**
For complex, multi-faceted research questions. Gemini deep research mode synthesizes across many sources and provides a structured analysis with citations. Use this when:
- The question spans multiple subfields
- You need synthesis, not just a list of papers
- The user explicitly asks for "deep research" or "comprehensive survey"

### Step 3: Execute Search

```bash
# Semantic Scholar — paper metadata, citations, author search
# Free, no API key needed
node scripts/search/semantic-scholar.mjs "query" -n 20

# arXiv — latest preprints, category filtering
# Free, no API key needed
node scripts/search/arxiv.mjs "query" -n 15 --sort submittedDate --cat cs.CL

# Tavily — general web search, AI-optimized
node scripts/search/search.mjs "query site:arxiv.org OR site:aclanthology.org" -n 10
node scripts/search/search.mjs "query" --deep  # deeper search mode

# Exa — semantic search, finding similar content
mcporter call 'exa.web_search_exa(query: "query", numResults: 10)'

# Gemini — deep research (for complex questions)
# Use gemini-3.1-pro model with web search grounding
# Prompt: "Survey the recent literature on [topic]. Identify key papers,
#          main approaches, and open problems. Cite specific papers."

# AMiner — Chinese academic community
# Uses AMINER_API_KEY
```

### Step 4: Deduplicate & Rank

Merge results across engines:
1. Deduplicate by title similarity (fuzzy match, >90% = same paper)
2. Rank by: citation count × recency × venue tier × relevance
3. Flag if a paper appears in multiple engines (higher confidence)

### Step 5: Present Results

Format as a ranked list with key metadata:

```
1. **[Title]** (Venue Year, Citations: N)
   Authors: [First author] et al.
   TL;DR: [1 sentence]
   Why relevant: [connection to user's query]

2. ...
```

### Step 6: Deep Dive (Optional)

If user wants to go deeper on any paper:
- Switch to paper-reading skill
- Or add to Zotero reading queue (use zotero-management skill)

## Search Tips

- **Use specific terminology**: "multi-agent reinforcement learning" > "MARL" > "agents working together"
- **Combine with venue filter**: Adding `venue:ACL` or category `cs.CL` dramatically improves precision
- **Check citation chains**: A highly-cited paper's references and citers are often gold
- **Cross-lingual**: For Chinese papers, try both English and Chinese queries
- **Date filter for SOTA**: Use `--sort submittedDate` on arXiv to find the latest approaches
- **Gemini for synthesis**: When you need to understand a field (not just list papers), use Gemini deep research to get a narrative overview first, then drill into specific papers

## Quality Signals

When ranking, weight these signals:
- **Citation count**: High for established work, less meaningful for papers < 6 months old
- **Venue tier**: ACL/EMNLP/NeurIPS/ICML > workshops > arXiv-only
- **Author reputation**: Check if senior authors are established in the field
- **Code availability**: Papers with code are more verifiable
- **Reproducibility**: Clear methodology sections and experimental details
