# Hard Architecture Mapping: Skill Seekers

**Date:** 2025-11-20  
**Analysis Level:** 1 (Data & Reality)  
**Target:** https://github.com/yusufkaraaslan/Skill_Seekers  
**Analyst:** GitHub Copilot (System Owner)

---

## Executive Summary

**Skill Seekers** is a **documentation-to-AI-skill transformation pipeline** that converts documentation websites, GitHub repositories, and PDFs into Claude AI Skills. At 11,291 LOC across 191 commits (Oct 17 - Nov 20, 2025), this is a **multi-source intelligence aggregator** that practices "Documentation as Executable Knowledge."

**Paradigm:** Skills are not just text—they are **structured knowledge graphs** with conflict detection, categorization, and AI enhancement. The system treats documentation + code + issues as **triple-source ground truth**, detecting discrepancies to expose reality vs. intent.

**Architecture Pattern:** 5-layer clean architecture with MCP integration, dual-mode enhancement (local + API), and async scraping engine achieving 3× performance gain.

---

## 1. Technical Ground Truth

### 1.1 Codebase Metrics

| Metric | Value | Notes |
|--------|-------|-------|
| **Total LOC** | 11,291 lines | Python 3.10+ codebase |
| **Commits** | 191 commits | 34-day development (Oct 17 - Nov 20, 2025) |
| **Peak Velocity** | ~20 commits/day | Oct 19, 2025 (foundation sprint) |
| **Files** | 32 Python modules | Organized in `src/skill_seekers/` |
| **Test Coverage** | 379 tests passing | 39% coverage, production-ready |
| **Package Status** | Published on PyPI | v2.0.0 production release |

### 1.2 Technology Stack

**Core Languages & Frameworks:**
- **Python 3.10+** (mandatory minimum for MCP)
- **FastMCP** - Model Context Protocol server framework
- **BeautifulSoup4** - HTML parsing and scraping
- **PyGithub** - GitHub API integration
- **PyMuPDF + Pillow + pytesseract** - PDF extraction with OCR
- **Pydantic** - Data validation and settings
- **Click** - CLI framework

**Optional/Enhancement:**
- **Anthropic SDK** - Claude API for AI enhancement
- **Pygments** - Code syntax highlighting
- **httpx + httpx-sse** - Async HTTP with streaming support

**Distribution:**
- **setuptools** - Modern Python packaging (pyproject.toml)
- **PyPI** - Public package distribution

---

## 2. Architecture Layers (5-Layer Clean Architecture)

Skill Seekers follows a **clean architecture pattern** with clear separation of concerns:

### Layer 1: Protocol Interface (MCP Server)

**Location:** `src/skill_seekers/mcp/`

**Purpose:** Expose Skills generation as MCP tools for AI agents

**Key Components:**
- **`server.py`** (200+ LOC) - FastMCP server with 9 tools
- **`tools/__init__.py`** - Tool implementations

**9 MCP Tools:**
1. `list_configs` - List available preset configurations
2. `generate_config` - Generate new config for any docs site
3. `validate_config` - Validate config file structure
4. `estimate_pages` - Estimate page count before scraping
5. `scrape_docs` - Scrape and build a skill
6. `package_skill` - Package skill into .zip (auto-upload)
7. `upload_skill` - Upload .zip to Claude
8. `split_config` - Split large documentation configs
9. `generate_router` - Generate router/hub skills

**Protocol Pattern:** Streaming subprocess execution to avoid blocking on long-running scrapes. Uses `select` (Unix) for real-time output.

**Key Innovation:** MCP tools **wrap CLI commands**, not reimplement them—maintaining single source of truth.

---

### Layer 2: Business Logic (Core Scrapers & Processors)

**Location:** `src/skill_seekers/cli/`

**5 Primary Scrapers:**

#### 2.1 Documentation Scraper (`doc_scraper.py`)
- **Function:** HTML scraping with BeautifulSoup4
- **Intelligence:** llms.txt auto-detection (10× speedup when available)
- **Categorization:** Automatic content classification by URL patterns
- **Selectors:** Configurable CSS selectors per site
- **Rate Limiting:** Configurable delays (default: 0.5s)

#### 2.2 GitHub Scraper (`github_scraper.py`)
- **Function:** Deep repository analysis via PyGithub API
- **Code Analysis:** AST parsing for Python, JS, TS, Java, C++, Go
- **Extracted Data:**
  - Functions, classes, methods with parameters/types
  - Repository metadata (README, file tree, language breakdown)
  - Issues & PRs (open/closed, labels, milestones)
  - CHANGELOG & releases (version history)
- **Depth Modes:** Surface (public APIs) vs. Deep (internals)

#### 2.3 PDF Scraper (`pdf_scraper.py`)
- **Function:** Extract text, code, images from PDFs
- **OCR Support:** pytesseract for scanned documents
- **Table Extraction:** Complex table parsing
- **Password Handling:** Encrypted PDF support
- **Performance:** 3× faster with parallel processing
- **Caching:** 50% faster on re-runs

#### 2.4 Unified Scraper (`unified_scraper.py`)
- **Function:** Multi-source aggregation (docs + GitHub + PDF)
- **Conflict Detection:** Compare documented vs. actual APIs
- **Merge Modes:**
  - `rule-based` - Deterministic conflict resolution
  - `claude-enhanced` - AI-powered merging
  - `side-by-side` - Show both versions with warnings
- **Gap Analysis:** Identify outdated docs and undocumented features

#### 2.5 Async Scraper (Mode within scrapers)
- **Function:** Async/await for 2-3× performance gain
- **Workers:** Configurable (4-8 recommended)
- **Performance:** ~55 pages/sec vs. ~18 pages/sec (sync)
- **Memory:** 40MB (async) vs. 120MB (sync)

---

### Layer 3: Intelligence & Enhancement

**Location:** `src/skill_seekers/cli/enhance_skill*.py`

#### 3.1 Conflict Detector (`conflict_detector.py`)
- **Function:** Find discrepancies between docs and code
- **Detection Types:**
  - APIs missing in documentation (undocumented features)
  - APIs missing in code (documentation drift)
  - Signature mismatches (parameter/return type differences)
- **Pattern:** AST parsing + regex-based doc parsing
- **Output:** Side-by-side comparison with ⚠️ warnings

#### 3.2 Code Analyzer (`code_analyzer.py`)
- **Function:** Language-specific AST parsing
- **Supported Languages:** Python, JavaScript, TypeScript, Java, C++, Go, C#
- **Extracted:** Function signatures, class hierarchies, docstrings
- **Depth Control:** Surface vs. Deep analysis

#### 3.3 AI Enhancement (Dual Mode)

**Local Enhancement** (`enhance_skill_local.py`):
- **Method:** Uses Claude Code Max (no API key required)
- **Terminal Detection:** Auto-detects iTerm2, Apple Terminal, VS Code
- **Process:** Opens Claude Code → pastes template → waits for enhancement
- **Cost:** **FREE** (uses local Claude session)

**API Enhancement** (`enhance_skill.py`):
- **Method:** Anthropic API with streaming
- **Process:** Sends template → receives enhanced version
- **Cost:** Per-token pricing (typically $0.50-2.00 per skill)

---

### Layer 4: Packaging & Distribution

**Location:** `src/skill_seekers/cli/package_*.py`

#### 4.1 Single Skill Packager (`package_skill.py`)
- **Function:** Bundle SKILL.md + references → .zip
- **Structure:**
  ```
  skill-name.zip
  ├── SKILL.md (main entry point with YAML frontmatter)
  ├── references/
  │   ├── category1.md
  │   ├── category2.md
  │   └── ...
  ```
- **YAML Frontmatter:** Title, description, contact info
- **Auto-Upload:** Detects ANTHROPIC_API_KEY → uploads to Claude

#### 4.2 Multi-Skill Packager (`package_multi.py`)
- **Function:** Process multiple skills in parallel
- **Use Case:** Batch generation for organizations

#### 4.3 Router Generator (`generate_router.py`)
- **Function:** Create hub skills for large documentation (10K-40K pages)
- **Pattern:** Main router → specialized sub-skills
- **Intelligence:** Routing logic based on query intent

---

### Layer 5: Configuration & Utilities

**Location:** `src/skill_seekers/cli/` (utils, validators, constants)

#### 5.1 Configuration System

**24 Preset Configs:**
- **Single-Source:** ansible-core, astro, claude-code, django, fastapi, godot, hono, kubernetes, laravel, react, tailwind, vue, etc.
- **Multi-Source:** django_unified, fastapi_unified, godot_unified, react_unified
- **Test Configs:** example_pdf, test-manual, python-tutorial-test

**Config Structure:**
```json
{
  "name": "react",
  "description": "When to use this skill",
  "merge_mode": "rule-based",
  "sources": [
    {
      "type": "documentation",
      "base_url": "https://react.dev/",
      "selectors": { "main_content": "article" },
      "categories": { "hooks": ["hooks", "usestate"] },
      "max_pages": 200
    },
    {
      "type": "github",
      "repo": "facebook/react",
      "include_issues": true,
      "code_analysis_depth": "surface"
    }
  ]
}
```

#### 5.2 Supporting Utilities

- **`config_validator.py`** - JSON schema validation
- **`llms_txt_detector.py`** - Auto-detect llms.txt files
- **`llms_txt_parser.py`** - Parse llms.txt format (10× faster than HTML)
- **`estimate_pages.py`** - Pre-scrape page count estimation
- **`split_config.py`** - Split large docs into sub-skills
- **`constants.py`** - Shared constants and patterns

---

## 3. Skills Pattern Analysis (Special Focus)

### 3.1 What IS a "Skill"?

**Formal Definition:**
A **Skill** is a **structured knowledge package** for Claude AI consisting of:
1. **SKILL.md** - Main entry point (YAML frontmatter + Markdown)
2. **references/** - Categorized reference files (category1.md, category2.md, ...)
3. **Metadata** - Title, description, usage guidance

**Format:**
```yaml
---
name: React
description: Use when building React applications
contact: https://react.dev
---

# React Skill

[Main content with links to references]

See [Hooks Reference](references/hooks.md) for details.
```

**Key Insight:** Skills are NOT raw dumps—they are **intelligently organized, categorized, and enhanced** knowledge graphs.

---

### 3.2 The Skills Pattern (Core Innovation)

**Pattern Name:** **Documentation-as-Executable-Knowledge**

**Problem:** Raw documentation is:
- Scattered across multiple sites
- Outdated (docs vs. code drift)
- Unstructured (no categorization)
- Verbose (not optimized for LLM context windows)

**Solution:** Skills transform documentation into:
- **Aggregated:** Combine docs + GitHub + PDFs
- **Validated:** Conflict detection finds drift
- **Structured:** Automatic categorization by topic
- **Enhanced:** AI extracts best examples and key concepts
- **Packaged:** Single .zip file with standardized format

**Implementation Patterns:**

#### Pattern 1: Triple-Source Ground Truth
```python
# Skill Seekers uses 3 sources of truth:
sources = [
    "documentation",  # Intent (what authors say it does)
    "github",         # Reality (what code actually does)
    "issues"          # Problems (what users report)
]

# Compare all 3 → detect conflicts
conflicts = detect_conflicts(docs, code, issues)
```

**Why This Matters:** Most tools scrape docs OR analyze code. Skill Seekers does BOTH and finds discrepancies.

#### Pattern 2: llms.txt First-Class Support
```python
# Before scraping 10K pages:
if detect_llms_txt(base_url):
    # Download single file (10× faster)
    return parse_llms_txt(llms_txt_url)
else:
    # Fall back to HTML scraping
    return scrape_html_pages(base_url)
```

**Why This Matters:** llms.txt is emerging as the standard for LLM-friendly docs. Skill Seekers supports it natively.

#### Pattern 3: Conflict-Aware Merging
```python
# When docs say one thing and code says another:
def merge_with_conflicts(doc_api, code_api):
    if signatures_match(doc_api, code_api):
        return doc_api  # Docs are correct
    else:
        return {
            "warning": "⚠️ Documentation drift detected",
            "documented": doc_api,
            "actual": code_api,
            "suggestion": "Use actual implementation"
        }
```

**Why This Matters:** Instead of hiding conflicts, Skills expose them—teaching AI agents to trust code over docs.

#### Pattern 4: Progressive Disclosure (Router Pattern)
```python
# For large documentation (40K pages):
def generate_router_skill(large_config):
    # Split into sub-skills
    sub_skills = split_by_category(large_config)
    
    # Create router
    router = {
        "name": "Django Hub",
        "description": "Routes to specialized Django sub-skills",
        "routing_logic": {
            "query_contains('ORM')": "django-orm-skill",
            "query_contains('views')": "django-views-skill",
            # ...
        }
    }
    
    return router, sub_skills
```

**Why This Matters:** Solves token limit problems while maintaining comprehensive coverage.

#### Pattern 5: Dual Enhancement Modes
```python
# Users can choose:
enhancement_modes = {
    "local": {  # FREE, uses Claude Code Max
        "cost": 0,
        "speed": "60 seconds",
        "quality": "high",
        "requires": "Claude Code Max access"
    },
    "api": {  # Paid, uses Anthropic API
        "cost": "$0.50-2.00 per skill",
        "speed": "30 seconds",
        "quality": "high",
        "requires": "ANTHROPIC_API_KEY"
    }
}
```

**Why This Matters:** Removes cost barrier for individual developers while offering faster option for production.

---

### 3.3 Skills Pattern as MCP Integration

**Key Realization:** Skills generation is exposed as **MCP tools**, not just CLI.

**Significance:**
- AI agents can **generate Skills autonomously**
- Natural language: "Scrape React documentation and create a skill"
- Streaming output prevents blocking on long scrapes
- MCP tools wrap CLI (no code duplication)

**Pattern:**
```python
@app.tool()
async def scrape_docs(config_path: str):
    # Don't reimplement scraping logic
    # Instead, call CLI command:
    cmd = ["skill-seekers", "scrape", "--config", config_path]
    stdout, stderr, code = run_subprocess_with_streaming(cmd)
    return {"output": stdout, "errors": stderr}
```

**Why This Matters:** MCP makes Skills generation **agent-accessible**, not just human-accessible.

---

### 3.4 Skills as Knowledge Graphs

**Insight:** Skills are not flat text files—they are **graph structures**:

```
SKILL.md (Hub)
  ├─→ references/getting_started.md
  ├─→ references/components.md
  │     ├─→ references/props.md
  │     └─→ references/state.md
  ├─→ references/hooks.md
  │     ├─→ references/usestate.md
  │     └─→ references/useeffect.md
  └─→ references/api.md
```

**Navigation:** Internal links create graph traversal paths
**Categorization:** Automatic topic clustering
**Hierarchy:** Natural tree structure emerges from URL patterns

**Why This Matters:** LLMs retrieve context more efficiently from graphs than from flat dumps.

---

## 4. Metadata & Technical Specifications

### Repository Information
- **URL:** https://github.com/yusufkaraaslan/Skill_Seekers
- **License:** MIT
- **Language:** Python 3.10+
- **Package:** https://pypi.org/project/skill-seekers/
- **Version:** v2.0.0 (production)

### Development Timeline
- **Started:** October 17, 2025
- **First Major Release:** October 19, 2025 (v1.0.0)
- **PyPI Publication:** November 7, 2025 (v2.0.0)
- **Analysis Date:** November 20, 2025
- **Development Duration:** 34 days

### Project Health
- **Tests:** 379 passing (39% coverage)
- **CI/CD:** GitHub Actions (5 test matrix jobs)
- **Documentation:** Comprehensive (README, CLAUDE.md, guides)
- **Community:** Active development, open PRs/issues
- **Maintenance:** High velocity (~5 commits/day avg)

---

## 5. Conclusion

**Skill Seekers is not a scraper—it's a knowledge transformation pipeline.**

The system embodies the **Documentation-as-Executable-Knowledge** paradigm, treating documentation as structured data rather than prose. By combining documentation, code, and issues into a **triple-source ground truth**, it exposes the reality of software (code) vs. the intent (docs).

The **Skills pattern** identified here—multi-source aggregation + conflict detection + categorization + AI enhancement + MCP exposure—is a **reusable architecture** for any system that needs to convert unstructured knowledge into LLM-ready formats.

Key innovations:
1. **Conflict detection** (docs vs. code)
2. **llms.txt support** (10× speedup)
3. **MCP integration** (agent-accessible)
4. **Dual enhancement** (free + paid)
5. **Router pattern** (progressive disclosure)

**Architectural Maturity:** Production-ready with clean separation of concerns, comprehensive testing, and active community development.

---

**Next Analysis:** Level 2 - Decision Forensics (Git history deep dive)
