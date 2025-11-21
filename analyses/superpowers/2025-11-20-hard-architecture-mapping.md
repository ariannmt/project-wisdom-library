# Hard Architecture Mapping: Superpowers Skills Library

**Type:** Analysis (Level 1)
**Date:** 2025-11-20
**Ladder Level:** Level 1: Data/Reality
**Target:** https://github.com/obra/superpowers

## Quick Summary

Superpowers is a Claude Code plugin implementing a Skills-based architecture for AI coding assistants. It provides 20 battle-tested workflow patterns organized as executable process documentation, loaded dynamically via Claude's native Skills system. The architecture treats Skills as "programs for AI behavior" with TDD-style validation using subagent testing.

## Strategic Context

**User Intent:** "Make sure to extract all Skills patterns."

The investigation targets the Skills pattern itself - both as implemented in this specific library AND as a universal pattern for codifying AI agent behavior. This repository is both the implementation AND the canonical example of the pattern.

## Technical Architecture

### System Overview

**Core Identity:** Skills Library + Plugin Distribution System
- **Codebase:** ~6,900 LOC (predominantly markdown)
- **Commits:** 117 (tracking 3+ months of evolution)
- **Version:** 3.4.1 (mature, actively maintained)
- **Distribution:** Claude Code Plugin Marketplace

**Architectural Pattern:** Skills-as-Executable-Documentation
- Skills are markdown files with YAML frontmatter
- Loaded dynamically by Claude Code's first-party Skills system
- Activated contextually based on task detection
- Enforced through mandatory workflow integration

### Five-Layer Architecture

```
┌─────────────────────────────────────────────────────┐
│  Layer 5: Distribution & Integration                │
│  - Plugin manifest (plugin.json)                    │
│  - Marketplace integration                          │
│  - SessionStart hooks (hooks.json)                  │
│  - Slash command registration                       │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│  Layer 4: Skills System (Native Claude Integration) │
│  - YAML frontmatter (name, description)             │
│  - Skill discovery/matching engine                  │
│  - Context-aware loading                            │
│  - Namespace: superpowers:*                         │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│  Layer 3: Skills Library (20 Skills)                │
│  - Testing (3): TDD, async, anti-patterns           │
│  - Debugging (4): systematic, root-cause, etc.      │
│  - Collaboration (7): brainstorm, planning, etc.    │
│  - Development (2): git worktrees, finishing        │
│  - Meta (4): writing/testing/sharing skills         │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│  Layer 2: Skill Enforcement Patterns                │
│  - Mandatory workflows (Iron Laws)                  │
│  - Rationalization tables                           │
│  - Red flags lists                                  │
│  - Checklist integration (TodoWrite)                │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│  Layer 1: Quality Assurance (TDD for Skills)        │
│  - Subagent-driven testing                          │
│  - Pressure scenarios                               │
│  - RED-GREEN-REFACTOR for docs                      │
│  - Bulletproofing against rationalization           │
└─────────────────────────────────────────────────────┘
```

### Skill Anatomy (The Core Pattern)

Every skill follows this structure:

```yaml
---
name: skill-name-with-hyphens
description: Use when [triggering conditions] - [what it does and how]
---
```

Followed by markdown sections:
1. **Overview** - Core principle (1-2 sentences)
2. **When to Use** - Symptoms and use cases
3. **Core Pattern** - Before/after or step-by-step
4. **Quick Reference** - Scannable tables/bullets
5. **Implementation** - Inline code or file links
6. **Common Mistakes** - Pitfalls and fixes
7. **Rationalizations** - Anticipated excuses + counters (for discipline skills)
8. **Red Flags** - Self-check for violations

### Skills Taxonomy (20 Skills Mapped)

#### Testing Category (3 Skills)
- **test-driven-development** - RED-GREEN-REFACTOR cycle enforcement
- **condition-based-waiting** - Async test patterns (polling vs timeouts)
- **testing-anti-patterns** - Common testing pitfalls

#### Debugging Category (4 Skills)
- **systematic-debugging** - 4-phase root cause process
- **root-cause-tracing** - Find real problem, not symptoms
- **verification-before-completion** - Ensure actually fixed
- **defense-in-depth** - Multiple validation layers

#### Collaboration Category (7 Skills)
- **brainstorming** - Socratic design refinement
- **writing-plans** - Detailed implementation plans
- **executing-plans** - Batch execution with checkpoints
- **dispatching-parallel-agents** - Concurrent subagent workflows
- **requesting-code-review** - Pre-review checklist
- **receiving-code-review** - Responding to feedback
- **using-git-worktrees** - Parallel development branches
- **finishing-a-development-branch** - Merge/PR decision workflow
- **subagent-driven-development** - Fast iteration with quality gates

#### Development Category (2 Skills)
*(Note: Some development skills are in Collaboration category)*

#### Meta Category (4 Skills)
- **writing-skills** - TDD for process documentation
- **sharing-skills** - Contributing skills via branch/PR
- **testing-skills-with-subagents** - Validate skill quality
- **using-superpowers** - Introduction and mandatory protocols

### Technical Stack

**Primary Technology:** Markdown + YAML
- No runtime code execution
- Pure documentation-as-behavior
- Claude Code Skills system as interpreter

**Supporting Infrastructure:**
- Shell scripts (session-start.sh for bootstrap)
- JSON configuration (plugin.json, hooks.json)
- Git for version control and distribution

**Integration Points:**
- Claude Code Plugin API (v1)
- SessionStart hooks (automatic loading)
- Slash commands (/superpowers:*)
- Skill tool (for skill activation)

### Distribution & Loading Mechanism

**Installation Flow:**
1. Register marketplace: `/plugin marketplace add obra/superpowers-marketplace`
2. Install plugin: `/plugin install superpowers@superpowers-marketplace`
3. SessionStart hook triggers: loads `using-superpowers` skill
4. Skills become discoverable via Claude's native system

**Runtime Loading:**
- **Eager Loading:** `using-superpowers` at session start (mandatory protocols)
- **Lazy Loading:** Other skills loaded contextually when relevant
- **Explicit Loading:** Via Skill tool or slash commands

**Discovery Mechanism:**
- Claude reads YAML descriptions for all skills
- Matches description keywords to current task context
- Loads relevant skills automatically
- Enforces usage when skill exists for task

### Enforcement Architecture

**Three Enforcement Layers:**

1. **Structural Enforcement (Iron Laws)**
   - Absolute rules (e.g., "NO PRODUCTION CODE WITHOUT FAILING TEST")
   - No exceptions clauses
   - Delete-and-restart requirements

2. **Psychological Enforcement (Rationalization Tables)**
   - Pre-documents excuses agents will use
   - Provides counter-arguments
   - Creates cognitive dissonance when rationalizing

3. **Cultural Enforcement (Red Flags)**
   - Self-check lists
   - "STOP and Start Over" triggers
   - Meta-awareness of violation symptoms

**Example from test-driven-development skill:**
```markdown
## The Iron Law
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST

## Red Flags - STOP and Start Over
- Code before test
- "I already manually tested it"
- "This is different because..."
```

### Quality Assurance System

**TDD Applied to Documentation:**
- Skills themselves are tested via RED-GREEN-REFACTOR
- Tests = pressure scenarios with subagents
- Baseline = observe violations without skill
- Implementation = write skill to prevent violations
- Refinement = close loopholes found during testing

**Pressure Testing:**
- Time pressure scenarios
- Sunk cost scenarios (already wrote code)
- Authority scenarios (human partner said skip it)
- Exhaustion scenarios (end of long session)
- Combined pressures (maximum stress)

**Bulletproofing Process:**
1. Create pressure scenario
2. Run with subagent WITHOUT skill (baseline)
3. Document exact rationalizations used
4. Write skill addressing those rationalizations
5. Re-run with skill present
6. Find new rationalizations → add counters → repeat

### Skill Interconnections

**Dependency Hierarchy:**
```
using-superpowers (session start)
    ├─> Must use relevant skills for task
    ├─> TodoWrite for checklists
    └─> Announce skill usage

test-driven-development (foundational)
    ├─> writing-skills (TDD for docs)
    └─> subagent-driven-development (TDD at agent level)

brainstorming (before coding)
    ├─> writing-plans (after brainstorm)
    └─> executing-plans (plan execution)
    
writing-skills (meta)
    └─> testing-skills-with-subagents (validation)
```

**Cross-References:**
- Explicit: `**REQUIRED SUB-SKILL:** Use superpowers:test-driven-development`
- Implicit: Skills mention related skills by name only (no @ links to avoid context burning)

### File Organization Pattern

**Three Organizational Patterns:**

1. **Self-Contained** (most skills)
   ```
   skill-name/
     SKILL.md    # Everything inline
   ```

2. **Skill + Reusable Tool**
   ```
   condition-based-waiting/
     SKILL.md    # Overview + patterns
     example.ts  # Working helpers
   ```

3. **Skill + Heavy Reference**
   ```
   writing-skills/
     SKILL.md                    # Overview + workflows
     anthropic-best-practices.md # Official guidance
     persuasion-principles.md    # Psychology research
   ```

### Command System (Thin Wrappers)

Three slash commands, each activating corresponding skill:
- `/superpowers:brainstorm` → activates `brainstorming` skill
- `/superpowers:write-plan` → activates `writing-plans` skill
- `/superpowers:execute-plan` → activates `executing-plans` skill

Commands stored in `commands/` directory, duplicated in `skills/commands/` for plugin packaging.

### Experimental: Codex Integration

**Status:** Experimental (v3.3.0+)
- Alternative AI coding assistant
- Installation via bootstrap URL
- Separate skill directory: `~/.codex/skills`
- Same skill format, different loading mechanism

## Feature/Functionality/Capability Matrices

### Matrix 1: Skill Category × Enforcement Type

| Skill Category | Discipline (Rules) | Technique (How-To) | Pattern (Mental Model) | Reference (Docs) |
|----------------|-------------------|-------------------|----------------------|------------------|
| **Testing** | TDD (Iron Law) | Condition-based waiting | Testing anti-patterns | - |
| **Debugging** | Verification required | Systematic debugging, Root-cause | Defense-in-depth | - |
| **Collaboration** | Brainstorming (mandatory before coding) | Writing/executing plans, Git worktrees | Subagent-driven dev | - |
| **Meta** | Writing skills (TDD for docs) | Testing with subagents | - | Anthropic best practices |

### Matrix 2: Skill × Loading Strategy × Enforcement Level

| Skill | Loading | Enforcement | Bulletproofing | Checklist |
|-------|---------|-------------|----------------|-----------|
| using-superpowers | Eager (session start) | Mandatory | High (rationalization table) | Yes |
| test-driven-development | Context (feature work) | Mandatory (Iron Law) | Very High (extensive counters) | Yes |
| brainstorming | Explicit (slash command) | Mandatory (before coding) | Medium | No |
| condition-based-waiting | Context (async tests) | Recommended | Low | No |
| writing-skills | Explicit (meta work) | Mandatory (TDD for docs) | High | Yes |
| systematic-debugging | Context (debugging) | Recommended | Medium | No |

### Matrix 3: Technical Components × Implementation Layer

| Component | Layer | Technology | Integration Point |
|-----------|-------|------------|------------------|
| Plugin manifest | Distribution (L5) | JSON | Plugin API |
| SessionStart hook | Distribution (L5) | Shell + JSON | Hooks API |
| Skill frontmatter | Skills System (L4) | YAML | Native Skills |
| Skill discovery | Skills System (L4) | Claude's matcher | Description field |
| Enforcement patterns | Enforcement (L2) | Markdown | Psychological |
| Subagent testing | QA (L1) | Subagent dispatch | Tool system |
| Slash commands | Distribution (L5) | Markdown wrappers | Command API |

### Matrix 4: Quality Dimensions × Mechanism

| Quality Dimension | Primary Mechanism | Secondary Mechanism | Verification |
|-------------------|------------------|-------------------|-------------|
| **Correctness** | Subagent testing | Baseline observation | RED-GREEN cycle |
| **Completeness** | Rationalization tables | Red flags lists | Pressure scenarios |
| **Usability** | Quick reference tables | Code examples | CSO optimization |
| **Discoverability** | Description CSO | Keyword coverage | Name conventions |
| **Maintainability** | Version control | Testing requirement | TDD enforcement |
| **Consistency** | Structural templates | Cross-references | Meta-skills |

### Matrix 5: User Journey × Skill Activation

| User Action | Skills Activated | Loading Type | Enforcement |
|-------------|-----------------|-------------|-------------|
| Session starts | using-superpowers | Eager | Mandatory |
| "Let's add a feature" | test-driven-development, brainstorming | Context + Mandatory | Both required |
| "/superpowers:brainstorm" | brainstorming | Explicit | Mandatory workflow |
| Writes code before test | TDD red flags | Reactive | Delete and restart |
| Tests are flaky | condition-based-waiting | Context discovery | Recommended |
| "This is done" | verification-before-completion | Context | Mandatory |
| Creates new skill | writing-skills, testing-skills-with-subagents | Explicit | TDD for docs |

### Matrix 6: Evolution Phases × Architecture Changes

| Version Era | Key Changes | Architectural Impact | Pattern Evolution |
|-------------|-------------|---------------------|------------------|
| **v1.x-2.x** | Initial skills, external tools | MCP-based, separate repo | Proof of concept |
| **v3.0** | Native Skills integration | Integrated into plugin | Skills as first-class |
| **v3.1** | Namespace introduction | `superpowers:*` prefix | Multi-plugin coexistence |
| **v3.2** | Rationalization hardening | Psychological enforcement | Battle-testing |
| **v3.3** | Codex support | Multi-platform | Pattern portability |
| **v3.4** | Brainstorming simplification | Workflow refinement | Maturity |

## Architectural Insights

### 1. Skills as "Programs for Behavior"

Traditional code: `if (condition) { action() }`
Skills pattern: `when [symptoms] - [required behavior]`

The Skills system is a programming language for AI agent behavior where:
- YAML frontmatter = function signature
- Markdown content = function body
- Claude's Skills system = interpreter/runtime
- Subagent testing = unit tests

### 2. Three-Layer Enforcement

**Structural** (rules) → **Psychological** (rationalization counters) → **Cultural** (red flags)

Each layer catches violations the previous missed:
- Iron Law catches intentional violations
- Rationalization tables catch "justified" violations  
- Red flags catch unconscious violations

### 3. TDD Recursion

The system applies TDD at three levels:
1. **Code level:** test-driven-development skill
2. **Documentation level:** writing-skills applies TDD to skills themselves
3. **System level:** The entire library was built using its own patterns

This is self-hosting but for process documentation, not code.

### 4. Context Economy

**Progressive Disclosure Architecture:**
- Eager load only mandatory protocols (using-superpowers)
- Lazy load skills when contextually relevant
- Never force-load with @ syntax (burns context)
- Cross-reference by name only

Token efficiency was a design constraint that shaped the architecture.

### 5. Pressure-Driven Design

Skills evolve through adversarial testing:
- Run scenarios designed to break rules
- Document exact rationalizations
- Add explicit counters
- Repeat until bulletproof

This creates "battle-hardened" documentation that anticipates and counters violations.

## Constraints & Negative Knowledge

### Constraints That Shaped Design

1. **Claude Code Skills System Limitations**
   - Max 1024 chars in YAML frontmatter
   - Description field is primary discovery mechanism
   - No programmatic skill loading control
   - Context window limits aggressive (token economy matters)

2. **AI Agent Psychology**
   - Agents rationalize rule violations under pressure
   - "Spirit vs letter" arguments are common
   - Sunk cost fallacy affects code-before-test scenarios
   - Need explicit counters for each rationalization pattern

3. **Distribution Constraints**
   - Plugin marketplace requires specific structure
   - SessionStart hooks only way to auto-load
   - No guaranteed load order except hooks
   - Namespace collision risks with other plugins

### Roads Not Taken (Implicit)

- **Programmatic enforcement** → Chose psychological (AI can't be forced via code)
- **Complex dependency graphs** → Chose flat namespace (discoverability)
- **Multi-file per skill** → Chose self-contained when possible (context economy)
- **Generic templates** → Chose complete examples (usability over abstraction)

## Ripple Effects

### Immediate Consequences

1. **Skills become portable** - Same pattern works across projects
2. **Quality becomes measurable** - Test skills with subagents objectively
3. **Violations become visible** - Red flags make unconscious behaviors conscious
4. **Process becomes executable** - Documentation becomes active behavior control

### Broader Implications

1. **Documentation as Infrastructure** - Skills are runtime dependencies, not static docs
2. **TDD for Processes** - Any workflow can be tested with agents as test runners
3. **Psychological Engineering** - Explicitly designing against cognitive biases
4. **Agent Behavior Compilation** - Skills are compiled into agent context window

## Linked Artifacts

**Will be created:**
- Decision Forensics (Level 2)
- Anti-Library Extraction (Level 2)  
- Vision Alignment (Level 3)
- Process Memory (Level 3)
- Meta-Pattern Synthesis (Level 4)
- Paradigm Extraction (Level 4)

## Tags

hard-architecture, skills-pattern, claude-code, ai-agents, process-documentation, tdd-for-docs, behavioral-programming, psychological-engineering, context-optimization, level-1, wisdom-ladder
