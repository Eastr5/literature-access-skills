# Download Sources Priority and Reliability

This document describes the priority ordering and reliability assessment of PDF download sources.

## Download Priority Order

| Priority | Source | Legal Status | Reliability | Use Case |
|----------|--------|--------------|-------------|----------|
| **1** | Open Access (Publisher) | ✅ Legal | High | First attempt |
| **2** | arXiv | ✅ Legal | High | CS/ML preprints |
| **3** | PubMed Central | ✅ Legal | High | Biomedical |
| **4** | Institutional Repository | ✅ Legal | Medium | University access |
| **5** | Unpaywall | ✅ Legal | Medium | OA discovery |
| **6** | SciHub | ⚠️ Gray area | Variable | Last resort |

---

## Open Access Sources

### Publisher OA

Many publishers now offer open access options:

| Publisher | OA Options | Notes |
|-----------|------------|-------|
| Elsevier | Hybrid OA, Subscribe to Open | Check "Open Access" badge |
| Springer | SpringerOpen, Nature OA | Some fully OA journals |
| Wiley | Wiley OA, Hybrid | Open Access indicator |
| IEEE | IEEE OA | Limited OA options |
| ACM | ACM DL | Mostly paywalled |

**Detection**: Look for "Open Access" label on publisher page.

### arXiv

- **URL pattern**: `https://arxiv.org/pdf/{arxiv_id}.pdf`
- **Reliability**: Very high
- **Speed**: Fast
- **Use**: CS, physics, math, statistics preprints

**Detection**: Paper has arXiv ID (e.g., "arXiv:2401.12345")

### PubMed Central

- **URL**: `https://pmc.ncbi.nlm.nih.gov/articles/PMC{id}/pdf`
- **Reliability**: High
- **Speed**: Fast
- **Use**: Biomedical papers, clinical research

**Detection**: Paper has PMID or PMC ID

### Institutional Repositories

Many universities host OA versions:

| Repository | Example | Detection |
|------------|---------|-----------|
| MIT DSpace | `dspace.mit.edu` | Author affiliation |
| Harvard DASH | `dash.harvard.edu` | Author affiliation |
| UCL Discovery | `discovery.ucl.ac.uk` | UK papers |
| Chinese universities | Various | CNKI, Wanfang |

**Detection**: Check author affiliation, search repository

---

## SciHub

### Legal Considerations

⚠️ **Important**: SciHub operates in legal gray areas in many jurisdictions.

- Some countries block SciHub domains
- Publishers actively pursue legal action
- Use institutional access when available
- Consider ethical implications

### Mirror Checking Protocol

Before using SciHub:

```yaml
scihub_protocol:
  step_1: check_scihub_mirrors
    - Get list of working mirrors
    - Note mirror status (active/inactive)
  
  step_2: select_mirror
    - Choose most reliable mirror
    - Prefer HTTPS mirrors
  
  step_3: attempt_download
    - Use DOI as primary identifier
    - Retry with title if DOI fails
  
  step_4: verify_file
    - Check file is valid PDF
    - Minimum size: 10KB
    - Contains %PDF- header
```

### Common SciHub Mirrors

| Mirror | Status | Notes |
|--------|--------|-------|
| `sci-hub.se` | Variable | Often blocked |
| `sci-hub.st` | Variable | Check availability |
| `sci-hub.ru` | Variable | Russian mirror |
| Others | Variable | Check `check_scihub_mirrors` tool |

**Always check mirror health before attempting download.**

---

## Unpaywall Integration

Unpaywall finds legal OA versions:

```yaml
unpaywall:
  api: "https://api.unpaywall.org/v2/{doi}?email={email}"
  
  response_fields:
    - is_oa: boolean
    - oa_status: "gold", "green", "hybrid", "bronze", "closed"
    - best_oa_location: URL and version
  
  oa_status_meaning:
    gold: Publisher-hosted OA
    green: Repository-hosted OA
    hybrid: Paywalled with OA option
    bronze: Free but not OA license
    closed: No OA found
```

---

## Download Workflow

### Step-by-Step

```yaml
download_workflow:
  step_1: check_oa
    - Query Unpaywall API
    - If is_oa=true, use best_oa_location
  
  step_2: check_arxiv
    - If arXiv ID available, download from arXiv
  
  step_3: check_pubmed
    - If PMID/PMC ID, check PubMed Central
  
  step_4: check_institutional
    - If configured, check institutional access
  
  step_5: scihub_fallback
    - Check mirrors
    - Attempt download
    - Verify file
  
  step_6: report_status
    - Document source used
    - Report success/failure
```

---

## File Verification

After download, verify:

```yaml
verification_checks:
  file_exists: true
  file_size: > 10KB
  pdf_header: "%PDF-" in first line
  not_error_page: not HTML response
  
  quality_checks:
    - No "Access Denied" text
    - No "Login Required" text
    - Pages > 0
```

---

## Source Attribution

Always report download source:

```markdown
## Download Source Attribution

- **Source**: [Open Access / SciHub / Institutional]
- **URL**: [Source URL]
- **Legal Status**: [Legal / Gray Area]
- **Verified**: [Yes / No]
```

---

## Batch Download Protocol

For multiple papers:

```yaml
batch_download:
  check_mirrors_once: true
  
  rate_limiting:
    oa_sources: no limit
    scihub: 1 request per 2 seconds
  
  error_handling:
    per_paper: log individual failures
    aggregate: summary at end
  
  priority_order: same as single paper
```

---

## Ethical Guidelines

1. **Always try legal sources first**
2. **Use institutional access when available**
3. **Consider contacting author for copy**
4. **SciHub should be last resort**
5. **Respect publisher copyright policies**
6. **Be aware of local legal implications**