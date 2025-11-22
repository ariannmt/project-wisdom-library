# Hard Architecture Mapping: HumanLayer

**Date:** 2025-11-22
**Type:** Level 1 Analysis (Hard Architecture Mapping)
**Subject:** https://github.com/humanlayer/humanlayer
**Status:** Complete

---

## Executive Summary

HumanLayer (now pivoting to **CodeLayer**) is a sophisticated polyglot orchestration platform implementing a **Human-in-the-Loop AI IDE**. Architecture comprises 7 major components across 3 programming languages (Go, TypeScript, Rust), employing Unix sockets + JSON-RPC for IPC, and implementing real-time collaboration via CRDT (Yjs). Core innovation: **daemon-coordinated session management** enabling parallel AI agent orchestration with human oversight at critical decision points.

**Key Metrics:**
- **Total LOC:** ~35K+ across 517 source files
- **Go Backend:** ~20K LOC (daemon, session mgmt, approval workflows)
- **TypeScript/React:** ~11K LOC (CLI, MCP server, React UI)
- **Rust (Tauri):** Desktop bridge layer
- **Commits:** 2,442 total (1,750 in 2025) - high velocity
- **Contributors:** 5+ core team (Dex, Kyle, Sundeep, Claude AI)
- **Recent Activity:** 70+ commits in last 30 days

---

## 1. System Architecture Overview

### 1.1 The Big Picture

```
┌─────────────────────────────────────────────────────────────────┐
│                    CODELAYER ECOSYSTEM                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    │
│  │   Claude     │    │   Human      │    │   Linear     │    │
│  │   Code       │◄──►│   Operator   │◄──►│   Issues     │    │
│  │  (Agent)     │    │   (WUI/TUI)  │    │  (Tasks)     │    │
│  └──────┬───────┘    └──────┬───────┘    └──────────────┘    │
│         │                    │                                 │
│         │ MCP Protocol       │ JSON-RPC                        │
│         ▼                    ▼                                 │
│  ┌─────────────────────────────────────────────────┐          │
│  │        HLD (HumanLayer Daemon) - Go              │          │
│  │  • Session Orchestration                         │          │
│  │  • Approval Workflow Engine                      │          │
│  │  • Real-time Event Bus (SSE)                     │          │
│  │  • SQLite State Store                            │          │
│  │  • Claude Code SDK Integration                   │          │
│  └─────────────────────────────────────────────────┘          │
│         ▲                                                       │
│         │ Unix Socket (daemon.sock)                            │
│         ▼                                                       │
│  ┌──────────────────┐         ┌──────────────────┐            │
│  │  hlyr (CLI/MCP)  │         │  WUI (Desktop)    │            │
│  │  TypeScript      │         │  Tauri + React    │            │
│  │  • MCP Server    │         │  • Rich UI        │            │
│  │  • Tool Proxy    │         │  • Hotkeys        │            │
│  │  • Launch API    │         │  • Collab (Yjs)   │            │
│  └──────────────────┘         └──────────────────┘            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Component Layering

```
┌─────────────────────────────────────────────────────────────┐
│ Layer 4: Presentation (Multi-Interface)                     │
├─────────────────────────────────────────────────────────────┤
│ • WUI (Tauri Desktop App) - Rich graphical interface        │
│ • TUI (Terminal UI) - Console-based approval flows          │
│ • CLI (hlyr) - Command-line orchestration                   │
└─────────────────────────────────────────────────────────────┘
                          ▲
                          │ JSON-RPC / Unix Socket
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ Layer 3: Coordination & Orchestration (Go Daemon)           │
├─────────────────────────────────────────────────────────────┤
│ • Session Manager - Lifecycle of AI agent runs              │
│ • Approval Engine - Human-in-the-loop decision gates        │
│ • Event Bus - Real-time notifications (SSE)                 │
│ • RPC Server - JSON-RPC 2.0 over Unix sockets               │
└─────────────────────────────────────────────────────────────┘
                          ▲
                          │ MCP + claudecode-go SDK
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ Layer 2: AI Agent Runtime (Claude Code)                     │
├─────────────────────────────────────────────────────────────┤
│ • Tool Calling Engine                                        │
│ • MCP Protocol Client                                        │
│ • Conversation State                                         │
└─────────────────────────────────────────────────────────────┘
                          ▲
                          │ Tool Definitions
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ Layer 1: Tool Ecosystem (MCP Servers)                       │
├─────────────────────────────────────────────────────────────┤
│ • hlyr MCP Server - Session control tools                   │
│ • Filesystem, Git, Bash - Standard tools                    │
│ • Linear, Search - Domain tools                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Component Deep Dive

### 2.1 HLD (HumanLayer Daemon) - Go Backend

**Purpose:** Central orchestration hub for all AI agent sessions and approval workflows

**Location:** `/hld/`
**Language:** Go 1.24
**Architecture Pattern:** Event-driven service with JSON-RPC API

**Key Modules:**

1. **Session Manager** (`hld/session/`)
   - Manages Claude Code session lifecycle
   - Coordinates multiple parallel sessions
   - Tracks session state (starting → running → completed/failed)
   - Draft sessions (user-initiated templates)
   
2. **Approval Engine** (`hld/approval/`)
   - Human-in-the-loop decision points
   - Approval types: function_call, bash_command, human_contact
   - Decision routing (approve/deny/respond)
   - Timeout handling
   
3. **RPC Server** (`hld/rpc/`)
   - JSON-RPC 2.0 over Unix domain sockets
   - Methods: launchSession, listSessions, fetchApprovals, sendDecision
   - Subscription system for real-time events
   
4. **Event Bus** (`hld/bus/`)
   - SSE (Server-Sent Events) for real-time updates
   - Event types: session_updated, approval_requested, approval_resolved
   - Pub/sub pattern for UI synchronization
   
5. **Store** (`hld/store/`)
   - SQLite database for persistent state
   - Tables: sessions, approvals, conversation_events
   - Schema evolution via migrations
   
6. **Claude Code SDK Integration** (`claudecode-go/`)
   - Go wrapper for Claude Code API
   - Session launching and control
   - Model selection (Opus vs Sonnet)

**Technology Stack:**
- Gin web framework (for HTTP/SSE endpoints)
- SQLite with mattn/go-sqlite3
- Viper for configuration
- UUID for session IDs
- Custom fuzzy search (sahilm/fuzzy)

**IPC Pattern:**
```
Unix Socket: ~/.humanlayer/daemon.sock
Format: Line-delimited JSON (JSON-RPC 2.0)
Permissions: 0600 (owner-only)
```

---

### 2.2 hlyr - TypeScript CLI & MCP Server

**Purpose:** Command-line interface and MCP protocol bridge between Claude and daemon

**Location:** `/hlyr/`
**Language:** TypeScript (Node.js)
**Package Manager:** Bun

**Key Components:**

1. **MCP Server** (`hlyr/src/mcp/`)
   - Implements Model Context Protocol
   - Exposes tools to Claude Code:
     - `session_create_draft` - Initialize new session templates
     - `session_list` - Query available sessions
     - `session_get_state` - Fetch session details
     - `session_continue` - Resume paused sessions
   - Tool schema validation via Zod
   
2. **Daemon Client** (`hlyr/src/daemon/`)
   - TypeScript client for daemon JSON-RPC API
   - Connection pooling and retry logic
   - Event stream handling
   
3. **CLI Commands** (`hlyr/src/commands/`)
   - `launch` - Start new Claude Code sessions
   - `list` - Display sessions
   - `logs` - Tail session logs
   - (Removed: login, ping, contactHuman - legacy SDK features)

**Integration Flow:**
```
Claude Code
    ↓ (asks for tool)
MCP Server (hlyr)
    ↓ (translates to RPC)
Unix Socket
    ↓
HLD Daemon
    ↓ (executes)
Claude Code SDK
```

---

### 2.3 WUI (Desktop UI) - Tauri + React

**Purpose:** Rich graphical interface for session management and approvals

**Location:** `/humanlayer-wui/`
**Frontend:** React 19 + TypeScript
**Backend Bridge:** Rust (Tauri)
**Build System:** Bun + Tauri CLI

**Architecture:**

```
┌──────────────────────────────────────────────┐
│          React Layer (TypeScript)            │
├──────────────────────────────────────────────┤
│ • Components (shadcn/ui)                     │
│ • Hooks (useApprovals, useSessions)          │
│ • Stores (Zustand + ElectricSQL)             │
│ • Real-time collaboration (Yjs + TipTap)     │
└──────────────────────────────────────────────┘
                    ▲
                    │ Tauri IPC
                    ▼
┌──────────────────────────────────────────────┐
│          Rust Bridge (Tauri)                 │
├──────────────────────────────────────────────┤
│ • Daemon client (Unix socket)                │
│ • System integration (file dialogs, etc)     │
│ • Window management                          │
└──────────────────────────────────────────────┘
```

**Key Features:**

1. **Session Management UI**
   - Table view with virtualization (react-virtual)
   - Draft/Active/Archived tabs
   - Fuzzy search across conversations
   - Keyboard shortcuts (Superhuman-style)
   
2. **Approval Flow UI**
   - Real-time approval notifications
   - Side-by-side code diffs
   - Quick approve/deny actions
   - Context-rich approval details
   
3. **Conversation Viewer**
   - TipTap rich text editor
   - Syntax highlighting
   - Tool call visualization
   - Collaborative editing (Yjs CRDT)
   
4. **Hotkeys System**
   - Cmd+K command palette
   - Navigation shortcuts (J/K vim-style)
   - Quick actions (Cmd+Enter to approve)
   - Configurable keyboard layouts

**State Management:**
- Zustand for UI state
- ElectricSQL (reactive SQLite sync)
- Yjs for CRDT-based collaboration

**UI Framework:**
- Radix UI primitives
- Tailwind CSS v4
- Lucide icons
- shadcn/ui components

---

### 2.4 Database Schema (SQLite)

**Location:** `/packages/database/`
**ORM:** Prisma-like custom schema

**Core Tables:**

1. **sessions**
   ```sql
   id TEXT PRIMARY KEY
   run_id TEXT
   claude_session_id TEXT
   parent_session_id TEXT
   status TEXT  -- 'starting', 'running', 'completed', 'failed'
   query TEXT
   model TEXT
   working_dir TEXT
   created_at TIMESTAMP
   last_activity_at TIMESTAMP
   completed_at TIMESTAMP
   error_message TEXT
   cost_usd REAL
   total_tokens INTEGER
   duration_ms INTEGER
   ```

2. **approvals**
   ```sql
   id TEXT PRIMARY KEY
   session_id TEXT
   type TEXT  -- 'function_call', 'bash_command', 'human_contact'
   status TEXT  -- 'pending', 'approved', 'denied', 'timeout'
   request_data JSON
   response_data JSON
   created_at TIMESTAMP
   resolved_at TIMESTAMP
   timeout_at TIMESTAMP
   ```

3. **conversation_events**
   ```sql
   id TEXT PRIMARY KEY
   session_id TEXT
   event_type TEXT
   event_data JSON
   timestamp TIMESTAMP
   parent_tool_use_id TEXT
   ```

**Indexing Strategy:**
- session_id indices for fast lookups
- status + last_activity_at for active session queries
- Full-text search on query + conversation content

---

## 3. Data Flow Patterns

### 3.1 Session Launch Flow

```
User (CLI/WUI)
    ↓ "Implement feature X"
hlyr CLI / WUI Tauri Command
    ↓ JSON-RPC: launchSession(query, options)
HLD Daemon
    ↓ 1. Create session record
    ↓ 2. Call claudecode-go.LaunchSession()
    ↓ 3. Return session_id
Claude Code Runtime
    ↓ Starts executing, calls tools
MCP Server (hlyr)
    ↓ Tools request approvals
HLD Daemon
    ↓ Approval workflow
    ↓ Emit events to WUI
WUI
    ↓ Shows approval UI
Human
    ↓ Approve/Deny
HLD Daemon
    ↓ Send decision back to Claude
Claude Code
    ↓ Continues execution
```

### 3.2 Approval Workflow

```
Claude Code
    ↓ Tool call: bash("rm -rf /")
MCP Server (hlyr)
    ↓ Recognizes dangerous operation
    ↓ JSON-RPC: requestApproval(session_id, tool, args)
HLD Daemon
    ↓ 1. Create approval record (status: pending)
    ↓ 2. Emit event: approval_requested
    ↓ 3. Block tool execution
Event Bus (SSE)
    ↓ Push to all connected clients
WUI/TUI
    ↓ Display approval request with context
Human
    ↓ Reviews → Clicks "Deny"
WUI
    ↓ JSON-RPC: sendDecision(approval_id, "denied", reason)
HLD Daemon
    ↓ 1. Update approval (status: denied)
    ↓ 2. Emit event: approval_resolved
    ↓ 3. Return error to MCP
MCP Server
    ↓ Return tool_error to Claude
Claude Code
    ↓ Receives error, adjusts plan
```

### 3.3 Real-time Sync

```
HLD Daemon Event Bus
    ↓ SSE endpoint: /events
    ↓ Events: session_updated, approval_*, conversation_*
Multiple Clients (WUI + TUI)
    ↓ Maintain persistent SSE connections
    ↓ Receive events in real-time
Client State
    ↓ Updates local stores (Zustand, ElectricSQL)
UI
    ↓ React re-renders automatically
```

---

## 4. Technology Stack Summary

### 4.1 Backend (Go)

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Runtime | Go 1.24 | Performance, concurrency |
| Web Framework | Gin | HTTP/SSE endpoints |
| Database | SQLite | Session persistence |
| IPC | Unix sockets | Low-latency local communication |
| RPC | JSON-RPC 2.0 | Structured API |
| Config | Viper | Configuration management |
| Testing | testify + go-mock | Unit/integration tests |

### 4.2 Frontend (TypeScript)

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Runtime | Node.js / Bun | JS execution |
| Language | TypeScript 5.9 | Type safety |
| CLI Framework | Custom (Bun) | Command handling |
| MCP | @mark3labs/mcp-go | Protocol implementation |
| Validation | Zod | Schema validation |
| Testing | Jest/Vitest | Unit tests |

### 4.3 Desktop UI (Tauri + React)

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Native Bridge | Rust (Tauri) | System integration |
| UI Framework | React 19 | Component model |
| State | Zustand | Global state |
| Sync | ElectricSQL | Reactive DB sync |
| Collab | Yjs + TipTap | CRDT editing |
| Styling | Tailwind v4 | Utility-first CSS |
| Components | Radix UI + shadcn | Accessible primitives |
| Icons | Lucide | Icon library |

### 4.4 Infrastructure

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Monorepo | Turborepo | Build orchestration |
| Package Manager | Bun 1.2 | Fast installs |
| Linting | Biome | Fast linting |
| Git Hooks | pre-commit | Quality gates |
| CI/CD | GitHub Actions | Automated workflows |
| Documentation | Markdown | In-repo docs |

---

## 5. Deployment & Distribution

### 5.1 Artifacts

1. **HLD Daemon Binary**
   - Platform-specific: `hld-macos-arm64`, `hld-linux-amd64`
   - Installed to: `~/.humanlayer/bin/`
   - Runs as background service
   
2. **WUI Desktop App**
   - macOS: `CodeLayer.app` (Homebrew cask)
   - Linux: `.deb` / `.AppImage`
   - Auto-update via Tauri updater
   
3. **hlyr CLI + MCP**
   - npm package: `@humanlayer/hlyr`
   - Installs to: `npx humanlayer` or `codelayer` alias
   - MCP server auto-registered with Claude

### 5.2 Installation Patterns

**macOS (Homebrew):**
```bash
brew install --cask codelayer
npx humanlayer launch "build feature"
```

**Linux:**
```bash
curl -fsSL https://install.humanlayer.dev | sh
codelayer launch "fix bug"
```

**Development:**
```bash
make daemon-dev     # Dev daemon
make wui-dev        # Dev WUI
make daemon-nightly # Stable production daemon
```

---

## 6. Inter-Process Communication (IPC)

### 6.1 Unix Socket Protocol

**Socket Path:** `~/.humanlayer/daemon.sock`
**Protocol:** JSON-RPC 2.0
**Transport:** Line-delimited JSON

**Example Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "launchSession",
  "params": {
    "query": "Implement user authentication",
    "model": "sonnet",
    "working_dir": "/path/to/project",
    "max_turns": 50
  },
  "id": 1
}
```

**Example Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "session_id": "sess_abc123",
    "run_id": "run_xyz789"
  },
  "id": 1
}
```

### 6.2 Event Streaming (SSE)

**Endpoint:** `http://localhost:8080/events`
**Format:** Server-Sent Events

**Event Types:**
- `session_started`
- `session_updated`
- `session_completed`
- `approval_requested`
- `approval_resolved`
- `conversation_message`

**Example Event:**
```
event: approval_requested
data: {"session_id": "sess_123", "approval_id": "apr_456", "type": "bash_command", "command": "rm important.txt"}
```

---

## 7. Security & Permissions

### 7.1 Socket Security

- Unix socket permissions: `0600` (owner-only)
- No network exposure (local IPC only)
- Process isolation via user boundaries

### 7.2 Approval Gates

**High-Stakes Operations Requiring Approval:**
- Bash commands (especially destructive ones)
- File writes outside working directory
- Network requests to sensitive APIs
- Function calls with side effects

**Automatic Approval:**
- Read-only operations
- Operations within sandbox
- Whitelisted safe commands

### 7.3 Session Isolation

- Each session has isolated working directory
- Environment variables scoped per session
- No cross-session state leakage

---

## 8. Scalability & Performance

### 8.1 Concurrency Model

**Go Daemon:**
- Goroutines for each session
- Concurrent session execution
- Non-blocking RPC handlers
- Channel-based event distribution

**React UI:**
- Virtual scrolling for large lists
- Debounced search
- Lazy loading of conversation history

### 8.2 Database Performance

- Indexed queries on hot paths
- Connection pooling (single-threaded SQLite)
- Periodic vacuum for space reclamation
- Automatic cleanup of old sessions

### 8.3 Resource Limits

- Max parallel sessions: Configurable (default: 10)
- Session timeout: 24 hours
- Approval timeout: 5 minutes
- Max conversation history: 1000 events per session

---

## 9. Observability

### 9.1 Logging

**Daemon Logs:**
- Location: `~/.humanlayer/logs/daemon-*.log`
- Rotation: Daily
- Levels: DEBUG, INFO, WARN, ERROR

**WUI Logs:**
- Location: `~/.humanlayer/logs/wui-{branch}/codelayer.log`
- Structured JSON logs
- Browser console in dev mode

### 9.2 Telemetry

**PostHog Integration:**
- Event tracking (session_launched, approval_actioned)
- Performance metrics (session_duration, token_usage)
- Privacy: User ID hashed, no PII

### 9.3 Health Checks

**Daemon:**
- JSON-RPC method: `health`
- Returns: status, version, uptime

**WUI:**
- Connection status indicator
- Auto-reconnect on disconnect

---

## 10. Development Environment

### 10.1 Parallel Environments

**Nightly (Stable):**
- Socket: `~/.humanlayer/daemon.sock`
- DB: `~/.humanlayer/daemon.db`
- WUI: Installed app

**Dev (Testing):**
- Socket: `~/.humanlayer/daemon-dev.sock`
- DB: `~/.humanlayer/dev/daemon-{timestamp}.db`
- WUI: Dev server (hot reload)

### 10.2 Monorepo Structure

```
humanlayer/
├── hld/                    # Go daemon
├── hlyr/                   # TS CLI/MCP
├── humanlayer-wui/         # Tauri desktop app
├── claudecode-go/          # Go SDK for Claude Code
├── packages/
│   ├── database/           # Shared DB schema
│   └── contracts/          # Shared types
├── apps/
│   ├── daemon/             # (Legacy, consolidated into hld)
│   └── react/              # Standalone React app (deprecated)
├── .github/workflows/      # CI/CD
└── docs/                   # Documentation
```

### 10.3 Build Commands

```bash
make setup              # Setup monorepo
make daemon-dev         # Build & run dev daemon
make wui-dev            # Run WUI in dev mode
make test               # Run all tests
make check              # Lint & type check
```

---

## 11. Integration Points

### 11.1 Claude Code Integration

- **claudecode-go SDK:** Go wrapper for Claude Code API
- **Launch API:** Programmatic session creation
- **MCP Config:** Custom tool configurations per session
- **System Prompts:** Inject custom instructions

### 11.2 Linear Integration

- **Issue Tracking:** Auto-create issues from sessions
- **Status Sync:** Update issue state based on session completion
- **CLI:** `linear-cli` for quick issue management

### 11.3 Git Integration

- **Worktrees:** Multiple sessions in isolated worktrees
- **Branch Management:** Auto-branch creation per session
- **Commit Tracking:** Link commits to sessions

---

## 12. Key Architectural Decisions

### 12.1 Why Unix Sockets?

**Rationale:**
- Lower latency than HTTP (no TCP overhead)
- Secure by default (filesystem permissions)
- Natural fit for local-only daemons
- Standard on Unix/Linux/macOS

**Trade-offs:**
- Not cross-platform (no native Windows support)
- Requires file-based discovery
- No built-in auth (relies on OS)

### 12.2 Why JSON-RPC?

**Rationale:**
- Lightweight, language-agnostic
- Well-defined spec (unlike REST)
- Easy to implement in any language
- Supports notifications (events)

**Trade-offs:**
- No HTTP semantics (status codes)
- Manual error code management
- Less tooling than gRPC

### 12.3 Why SQLite?

**Rationale:**
- Zero-config, serverless
- ACID guarantees
- Fast for local-only workloads
- Easy backups (single file)

**Trade-offs:**
- Single-writer bottleneck
- No built-in replication
- Limited concurrency

### 12.4 Why Go for Daemon?

**Rationale:**
- Excellent concurrency (goroutines)
- Single-binary distribution
- Cross-compilation support
- Fast startup times

**Trade-offs:**
- Verbose error handling
- No generics (until 1.18+)
- GC pauses (mitigated by tuning)

### 12.5 Why Tauri for Desktop?

**Rationale:**
- Smaller binaries than Electron
- Native webview (no Chromium bundle)
- Rust for system integration
- Auto-updater built-in

**Trade-offs:**
- Newer ecosystem (less mature)
- Platform webview inconsistencies
- Rust learning curve

---

## 13. Architecture Smells & Technical Debt

### 13.1 Identified Issues

1. **Monorepo Complexity**
   - Multiple package managers (npm, bun, go)
   - Inconsistent build tooling
   - Circular dependencies between packages
   
2. **State Synchronization**
   - Multiple sources of truth (daemon DB, WUI ElectricSQL)
   - Race conditions on rapid updates
   - Eventual consistency issues
   
3. **Error Handling**
   - Inconsistent error types across layers
   - Generic error messages to users
   - Missing error boundaries in UI
   
4. **Test Coverage**
   - Backend: Good (unit tests exist)
   - Frontend: Sparse (few component tests)
   - E2E: Limited (manual testing)
   
5. **Documentation Drift**
   - Code comments sparse
   - API docs incomplete
   - Architecture diagrams missing

### 13.2 TODO Priority System

**In-code annotations:**
- `TODO(0)`: Critical - never merge
- `TODO(1)`: High - architectural flaws
- `TODO(2)`: Medium - minor bugs
- `TODO(3)`: Low - polish
- `TODO(4)`: Questions/investigations

---

## 14. Deployment Challenges

### 14.1 Multi-Platform Support

**Current State:**
- macOS: Full support (primary target)
- Linux: Partial support (CLI works, WUI experimental)
- Windows: Not supported (Unix sockets limitation)

**Workarounds:**
- Windows: WSL2 + Linux binary
- Future: Consider named pipes for Windows

### 14.2 Auto-Update

- Tauri updater for WUI
- Manual daemon updates (no auto-update)
- Version compatibility checks needed

---

## 15. Future Architecture Considerations

### 15.1 Potential Enhancements

1. **Remote Daemon Support**
   - Run daemon on cloud VM
   - Secure tunnel (SSH/WireGuard)
   - Team collaboration mode
   
2. **Plugin System**
   - Dynamic MCP server registration
   - Custom approval workflows
   - Third-party integrations
   
3. **Multi-Tenancy**
   - Support multiple users per daemon
   - RBAC for approvals
   - Audit logs
   
4. **Distributed Sessions**
   - Horizontal scaling
   - Session migration
   - Load balancing

### 15.2 Performance Optimizations

- Replace SQLite with PostgreSQL (for scale)
- Implement caching layer (Redis)
- gRPC for internal RPC (vs JSON-RPC)
- Protobuf for wire format (vs JSON)

---

## Conclusion

HumanLayer/CodeLayer implements a **sophisticated multi-layer architecture** for orchestrating AI coding agents with human oversight. The system demonstrates strong engineering practices: polyglot architecture leveraging each language's strengths (Go for concurrency, TypeScript for tooling, Rust for system integration), Unix-native IPC patterns, and real-time synchronization. Core innovation lies in the **daemon-coordinated approval workflow** enabling safe AI autonomy with deterministic human gates.

**Architectural Strengths:**
- Clean separation of concerns (4-layer architecture)
- Language-appropriate technology choices
- Real-time event-driven synchronization
- Secure-by-default IPC

**Architectural Challenges:**
- Monorepo complexity across 3 languages
- State synchronization between daemon & UI
- Platform support limitations (Unix-only)
- Test coverage gaps

The pivot from "HumanLayer SDK" (human-in-the-loop API) to "CodeLayer IDE" (full orchestration platform) represents a strategic shift from **library to platform**, targeting 10x productivity gains for developer teams through parallel AI agent coordination.

---

**Next Steps for Investigation:**
- Level 2: Decision Forensics (git history analysis)
- Level 2: Anti-Library (failed approaches, discarded features)
- Level 3: Vision Alignment (stated goals vs implementation)
- Level 4: Paradigm Extraction (mental models & worldview shifts)
