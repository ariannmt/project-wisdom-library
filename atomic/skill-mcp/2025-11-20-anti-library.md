# Anti-Library Extraction: skill-mcp

**Date:** 2025-11-20  
**Type:** Level 2 Analysis (Negative Knowledge)  
**Target:** [fkesheh/skill-mcp](https://github.com/fkesheh/skill-mcp)  
**Purpose:** Document rejected approaches, failed experiments, and constraints that shaped the system

## Executive Summary

This anti-library captures **8 explicit rejections**, **12+ deferred features**, and **6 constraints-as-specifications** that define skill-mcp's boundaries. Every "no" reflects a conscious design choice optimizing for simplicity, security, or context efficiency.

**Key Pattern:** Constraints became competitive advantages - not limitations to overcome, but specifications to embrace.

---

## 1. Explicit Rejections (The "We Decided NOT To")

### Rejection 1: Global Secrets File

**What Was Considered:**
```
~/.skill-mcp/secrets.env  # Central secrets for all skills
```

**Why It Was Rejected:**
1. **Security Risk:** One file breach exposes all secrets
2. **Unclear Ownership:** Which skill uses which secret?
3. **Portability:** Can't share skill without manually extracting its secrets
4. **Merge Conflicts:** Multiple skills updating same file

**What Was Chosen Instead:**
```
~/.skill-mcp/skills/
├── skill-a/.env  # skill-a secrets
└── skill-b/.env  # skill-b secrets
```

**Trade-Off Accepted:**
- Lost: Centralized secret management UI
- Gained: Security isolation, clear ownership, skill portability

**Constraint Became Specification:** **"Per-skill isolation is more important than centralized convenience."**

**Evidence:** Commit 11436b6 explicitly documents per-skill .env architecture.

---

### Rejection 2: HTTP/REST API

**What Was Considered:**
- HTTP server on localhost:8000
- REST endpoints for skill management (/skills, /skills/:id, etc.)
- JSON responses
- CORS, authentication, etc.

**Why It Was Rejected:**
1. **Complexity:** Need port management, auth, networking
2. **Deployment:** Requires server process, not just script
3. **MCP Exists:** MCP protocol already solves this
4. **stdio = Simpler:** No ports, no auth, no CORS

**What Was Chosen Instead:**
- MCP stdio transport
- Async stdio server
- uvx deployment (no installation)

**Trade-Off Accepted:**
- Lost: Familiar REST API, HTTP tools (curl, Postman)
- Gained: Zero networking complexity, uvx-friendly deployment

**Constraint Became Specification:** **"stdio transport is mandatory for uvx deployment."**

**Evidence:** `server.py` uses `mcp.server.stdio.stdio_server()`

---

### Rejection 3: Database Storage (SQLite)

**What Was Considered:**
- SQLite database for skill metadata
- Schema: `skills(id, name, description, created_at, ...)`
- Query capabilities: `SELECT * FROM skills WHERE name LIKE '%data%'`
- Transactional guarantees

**Why It Was Rejected:**
1. **Overkill:** File system sufficient for metadata
2. **Migration Pain:** Schema changes = migrations
3. **Tooling:** Need DB browser, SQL knowledge
4. **YAML Sufficient:** Frontmatter in SKILL.md is enough

**What Was Chosen Instead:**
- YAML frontmatter in SKILL.md
- File system as "database"
- `yaml_parser.py` for metadata extraction

**Trade-Off Accepted:**
- Lost: SQL queries, transactions, schema validation
- Gained: Simplicity, git-friendliness, human-readable

**Constraint Became Specification:** **"Skills are regular files, not database records."**

**Evidence:** `skill_service.py` scans directories, reads SKILL.md files.

---

### Rejection 4: Multi-User Support

**What Was Considered:**
- User authentication (API keys, OAuth)
- Per-user skill directories
- Permission system (read/write/execute)
- Admin users vs. regular users

**Why It Was Rejected:**
1. **Scope Creep:** Personal tool, not enterprise system
2. **Complexity:** Auth, authorization, user management
3. **Use Case:** Single developer using local skills
4. **Future:** Can add later if needed

**What Was Chosen Instead:**
- Single-user, user-scoped directory (~/.skill-mcp)
- No authentication (runs as user)
- No permissions (user has full access)

**Trade-Off Accepted:**
- Lost: Multi-user collaboration, shared environments
- Gained: Simplicity, faster development, clear scope

**Constraint Became Specification:** **"Skills are personal, not shared infrastructure."**

**Evidence:** `config.py` uses `Path.home() / ".skill-mcp" / "skills"`

---

### Rejection 5: Skill Registry/Marketplace

**What Was Considered:**
- Central registry of public skills
- `skill install weather-skill`
- Skill discovery (browse, search, ratings)
- Skill publishing workflow

**Why It Was Rejected:**
1. **Infrastructure:** Requires hosted service, storage, CDN
2. **Moderation:** Who verifies skill security/quality?
3. **Scope:** MVP doesn't need marketplace
4. **Alternative:** GitHub repos work for now

**What Was Chosen Instead:**
- Local skills only
- Manual sharing via git clone
- README documents skill structure

**Trade-Off Accepted:**
- Lost: Easy skill discovery, one-click install
- Gained: No infrastructure, no moderation burden

**Deferred, Not Rejected:** Could add later with community demand.

**Evidence:** No registry code in codebase, README mentions "custom tool for personal use."

---

### Rejection 6: Skill Versioning System

**What Was Considered:**
- Version field in SKILL.md frontmatter
- Semantic versioning (1.2.3)
- Changelog files
- Version compatibility checks

**Why It Was Rejected:**
1. **Git Exists:** Version control already solved
2. **Manual Effort:** Developers must bump versions
3. **Enforcement:** How to prevent version mismatches?
4. **Complexity:** Dependencies on specific skill versions

**What Was Chosen Instead:**
- Skills are regular files (use git for versioning)
- No version field in SKILL.md
- Git tags for releases

**Trade-Off Accepted:**
- Lost: Semantic versioning, programmatic version checks
- Gained: Simplicity, leverage existing git workflows

**Deferred, Not Rejected:** Could add `version:` field to SKILL.md frontmatter.

**Evidence:** SKILL.md schema has no version field.

---

### Rejection 7: Merge/Replace Modes for Environment Variables

**What Was Considered:**
```python
set_env(skill, {"API_KEY": "..."}, mode="merge")   # Add to existing
set_env(skill, {"API_KEY": "..."}, mode="replace")  # Replace all
```

**Why It Was Rejected:**
1. **Footgun:** "replace" can accidentally wipe all secrets
2. **Complexity:** More modes = more edge cases
3. **Clarity:** Always merge is clearer
4. **Workaround:** `clear_env()` then `set_env()` for replace

**What Was Chosen Instead:**
```python
set_variables(skill, {"API_KEY": "..."})  # Always merges
# If you want replace: clear_env(skill) then set_variables(skill, {...})
```

**Trade-Off Accepted:**
- Lost: Explicit replace mode (convenience)
- Gained: Safety (can't accidentally wipe secrets), simplicity

**Constraint Became Specification:** **"Always merge is safer than sometimes replace."**

**Evidence:** Commit 1e3e7d7 "refactor: simplify env variable operations by removing modes"

---

### Rejection 8: Individual MCP Tools (Pre-CRUD Refactor)

**What Was Considered:**
```
list_skills, get_skill, create_skill, delete_skill,
read_file, create_file, update_file, delete_file,
read_env, set_env, delete_env, clear_env, ...
→ 10+ individual tools
```

**Why It Was Rejected:**
1. **Context Bloat:** 10+ tools = more tokens per request
2. **Inconsistency:** Each tool has different patterns
3. **No Bulk Ops:** Can't create multiple files atomically
4. **Error Handling:** Different error formats per tool

**What Was Chosen Instead:**
```
skill_crud(operation="list|get|create|delete|...")
skill_files_crud(operation="read|create|update|delete")
skill_env_crud(operation="read|set|delete|clear")
→ 3 unified CRUD tools
```

**Trade-Off Accepted:**
- Lost: Simple, focused tool descriptions
- Gained: Fewer tools, bulk operations, consistent patterns

**Constraint Became Specification:** **"Context efficiency demands tool consolidation."**

**Evidence:** Commit 78bcb08 refactor (-706 LOC, +1837 LOC for tests/features)

---

## 2. Deferred Features (The "Not Now, Maybe Later")

### Deferred 1: Remote Skill Fetching

**What:** `skill_crud(operation="install", url="https://github.com/user/skill-repo")`

**Why Deferred:**
- MVP doesn't need remote fetch
- Security: Need verification, sandboxing
- Complexity: Git cloning, version resolution

**Workaround:** Manual `git clone` for now

**Opportunity:** If users request it, add later

---

### Deferred 2: Skill Templates Marketplace

**What:** Community-contributed skill templates beyond basic/python/bash/nodejs

**Why Deferred:**
- 4 templates sufficient for MVP
- No infrastructure for hosting templates
- Quality control burden

**Workaround:** Users can create custom templates locally

**Opportunity:** Could add template discovery if demand exists

---

### Deferred 3: Multi-Language Code Execution

**What:** `execute_python_code`, `execute_javascript_code`, `execute_bash_code`

**Why Deferred:**
- Python covers 80% of use cases
- Multi-language = much more complexity
- PEP 723 is Python-specific

**Workaround:** Use `run_skill_script` for JS/Bash files

**Opportunity:** Could extend if multi-language composition becomes critical

---

### Deferred 4: Dependency Locking (uv.lock)

**What:** Generate uv.lock files for reproducible builds

**Why Deferred:**
- PEP 723 uses version ranges (≥2.0.0)
- uv handles dep resolution automatically
- Lock files = more files to manage

**Workaround:** Pin exact versions in PEP 723 metadata

**Opportunity:** Add `--locked` flag to execution if users need reproducibility

---

### Deferred 5: Skill Composition DSL

**What:** Higher-level language for composing skills

```yaml
workflow:
  - name: Fetch Data
    skill: data-fetcher
    input: {url: "https://..."}
  - name: Process
    skill: processor
    input: {data: $prev.output}
```

**Why Deferred:**
- Python code execution sufficient for now
- DSL = new language to learn, maintain
- Code is more flexible than DSL

**Workaround:** Write Python code with imports

**Opportunity:** Could add if users struggle with code-based composition

---

### Deferred 6: Skill Analytics

**What:** Track skill usage, execution times, error rates

**Why Deferred:**
- Privacy concerns (what data to collect?)
- Storage (where to persist analytics?)
- Use case unclear (personal tool)

**Workaround:** Check script exit codes, manually track

**Opportunity:** Add if users want usage insights

---

### Deferred 7: Skill Testing Framework

**What:** Built-in testing support for skills

```yaml
tests:
  - name: "Test script execution"
    script: scripts/process.py
    input: test_data.csv
    expected_output: "Success"
```

**Why Deferred:**
- Skills can use their own test frameworks (pytest, etc.)
- MCP server tests are sufficient
- Each skill has different testing needs

**Workaround:** Skills use standard testing tools

**Opportunity:** Add if users want standardized skill testing

---

### Deferred 8: Skill Documentation Generator

**What:** Auto-generate docs from SKILL.md + scripts

**Why Deferred:**
- SKILL.md already serves as documentation
- Not critical for MVP
- Maintenance burden

**Workaround:** Manually write/update SKILL.md

**Opportunity:** Add if users want prettier docs

---

### Deferred 9: Skill Backup/Restore

**What:** `skill_crud(operation="backup")` → ZIP archive

**Why Deferred:**
- Skills are regular files (use git, rsync, etc.)
- Specialized backup tools exist
- Not unique to skills

**Workaround:** Use git, file system backups

**Opportunity:** Add if users want built-in backup

---

### Deferred 10: Skill Migration Tool

**What:** Migrate from other skill systems (e.g., Claude's native skills)

**Why Deferred:**
- Low demand (new project)
- Each system has different formats
- Manual migration works for now

**Workaround:** Manually recreate skills

**Opportunity:** Add if users need bulk migration

---

### Deferred 11: Skill Sandboxing

**What:** Run scripts in isolated containers/VMs

**Why Deferred:**
- Complexity (Docker, VMs, etc.)
- Performance overhead
- User responsibility to review scripts

**Workaround:** README warns users to review LLM-generated code

**Opportunity:** Add if security becomes critical

---

### Deferred 12: Skill Marketplace Monetization

**What:** Paid skills, subscription model

**Why Deferred:**
- No marketplace yet
- Personal tool, not commercial
- Payment infrastructure complex

**Workaround:** N/A (no marketplace)

**Opportunity:** If marketplace launched, could add payments

---

## 3. Constraints-as-Specifications

### Constraint 1: Token Limits → Progressive Disclosure

**Constraint:** LLMs have finite context windows  
**Specification:** Load minimal data upfront, full details on demand

**Implementation:**
- `list` returns lightweight SkillInfo (name, description)
- `get` returns comprehensive SkillDetails (SKILL.md content, files, scripts)

**Result:** 98.7% token reduction (Anthropic research validates pattern)

---

### Constraint 2: Execution Time → 30-Second Timeout

**Constraint:** Scripts can hang forever  
**Specification:** Hard 30-second limit

**Implementation:**
```python
SCRIPT_TIMEOUT_SECONDS = 30
# subprocess.run(cmd, timeout=30)
```

**Result:** Prevents runaway scripts, forces efficient algorithms

---

### Constraint 3: File Size → 1MB Limit

**Constraint:** Large files bloat memory  
**Specification:** Reject files over 1MB

**Implementation:**
```python
MAX_FILE_SIZE = 1_000_000  # 1MB
```

**Result:** Forces users to use references/assets for large data, not inline

---

### Constraint 4: Output Size → 100KB Limit

**Constraint:** Scripts can dump huge output  
**Specification:** Truncate stdout/stderr at 100KB

**Implementation:**
```python
MAX_OUTPUT_SIZE = 100_000  # 100KB
```

**Result:** Forces users to write to files, not print everything

---

### Constraint 5: MCP Protocol → stdio Transport

**Constraint:** MCP uses stdio for communication  
**Specification:** Server must use async stdio, no HTTP

**Implementation:**
```python
async with mcp.server.stdio.stdio_server() as (read, write):
    await app.run(read, write, ...)
```

**Result:** Enables uvx deployment, eliminates networking complexity

---

### Constraint 6: Python 3.10+ → Modern Type Hints

**Constraint:** Older Python lacks type features  
**Specification:** Require Python 3.10+

**Implementation:**
```toml
requires-python = ">=3.10"
```

**Result:** Use match/case, union types (X | Y), better type checking

---

## 4. Failed Experiments (Implied from Refactors)

### Failed Experiment 1: Merge/Replace Modes

**Evidence:** Commit 1e3e7d7 removed modes

**What Failed:** Having both merge and replace modes for env vars

**Why It Failed:** Users confused about which to use, "replace" was footgun

**Lesson Learned:** Less choice = better UX when one option is clearly safer

---

### Failed Experiment 2: Individual MCP Tools

**Evidence:** Commit 78bcb08 consolidated to CRUD

**What Failed:** 10+ individual tools (list_skills, get_skill, create_skill, ...)

**Why It Failed:** Context bloat, no bulk operations, inconsistent patterns

**Lesson Learned:** Fewer, richer tools > many simple tools (for LLMs)

---

### Failed Experiment 3: Global Secrets

**Evidence:** Commit 11436b6 documents per-skill .env

**What Failed:** (Implied) initial attempt at global secrets

**Why It Failed:** Security, clarity, portability issues

**Lesson Learned:** Isolation > centralization for secrets

---

## 5. Constraints That Became Competitive Advantages

### Advantage 1: stdio Transport → uvx Deployment

**Constraint:** MCP requires stdio  
**Advantage:** `uvx skill-mcp-server` just works (no installation)

**Competitor Burden:** HTTP servers need pip install, port config, networking

**Result:** skill-mcp is easier to deploy than custom HTTP APIs

---

### Advantage 2: Per-Skill .env → Security Isolation

**Constraint:** Can't use global secrets (security risk)  
**Advantage:** Skill breach doesn't expose all secrets

**Competitor Burden:** Global secrets = one breach exposes everything

**Result:** skill-mcp is more secure by default

---

### Advantage 3: CRUD Consolidation → Context Efficiency

**Constraint:** Token limits force fewer tools  
**Advantage:** 4 tools vs 10+ = less context consumed

**Competitor Burden:** Many tools = more context = slower, costlier

**Result:** skill-mcp scales better with many skills

---

### Advantage 4: Python-Only execute_python_code → Better Integration

**Constraint:** Can't support all languages easily  
**Advantage:** Deep PEP 723 integration, dependency aggregation

**Competitor Burden:** Multi-language = shallow integration for all

**Result:** skill-mcp provides best-in-class Python experience

---

### Advantage 5: No Database → Git-Friendly

**Constraint:** Can't use SQLite (adds complexity)  
**Advantage:** Skills are regular files (git-friendly, versionable)

**Competitor Burden:** Database = opaque, not git-friendly

**Result:** skill-mcp fits into existing workflows (git, editors, etc.)

---

### Advantage 6: Single-User → Simpler Mental Model

**Constraint:** Can't support multi-user (scope)  
**Advantage:** No auth, no permissions, no user management

**Competitor Burden:** Multi-user = auth, RBAC, audit logs

**Result:** skill-mcp is simpler to understand and use

---

## 6. The "We Almost Did But Didn't"

### Almost: WebSocket Transport

**Why Considered:** More interactive than stdio

**Why Didn't:** MCP stdio already works, no benefit

**Lesson:** Don't add technology just because it exists

---

### Almost: TypeScript Server

**Why Considered:** Node.js MCP SDK available

**Why Didn't:** Python has better data science libraries (PEP 723 needs Python)

**Lesson:** Choose language for ecosystem, not personal preference

---

### Almost: Skill Encryption

**Why Considered:** Protect secrets in .env files

**Why Didn't:** Complexity (key management), chmod 600 sufficient

**Lesson:** Use OS security features (file permissions) instead of reinventing

---

### Almost: Skill Signing

**Why Considered:** Verify skill authenticity

**Why Didn't:** No marketplace = no verification needed

**Lesson:** Defer features until use case is clear

---

## 7. Constraints Documentation

### Documented Constraints

From `config.py`:
```python
MAX_FILE_SIZE = 1_000_000      # 1MB limit
MAX_OUTPUT_SIZE = 100_000      # 100KB limit
SCRIPT_TIMEOUT_SECONDS = 30    # 30s timeout
```

From README:
```markdown
## Security Features
- 30-second timeout prevents infinite loops
- Scripts run with user's permissions (not elevated)
- Output size limits prevent memory issues
```

**Purpose:** Make constraints explicit so users understand boundaries.

---

## 8. Strategic Insights from Rejections

### Insight 1: Constraints → Competitive Advantages

**Pattern:** What seemed like limitations became strengths.

**Examples:**
- stdio (constraint) → uvx deployment (advantage)
- Per-skill .env (constraint) → security isolation (advantage)
- CRUD consolidation (constraint) → context efficiency (advantage)

**Lesson:** Embrace constraints, don't fight them.

---

### Insight 2: Simplicity Through Subtraction

**Pattern:** Removing features improved the product.

**Examples:**
- Removed merge/replace modes → safer API
- Removed individual tools → better context efficiency
- Removed global secrets → better security

**Lesson:** Less is more when each feature has a cost (complexity, maintenance, documentation).

---

### Insight 3: Defer > Delete

**Pattern:** Rejected ≠ impossible; deferred ≠ rejected.

**Examples:**
- Skill marketplace: Deferred (could add later)
- Multi-language execution: Deferred (Python sufficient for now)
- Skill versioning: Deferred (git handles it)

**Lesson:** Defer features until demand is proven, don't reject forever.

---

### Insight 4: Constraints Clarify Scope

**Pattern:** Constraints prevent scope creep.

**Examples:**
- Single-user → no auth complexity
- Local-only → no infrastructure costs
- Python-only → deep integration possible

**Lesson:** Constraints are strategic - they define what you WON'T build.

---

## 9. Lessons for Future Projects

### Lesson 1: Document What You DON'T Build

**Insight:** Anti-library prevents repeating rejected experiments.

**Example:** If someone proposes "global secrets," point to this document.

**Value:** Saves time debating settled decisions.

---

### Lesson 2: Constraints Enable Focus

**Insight:** Finite context window → forced CRUD consolidation → better product.

**Example:** Token limits made fewer tools mandatory, not optional.

**Value:** Constraints guide toward better solutions.

---

### Lesson 3: Simplicity is a Feature

**Insight:** Removing merge/replace modes improved UX.

**Example:** Always-merge is simpler than sometimes-merge-sometimes-replace.

**Value:** Fewer options = clearer mental model.

---

### Lesson 4: Research Validates Bold Bets

**Insight:** Anthropic research justified multi-skill execution.

**Example:** 98.7% token reduction → confident to build `execute_python_code`.

**Value:** External validation enables ambitious features.

---

### Lesson 5: Defer > Decide

**Insight:** Don't reject features permanently if uncertain.

**Example:** Skill marketplace deferred (not rejected) - could add later.

**Value:** Keeps options open without committing.

---

## 10. Conclusion

skill-mcp's anti-library reveals **disciplined scope management**:

**8 Explicit Rejections:** Global secrets, HTTP API, database, multi-user, marketplace, versioning, merge modes, individual tools

**12+ Deferred Features:** Remote fetch, template marketplace, multi-language, dependency locking, composition DSL, analytics, testing, docs gen, backup, migration, sandboxing, monetization

**6 Constraints-as-Specifications:** Token limits, timeouts, file size, output size, stdio transport, Python 3.10+

**Key Pattern:** Constraints became competitive advantages - stdio → uvx, per-skill .env → security, CRUD → context efficiency

**Strategic Takeaway:** What you DON'T build is as important as what you DO build. Every "no" preserved focus on the core innovation: **multi-skill execution with automatic dependency aggregation.**

**Next Level:** Vision Alignment - verify that what WAS built matches what was PROMISED (98.7% token reduction, 145 tests, production-ready).
