# Hard Architecture Mapping: Claude Skills MCP Server

**Date:** 2025-11-20  
**Level:** 1 (Data - The Reality)  
**Target:** https://github.com/K-Dense-AI/claude-skills-mcp  
**Codebase:** ~7,100 LOC (3,477 backend + test infrastructure)  
**Timeline:** 22 days (Oct 20 - Nov 10, 2025), 50 commits  

## Executive Summary

The Claude Skills MCP Server implements **Skills-as-Infrastructure**—making Anthropic's Agent Skills available to ANY AI model via Model Context Protocol. This is the "npm moment" for AI capabilities: portable, searchable, semantically-indexed packages of AI competence.

**Core Innovation:** Skills are NOT documentation. They are first-class infrastructure components that can be discovered by task description, loaded progressively to manage context windows, and work across any MCP-compatible AI assistant.

---

## 1. System Architecture: Two-Package Design

**Problem:** Cursor terminates MCP servers that don't respond within 5 seconds. Backend with PyTorch + transformers = 60+ seconds startup.

**Solution:** Frontend-Backend Split

```
AI Assistant (Cursor, Claude Desktop, etc.)
  ↕ stdio MCP
Frontend (~15 MB, <5s start) ✅ Solves timeout
  ↕ HTTP (streamable MCP)
Backend (~250 MB, 15-20s background start)
  → GitHub Skills Repos + Local Directories
```

### 1.1 Frontend Package (`claude-skills-mcp`)

**Purpose:** Lightweight instant-start proxy

**Components:**
- `mcp_proxy.py`: stdio MCP server + HTTP client bridge
- `backend_manager.py`: Process lifecycle management
  - Auto-installs backend via `uvx` if missing
  - Spawns backend process
  - Health checking
  - Zombie process cleanup

**Dependencies:** `mcp`, `httpx` (~15 MB)  
**Startup:** <5 seconds (Cursor compliant)

### 1.2 Backend Package (`claude-skills-mcp-backend`)

**Purpose:** Heavy computation engine

**Core Components:**

1. **http_server.py** (351 LOC): Starlette/Uvicorn HTTP MCP server
2. **mcp_handlers.py** (854 LOC): MCP protocol implementation
   - 3 tools: `find_helpful_skills`, `read_skill_document`, `list_skills`
   - LoadingState tracker (thread-safe progress)
   - Progressive disclosure orchestration

3. **skill_loader.py** (1,090 LOC): Multi-source skill loading
   - GitHub API integration (public repos, no auth)
   - Local directory scanning
   - YAML frontmatter parsing
   - Lazy document loading (4× faster startup: 60s → 15s)
   - Dual caching: memory + disk

4. **search_engine.py** (194 LOC): Vector semantic search
   - sentence-transformers integration
   - Default: all-MiniLM-L6-v2 (384 dims, 90MB)
   - Cosine similarity ranking
   - Lazy model loading
   - Thread-safe incremental indexing

5. **update_checker.py** (416 LOC): Auto-update system
   - Hourly checks (aligned to :00 minutes)
   - GitHub: SHA comparison
   - Local: file mtime tracking
   - State persistence

6. **config.py** (141 LOC): Configuration management
   - Default sources: Anthropic + K-Dense Scientific Skills (~90 skills)
   - JSON config loading
   - Model selection, content limits, update settings

**Dependencies:** `mcp`, `torch`, `sentence-transformers`, `starlette`, `uvicorn`, `httpx`, `numpy` (~250 MB)  
**Startup:** 15-20 seconds (non-blocking background)

---

## 2. Core Architectural Patterns

### 2.1 Skills-as-Infrastructure Pattern

**Structure:**
```yaml
---
name: "PDF Document Parser"
description: "Extract text, tables, and metadata from PDFs"
version: "1.2.0"
tags: ["pdf", "parsing", "documents"]
documents:
  - path: "scripts/parse_pdf.py"
  - path: "data/sample.pdf"
---
# Usage Instructions (Markdown)
...
```

**Key Properties:**
- **Discoverable**: Via semantic vector search
- **Portable**: Works across any MCP-compatible AI
- **Versioned**: SemVer for compatibility
- **Composable**: Can reference other skills
- **Progressive**: Load metadata → content → documents on-demand

**Paradigm:** Skills are the "npm packages" of AI—reusable capability units.

### 2.2 Progressive Disclosure Architecture

**Context Window Economics:**

Without progressive disclosure:
- 90 skills × 2k tokens = 180k tokens (burns context immediately)

With progressive disclosure:
- Level 1: Tool definitions (500 tokens, always)
- Level 2: Skill metadata on search (5 × 100 = 500 tokens)
- Level 3: Full content when relevant (~2k tokens/skill)
- Level 4: Documents on demand (variable)
- **Result: 1k tokens baseline (99.4% reduction)**

**Implication:** Progressive disclosure is MANDATORY for skills to scale, not optional.

### 2.3 Lazy Loading Pattern

**Problem:** Loading 90 skills with documents = 300+ GitHub API calls = 60+ seconds

**Solution:**
1. Startup: Load only SKILL.md files (90 calls) + document metadata
2. On-demand: Fetch document content when `read_skill_document` called
3. Caching: Memory + disk for repeated access

**Performance:**
- Startup: 60s → 15s (4× improvement)
- First document access: ~200ms (network)
- Subsequent: <1ms (memory cache)

### 2.4 Constraint-Driven Design

**Constraint:** Cursor 5-second timeout

**Response:** Not "this is a problem" but "this is a forcing function for better architecture"

**Outcome:**
- Frontend-backend split (separation of concerns)
- Instant user feedback (always responsive)
- Future cloud deployment enabled
- **Insight: Embrace constraints as design specifications**

---

## 3. Data Flow

### 3.1 Startup Sequence

```
1. User: uvx claude-skills-mcp
2. Frontend starts (<5s)
   - Kill zombies, install backend if needed
   - Spawn backend process
   - Start stdio MCP server → Cursor connects ✅
3. Backend starts (background)
   - Load config
   - Background thread: load_all_skills()
     * GitHub: Fetch SKILL.md only (lazy documents)
     * Parse YAML frontmatter
   - Lazy load embedding model
   - Index skills (generate 384-dim vectors)
   - Start HTTP server
   - Initialize hourly scheduler
4. Ready for queries (20-25s total, non-blocking)
```

### 3.2 Query Flow (find_helpful_skills)

```
1. User: "Find skills for parsing PDFs"
2. Frontend → HTTP → Backend
3. Search Engine:
   - Encode query → 384-dim vector
   - Compute cosine similarity with all skills
   - Rank by score, return top-5
4. Format: name, description, score, source, truncated content
5. AI uses skill content in context
```

### 3.3 Document Loading (read_skill_document)

```
1. Match skill by name (fuzzy)
2. Filter documents by pattern (e.g., "*.py")
3. For each document:
   - Check memory cache → return if hit
   - Check disk cache → return if hit
   - Fetch from GitHub (raw content, unlimited)
   - Save to both caches
   - Return content
```

### 3.4 Auto-Update (Hourly)

```
1. For each GitHub source:
   - GET /repos/{owner}/{repo}/commits/HEAD
   - Compare SHA with persisted state
   - If changed: mark for reload
2. For each local source:
   - Scan files, check mtimes
   - If changed: mark for reload
3. If ANY changed:
   - Full reload + re-index (~15s)
   - Update state
```

---

## 4. Technical Stack

### 4.1 Key Technologies

| Component | Technology | Purpose |
|-----------|-----------|----------|
| Frontend MCP | mcp (stdio) | Cursor connection |
| Backend MCP | mcp (streamable HTTP) | Remote-capable server |
| Embeddings | sentence-transformers | Local semantic search |
| Model | all-MiniLM-L6-v2 | 384-dim vectors, 90MB |
| HTTP Server | Starlette + Uvicorn | ASGI async server |
| ML Framework | PyTorch (CPU) | Transformer inference |
| Caching | File system | /tmp/claude_skills_mcp_cache/ |

### 4.2 Configuration

```json
{
  "skill_sources": [
    {"type": "github", "url": "github.com/anthropics/skills"},
    {"type": "github", "url": "github.com/K-Dense-AI/claude-scientific-skills"},
    {"type": "local", "path": "~/.claude/skills"}
  ],
  "embedding_model": "all-MiniLM-L6-v2",
  "max_skill_content_chars": 30000,
  "auto_update_enabled": true,
  "auto_update_interval_minutes": 60
}
```

---

## 5. Performance Characteristics

### 5.1 Startup

| Metric | Time | Blocking? |
|--------|------|-----------|
| Frontend start | <5s | Yes ✅ |
| Backend install (first) | 60-120s | No |
| Backend start | 15-20s | No |
| Total to ready | 20-25s | No |

**vs. v0.x:** 60s blocking → Cursor timeout ❌  
**v1.0:** <5s → Cursor happy ✅

### 5.2 Query Performance

| Operation | Time | Notes |
|-----------|------|-------|
| find_helpful_skills | <1s | Vector search |
| read_skill_document (cached) | <1ms | Memory |
| read_skill_document (disk) | <50ms | Disk |
| read_skill_document (network) | ~200ms | GitHub |

### 5.3 Memory

| Component | Size |
|-----------|------|
| Frontend | ~50 MB |
| Backend base | ~100 MB |
| Embedding model | ~90 MB |
| Skill data | ~600 KB |
| **Total** | ~250 MB |

### 5.4 GitHub API Budget

Unauthenticated (60 req/hr):
- Startup: 2 calls (tree API)
- Auto-update: 2 calls/hr
- Documents: 0 (raw content unlimited)
- **Usage: 4/hr (56 spare)**

---

## 6. Key Architectural Decisions

### 6.1 Why Two Packages?

**Rejected:** Single package  
**Problem:** 250 MB + 60s startup → Cursor timeout  
**Chosen:** Split (15 MB instant + 250 MB background)  
**Verdict:** **Mandatory.** Timeout elimination critical for adoption.

### 6.2 Why Local Embeddings?

**Rejected:** OpenAI/Cohere APIs  
**Chosen:** Local sentence-transformers  
**Benefits:** Zero API keys, zero cost, privacy, offline, fast  
**Trade-off:** Slightly lower quality (acceptable)  
**Verdict:** **Strongly justified.** Eliminates setup friction and costs.

### 6.3 Why Full Reload vs. Incremental?

**Rejected:** Incremental update  
**Chosen:** Full reload on change  
**Benefits:** Simpler, atomic consistency, handles deletions  
**Trade-off:** 15s service interruption (hourly)  
**Verdict:** **Acceptable.** Simplicity > optimization.

### 6.4 Why Three Tools?

**Rejected:** Single unified tool  
**Chosen:** `find_helpful_skills`, `read_skill_document`, `list_skills`  
**Benefits:** Clear separation, enables progressive disclosure by design  
**Trade-off:** More tokens (~500 vs ~200)  
**Verdict:** **Justified.** Progressive disclosure benefits >> token cost.

---

## 7. Skills Pattern: Core Innovation

### 7.1 Skills as "npm for AI"

| npm Packages | Claude Skills |
|--------------|---------------|
| `npm install` | Semantic search |
| Versioned | Versioned |
| Dependencies | Can reference others |
| npmjs.com | GitHub |
| Reusable | Platform-agnostic |

**Paradigm Shift:**
- Before: AI with generic capability + hope
- After: AI discovers specialized skill + guaranteed competence

### 7.2 Semantic Discovery

Query: "I need to extract tables from scientific PDFs"

Results:
1. PDF Document Parser (0.89) - Extract text, tables, metadata
2. Table Extraction Tool (0.82) - Structure tables from docs
3. Scientific Paper Analyzer (0.76) - Analyze paper structure

**Insight:** Discovery is task-oriented, not name-based.

### 7.3 Progressive Disclosure Economics

**Math:** 180k tokens (all skills) → 1k tokens (progressive) = **99.4% savings**

**Scaling:** Works with 90, 1,000, or 10,000 skills (same baseline)

**Conclusion:** Progressive disclosure is MANDATORY for scale.

---

## 8. Key Insights for Wisdom Extraction

### 8.1 Skills as Infrastructure-as-Code

**Observation:** Skills are executable infrastructure, not documentation.

**Evidence:** Versioned, discoverable, composable, progressive, portable, testable

**Implication:** **Skills are "npm packages" of AI era**—infrastructure for capability distribution.

### 8.2 Progressive Disclosure = Requirement

**Observation:** Not optimization—MANDATORY at scale.

**Evidence:** 99.4% token savings, Anthropic blog confirms, scales to 10k+ skills

**Implication:** **Any AI capability system at scale MUST implement progressive disclosure.**

### 8.3 Constraint-Driven Design

**Observation:** 5-second timeout drove superior architecture.

**Evidence:** Forced split → better separation, cloud path, instant UX

**Implication:** **Embrace constraints as design specifications** (forcing functions).

### 8.4 Token Economics Drive Architecture

**Observation:** Decisions motivated by token costs.

**Evidence:** Progressive disclosure, lazy loading, caching, local embeddings

**Implication:** **Token economics are first-class architectural concerns** in AI systems.

### 8.5 Local-First = Strategic Advantage

**Observation:** Local embeddings is strategic, not just technical.

**Evidence:** No API keys → adoption, no costs → lower barrier, privacy → trust

**Implication:** **Minimize external dependencies to maximize adoption.**

---

## 9. Skill Sources & Ecosystem

### 9.1 Default Repositories

1. **Anthropic Official Skills** (~15 skills)
   - Documents, presentations, web artifacts, general tools
   
2. **K-Dense AI Scientific Skills** (~78 skills)
   - Bioinformatics, cheminformatics, scientific analysis

3. **Local Skills** (optional)
   - Custom/private skills in `~/.claude/skills`

**Total Default:** ~90 skills

### 9.2 Extensibility

Add custom sources:
```json
{
  "skill_sources": [
    {"type": "github", "url": "github.com/myorg/custom-skills"},
    {"type": "local", "path": "~/my-skills"}
  ]
}
```

Or fork and contribute to ecosystem repos.

---

## 10. Conclusion

The Claude Skills MCP Server is a **complete implementation of Skills-as-Infrastructure**, demonstrating:

1. **Skills are the unit of AI capability distribution** (portable packages)
2. **Progressive disclosure is mandatory at scale** (99.4% token savings)
3. **Semantic discovery enables task-oriented AI** (not name-based)
4. **Constraints drive superior architecture** (timeout → better design)
5. **Token economics shape decisions** (lazy, caching, progressive)
6. **Local-first maximizes adoption** (no keys, no costs, privacy)

**Strategic Impact:** By making Anthropic's Skills available to ANY AI via MCP, this proves Skills are platform-agnostic and establishes the pattern for AI capability distribution.

**This is infrastructure for the AI-native era.**

---

## Appendix: Repository Structure

```
claude-skills-mcp/
├── packages/
│   ├── frontend/              # ~15 MB, <5s start
│   │   └── src/claude_skills_mcp/
│   │       ├── __main__.py
│   │       ├── mcp_proxy.py
│   │       └── backend_manager.py
│   │
│   └── backend/               # ~250 MB, 15-20s start
│       ├── src/claude_skills_mcp_backend/
│       │   ├── mcp_handlers.py       # 854 LOC
│       │   ├── skill_loader.py       # 1090 LOC
│       │   ├── search_engine.py      # 194 LOC
│       │   ├── http_server.py        # 351 LOC
│       │   ├── update_checker.py     # 416 LOC
│       │   ├── config.py             # 141 LOC
│       │   ├── scheduler.py          # 185 LOC
│       │   └── state_manager.py      # 141 LOC
│       └── tests/                    # Comprehensive test suite
│
├── docs/                             # Architecture, API, usage
├── VERSION                           # Centralized versioning
└── config.example.json
```

**Artifact ID:** `claude-skills-mcp-architecture-2025-11-20`  
**Status:** Complete  
**Next:** Decision Forensics, Anti-Library (Level 2)
