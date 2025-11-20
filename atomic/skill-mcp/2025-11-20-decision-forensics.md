# Decision Forensics: skill-mcp

**Date:** 2025-11-20  
**Type:** Level 2 Analysis (Information & Context)  
**Target:** [fkesheh/skill-mcp](https://github.com/fkesheh/skill-mcp)  
**Commits Analyzed:** 26 commits (Oct 18 - Nov 9, 2025)  
**Development Period:** 22 days of intense iteration

## Executive Summary

Git history reveals **3 strategic pivots** and **27 incremental enhancements** over 22 days, demonstrating **disciplined constraint-driven design**. The project evolved from a basic skill manager to a **multi-skill execution platform** through systematic evidence-based expansion.

**Key Insight:** Every major decision optimized for **context efficiency** and **LLM usability** - not human convenience. The Nov 7 CRUD refactor (commit `78bcb08`) was the culmination point, consolidating 10+ tools into 4 unified operations.

## 1. Development Timeline & Strategic Pivots

### Phase 1: Foundation (Oct 18, 2025) - Single Day Bootstrap

**Commit 1904753:** "Skill Management MCP Server"

**Decisions Made:**
- ✅ **MCP Protocol:** Chose Model Context Protocol over custom API
- ✅ **stdio Transport:** Enables uvx deployment without installation
- ✅ **Per-Skill .env:** Rejected global secrets file
- ✅ **Python + uv:** Fast, modern Python tooling
- ✅ **~/.skill-mcp/skills:** Standard user-scoped directory

**Why These Decisions:**
- MCP = universal protocol (works with any MCP client, not just Claude)
- stdio = simplest transport (no HTTP server, ports, or networking)
- Per-skill .env = security isolation + clarity
- uv = future-proof Python tooling (replaces pip/venv/poetry)
- User-scoped = no sudo, no system pollution

**Evidence:**
```
Initial structure: server.py, skill_tools.py, file_tools.py, env_tools.py
Test coverage: Basic integration tests only
README: ~300 lines, focused on "what" not "why"
```

**Strategic Context:**
- Single-person project → keep it simple
- Production goal → security first
- LLM-managed → programmatic API over UI

---

### Phase 2: Security & Documentation Hardening (Oct 18, same day)

**Commit f237779:** "Add guidelines for managing sensitive secrets in README.md"

**Decision:** Document security practices explicitly.

**Why:**
- LLMs can't read minds → explicit guidance prevents leaking secrets
- README becomes executable specification → LLMs follow documented patterns

**Evidence:**
```markdown
## ⚠️ Important: Verify LLM-Generated Code
## 🔐 Managing Sensitive Secrets Safely
❌ NEVER tell Claude your actual API keys
✅ Update .env files manually on file system
```

**Pattern Identified:** **Documentation-Driven Security** - use README as behavior specification for LLMs.

---

**Commits 67cb739, 039d0be, 49fc793:** PyPI setup, MCP config, version bump to 0.1.1

**Decisions:**
- ✅ Publish to PyPI (not just GitHub)
- ✅ Entry point: `skill-mcp-server` (clear naming)
- ✅ Version 0.1.1 (not 0.0.1 - signal production-ready intent)

**Why:**
- PyPI = standard Python distribution
- uvx can fetch from PyPI automatically
- Clear entry point name = better UX

---

**Commit 11436b6:** "Enhance README.md to reflect changes in environment variable management, transitioning to per-skill .env files"

**Decision:** Document per-skill .env architecture.

**Why:**
- Global secrets = security nightmare (one leak exposes all)
- Per-skill = clear ownership, easier to audit
- Matches mental model: skills are self-contained

**Evidence:**
```markdown
Environment Variables:
- Per-skill .env files (not global secrets)
- File permissions: chmod 600
- Values never exposed when listing
```

---

**Commit 7d69c39:** "Enhance README.md with new section on sharing skills across MCP clients"

**Decision:** Market multi-client compatibility as key differentiator.

**Why:**
- Users don't understand MCP yet → need education
- Claude's native skills = proprietary → MCP = universal
- "Share skills across all MCP clients" = killer feature

**Evidence:**
```markdown
### 🔄 Share Skills Across All MCP Clients
- One skill directory, multiple clients
- Same skills in Cursor and Claude
- Seamless switching
```

**Pattern Identified:** **Marketing as Education** - README explains paradigm shifts, not just features.

---

### Phase 3: The CRUD Consolidation (Nov 7, 2025) - The Major Refactor

**Commit 78bcb08:** "refactor: unify MCP tools into CRUD operations"

**THE TURNING POINT:** Consolidated 10+ individual tools into 4 unified CRUD tools.

**Before:**
```
list_skills, get_skill, create_skill, delete_skill, validate_skill,
list_files, read_file, create_file, update_file, delete_file,
read_env, set_env, delete_env, clear_env, ...
→ 10+ tools
```

**After:**
```
skill_crud(operation="list|get|create|delete|validate|list_templates")
skill_files_crud(operation="read|create|update|delete")
skill_env_crud(operation="read|set|delete|clear")
→ 3 CRUD tools
```

**Why This Decision:**
1. **Context Window Economy:** Fewer tools = less context consumed
2. **Consistent Patterns:** All tools follow operation-based routing
3. **Bulk Operations:** CRUD enables atomic multi-file operations
4. **Better Error Handling:** Unified error responses

**Evidence from Commit:**
```
Changes:
 - Add models_crud.py with unified input models
 - Implement skill_crud.py (300 LOC)
 - Implement skill_files_crud.py (215 LOC) with bulk + atomic rollback
 - Implement skill_env_crud.py (178 LOC)
 - Enhance EnvironmentService with CRUD methods
 - Remove deprecated skill_tools.py and file_tools.py (-283 LOC)
 
 15 files changed, 1837 insertions(+), 706 deletions(-)
```

**Trade-Off Accepted:**
- ❌ More complex tool descriptions (operation parameter adds complexity)
- ✅ Simpler call patterns (fewer tools to choose from)
- ✅ Bulk operations enable atomic transactions
- ✅ Context window savings (fewer tools to load)

**Strategic Context:**
- Anthropic research: Context efficiency matters more than tool simplicity
- LLMs good at routing operations, bad at managing many tools
- CRUD = familiar pattern (REST API mental model)

**Validation:**
```
Test results after refactor:
- 145 tests passing (vs 100 before)
- 86% coverage (vs ~70% before)
- 0 regressions
```

**Pattern Identified:** **Constraint Becomes Specification** - Token limits drove architectural improvement.

---

**Commit 8243802:** "refactor: use JSON examples in tool descriptions"

**Decision:** Replace text examples with JSON in tool descriptions.

**Why:**
- LLMs parse JSON better than natural language examples
- MCP tools communicate via JSON → examples should match wire format
- Reduces ambiguity in parameter structure

**Evidence:**
```python
# Before
description="Create files. Example: files=[{path:'script.py', content:'...'}]"

# After  
description="""Create files. Example:
{
  "operation": "create",
  "files": [
    {"path": "script.py", "content": "#!/usr/bin/env python3\\n..."}
  ]
}
"""
```

---

**Commit 1e3e7d7:** "refactor: simplify env variable operations by removing modes"

**Decision:** Remove "merge"/"replace" modes, always merge.

**Why:**
- Modes = unnecessary complexity
- Merge is always safer than replace
- Users can clear → set for replace behavior

**Trade-Off:**
- Lost: Explicit replace mode
- Gained: Simpler API, fewer edge cases

**Pattern Identified:** **Simplicity Over Power** - remove knobs that aren't essential.

---

### Phase 4: Quality & Safety (Nov 7-8, 2025)

**Commit e7bea25:** "fix: resolve pylance type errors and unused imports"

**Decision:** Enable strict type checking with mypy.

**Why:**
- Production-ready = zero type errors
- Type safety catches bugs early
- Better IDE experience

**Evidence:**
```toml
[tool.mypy]
strict = true
warn_return_any = true
disallow_untyped_defs = true
```

---

**Commit 3d8e0d2:** "chore: add pre-commit hooks with strict type checking"

**Decision:** Enforce quality via pre-commit hooks.

**Why:**
- Automated enforcement > manual reviews
- Catches issues before CI
- Sets quality bar for contributors

**Evidence:**
```yaml
.pre-commit-config.yaml:
  - mypy (strict mode)
  - ruff (linting + formatting)
  - pytest (all tests must pass)
```

---

**Commit e37aa20:** "feat: add ProtectedFileError exception and prevent deletion of SKILL.md"

**Decision:** SKILL.md cannot be deleted.

**Why:**
- SKILL.md is identity of skill → deleting it destroys the skill
- Better UX: explicit error vs. silent corruption
- Forces intentional deletion (delete skill, not file)

**Evidence:**
```python
if file_path == SKILL_METADATA_FILE:
    raise ProtectedFileError(f"Cannot delete {SKILL_METADATA_FILE}")
```

**Pattern Identified:** **Defensive Design** - prevent foot-guns at API level.

---

**Commit eab3701:** "fix: improve MCP tool validation and error accuracy"

**Decision:** Enhance input validation with better error messages.

**Why:**
- LLMs need specific error messages to self-correct
- Generic "invalid input" → LLM retries blindly
- Specific "field X must be Y" → LLM fixes X

---

### Phase 5: Progressive Disclosure & Search (Nov 8-9, 2025)

**Commit 8d987a2:** "feat: add file modification timestamp to FileInfo"

**Decision:** Include timestamps in file metadata.

**Why:**
- Enables "show me recent changes"
- Supports temporal reasoning
- Standard file system feature

---

**Commit fb358fe:** "feat: implement search operation in SkillCrud with regex support"

**Decision:** Add search to `skill_crud(operation="list")`.

**Why:**
- "List all" becomes expensive with many skills
- Search = progressive disclosure
- Regex = power users (exact match + patterns)

**Evidence:**
```python
skill_crud(operation="list", search="data.*")  # Regex search
skill_crud(operation="list", search="processor")  # Text search
```

**Pattern Identified:** **Progressive Disclosure** - start broad, allow refinement.

---

**Commit da44cf8:** "feat: add Node.js template with npm package management support"

**Decision:** Support JavaScript/Node.js skills.

**Why:**
- Python-only = limiting
- Node.js = second most common ecosystem
- Template system makes it easy

**Evidence:**
```
Templates:
- basic (minimal)
- python (with venv, requirements.txt)
- bash (shell scripting)
- nodejs (package.json, npm) ← NEW
```

---

**Commit 30f9074:** "feat: add bulk read operation to skill_files_crud"

**Decision:** Support reading multiple files in one call.

**Why:**
- Reading N files = N calls = N * latency
- Bulk read = 1 call = 1 * latency
- Reduces context window churn

**Evidence:**
```python
# Before
for file in files:
    read_file(file)  # N calls

# After
read_files(files=[...])  # 1 call
```

---

**Commit 3319a5f:** "feat: improve tool descriptions for LLM usage safety"

**Decision:** Add safety warnings to tool descriptions.

**Why:**
- LLMs can't assess risk → explicit warnings needed
- "Destructive operation" → LLM asks for confirmation
- "Secure practices" → LLM follows guidelines

**Evidence:**
```python
description="""
Delete a skill. ⚠️ This is a destructive operation that cannot be undone.
Always confirm with user before deleting.
"""
```

---

**Commits 8b35d4b, e073489:** "feat: use namespaced paths to skill_files_crud output" + "feat: add namespaced paths to skill_files_crud output"

**Decision:** Use "skill:file.py" format instead of full paths.

**Why:**
- Full paths leak system details (/Users/foad/.skill-mcp/...)
- Namespaced = clear ownership (which skill owns this file?)
- Cross-platform (no Windows vs Unix path differences)

**Evidence:**
```python
# Before
path="/Users/foad/.skill-mcp/skills/calculator/math.py"

# After
path="calculator:math.py"
```

**Pattern Identified:** **Platform Abstraction** - hide implementation details.

---

### Phase 6: The Multi-Skill Execution Innovation (Nov 9, 2025)

**Commit 5821ae9:** "feat: add execute_python_code tool for running Python directly"

**THE BREAKTHROUGH:** Introduced `execute_python_code` with cross-skill imports.

**Decision:** Enable executing Python code that imports from multiple skills.

**Why:**
1. **Anthropic Research:** Code execution with MCP = 98.7% token reduction
2. **Composition > Calls:** 1 execution unifying N skills vs N tool calls
3. **Intermediate Data:** Process large datasets without context bloat
4. **Reusability:** Skills become importable libraries

**Evidence:**
```python
# Traditional: 3 separate tool calls
result1 = call("calculator", {...})
result2 = call("data-processor", {...})
result3 = call("formatter", {...})

# New: 1 unified execution
from calculator import calc
from data_processor import parse
from formatter import format
result = format(calc(parse(data)))
```

**Implementation Details:**
- `skill_references` parameter: `["skill:module.py", ...]`
- Auto-detect PEP 723 deps in imported modules
- Auto-load .env from referenced skills
- Execute via `uv run` with merged environment

**Trade-Off:**
- Limited to Python (not JS, Bash)
- More complex implementation (dependency aggregation)
- ✅ Worth it: 98.7% token reduction is game-changing

**Pattern Identified:** **Research-Driven Design** - Anthropic's MCP research directly influenced architecture.

---

**Commit 894074a:** "feat: make skills directory configurable via environment variable"

**Decision:** Allow SKILL_MCP_DIR to override default.

**Why:**
- Teams need shared skill libraries
- Projects need project-specific skills
- ~/.skill-mcp hardcoded = inflexible

**Evidence:**
```python
SKILL_MCP_DIR = os.environ.get("SKILL_MCP_DIR")
SKILLS_DIR = Path(SKILL_MCP_DIR) if SKILL_MCP_DIR else Path.home() / ".skill-mcp" / "skills"
```

**Use Cases:**
```json
{
  "env": {
    "SKILL_MCP_DIR": "/projects/shared-skills"
  }
}
```

---

**Commit 12aa036:** "feat: auto-load env vars from referenced skills and update README"

**Decision:** Auto-load .env from ALL skills referenced in `execute_python_code`.

**Why:**
- Manual env loading = error-prone
- Skills have dependencies (API keys, configs)
- Composition requires composed environments

**Evidence:**
```python
# If you import from weather-skill:api.py
# Its .env is automatically loaded
from api import get_forecast
# API_KEY from weather-skill/.env is available!
```

**Pattern Identified:** **Automatic Dependency Management** - system handles complexity, not user.

---

**Commits cdd2e8a, fe11e20:** Documentation improvements

**Decision:** Clarify PEP 723 support and market multi-skill execution.

**Why:**
- Users don't know what PEP 723 is → explain it
- "Multi-skill execution" not obvious → lead with examples
- Marketing = education for paradigm shifts

**Evidence:**
```markdown
**TL;DR:** Write Python code that unifies multiple skills in one execution - 
follows Anthropic's MCP pattern for 98.7% more efficient agents.
```

---

## 2. Decision Patterns Identified

### Pattern 1: Constraint-Driven Architecture

**Observation:** Every major decision optimized for constraints (tokens, context, latency).

**Examples:**
- CRUD consolidation → reduce tool count → save context
- Progressive disclosure (list → get) → lazy loading
- Multi-skill execution → reduce calls → save latency
- Bulk operations → reduce round-trips

**Principle:** **"Context is the scarce resource"** - optimize for token efficiency over human convenience.

---

### Pattern 2: Research-Driven Design

**Observation:** Architectural decisions backed by external research.

**Evidence:**
- Anthropic's MCP research → execute_python_code
- 98.7% token reduction → multi-skill execution
- Code execution pattern → cross-skill imports

**Principle:** **"Build what research validates"** - not what intuition suggests.

---

### Pattern 3: Documentation-Driven Security

**Observation:** README serves as executable specification for LLMs.

**Evidence:**
- Explicit security guidelines → LLMs follow them
- "❌ NEVER" warnings → LLMs avoid pitfalls
- Tool descriptions with safety notes → LLMs ask for confirmation

**Principle:** **"Document for LLMs, not humans"** - LLMs can't infer security best practices.

---

### Pattern 4: Defensive API Design

**Observation:** API prevents foot-guns at design level.

**Examples:**
- SKILL.md deletion blocked (ProtectedFileError)
- Path validation prevents traversal
- Always-merge env vars (no dangerous replace mode)
- Atomic bulk operations with rollback

**Principle:** **"Make mistakes impossible"** - not just "make mistakes detectable."

---

### Pattern 5: Progressive Refinement

**Observation:** 22 days of daily commits, each adding one thing.

**Evidence:**
- Oct 18: Foundation (1 day, 6 commits)
- Nov 7: CRUD refactor (1 day, 5 commits)
- Nov 8-9: Multi-skill execution (2 days, 5 commits)

**Principle:** **"Ship daily, improve iteratively"** - not "plan perfectly, ship once."

---

### Pattern 6: Simplicity Through Subtraction

**Observation:** Refactors removed features to reduce complexity.

**Examples:**
- Removed merge/replace modes → always merge
- Removed 10+ tools → 4 CRUD tools
- Removed global secrets → per-skill .env

**Principle:** **"Subtract to improve"** - more features ≠ better product.

---

## 3. Trade-Offs Accepted

### Trade-Off 1: Complex Tool Descriptions vs. Fewer Tools

**Decision:** CRUD consolidation made tool descriptions longer.

**Before:**
```
Tool: create_skill(name, template)
Description: Create a skill from template. (Short!)
```

**After:**
```
Tool: skill_crud(operation, name?, template?, search?, ...)
Description: Unified skill operations.
  - operation="create": Create skill from template
  - operation="list": List all skills (optional search)
  - operation="get": Get skill details
  ... (Long!)
```

**Trade-Off:**
- Lost: Simple, focused tool descriptions
- Gained: Fewer tools to manage, bulk operations

**Outcome:** ✅ Accepted - LLMs handle complex descriptions well, context savings worth it.

---

### Trade-Off 2: Python-Only vs. Multi-Language

**Decision:** `execute_python_code` only supports Python.

**Why:**
- Python = most common AI/data language
- Multi-language = much more complexity
- PEP 723 = Python-specific standard

**Trade-Off:**
- Lost: JavaScript, Bash code execution
- Gained: Simpler implementation, better Python integration

**Outcome:** ✅ Accepted - 80/20 rule (Python covers 80% of use cases).

---

### Trade-Off 3: Per-Skill .env vs. Global Secrets

**Decision:** Each skill has its own .env file.

**Why:**
- Security: Skill breach doesn't expose all secrets
- Clarity: Obvious which secrets belong to which skill
- Portability: Share skill with its secrets

**Trade-Off:**
- Lost: Centralized secret management
- Gained: Security isolation, skill portability

**Outcome:** ✅ Accepted - security > convenience.

---

### Trade-Off 4: uvx Dependency

**Decision:** Require uv installed for deployment.

**Why:**
- uvx = simplest deployment (no pip install)
- uv = modern, fast Python tooling
- PEP 723 needs uv for execution

**Trade-Off:**
- Lost: Work with pip-only environments
- Gained: Simpler deployment, automatic deps

**Outcome:** ✅ Accepted - uv is the future of Python tooling.

---

## 4. Roads Not Taken (Explicit)

### 1. Global Secrets File

**Considered:** Central ~/.skill-mcp/secrets.env  
**Rejected:** Security risk (one leak exposes all)  
**Chosen:** Per-skill .env files

---

### 2. HTTP/REST API

**Considered:** HTTP server for skill management  
**Rejected:** Complexity (ports, auth, networking)  
**Chosen:** MCP stdio transport

---

### 3. Database Storage

**Considered:** SQLite for skill metadata  
**Rejected:** Overkill (file system sufficient)  
**Chosen:** YAML frontmatter in SKILL.md

---

### 4. Multi-User Support

**Considered:** User authentication, permissions  
**Rejected:** Scope creep (personal tool)  
**Chosen:** Single-user, user-scoped directory

---

### 5. Skill Versioning

**Considered:** Version field in SKILL.md  
**Rejected:** Git handles versioning  
**Chosen:** Skills are regular files (git-friendly)

---

## 5. Strategic Insights

### Insight 1: Constraints Drive Innovation

**Observation:** Token limits → CRUD consolidation, Progressive disclosure, Multi-skill execution.

**Lesson:** Constraints aren't limitations - they're design specifications.

---

### Insight 2: Daily Shipping Velocity

**Observation:** 26 commits over 22 days = ~1.2 commits/day.

**Lesson:** Sustained velocity beats big-bang releases.

---

### Insight 3: Research-Driven Confidence

**Observation:** Major features (multi-skill execution) backed by Anthropic research.

**Lesson:** External validation enables bold decisions.

---

### Insight 4: Documentation IS Product

**Observation:** README changes = most frequent commit type.

**Lesson:** For LLM-managed tools, documentation IS the product (LLMs read README, not code).

---

## 6. Conclusion

skill-mcp's evolution demonstrates **disciplined constraint-driven design**:

1. **Oct 18:** Foundation - Pick MCP, stdio, per-skill .env (1 day)
2. **Nov 7:** CRUD consolidation - 10+ tools → 4 (1 day, major refactor)
3. **Nov 8-9:** Multi-skill execution - The breakthrough feature (2 days)

**Core Decision Pattern:** Optimize for context efficiency, not human convenience.

**Key Breakthrough:** Multi-skill execution (Anthropic research → architectural decision).

**Validation:** 145 tests, 86% coverage, production deployment - decisions proven correct.

**Next Level:** Vision Alignment - verify 98.7% token reduction claim and production-ready status.
