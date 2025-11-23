# Hard Architecture Mapping: Claude Journal MCP
**Level 1 Analysis - The "What" (Data & Reality)**

**Investigation Date:** 2025-11-23  
**Target:** https://github.com/chrismbryant/claude-journal-mcp  
**Version:** v0.1.0  
**Status:** Active development  

---

## Executive Summary

Claude Journal MCP is a **three-layer architecture** designed as a human-centered memory system for Claude Code. It inverts the standard AI architecture by making AI the **interface layer** (translator) rather than the intelligence layer (embeddings/inference).

**Architecture Pattern:** Interface-Storage Inversion  
**Technology Stack:** Python 3.12+, SQLite, MCP Protocol  
**Scale:** Micro-service (188 LOC core, 1,004 LOC total)  
**Dependencies:** 2 (mcp, python-dateutil)  

---

## System Architecture

### Three-Layer Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Layer 3: Integration                      │
│                  (Behavioral Programming)                    │
├──────────────────────────────────────────────────────────────┤
│  Hooks (journal-auto-capture.js)                             │
│   └─ Trigger: Every 30min OR 3 messages                      │
│   └─ Action: Prompt Claude to reflect + capture              │
│                                                              │
│  Skills (3 markdown files)                                   │
│   ├─ journal-capture: When to capture proactively           │
│   ├─ context-recovery: Restore after /clear                 │
│   └─ find-related-work: Search before similar tasks         │
│                                                              │
│  Commands (6 markdown files)                                 │
│   ├─ /journal-add: Guided entry creation                    │
│   ├─ /journal-search: Interactive search                    │
│   ├─ /journal-recent: Context restoration                   │
│   ├─ /journal-time: Time-based queries                      │
│   ├─ /journal-stats: Analytics view                         │
│   └─ /journal-export: Backup workflow                       │
│                                                              │
│  Agent (1 markdown file - opt-in)                            │
│   └─ journal-assistant: Strategic guidance layer            │
└──────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    Layer 2: Interface                        │
│                   (MCP Protocol Bridge)                      │
├──────────────────────────────────────────────────────────────┤
│  MCP Server (server.py - 418 LOC)                            │
│   ├─ list_tools() → 11 MCP tools                            │
│   ├─ call_tool() → Route + format                           │
│   └─ format_entries() → Markdown output                     │
│                                                              │
│  Tools Exposed (11):                                         │
│   Write:                                                     │
│   ├─ journal_add (manual capture)                           │
│   └─ journal_auto_capture (automatic capture)               │
│                                                              │
│   Read:                                                      │
│   ├─ journal_search (advanced query syntax)                 │
│   ├─ journal_time_query (natural language time)             │
│   ├─ journal_list_recent (context recovery)                 │
│   ├─ journal_list_projects (project list)                   │
│   └─ journal_stats (analytics)                              │
│                                                              │
│   Management:                                                │
│   ├─ journal_delete (by ID)                                 │
│   ├─ journal_delete_by_project (bulk delete)                │
│   ├─ journal_import (merge databases)                       │
│   └─ journal_export (backup)                                │
└──────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    Layer 1: Storage                          │
│                (Transparent Persistence)                     │
├──────────────────────────────────────────────────────────────┤
│  Database Layer (database.py - 425 LOC)                      │
│   ├─ JournalDatabase class                                  │
│   ├─ Connection: SQLite (~/.claude/journal.db)              │
│   ├─ Schema: Single table (journal_entries)                 │
│   └─ Indexing: created_at, project                          │
│                                                              │
│  Time Parser (time_parser.py - 157 LOC)                      │
│   ├─ parse_time_expression()                                │
│   ├─ Input: "last week", "january 2024", etc.               │
│   └─ Output: SQLite timestamp pairs (start, end)            │
│                                                              │
│  CLI (cli.py - minimal)                                      │
│   └─ Entry point for hook invocation                        │
└──────────────────────────────────────────────────────────────┘
```

---

## Component Details

### Layer 1: Storage (database.py)

**Purpose:** Transparent, queryable persistence

**Schema:**
```sql
CREATE TABLE journal_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    project TEXT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    tags TEXT  -- Comma-separated
);

CREATE INDEX idx_created_at ON journal_entries(created_at);
CREATE INDEX idx_project ON journal_entries(project);
```

**Key Operations:**

| Operation | Method | Complexity |
|-----------|--------|------------|
| Add entry | `add_entry()` | O(1) - Single INSERT |
| Search | `search()` | O(n) - Full table scan with LIKE |
| Time range | `get_by_time_range()` | O(log n) - Indexed by created_at |
| Recent | `list_recent()` | O(1) - Indexed LIMIT query |
| Stats | `get_stats()` | O(n) - Aggregation |
| Import | `import_from_db()` | O(n) - ATTACH + INSERT SELECT |
| Export | `export_to_db()` | O(n) - SQLite backup API |

**Advanced Search Parser:**
Supports complex query syntax:
- ID search: `42` or `id:42` → Direct ID lookup (O(1))
- Tag filter: `tag:bugfix` or `#bugfix` → Tag matching
- Exact phrase: `"user authentication"` → LIKE with quoted string
- Time range: `last week authentication` → Combined time + text
- Keywords: `auth bug` → AND all terms across title/desc/tags

**Design Choices:**
- **No ORM:** Direct SQL for transparency and performance
- **Single table:** Simple, no joins required
- **Comma-separated tags:** No junction table (simplicity over normalization)
- **Text timestamps:** SQLite's datetime() format (YYYY-MM-DD HH:MM:SS)
- **No migrations:** Schema frozen at v0.1.0

### Layer 2: Interface (server.py)

**Purpose:** MCP protocol bridge + AI translation layer

**MCP Protocol Flow:**
```
Claude → MCP Client → stdio → server.py → database.py → SQLite
```

**Tool Schema Example:**
```python
Tool(
    name="journal_search",
    description="Search with advanced syntax: ID (42), tags (#auth), phrases (\"...\"), time (last week)",
    inputSchema={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Search query"},
            "project": {"type": "string"},
            "limit": {"type": "integer", "default": 20}
        },
        "required": ["query"]
    }
)
```

**Response Format:**
All tools return `List[TextContent]` (markdown formatted).

Example output:
```markdown
**Journal Entries (last week):** (3 found)

**[42]** Implemented OAuth2
📅 2025-11-20 15:30:00 | 📁 my-app | 🏷️ auth,security
Built OAuth2 flow with JWT tokens

**[43]** Fixed cache leak
📅 2025-11-21 09:15:00 | 📁 api-service | 🏷️ bugfix,performance
Cache wasn't clearing old entries

...
```

**Design Choices:**
- **Async MCP server:** Non-blocking I/O (though DB is sync)
- **Markdown output:** Claude-native format (emoji icons)
- **Stateless tools:** Each tool call is independent
- **No caching:** Direct DB reads (sub-ms latency)

### Layer 3: Integration (Plugin Ecosystem)

**Purpose:** Behavioral programming layer

**Plugin Manifest (.claude-plugin/plugin.json):**
```json
{
  "name": "claude-journal",
  "version": "0.1.0",
  "hooks": "./hooks/hooks.json",
  "mcpServers": {
    "journal": {
      "command": "python",
      "args": ["-m", "claude_journal.server"]
    }
  }
}
```

**Hook Configuration (hooks/hooks.json):**
```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "node ${CLAUDE_PLUGIN_ROOT}/hooks/journal-auto-capture.js"
      }]
    }]
  }
}
```

**Hook Behavior:**
1. Runs on **every** user prompt submission
2. Checks state file (`~/.claude/journal-capture-state.json`)
3. Tracks: message count, last capture timestamp
4. Triggers if: 30 minutes elapsed **OR** 3+ messages sent
5. Prompts Claude to review session and decide (capture or explain why not)

**Skill Structure:**
Each skill is a markdown file (`SKILL.md`) with frontmatter:
```yaml
---
name: journal-capture
description: Proactively captures significant work
when_to_use: After completing features, fixing bugs, making decisions
---
```

**Command Structure:**
Each command is a markdown file with guidance for Claude:
```markdown
# /journal-add Command

When the user types `/journal-add`, guide them through:
1. Title (brief summary)
2. Description (what was done)
3. Project (auto-detect from git or ask)
4. Tags (suggest based on content)
```

**Agent Structure:**
Opt-in agent defined in `agents/journal-assistant.md`:
- Proactive capture after significant work
- Automatic context recovery after `/clear`
- Search for related work before similar tasks
- Interactive journal management

**Design Choices:**
- **Behavior as configuration:** No Python code for personality
- **Markdown documentation:** Human-readable + AI-parseable
- **Opt-in agent:** User controls AI proactivity level
- **Forcing function hook:** Prompt for reflection, not automation

---

## Data Flow

### Write Path: Adding an Entry

```
User: "Remember we implemented OAuth2"
  ↓
Claude (via MCP): journal_add(
  title="Implemented OAuth2",
  description="Built OAuth2 flow with JWT tokens",
  project="my-app",
  tags=["auth", "security"]
)
  ↓
server.py: call_tool("journal_add", arguments)
  ↓
database.py: add_entry(title, desc, project, tags)
  ↓
SQLite: INSERT INTO journal_entries VALUES (...)
  ↓
Return: "✅ Journal entry created (ID: 42)"
```

### Read Path: Time-Based Search

```
User: "What did I work on last week?"
  ↓
Claude: journal_time_query(time_expression="last week")
  ↓
server.py: call_tool("journal_time_query", {"time_expression": "last week"})
  ↓
time_parser.py: parse_time_expression("last week")
  → Returns: ("2025-11-16 00:00:00", "2025-11-22 23:59:59")
  ↓
database.py: get_by_time_range(start_date, end_date)
  ↓
SQLite: SELECT * FROM journal_entries 
        WHERE created_at BETWEEN ? AND ?
        ORDER BY created_at DESC
  ↓
server.py: format_entries(results, show_time="last week")
  ↓
Return: Markdown-formatted list of entries
```

### Hook Path: Auto-Capture

```
User submits prompt
  ↓
Claude Code: Trigger UserPromptSubmit hook
  ↓
journal-auto-capture.js:
  - Load state from ~/.claude/journal-capture-state.json
  - Increment message count
  - Check: 30min elapsed OR 3+ messages?
  ↓
If threshold met:
  - Inject prompt: "🕐 Journal auto-capture triggered..."
  - Claude MUST respond (capture or explain)
  ↓
Claude: journal_auto_capture(
  title="Session summary",
  description="Goal + accomplishments"
)
  ↓
[Same write path as manual add, but with "auto-capture" tag]
```

---

## Technology Stack

### Core Dependencies

| Dependency | Version | Purpose | Size |
|------------|---------|---------|------|
| Python | ≥3.12 | Runtime | - |
| mcp | ≥1.0.0 | MCP protocol | ~2 MB |
| python-dateutil | ≥2.8.0 | Date parsing | ~500 KB |
| SQLite | 3.x (bundled) | Database | ~1 MB |

**Total footprint:** ~10 MB (including Python stdlib)

### Development Dependencies

| Dependency | Purpose |
|------------|---------|
| pytest | Unit testing |
| pytest-asyncio | Async test support |
| pytest-cov | Coverage reporting |

### External Integrations

| System | Interface | Purpose |
|--------|-----------|---------|
| Claude Code | MCP stdio | AI integration |
| Claude Code Plugin | JSON manifest | Behavioral config |
| Git | Shell commands | Project detection |
| File system | ~/.claude/ | State + database |

---

## Deployment Architecture

### Installation Modes

**Mode 1: Plugin (Recommended)**
```bash
claude /plugin install .
```
Installs:
- MCP server (auto-configured)
- 6 slash commands
- 3 skills
- 1 agent (opt-in prompt)
- 1 hook (auto-enabled)

**Mode 2: MCP Server Only**
```bash
pip install -e .
# Add to ~/.claude/config.json manually
```
Installs:
- MCP server only (11 tools)
- No commands, skills, agent, or hooks

### Runtime Configuration

**Database Location:**
- Default: `~/.claude/journal.db`
- Override: `JOURNAL_DB_PATH` environment variable

**Hook State:**
- Location: `~/.claude/journal-capture-state.json`
- Format: `{"lastCapture": "2025-11-23T02:00:00Z", "messageCount": 0}`

**Plugin Root:**
- Location: Managed by Claude Code
- Variable: `${CLAUDE_PLUGIN_ROOT}` (available in hooks)

### Scalability Characteristics

| Metric | Performance | Notes |
|--------|-------------|-------|
| Entries | Sub-linear | Indexed queries O(log n) |
| Database size | 1 KB per entry | Simple text storage |
| Search latency | <1 ms | SQLite LIKE on small datasets |
| Concurrent users | 1 | SQLite single-writer |
| Max entries (practical) | ~100K | Before search degrades |

**Not designed for:**
- Multi-user access (no auth, no locking)
- Large-scale datasets (>100K entries)
- Real-time sync (local-only storage)
- Web interface (CLI + MCP only)

---

## Architectural Patterns

### Pattern 1: Inversion Architecture

**Standard AI Memory:**
```
User → AI → Vector DB (embeddings) → Semantic Search → Results
```

**This System:**
```
User → AI (translator) → SQLite (keywords) → Exact Search → Results
```

**Inversion:** AI is the interface, not the intelligence.

### Pattern 2: Behavioral Programming

**Separation of Concerns:**
- **Capabilities** (Python): What the system *can* do (11 MCP tools)
- **Behavior** (Markdown): What the system *should* do (skills, commands, agent)

**Benefit:** Same core, different personalities (configurable via markdown).

### Pattern 3: Forcing Function Design

**Traditional Automation:**
```
Timer → Auto-save → Done
```

**This System:**
```
Timer → Prompt AI → AI reflects → AI decides (capture OR explain)
```

**Benefit:** Visibility into AI decision-making + forced meta-cognition.

### Pattern 4: Cognitive Ergonomics

**Design Principle:** Match human memory patterns, not AI capabilities.

**Manifestations:**
- Keyword search (how humans recall: "that auth thing")
- Time queries (how humans reference: "last week")
- Project organization (how humans categorize: "the API service")
- ID lookup (how humans bookmark: "entry 42")

---

## Security & Privacy

### Data Storage

- **Location:** Local file system (`~/.claude/journal.db`)
- **Encryption:** None (plain SQLite)
- **Access control:** File system permissions only
- **Network:** No network calls (fully offline)

### Privacy Characteristics

| Aspect | Status |
|--------|--------|
| Data leaves machine | ❌ Never |
| Telemetry | ❌ None |
| Auth required | ❌ No (local-only) |
| Encrypted at rest | ❌ No |
| Encrypted in transit | N/A (no network) |
| PII handling | ⚠️ User's responsibility |

**Trade-off:** Maximum privacy (local-only) but zero collaboration features.

---

## Testing & Quality

### Test Coverage

| Component | Test File | Tests | Coverage |
|-----------|-----------|-------|----------|
| Database | test_database.py | 15+ | High |
| Time Parser | test_time_parser.py | 12+ | High |
| MCP Server | (manual) | - | - |

### CI/CD

- **Platform:** GitHub Actions
- **Triggers:** PR + push to main
- **Matrix:** Python 3.12, 3.13
- **Checks:** pytest, linting

### Code Quality

- **LOC:** 1,004 total (188 core logic)
- **Files:** 7 Python files
- **Complexity:** Low (no complex algorithms)
- **Dependencies:** Minimal (2 runtime)

---

## Limitations & Constraints

### By Design

1. **No embeddings:** Keyword search only (deliberate)
2. **Single-user:** No multi-user support (local SQLite)
3. **No sync:** Local-only (no cloud backup)
4. **No encryption:** Plain text storage (trust file system)

### Technical

1. **SQLite limits:** Single writer, ~100K entries practical max
2. **Search quality:** Keyword exact match (no fuzzy, no semantic)
3. **Performance:** O(n) search on large datasets
4. **Portability:** Python 3.12+ required (newer Python)

### Operational

1. **Backup:** Manual export (no auto-backup)
2. **Migration:** No schema migration system
3. **Monitoring:** No observability hooks
4. **Recovery:** SQLite corruption = data loss

---

## Architecture Assessment

### Strengths

✅ **Simplicity:** 188 LOC core, 2 dependencies  
✅ **Transparency:** Direct SQL, human-readable storage  
✅ **Performance:** Sub-millisecond queries  
✅ **Privacy:** Local-only, no network  
✅ **Portability:** SQLite = universal format  
✅ **Extensibility:** MCP protocol + plugin ecosystem  

### Weaknesses

⚠️ **Scalability:** Limited to ~100K entries  
⚠️ **Search quality:** No semantic search, no fuzzy matching  
⚠️ **Collaboration:** Single-user only  
⚠️ **Durability:** No encryption, no auto-backup  

### Trade-offs Made

| Rejected | Chosen | Rationale |
|----------|--------|-----------|
| Embeddings | Keywords | 400x smaller, 100x faster, sufficient for journals |
| Vector DB | SQLite | Transparent, portable, no lock-in |
| Multi-user | Local-only | Privacy + simplicity |
| Cloud sync | Export/import | User control, no vendor dependency |
| Complex queries | Natural language | Cognitive ergonomics |

---

## Conclusion

Claude Journal MCP is a **minimalist, human-centered memory system** that inverts the standard AI architecture by making AI the interface layer (translator) rather than the intelligence layer (embeddings).

**Key Architectural Innovation:**  
AI translates natural language → structured queries → transparent storage (SQLite).  
Not: AI stores/retrieves from opaque vector DB.

**Design Philosophy:**  
Match human cognition (keywords, time, projects), not AI capabilities (semantics, embeddings, inference).

**Pattern Contribution:**  
Blueprint for human-centered AI tooling: simple storage + smart interface > smart storage + simple interface.

**Maturity Level:** MVP (v0.1.0)  
**Production Readiness:** Personal use (not enterprise)  
**Innovation Factor:** High (architectural pattern, not technical feat)  

---

**Document Version:** 1.0  
**Last Updated:** 2025-11-23  
**Analyst:** GitHub Copilot Coding Agent
