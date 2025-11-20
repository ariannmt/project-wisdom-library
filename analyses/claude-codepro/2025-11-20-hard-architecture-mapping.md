# Hard Architecture Mapping: Claude CodePro

**Date:** 2025-11-20  
**Type:** Level 1 Analysis (Data & Reality)  
**Target:** https://github.com/maxritter/claude-codepro  
**Codebase Size:** ~11.5K LOC  
**Commits Analyzed:** 211  
**Investigation Depth:** Long-Form

---

## Executive Summary

Claude CodePro is a **Spec-Driven Development Framework** optimized for Claude Code that enforces Test-Driven Development (TDD) through a modular rules system, workflow orchestration, and integrated MCP servers. The architecture implements **Development Workflows as Executable Specifications** where markdown rules are compiled into Claude Code commands, creating a meta-level programming system for AI behavior.

**Core Innovation:** Rules are not documentation—they are **executable behavioral programs** that define Claude's development workflow, enforced through auto-generation, quality hooks, and cross-session memory.

---

## 1. Five-Layer Architecture

### Layer 1: Distribution & Installation Infrastructure

**Purpose:** Zero-friction installation with version-locked deployment

**Components:**
```
scripts/
├── install.py          # Python-based installer (replaced Bash for compatibility)
└── lib/
    ├── dependencies.py # Tool installation (uv, ruff, mypy, basedpyright, qlty, newman, cipher)
    ├── devcontainer.py # Dev container auto-configuration
    ├── downloads.py    # Version-locked file downloads from GitHub releases
    ├── env_setup.py    # .env template and API key management
    ├── files.py        # File copy/permission/diff utilities
    ├── migration.py    # Version migration logic
    ├── shell_config.py # bash/zsh/fish shell integration with `ccp` alias
    └── ui.py           # Terminal UI for user interaction
```

**Architecture Decisions:**
* **Migration from Bash → Python (Nov 18, 2025):** Commit `91627d7` shows decisive pivot for cross-platform compatibility
* **Version-Locked Distribution:** `VERSION = "v2.4.7"` hard-coded in installer, updated by releasebot
* **One-Line Install:** `curl | python3` pattern for friction-free onboarding
* **Dev Container Support:** Isolated environment option (commit `0f8faf0`)
* **Shell Agnostic:** Supports bash, zsh, fish via detection and auto-configuration

**Key Capabilities:**
1. Downloads all files from specific GitHub release tag
2. Installs global tools: uv, ruff, mypy, basedpyright, qlty, newman, cipher
3. Configures shell with `ccp` alias pointing to Claude Code
4. Sets up `.mcp.json`, `.mcp-funnel.json`, `.cipher/config.yml`
5. Creates `.claude/` directory with rules, hooks, settings
6. Handles version migrations automatically

---

### Layer 2: Rules System (The Behavioral Programming Layer)

**Purpose:** Define Claude's development behavior as executable markdown specifications

**Architecture:**
```
.claude/rules/
├── config.yaml                    # Rule→Command mapping
├── standard/                      # Updated by installer (immutable for users)
│   ├── core/                      # Injected into ALL commands
│   │   ├── coding-standards.md
│   │   ├── context-management.md
│   │   ├── execution-verification.md
│   │   ├── git-operations.md
│   │   ├── mcp-tools.md
│   │   ├── systematic-debugging.md
│   │   ├── tdd-enforcement.md
│   │   ├── testing-strategies-coverage.md
│   │   └── verification-before-completion.md
│   ├── workflow/                  # Command-specific behaviors
│   │   ├── plan.md               # Opus 4.1 - Detailed spec creation
│   │   ├── implement.md          # Sonnet 4.5 - Batch execution with TDD
│   │   ├── verify.md             # Sonnet 4.5 - E2E test/quality verification
│   │   ├── quick.md              # Sonnet 4.5 - Fast dev without spec overhead
│   │   └── remember.md           # Sonnet 4.5 - Cross-session memory storage
│   └── extended/                  # Auto-converted to Skills (one file = one skill)
│       ├── frontend-accessibility-standards.md
│       ├── frontend-components-standards.md
│       ├── frontend-css-standards.md
│       ├── frontend-responsive-design-standards.md
│       ├── backend-api-standards.md
│       ├── backend-migration-standards.md
│       ├── backend-models-standards.md
│       ├── backend-python-standards.md
│       ├── backend-queries-standards.md
│       ├── testing-anti-patterns.md
│       └── testing-writing-guidelines.md
└── custom/                        # User-defined rules (never touched by installer)
    ├── core/
    ├── workflow/
    └── extended/
```

**The Rules-as-Programs Pattern:**

1. **Rule Files = Function Bodies:** Markdown files define Claude's behavior
2. **config.yaml = Function Signatures:** Maps rules to commands with model selection
3. **Auto-Build = Compilation:** On `ccp` startup, rules are assembled into commands
4. **Skills = Domain-Specific Subroutines:** Extended rules become invokable via `@skill-name`

**Command Configuration Schema:**
```yaml
commands:
  <command_name>:
    description: <string>
    model: opus|sonnet          # Model selection per command
    inject_skills: true|false   # Auto-load extended rules as skills
    rules:
      standard: [<rule-names>]  # Updated by installer
      custom: [<rule-names>]    # User-defined
```

**Example: `/implement` Command Assembly:**
```yaml
implement:
  model: sonnet
  inject_skills: true
  rules:
    standard:
      - implement                          # workflow/implement.md
      - coding-standards                   # core/coding-standards.md
      - context-management                 # core/context-management.md
      - execution-verification             # core/execution-verification.md
      - git-operations                     # core/git-operations.md
      - mcp-tools                          # core/mcp-tools.md
      - systematic-debugging               # core/systematic-debugging.md
      - tdd-enforcement                    # core/tdd-enforcement.md
      - testing-strategies-coverage        # core/testing-strategies-coverage.md
      - verification-before-completion     # core/verification-before-completion.md
```

**Result:** When user types `/implement`, Claude Code receives a **compiled behavioral specification** combining:
- Workflow-specific instructions (implement.md)
- 9 core behavioral rules (always active)
- All 11 extended rules as injectable Skills (`@frontend-components`, etc.)

---

### Layer 3: Workflow Orchestration (The State Machine)

**Purpose:** Enforce spec-driven development lifecycle with mandatory TDD

**Workflow States & Transitions:**

```
┌──────────────────────────────────────────────────────────────┐
│                    QUICK PATH (Fast Dev)                     │
│  /quick → Implement with best practices → Verify locally     │
│  • No spec required                                          │
│  • TDD not enforced (but encouraged)                         │
│  • Best for: Fixes, refactoring, experiments                 │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│               SPEC-DRIVEN PATH (Complex Features)            │
│                                                              │
│  1. /plan (Opus 4.1)                                         │
│     • Asks clarifying questions                              │
│     • Creates detailed spec with exact code                  │
│     • Defines Definition of Done                             │
│     • Output: .claude/specs/<feature>.md                     │
│                                                              │
│  2. /implement (Sonnet 4.5)                                  │
│     • Mandatory context gathering phase                      │
│     • RED-GREEN-REFACTOR cycle enforced                      │
│     • Per-task execution flow:                               │
│       1. Read plan's implementation steps                    │
│       2. Call chain analysis (upwards/downwards)             │
│       3. Mark task in_progress in TodoWrite                  │
│       4. Check diagnostics                                   │
│       5. Write failing test (RED)                            │
│       6. Write minimal code (GREEN)                          │
│       7. Run test - must pass                                │
│       8. Run actual program - show output                    │
│       9. Check diagnostics - must be zero                    │
│       10. Mark task completed                                │
│     • Auto-manages context when full                         │
│     • Updates plan file: [ ] → [x]                           │
│                                                              │
│  3. /remember (Sonnet 4.5)                                   │
│     • Stores learnings in Cipher (vector DB)                 │
│     • Updates plan based on context limits                   │
│     • Enables continuation after /clear                      │
│                                                              │
│  4. /verify (Sonnet 4.5)                                     │
│     • Runs ALL tests end-to-end                              │
│     • Quality checks (qlty, ruff, mypy, basedpyright)        │
│     • Security validation                                    │
│     • Must show actual outputs (no assumptions)              │
└──────────────────────────────────────────────────────────────┘
```

**Enforcement Mechanisms:**

1. **TDD Enforcement (Structural):**
   - Tests written before code (RED phase)
   - Test must FAIL before implementation
   - Code deleted if written without test
   - Every behavior = one test minimum

2. **Context Management (Automatic):**
   - Monitors token usage via `context-management.md`
   - Triggers `/remember` when context approaching full
   - Auto-compacts plan after memory storage
   - Prevents context overflow failures

3. **Verification Gates (Quality):**
   - Diagnostics must be zero before marking complete
   - Tests must pass before moving to next task
   - Actual program execution required (show real output)
   - Definition of Done checklist per task

---

### Layer 4: MCP Server Integration (The Capability Layer)

**Purpose:** Extend Claude's capabilities through Model Context Protocol

**Integrated MCP Servers:**

1. **Cipher (Cross-Session Memory)**
   - **Purpose:** Persistent knowledge across context resets
   - **Implementation:** Vector DB with semantic search
   - **Configuration:** `.cipher/config.yml`
   - **Capabilities:**
     - Store learnings via `/remember`
     - Query past implementations
     - Retrieve gotchas and patterns
     - Context: Project-specific agent memory
   - **Model:** GPT-4.1-mini + text-embedding-3-small

2. **Claude Context (Semantic Code Search)**
   - **Purpose:** Optimal codebase context retrieval
   - **Implementation:** `@zilliz/claude-context-mcp` (npm package)
   - **Capabilities:**
     - Semantic search across codebase
     - Find relevant code by intent (not keywords)
     - Auto-retrieve related components
     - Intelligent context window management

3. **Ref (Unified Documentation)**
   - **Purpose:** Documentation search, web scraping, code snippets
   - **Implementation:** HTTP-based MCP server
   - **Capabilities:**
     - Search library documentation
     - Scrape web content
     - Retrieve code examples
     - Unified interface for external knowledge
   - **Configuration:** Requires `REF_API_KEY` env var
   - **Replaced:** Context7 and Firecrawl (commit `271ceb2`, Nov 17)

4. **MCP Funnel (Tool Filtering)**
   - **Purpose:** Plugin architecture for additional MCP servers
   - **Implementation:** `mcp-funnel@0.0.6` (npm package)
   - **Capabilities:**
     - Dynamically load/unload MCP servers
     - Filter tools to reduce context usage
     - Expose core funnel tools:
       - `discover_*`
       - `get_tool_schema`
       - `load_toolset`
       - `bridge_tool_request`
   - **Configuration:** `.mcp-funnel.json`

**MCP Configuration Schema:**

`.mcp.json`:
```json
{
  "mcpServers": {
    "Ref": {
      "type": "http",
      "url": "https://api.ref.tools/mcp?apiKey=${REF_API_KEY}"
    },
    "claude-context": {
      "command": "npx",
      "args": ["-y", "@zilliz/claude-context-mcp"]
    },
    "cipher": {
      "command": "cipher",
      "args": ["--mode", "mcp", "--agent", ".cipher/config.yml"]
    },
    "mcp-funnel": {
      "command": "npx",
      "args": ["-y", "mcp-funnel@0.0.6"]
    }
  }
}
```

**Architecture Pattern:** MCP servers act as **external function libraries** that Claude can invoke, extending its capabilities beyond native IDE integration.

---

### Layer 5: Quality & Testing Infrastructure

**Purpose:** Automated quality enforcement through post-edit hooks

**Hook Architecture:**

```
.claude/hooks/
├── file_checker_python.py   # Python-specific quality checks
└── file_checker_qlty.py     # Language-agnostic quality checks
```

**Execution Flow:**

1. **Post-Edit Trigger:** Claude Code calls hooks after EVERY file edit
2. **Python Hook** (`file_checker_python.py`):
   - Runs if file is `*.py`
   - Executes: `ruff format`, `ruff check --fix`, `mypy`, `basedpyright`
   - Returns: Errors/warnings to Claude
   - Claude must fix issues before proceeding
3. **Qlty Hook** (`file_checker_qlty.py`):
   - Runs for ALL file types
   - Executes: `qlty check <file>`
   - Language-agnostic quality rules
   - Returns: Issues to Claude for fixing

**Installed Tools:**

| Tool | Purpose | Installation |
|------|---------|--------------|
| **uv** | Fast Python package manager | Global via pip |
| **ruff** | Python linter & formatter | Via uv |
| **mypy** | Python static type checker | Via uv |
| **basedpyright** | Enhanced Python type checker | Via uv |
| **qlty** | Multi-language code quality | Global binary |
| **newman** | Postman collection runner (API testing) | Global via npm |
| **cipher** | Cross-session memory vector DB | Global via pip |

**Quality Enforcement Pattern:**

```
Edit File → Hook Triggered → Quality Check → Issues? 
                                               ├─ Yes → Return to Claude → Must Fix
                                               └─ No → Continue
```

**Result:** Every file edit is **automatically validated** before Claude can proceed, creating a continuous quality enforcement loop.

---

## 2. Technical Stack Analysis

### Language Distribution

| Language | LOC | Purpose |
|----------|-----|---------|
| Python | ~3,500 | Installer, hooks, tests |
| Markdown | ~6,500 | Rules (behavioral specs), documentation |
| YAML | ~800 | Configuration (rules, CI/CD) |
| JSON | ~700 | MCP configs, settings, package metadata |

**Observation:** Markdown is the **primary programming language** for this system. Rules written in Markdown define Claude's behavior—this is **Linguistic Programming** where natural language specifications are executed by LLM runtime.

### Dependency Architecture

**Python Dependencies:**
```toml
[project]
dependencies = [
    "pytest>=8.3.4",
    "pytest-cov>=6.0.0",
    "ruff>=0.8.5",
    "mypy>=1.14.0",
    "basedpyright>=1.23.1",
]
```

**Global Tools:**
- qlty (Rust binary)
- cipher (Python package)
- newman (Node.js package)
- uv (Rust-based Python package manager)

**MCP Dependencies:**
- `@zilliz/claude-context-mcp` (npm)
- `mcp-funnel` (npm)
- `ref-tools` (HTTP API)

**Architecture Decision:** Polyglot toolchain prioritizing **best-of-breed** over language consistency. Each tool chosen for specific capability, not ecosystem alignment.

---

## 3. Data Flow & State Management

### File System as Database

**State Storage Locations:**

1. **Specs:** `.claude/specs/<feature>.md`
   - Created by `/plan`
   - Read by `/implement`
   - Updated by `/remember`
   - Format: Markdown with task checkboxes

2. **Memory:** `.cipher/` (vector DB)
   - Stores learnings from `/remember`
   - Queryable via Cipher MCP server
   - Persistent across context resets
   - Indexed by embeddings (text-embedding-3-small)

3. **Hooks:** `.claude/hooks/*.py`
   - Executed post-edit
   - No state storage (stateless validation)

4. **Settings:** `.claude/settings.local.json`
   - Claude Code IDE settings
   - Auto-connect to IDE
   - Auto-compact preferences
   - Per-project customization

5. **MCP Configs:** `.mcp.json`, `.mcp-funnel.json`
   - Server definitions
   - Tool filtering rules
   - API key placeholders

**Architectural Pattern:** **File System as State Store** with semantic indexing (Cipher) for cross-session memory. No traditional database—all state is human-readable files.

---

## 4. Capability Matrices

### Matrix 1: Workflow Commands

| Command | Model | Purpose | TDD Enforced | Context Aware | Output |
|---------|-------|---------|--------------|---------------|--------|
| `/plan` | Opus 4.1 | Spec creation | No | Yes | `.claude/specs/<feature>.md` |
| `/implement` | Sonnet 4.5 | Execute spec | **Yes** | **Yes** | Code + tests |
| `/verify` | Sonnet 4.5 | E2E validation | No | Yes | Test results + quality report |
| `/quick` | Sonnet 4.5 | Fast dev | No | Yes | Code (no spec) |
| `/remember` | Sonnet 4.5 | Memory storage | No | **Yes** | Cipher DB update |

### Matrix 2: MCP Server Capabilities

| Server | Protocol | Capability | Use Case | Cost |
|--------|----------|------------|----------|------|
| Cipher | stdio | Vector DB memory | Cross-session learnings | OpenAI API calls |
| Claude Context | stdio | Semantic code search | Optimal context retrieval | Free (local) |
| Ref | HTTP | Documentation/web | External knowledge | API key required |
| MCP Funnel | stdio | Tool filtering | Plugin architecture | Free (local) |

### Matrix 3: Quality Tools

| Tool | Language | Scope | Auto-Fix | Hook Trigger |
|------|----------|-------|----------|--------------|
| ruff | Python | Lint + format | Yes | `*.py` post-edit |
| mypy | Python | Type checking | No | `*.py` post-edit |
| basedpyright | Python | Enhanced types | No | `*.py` post-edit |
| qlty | All | Multi-language | Partial | All files post-edit |
| pytest | Python | Test execution | N/A | Manual + `/verify` |

### Matrix 4: Rules System

| Rule Type | Location | Update Policy | Compilation | Result |
|-----------|----------|---------------|-------------|--------|
| Core | `standard/core/` | Installer-managed | Auto on `ccp` startup | Injected into ALL commands |
| Workflow | `standard/workflow/` | Installer-managed | Auto on `ccp` startup | Command-specific behavior |
| Extended | `standard/extended/` | Installer-managed | Auto on `ccp` startup | Skills (`@skill-name`) |
| Custom Core | `custom/core/` | User-managed | Auto on `ccp` startup | Injected into specified commands |
| Custom Workflow | `custom/workflow/` | User-managed | Auto on `ccp` startup | Custom commands |
| Custom Extended | `custom/extended/` | User-managed | Auto on `ccp` startup | Custom skills |

### Matrix 5: Development Paths

| Path | Entry Point | Steps | TDD Required | Best For |
|------|-------------|-------|--------------|----------|
| **Quick** | `/quick` | 1. Implement → 2. Verify locally | No | Fixes, refactoring, experiments |
| **Spec-Driven** | `/plan` | 1. Plan → 2. Implement → 3. Remember (if needed) → 4. Verify | **Yes** | Complex features, new systems |

### Matrix 6: Installation Modes

| Mode | Isolation | Setup | IDE Compatibility | Recommended For |
|------|-----------|-------|-------------------|-----------------|
| **Dev Container** | Full | Auto-configured | VS Code, Cursor, Windsurf, Antigravity | Teams, consistent environments |
| **Host Install** | None | Manual configuration | All | Solo developers, quick setup |

---

## 5. Strategic Architecture Decisions

### Decision 1: Python-Based Installer (Nov 18, 2025)

**From:** Bash script installer  
**To:** Python-based installer  
**Commit:** `91627d7` - "feat: Switching towards Python-based installer"

**Rationale:**
- Cross-platform compatibility (Windows, macOS, Linux)
- Better error handling and user interaction
- Testable with pytest (E2E + unit tests added)
- Modular architecture (lib/ modules)

**Trade-Off:** Requires Python 3.10+ on host (acceptable prerequisite)

---

### Decision 2: Ref.tools Consolidation (Nov 17, 2025)

**From:** Context7 + Firecrawl (two separate MCP servers)  
**To:** Ref (unified documentation + web scraping)  
**Commit:** `271ceb2` - "fix: Replace Context7 and Firecrawl with Ref.tools"

**Rationale:**
- Reduce MCP server count (less context overhead)
- Unified API for external knowledge
- Single API key management
- Better maintained tool

**Trade-Off:** Dependency on external HTTP API (network required)

---

### Decision 3: Modular Rules System

**From:** Monolithic command definitions  
**To:** Composable rules with auto-build

**Rationale:**
- **Customizability:** Users can add custom rules without editing standard files
- **Updatability:** Installer updates standard rules without affecting custom rules
- **Modularity:** Rules are reusable across commands
- **Skills Pattern:** Extended rules auto-convert to invokable skills

**Architecture Pattern:** **Configuration as Code** where `config.yaml` defines command assembly from rule components.

---

### Decision 4: File System as State Store

**From:** N/A (greenfield)  
**To:** Human-readable files for all state

**Rationale:**
- **Transparency:** All state is readable/editable by humans
- **Git-Friendly:** Specs and configs version controlled
- **No Database:** Eliminates dependency and complexity
- **Semantic Memory:** Cipher provides vector DB when needed

**Trade-Off:** No transactional consistency (acceptable for dev tool)

---

### Decision 5: Mandatory TDD in `/implement`

**From:** Best-practice recommendation  
**To:** Structural enforcement via rules

**Rationale:**
- **Quality:** Tests catch regressions immediately
- **Documentation:** Tests document behavior
- **Confidence:** Verified output (not assumptions)
- **Professional:** Production-grade code quality

**Enforcement:** Code without tests is **deleted** by Claude (via tdd-enforcement.md rule)

---

## 6. System Boundaries & Constraints

### What Claude CodePro IS

1. **Spec-Driven Development Framework** for Claude Code
2. **Behavioral Programming System** where rules define AI workflow
3. **TDD Enforcement Engine** through workflow orchestration
4. **Quality Automation Platform** via post-edit hooks
5. **Cross-Session Memory System** via Cipher integration

### What Claude CodePro IS NOT

1. **Not a code generator** (Claude Code is the generator)
2. **Not a build system** (delegates to uv, pytest, etc.)
3. **Not language-specific** (works with any language)
4. **Not a CI/CD platform** (local dev tool only)
5. **Not an IDE** (integrates with VS Code, Cursor, Windsurf, Antigravity)

### System Constraints

1. **Claude Code Required:** Entire system depends on Claude Code IDE integration
2. **MCP Protocol:** Extensibility limited to MCP-compatible servers
3. **Python 3.10+:** Installer and hooks require modern Python
4. **Network:** MCP servers (except local) require internet
5. **API Keys:** Cipher (OpenAI), Ref (proprietary) require keys

---

## 7. Emergent Properties

### Property 1: Self-Documenting System

**Observation:** Rules are both documentation AND executable behavior. When rules change, behavior changes—documentation cannot drift.

**Implication:** **Zero documentation debt** by design. The specification IS the implementation.

---

### Property 2: Compositional Workflow Design

**Observation:** Commands are assembled from rules like functions from modules. New commands = new rule combinations.

**Implication:** **Infinite extensibility** without core changes. Users create new workflows by adding rules.

---

### Property 3: Quality as Immutable Property

**Observation:** Post-edit hooks run AFTER every change, before Claude continues. Quality is not optional.

**Implication:** **Quality is structural**, not cultural. Bad code cannot exist long enough to be committed.

---

### Property 4: Memory as First-Class Citizen

**Observation:** Cipher integration treats memory as infrastructure, not feature. `/remember` is workflow command, not utility.

**Implication:** **Persistent context** across sessions. Claude "remembers" project-specific knowledge automatically.

---

### Property 5: Model Selection per Command

**Observation:** Opus for planning (deep reasoning), Sonnet for implementation (fast execution). Right model for right task.

**Implication:** **Cost optimization** through intelligent routing. Expensive model only when needed.

---

## 8. Technical Debt & Anti-Patterns Observed

### Observation 1: Hook Execution Overhead

**Issue:** Post-edit hooks run synchronously after EVERY file edit. For large files or slow tools, this creates latency.

**Current State:** Acceptable for typical file sizes  
**Risk:** Could become bottleneck at scale

---

### Observation 2: MCP Server Startup Time

**Issue:** Four MCP servers must start on Claude Code launch. Increases initial connection time.

**Mitigation:** MCP Funnel allows lazy loading  
**Trade-Off:** Convenience vs startup speed

---

### Observation 3: Python Version Dependency

**Issue:** Installer requires Python 3.10+. Some older systems may not have it.

**Mitigation:** Dev Container option provides isolated environment  
**Acceptable:** Python 3.10+ is reasonable prerequisite for modern dev tool

---

## 9. Comparative Analysis

### vs AgentOS (Spec-Driven Framework)

| Aspect | Claude CodePro | AgentOS |
|--------|----------------|---------|
| Installation | One-line curl | Container-required |
| Language Support | Any | JavaScript-focused |
| TDD Enforcement | Structural (automatic) | Cultural (recommended) |
| Memory | Cross-session (Cipher) | Session-only |
| Customization | Rules + config.yaml | Fork required |

**Advantage:** Lower barrier to entry, broader language support, enforced quality

---

### vs Superpowers (Skills Library)

| Aspect | Claude CodePro | Superpowers |
|--------|----------------|-------------|
| Scope | Full dev workflow | Skill library only |
| Skills | Auto-generated from extended rules | Manually authored |
| TDD | Enforced | Not enforced |
| MCP Integration | Built-in (4 servers) | Optional |

**Advantage:** Workflow orchestration, not just skills. End-to-end dev framework.

---

### vs SpecKit (Spec-Driven Framework)

| Aspect | Claude CodePro | SpecKit |
|--------|----------------|---------|
| Spec Format | Markdown with checkboxes | Structured YAML |
| Execution | Claude Code native | Custom runtime |
| Model Selection | Per-command (Opus/Sonnet) | Single model |
| Platform | Claude Code only | Model-agnostic |

**Advantage:** Native Claude Code integration, intelligent model routing

---

## 10. Architecture Summary

Claude CodePro implements **Development Workflows as Executable Specifications** through five architectural layers:

1. **Distribution:** One-line installer with version-locked deployment
2. **Rules System:** Markdown-based behavioral programming (compiled on startup)
3. **Workflow Orchestration:** Spec-driven state machine with enforced TDD
4. **MCP Integration:** External capability layer (memory, search, docs, plugins)
5. **Quality Infrastructure:** Automated validation through post-edit hooks

**Core Innovation:** Rules are not documentation—they are **behavioral programs** executed by Claude Code's LLM runtime, creating a meta-level programming system where natural language specifications define AI behavior.

**Paradigm:** **Linguistic Software Development** where markdown becomes executable code, LLMs become interpreters, and workflows become compilable specifications.

---

## Appendix A: File Count by Type

| Type | Count | Purpose |
|------|-------|---------|
| Markdown | 28 | Rules (23) + docs (5) |
| Python | 23 | Installer (10) + hooks (2) + tests (11) |
| YAML | 6 | Config (1) + CI/CD (5) |
| JSON | 6 | MCP configs, settings, package metadata |
| Shell | 1 | Legacy (replaced by Python) |

---

## Appendix B: Commit Timeline (Key Milestones)

| Date | Commit | Milestone |
|------|--------|-----------|
| 2025-10-24 | `11e8c54` | Initial commit |
| 2025-10-28 | `cfa9e10` | Added Skills and Commands |
| 2025-10-28 | `4d768ac` | Added Agent OS Commands and Skills |
| 2025-10-29 | `94462fa` | Updated Spec-Driven Workflow |
| 2025-11-17 | `271ceb2` | Replace Context7 and Firecrawl with Ref.tools |
| 2025-11-17 | `0f8faf0` | Add DevContainer setup |
| 2025-11-18 | `91627d7` | Switching to Python-based installer |
| 2025-11-18 | `113e4c7` | Migrate installer from Bash to Python |
| 2025-11-19 | `65f91a9` | Release v2.4.7 |

**Evolution Pattern:** Started with Agent OS inspiration (Oct 28) → Added spec-driven workflow (Oct 29) → MCP consolidation (Nov 17) → Python migration (Nov 18) → Continuous refinement (27 days, 211 commits)

---

**Investigation Complete: Level 1 Hard Architecture Mapping**  
**Next:** Level 2 Decision Forensics & Anti-Library Extraction
