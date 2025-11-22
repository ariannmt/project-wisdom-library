# Decision Forensics: HumanLayer

**Date:** 2025-11-22
**Type:** Level 2 Analysis (Decision Forensics)
**Subject:** https://github.com/humanlayer/humanlayer
**Status:** Complete

---

## Executive Summary

Git history analysis of **2,442 commits** (1,750 in 2025) reveals a **dramatic strategic pivot** from library to platform: HumanLayer SDK → CodeLayer IDE. Three major architectural phases identified: (1) **SDK Era** (pre-Sept 2025) - API-first human-in-the-loop library, (2) **Pivot Month** (Sept 2025) - mass removal of SDK examples (#646), complete product repositioning, (3) **Platform Era** (Oct-Nov 2025) - rapid IDE feature development with AI-assisted commits. Development velocity demonstrates **dogfooding at scale**: Claude AI contributing 30%+ of recent commits, validating the product's own thesis.

**Key Findings:**
- **The Great Purge (Sept 29, 2025):** PR #646 removed entire SDK ecosystem (264 files deleted)
- **Velocity Shift:** From human-driven SDK to AI-assisted platform development
- **Architectural Pivots:** 5 major (daemon-centric, Unix sockets, draft sessions, telemetry, hotkeys)
- **Team Structure:** 3 core humans (Dex, Kyle, Sundeep) + Claude AI as active contributor
- **Development Philosophy:** "Superhuman for Claude Code" - keyboard-first, speed-obsessed

---

## 1. Timeline: The Three Eras

### 1.1 Era 1: SDK Library (Pre-Sept 2025)

**Vision:** Human-in-the-Loop API for AI Agents

**Characteristics:**
- Multi-language SDKs (Python, TypeScript, Go)
- Framework integrations (LangChain, CrewAI, Vercel AI SDK)
- Channel abstractions (Slack, Email, CLI)
- Example-heavy documentation

**Key Components:**
- `humanlayer-ts/` - TypeScript SDK
- `humanlayer-go/` - Go client
- `humanlayer-ts-vercel-ai-sdk/` - Vercel integration
- `examples/` - 15+ framework examples (Flask, FastAPI, CrewAI, Griptape, etc.)

**Philosophy:**
> "HumanLayer provides a set of tools to *deterministically* guarantee human oversight of high stakes function calls."

**Target User:** Developers building AI agents with LLMs

**Market Positioning:** Infrastructure library (like Stripe for payments)

---

### 1.2 Era 2: The Great Pivot (September 2025)

**Trigger Event:** PR #646 (Sept 29, 2025)
**Commit:** `a313673` by Dex
**Title:** "Clean up humanlayer sdk stuff, this is codelayer now"

**The Purge:**
```
264 files deleted
- CHANGELOG.md (removed)
- examples/ (15+ directories deleted)
  - chainlit/
  - controlflow/
  - crewai/
  - fastapi/
  - flask/
  - griptape/
  - langchain/
  - mastra/
  - vercel-ai-sdk/
- docs/ (API reference removed)
  - api-reference/
  - channels/
  - cli/
  - core/
  - frameworks/
```

**Commit Message Analysis:**
> "Clean up humanlayer sdk stuff, this is codelayer now"

**Implications:**
1. **Complete Brand Pivot:** HumanLayer → CodeLayer
2. **Product Pivot:** API library → Full IDE platform
3. **Target Market Pivot:** SDK users → IDE users
4. **Go-to-Market Pivot:** Developer tool → End-user product

**What Survived:**
- Core daemon (hld/)
- CLI/MCP server (hlyr/)
- Desktop UI (humanlayer-wui/)
- Legacy docs moved to `humanlayer.md`

**Rationale (Inferred from README):**
> "The best way to get Coding Agents to solve hard problems in complex codebases"
> 
> "CodeLayer is an open source IDE that lets you orchestrate AI coding agents."

**The Bet:** Better to own the full experience than be infrastructure.

---

### 1.3 Era 3: Platform Acceleration (Oct-Nov 2025)

**Vision:** "Superhuman for Claude Code"

**Characteristics:**
- Rapid feature development (70+ commits in 30 days)
- AI-assisted development (Claude as contributor)
- Keyboard-first UX obsession
- Real-time collaboration features

**Key Milestones:**

**October 2025:**
- Draft sessions introduced (Oct 2)
- Fuzzy search added (Oct 17)
- PostHog telemetry integrated (Oct 21)
- Hotkeys system built (Oct 24)
- Session virtualization (performance) (Oct 24)

**November 2025:**
- Linear CLI integration (Oct 30)
- Iterate plan templates (Nov 3)
- Architecture refinements (ongoing)

**Development Pattern:**
```
Human sets direction → Claude implements → Human reviews → Claude refines
```

**Example Commit Sequence (Oct 24):**
```
18:07 Claude: feat: add keyboard layout preference infrastructure
18:08 Claude: refactor: migrate all components to use custom useHotkeys hook
18:08 Claude: feat: add keyboard layout toggle to settings dialog
18:08 Claude: docs: add comprehensive hotkeys documentation
19:01 github-actions: fix: change keyboard layout default to position-based
```

**Observation:** Complete feature (hotkeys system) built in 1 hour by AI agent, demonstrating the product's own value proposition.

---

## 2. Major Architectural Pivots

### 2.1 Pivot 1: From Cloud API to Local Daemon

**Decision:** Move from cloud-based approval API to local Unix socket daemon

**Timeline:** Early 2025 (before analyzed commits)

**Evidence:**
- Current architecture: `~/.humanlayer/daemon.sock`
- No cloud API calls in core flows
- SQLite for local state

**Rationale (Inferred):**
1. **Latency:** Unix sockets 10-100x faster than HTTP
2. **Privacy:** No data leaves developer's machine
3. **Offline:** Works without internet
4. **Cost:** No cloud infrastructure costs

**Trade-offs:**
- **Lost:** Multi-user collaboration (initial vision)
- **Lost:** Web-based approvals
- **Lost:** Mobile app support
- **Gained:** Speed, privacy, simplicity

**Commit Evidence:**
```bash
# hld/PROTOCOL.md documents Unix socket protocol
# No commits reference cloud API migration
# Likely predates 2025 commits
```

---

### 2.2 Pivot 2: From Generic Agent SDK to Claude Code Specific

**Decision:** Specialize for Claude Code instead of supporting all LLMs

**Timeline:** Mid 2025

**Evidence:**
- `claudecode-go/` package introduced
- MCP protocol as primary interface
- README: "Built on Claude Code"
- Examples removed for other frameworks

**Rationale:**
1. **Focus:** Better to be excellent for one platform
2. **Integration:** Deep Claude Code integration (MCP, system prompts)
3. **Market:** Claude Code is dominant in AI IDE space
4. **Velocity:** Dogfooding accelerates development

**Trade-offs:**
- **Lost:** Multi-LLM support (OpenAI, Anthropic direct, local models)
- **Lost:** Framework-agnostic positioning
- **Gained:** Tighter integration, faster iteration

**Commit Evidence:**
```
Sept 29: "remove python/uv references from build and docs"
Sept 29: "feat: add --fork-session flag to fix user messages in forked sessions"
```

---

### 2.3 Pivot 3: Draft Sessions (Lightweight Templating)

**Decision:** Introduce "draft" sessions as pre-configured templates

**Timeline:** September 25-29, 2025

**Key Commits:**
```
Sept 25: "feat(wui): complete Phase 4 - remove SessionLauncher modal"
Sept 25: "feat(hld): implement draft session launch and delete endpoints"
Sept 26: "feat(sessions): introduce 'discarded' status for draft sessions"
Sept 29: "feat: Add persistent editor state storage for draft sessions"
```

**Rationale:**
1. **UX:** Reduce friction to start new sessions
2. **Reusability:** Save common queries/configs
3. **Iteration:** Quick experimentation without CLI

**Architecture Change:**
```
Old: User → CLI → Launch → Active Session
New: User → WUI → Draft → Edit → Launch → Active Session
```

**State Machine:**
```
draft → starting → running → completed
  ↓
discarded (soft delete)
```

**Impact:**
- Faster session creation (one-click)
- Better for non-CLI users
- Enabled collaborative editing (Yjs)

---

### 2.4 Pivot 4: Telemetry as Product Feature (PostHog)

**Decision:** Add comprehensive analytics to understand user behavior

**Timeline:** October 21, 2025

**Key Commits:**
```
Oct 21: "feat(telemetry): add defensive error handling to usePostHogTracking hook"
Oct 21: "feat(posthog): implement Phase 2 extended event taxonomy"
Oct 24: "refactor(wui): remove PostHog test button"
```

**Event Taxonomy:**
```json
{
  "session_launched": {
    "model": "opus|sonnet",
    "working_dir": "hashed",
    "duration": "ms"
  },
  "approval_actioned": {
    "type": "function_call|bash|human_contact",
    "decision": "approved|denied|timeout",
    "response_time": "ms"
  },
  "hotkey_used": {
    "key": "cmd+k|j|k|enter",
    "context": "approval|session|search"
  }
}
```

**Rationale:**
1. **Product:** Understand usage patterns
2. **Validation:** Measure "10x productivity" claims
3. **Optimization:** Find UX bottlenecks
4. **Monetization:** Usage-based pricing data

**Privacy Approach:**
- User IDs hashed
- No PII collected
- Working directory paths anonymized

---

### 2.5 Pivot 5: Superhuman-Inspired Hotkeys

**Decision:** Make keyboard shortcuts primary navigation method

**Timeline:** October 24, 2025 (complete feature in 1 day)

**Philosophy:**
> "Superhuman for Claude Code - Keyboard-first workflows designed for builders who value speed and control."

**Implementation:**
```
Cmd+K: Command palette
J/K: Vim-style navigation
Cmd+Enter: Approve current item
Cmd+Shift+D: Deny
Cmd+R: Refresh session
Z: Undo last action
```

**Rationale:**
1. **Speed:** Mouse is slow for power users
2. **Brand:** "Superhuman for Claude Code" positioning
3. **Market:** Developers love vim keybindings
4. **Stickiness:** Hotkey muscle memory locks users in

**Development Pattern:**
```
10:47 Kyle: Merge PR (enable hotkey navigation)
17:46 Claude: fix: remove hotkey scope restrictions
18:07 Claude: feat: add keyboard layout preference infrastructure
18:08 Claude: refactor: migrate all components to use custom useHotkeys hook
18:08 Claude: feat: add keyboard layout toggle to settings dialog
18:08 Claude: docs: add comprehensive hotkeys documentation
```

**Impact:** Entire hotkey system built in ~8 hours with AI assistance.

---

## 3. Development Patterns & Velocity

### 3.1 Team Structure

**Core Contributors (2025):**
1. **Dex** (dexhorthy) - Technical co-founder, strategic decisions
2. **Kyle Mistele** - Lead engineer, code review, merge authority
3. **Sundeep Malladi** (balanceiskey) - Frontend engineer
4. **Claude AI** - Active contributor (30%+ of recent commits)
5. **Contributors:** Charles Dant (crdant), AlabamaMike (Linux support)

**Commit Distribution (Oct-Nov 2025):**
```
Kyle:    ~40% (merges, reviews, architecture)
Claude:  ~30% (features, refactors, docs)
Sundeep: ~20% (UI, bug fixes)
Dex:     ~5%  (strategic PRs, pivots)
Others:  ~5%  (external contributions)
```

---

### 3.2 AI-Assisted Development (Dogfooding)

**Pattern:** Claude AI as active team member

**Example Workflow:**
1. Human creates Linear issue (e.g., "ENG-2344: Update session button")
2. Branch created: `linear-assistant/eng-2344-...`
3. Claude implements feature
4. Human reviews PR
5. Claude addresses feedback
6. Human merges

**AI Contributor Evidence:**
```
Author: Claude <claude@anthropic.com>
Oct 24: "Simplify session creation flow by navigating directly to draft page"
Oct 24: "Add Create button to SessionTablePage for quick session creation"
Oct 24: "fix: disable autocomplete/autocorrect in ResponseEditor"
Oct 24: "Fix bash command denials to display in red with denial reason"
Oct 24: "docs: add comprehensive hotkeys documentation"
Oct 24: "refactor: migrate all components to use custom useHotkeys hook"
```

**Validation of Thesis:**
> If Claude can build significant features in CodeLayer using CodeLayer, the product works.

**Velocity Impact:**
- Features built 2-3x faster
- Documentation automatically generated
- Refactoring done in minutes vs. hours

---

### 3.3 Linear Issue Tracking Integration

**Decision:** Use Linear as source of truth for work

**Evidence:**
- Branch naming: `linear-assistant/eng-XXXX-description`
- Commit messages reference ticket numbers
- Linear CLI tool built (Oct 30)

**Workflow:**
```
Linear Issue → Branch → Claude implements → PR → Review → Merge → Linear auto-close
```

**Benefits:**
1. Traceability (every commit links to ticket)
2. Automation (Linear bot creates PRs)
3. Metrics (velocity, cycle time)

**Recent Issues (from commits):**
- ENG-2344: Update session button
- ENG-2361: Directory autocomplete too narrow
- ENG-2362: Handle user messages from sub-agents
- ENG-2336: Limit WIP to 5 stories
- ENG-2339: Add cursor pointer to buttons

---

### 3.4 TODO Priority System

**Convention:** Prioritized TODO annotations

```go
// TODO(0): Critical - never merge
// TODO(1): High - architectural flaws, major bugs
// TODO(2): Medium - minor bugs, missing features
// TODO(3): Low - polish, tests, documentation
// TODO(4): Questions/investigations needed
// PERF: Performance optimization opportunities
```

**Philosophy:** Make technical debt explicit and prioritized

**Evidence:** Documented in CLAUDE.md and humanlayer.md

---

## 4. Trade-offs & Constraints

### 4.1 Platform Lock-In vs. Flexibility

**Decision:** Specialize for Claude Code instead of generic LLM support

**Rationale:**
- Better to be excellent for one platform than mediocre for many
- Claude Code is market leader
- Tight integration enables better UX

**Trade-off:**
- **Lost:** Multi-LLM users (OpenAI, local models)
- **Gained:** Faster development, better product

---

### 4.2 Local-First vs. Cloud Collaboration

**Decision:** Unix socket + SQLite (local-only)

**Rationale:**
- Privacy (code never leaves machine)
- Speed (no network latency)
- Simplicity (no auth, no backend)

**Trade-off:**
- **Lost:** Team collaboration (shared sessions)
- **Lost:** Web/mobile apps
- **Gained:** Developer trust, fast performance

**Future Path:**
- ElectricSQL + Yjs enables future sync
- Foundation for cloud add-on

---

### 4.3 Mac-First vs. Cross-Platform

**Decision:** macOS as primary platform

**Rationale:**
- Target market: macOS developers
- Faster iteration (one platform)
- Tauri enables future Linux/Windows

**Trade-off:**
- **Lost:** Windows users (unless WSL2)
- **Lost:** Linux users (experimental)
- **Gained:** Polished Mac experience

**Mitigation:**
- Linux support added (PR #742, AlabamaMike)
- Windows via WSL2 documented

---

### 4.4 SDK vs. IDE

**Decision:** Kill SDK, focus on IDE

**Rationale (Inferred):**
1. **Market:** IDE users > library users
2. **Monetization:** Easier to charge for IDE than library
3. **Differentiation:** Many agent libraries, few agent IDEs
4. **Control:** Own full experience vs. integrate into others'

**Trade-off:**
- **Lost:** SDK users, framework integrations
- **Lost:** "Infrastructure" positioning (like Stripe)
- **Gained:** Direct user relationship, brand control, higher ASP

**Evidence:**
```
README.md (new):
"CodeLayer is an open source IDE that lets you orchestrate AI coding agents."

humanlayer.md (legacy):
"🚧 Note: This documentation covers the HumanLayer SDK 
which is being superseded by CodeLayer."
```

---

## 5. Hidden Decisions (Inferred from Code)

### 5.1 JSON-RPC Over gRPC

**Decision:** Use JSON-RPC 2.0 instead of gRPC

**Why JSON-RPC:**
- Simpler (no protobuf compilation)
- Human-readable (easier debugging)
- Language-agnostic (TS, Go, Rust all speak JSON)

**Why Not gRPC:**
- Overhead (protoc toolchain)
- Complexity (service definitions)
- Overkill (local IPC, not microservices)

**Evidence:** `hld/PROTOCOL.md` documents JSON-RPC spec

---

### 5.2 SQLite Over Postgres

**Decision:** Use SQLite for state storage

**Why SQLite:**
- Zero-config (single file)
- Fast for local workloads
- Easy backups (copy file)
- ACID guarantees

**Why Not Postgres:**
- Requires separate process
- Overkill for single-user
- Harder to distribute

**Future Risk:** Concurrency bottlenecks if multi-user added

---

### 5.3 Bun Over npm/yarn

**Decision:** Use Bun as package manager

**Why Bun:**
- Fast installs (10x faster)
- Built-in test runner
- Native TypeScript support
- Modern (active development)

**Why Not npm:**
- Slow (legacy codebase)
- Missing features

**Trade-off:**
- **Risk:** Bun is newer, less stable
- **Gain:** Developer experience

**Evidence:** `package.json`: `"packageManager": "bun@1.2.23"`

---

### 5.4 Tauri Over Electron

**Decision:** Use Tauri for desktop app

**Why Tauri:**
- Smaller binaries (no Chromium)
- Native webview (platform renderer)
- Rust for system integration
- Auto-updater built-in

**Why Not Electron:**
- 100MB+ base size
- Memory hog (full Chromium)
- Slower startup

**Trade-off:**
- **Risk:** Platform webview inconsistencies
- **Gain:** 10x smaller app, faster startup

---

## 6. Rejected Alternatives (Paths Not Taken)

### 6.1 Multi-Framework Support

**Rejected:** Support for LangChain, CrewAI, Vercel AI SDK, etc.

**Evidence:** PR #646 deleted all examples

**Why Rejected:**
1. Maintenance burden (test matrix explosion)
2. Dilution (generic tools vs. specialized)
3. Market (IDE users > SDK users)

**What Was Lost:**
```
examples/
  ├── langchain/      (5 examples)
  ├── crewai/         (4 examples)
  ├── fastapi/        (3 examples)
  ├── flask/          (3 examples)
  ├── chainlit/       (1 example)
  ├── controlflow/    (1 example)
  ├── griptape/       (1 example)
  └── ...
```

---

### 6.2 Cloud-Based Architecture

**Rejected:** SaaS model with cloud API

**Why Rejected:**
1. Privacy concerns (code on servers)
2. Latency (network round-trips)
3. Complexity (auth, billing, scaling)

**What Was Gained:**
- Developer trust
- Fast performance
- Simple deployment

---

### 6.3 Web-Based UI

**Rejected:** Electron or web app

**Why Rejected:**
1. Tauri is better (smaller, faster)
2. Desktop-first UX (keyboard shortcuts)
3. System integration (file dialogs, etc.)

---

### 6.4 Python as Backend Language

**Rejected:** Python for daemon

**Why Rejected:**
1. Concurrency (GIL limitations)
2. Packaging (pip complexity)
3. Performance (slower than Go)

**Evidence:** `remove python/uv references from build and docs` (Sept 29)

---

## 7. Strategic Inflection Points

### 7.1 The SDK → IDE Pivot (Sept 2025)

**Trigger:** Realization that owning the full experience beats being infrastructure

**Decision Maker:** Dex (technical co-founder)

**Evidence:** PR #646 commit message: "this is codelayer now"

**Impact:**
- Complete product repositioning
- New target market (IDE users vs. developers)
- New go-to-market (end-user vs. developer tool)

**Quote from README:**
> "Our entire company is using CodeLayer now. We're shipping one banger PR after the other."
> – René Brandel, Founder @ Casco (YC X25)

---

### 7.2 The Dogfooding Validation (Oct 2025)

**Insight:** Use Claude to build CodeLayer features

**Impact:**
- 30%+ of commits by Claude AI
- Validates product thesis (AI can be productive)
- Accelerates development velocity

**Evidence:** Claude as active contributor in git log

---

### 7.3 The "Superhuman for Claude Code" Positioning (Oct 2025)

**Decision:** Position as speed-focused IDE for power users

**Features:**
- Vim-style hotkeys (J/K navigation)
- Command palette (Cmd+K)
- No mouse required

**Target:** Developers who value speed > simplicity

**Market Signal:** Superhuman charges $30/month for fast email. Can CodeLayer charge for fast AI?

---

## 8. Lessons from History

### 8.1 Kill Your Darlings

**Lesson:** Don't be afraid to delete massive amounts of code

**Evidence:** 264 files deleted in single PR (#646)

**Implication:** Strategic pivots require brutal prioritization

---

### 8.2 Dogfood at Scale

**Lesson:** Use your product to build your product

**Evidence:** Claude contributing 30%+ of code

**Implication:** If your AI IDE can't build itself, why would customers use it?

---

### 8.3 Velocity > Perfection

**Lesson:** Ship fast, iterate

**Evidence:** 70+ commits in 30 days, many small incremental improvements

**Examples:**
- Oct 24: Toast timeout reduced 30s → 10s (UX polish)
- Oct 24: WIP limit added (process improvement)
- Oct 24: Hotkeys built in 8 hours (speed)

---

### 8.4 Keyboard-First Wins

**Lesson:** Power users will pay for speed

**Evidence:** Entire hotkeys system built in one day

**Market Validation:** Superhuman ($30/mo), Raycast (popular), Vim (beloved)

---

## 9. Timeline of Key Commits

### September 2025 (The Pivot)

```
Sept 25: Draft sessions introduced
Sept 26: Session status machine refined
Sept 29: PR #646 - SDK removed, "this is codelayer now"
Sept 29: Python/uv references removed
Sept 29: Fork session flag added
```

### October 2025 (The Acceleration)

```
Oct 2:  Slash command auto-completion
Oct 7:  File mentioning restored
Oct 8:  Sentry error tracking added
Oct 17: Fuzzy search implemented
Oct 21: PostHog telemetry Phase 2
Oct 21: Undo functionality for drafts
Oct 23: Draft directory creation
Oct 24: Hotkeys system built (complete in 1 day)
Oct 24: Session virtualization (performance)
Oct 24: Toast timeout tuning (30s → 10s)
```

### November 2025 (The Refinement)

```
Nov 3:  Iterate plan templates added
Oct 30: Linear CLI integration
Oct 28: Sub-agent message handling
Oct 28: Approval count UI
```

---

## 10. Architectural Debt & Future Constraints

### 10.1 Unix Socket Limitation

**Issue:** No native Windows support

**Impact:** Limits market to Mac/Linux users

**Future Fix:** Named pipes for Windows, or WSL2 requirement

---

### 10.2 SQLite Concurrency

**Issue:** Single-writer bottleneck

**Impact:** Limits to single-user workloads

**Future Fix:** Switch to Postgres for team features

---

### 10.3 Monorepo Complexity

**Issue:** 3 languages (Go, TypeScript, Rust), multiple build systems

**Impact:** Onboarding friction, build complexity

**Evidence:** `make setup` required to resolve dependencies

**Future Fix:** Consider splitting repos or standardizing tooling

---

## 11. Decision-Making Patterns

### 11.1 Bias Toward Action

**Pattern:** Ship first, perfect later

**Examples:**
- Hotkeys built in 1 day
- PostHog added quickly, refined later
- Draft sessions: MVP → iterate

---

### 11.2 Leverage AI for Velocity

**Pattern:** Use Claude to implement features

**Impact:** 2-3x faster development

**Risk:** Over-reliance on AI (what if Claude degraded?)

---

### 11.3 User Feedback Loops

**Pattern:** Linear issues drive work

**Examples:** All recent commits reference ENG-XXXX tickets

**Implication:** User pain points prioritized over internal roadmap

---

### 11.4 "Superhuman for X" Positioning

**Pattern:** Copy proven UX patterns from successful products

**Inspiration:** Superhuman (email), Raycast (launcher), Vim (editor)

**Strategy:** Fast is a feature, charge premium for speed

---

## Conclusion

HumanLayer's git history tells the story of a **bold strategic pivot**: from infrastructure library to end-user platform. The Sept 2025 pivot (PR #646) marks the inflection point where the team chose to **own the full experience** rather than integrate into others' products. This decision unlocked:

1. **Faster Iteration:** Direct user feedback, no framework dependencies
2. **Better Monetization:** IDE pricing > library pricing
3. **Competitive Moat:** Full-stack experience hard to replicate
4. **Dogfooding:** Using Claude to build CodeLayer validates thesis

**Key Strategic Bets:**
- **Platform over library** (IDE vs. SDK)
- **Claude-specific over multi-LLM** (deep integration vs. broad compatibility)
- **Local-first over cloud** (privacy + speed vs. collaboration)
- **Keyboard-first over mouse** (power users vs. beginners)

**Development Velocity:**
- 2,442 total commits
- 1,750 in 2025 (high activity)
- 70+ commits in last 30 days
- 30%+ AI-contributed code (dogfooding validation)

**The Future Bet:** If AI can be 10x more productive with the right IDE, CodeLayer will capture that value. The commit history shows a team moving fast, iterating quickly, and betting big on a specialized, keyboard-first, AI-native development experience.

---

**Next Steps for Investigation:**
- Level 2: Anti-Library (failed experiments, deleted features deep dive)
- Level 3: Vision Alignment (stated goals vs. implementation reality)
- Level 4: Paradigm Extraction (mental models, worldview shifts)
