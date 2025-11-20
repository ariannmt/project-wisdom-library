# Hard Architecture Mapping: MCP Code Execution Enhanced

**Date:** 2025-11-20  
**Type:** Level 1 Analysis (Data/Reality)  
**Subject:** mcp-code-execution-enhanced  
**Repository:** https://github.com/yoloshii/mcp-code-execution-enhanced  
**Version:** 3.0.0 (Released Nov 20, 2025)

---

## Executive Summary

**What This System IS:** A Python runtime that implements Anthropic's "Progressive Disclosure" pattern for MCP (Model Context Protocol) tool orchestration, enhanced with a Skills framework achieving 99.6% token reduction, multi-transport support (stdio/SSE/HTTP), and optional container sandboxing. The system merges two prior art projects (ipdelete/mcp-code-execution + elusznik/mcp-server-code-execution-mode) and adds significant architectural innovations.

**Core Innovation:** Skills-as-CLI-Immutable-Templates pattern where agents discover workflows via `ls skills/`, read execution instructions from docstrings, and execute with parameters via command-line arguments—achieving 99.6% token reduction (110 tokens vs 27,300 traditional) and 96% time reduction (5s vs 2min script writing).

**Domain Imperatives:** Token Economy, Context Efficiency, Type Safety, Production Security, Multi-Modal Transport, Lazy Resource Loading

---

## 1. System Profile

### 1.1 Codebase Metrics

```
Total LOC:              ~6,400 Python
Modules:                17 core modules
Git Commits:            5 commits (brand new v3.0.0 release)
Release Date:           November 20, 2025
Python Version:         3.11+ (3.14 not recommended due to anyio issues)
Tests:                  129 comprehensive tests
Technology Stack:       Python, MCP SDK, Pydantic, aiofiles, Docker/Podman
```

### 1.2 Architectural Classification

**Pattern:** Lazy-Loading Orchestration Runtime with Progressive Disclosure  
**Paradigm:** Skills-as-Immutable-CLI-Templates + Multi-Transport MCP Client  
**Architecture Style:** 5-Layer Clean Architecture with State Machine  
**Execution Modes:** Dual-Mode (Direct + Sandboxed)

---

## 2. The Five-Layer Architecture

### Layer 1: **Skills Layer** (Reusable Workflows)
**Purpose:** CLI-based immutable workflow templates for agent execution  
**Location:** `skills/`  
**Key Pattern:** Immutable Logic + Mutable Parameters via CLI

**Structure:**
```
skills/
├── simple_fetch.py           # Basic single-tool pattern (110 tokens)
├── multi_tool_pipeline.py    # Multi-tool chaining pattern
├── README.md                 # Framework guide
└── SKILLS.md                 # Complete system documentation
```

**Skills Architecture:**
- **Immutable Logic:** Workflow code should not be edited to change parameters
- **Mutable Parameters:** All configuration via argparse CLI arguments
- **Self-Documenting:** USAGE section in docstring with CLI examples
- **Discoverable:** Agents use `ls skills/` then `cat skills/<skill>.py`
- **99.6% Token Reduction:** From 27,300 → 110 tokens per execution

**Example Pattern:**
```python
"""
SKILL: Simple Fetch

CLI ARGUMENTS:
    --url    Target URL to fetch (required)

USAGE:
    uv run python -m runtime.harness skills/simple_fetch.py \
        --url "https://example.com"
"""

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    args_to_parse = [arg for arg in sys.argv[1:] if not arg.endswith(".py")]
    return parser.parse_args(args_to_parse)
```

---

### Layer 2: **Runtime Layer** (Execution Harness)
**Purpose:** Dual-mode execution environment with lifecycle management  
**Location:** `src/runtime/`  
**Key Modules:**

#### 2.1 `harness.py` (378 LOC)
**Role:** Main execution entry point with async orchestration

**Responsibilities:**
- Dual-mode execution (direct vs sandboxed)
- PYTHONPATH management for generated wrappers
- Signal handling (SIGTERM, SIGINT)
- MCP client initialization
- Async event loop management
- Error handling and cleanup

**Execution Flow:**
```
1. Parse command (script path + args)
2. Set PYTHONPATH for generated wrappers
3. Initialize MCP client manager
4. Choose execution mode (direct/sandbox)
5. Load and execute Python module
6. Handle cleanup and signals
```

#### 2.2 `mcp_client.py` (400+ LOC)
**Role:** State machine-based lazy-loading MCP client manager

**State Machine:**
```
UNINITIALIZED → INITIALIZED → CONNECTED
     ↑              ↓              ↓
     └──────────── cleanup() ──────┘
```

**States:**
- `UNINITIALIZED`: Manager created, no config loaded
- `INITIALIZED`: Config loaded, servers NOT connected
- `CONNECTED`: At least one server connection established

**Key Methods:**
- `initialize()`: Load config, transition to INITIALIZED (NO connections)
- `call_tool()`: Lazy connect on first call, transition to CONNECTED
- `_connect_to_server()`: Establish connection based on transport type
- `cleanup()`: Close all connections, return to UNINITIALIZED

**Lazy Loading Benefits:**
- Servers connect only when tools are actually called
- Faster startup (no upfront connection overhead)
- Resource efficiency (unused servers never connect)

#### 2.3 `config.py` (150+ LOC)
**Role:** Pydantic-based configuration validation

**Models:**
- `ServerConfig`: Multi-transport server configuration
  - stdio: command, args, env
  - sse: url, headers
  - http: url, headers
- `SandboxConfig`: Container execution settings
- `McpConfig`: Top-level configuration wrapper

**Validation Features:**
- Transport-specific field validation
- Required field enforcement per transport type
- Type coercion and defaults
- Error messages with context

---

### Layer 3: **Code Generation Layer** (Auto-Generated Wrappers)
**Purpose:** Generate type-safe Python wrappers from MCP tool schemas  
**Location:** `servers/` (gitignored, regenerated on demand)

#### 3.1 `generate_wrappers.py` (350+ LOC)
**Role:** Connect to all MCP servers, introspect schemas, generate typed wrappers

**Generation Process:**
```
1. Load mcp_config.json
2. Connect to each server (stdio/SSE/HTTP)
3. Call list_tools() to get tool schemas
4. Generate for each tool:
   - Pydantic models for input parameters
   - Async wrapper function
   - Type hints and documentation
5. Generate __init__.py barrel exports
6. Write to servers/<server_name>/<tool_name>.py
```

**Generated Structure:**
```
servers/
├── <server_name>/
│   ├── __init__.py              # Barrel exports
│   ├── <tool_name>.py           # Pydantic input model + async wrapper
│   ├── discovered_types.py      # Optional: Real API response types
│   └── ...
```

**Key Features:**
- Multi-transport support (stdio, SSE, HTTP)
- Type-safe Pydantic input models
- Async/await wrapper functions
- Defensive unwrapping (handles `response.value` variations)
- Tool name format: `serverName__toolName`

#### 3.2 `discover_schemas.py` (250+ LOC)
**Role:** Execute safe read-only tools to infer actual response schemas

**Discovery Process:**
```
1. Load discovery_config.json (tool → test params mapping)
2. Connect to servers
3. Execute safe tools with test parameters
4. Capture actual API responses
5. Generate Pydantic models from responses
6. Write to servers/<server>/discovered_types.py
```

**Benefits:**
- Real-world API response types (not just documentation)
- Handles inconsistent API behavior
- Provides fallback types for defensive coding

#### 3.3 `normalize_fields.py` (150+ LOC)
**Role:** Auto-convert inconsistent API field casing

**Problem:** Some APIs (e.g., Azure DevOps) use inconsistent casing:
- Documented: `system.parent`
- Actual: `System.Parent`

**Solution:** Normalization layer that auto-converts field names on-the-fly

---

### Layer 4: **Transport Layer** (Multi-Modal MCP Connections)
**Purpose:** Support multiple MCP transport protocols  
**Implementation:** In `mcp_client.py` via MCP SDK

**Supported Transports:**

#### 4.1 STDIO (Process-based)
```json
{
  "type": "stdio",
  "command": "uvx",
  "args": ["mcp-server-git"],
  "env": {"API_KEY": "key"}
}
```
- Local process spawning
- stdin/stdout communication
- Environment variable injection

#### 4.2 SSE (Server-Sent Events)
```json
{
  "type": "sse",
  "url": "https://mcp.example.com/sse",
  "headers": {"Authorization": "Bearer KEY"}
}
```
- Remote server connections
- Streaming updates
- HTTP header authentication

#### 4.3 HTTP (Streamable HTTP)
```json
{
  "type": "http",
  "url": "https://mcp.example.com/mcp",
  "headers": {"x-api-key": "KEY"}
}
```
- RESTful MCP interactions
- Standard HTTP semantics
- Header-based auth

**Unified Interface:** All transports expose identical `ClientSession` API

---

### Layer 5: **Sandbox Layer** (Optional Security Isolation)
**Purpose:** Container-based code execution isolation  
**Location:** `src/runtime/sandbox/`  
**LOC:** 533 lines

#### 5.1 `container.py` (369 LOC)
**Role:** Rootless container orchestration

**Features:**
- Auto-detect runtime (Docker/Podman)
- Rootless execution (no privileged mode)
- Memory and CPU limits
- Network isolation
- Temporary workspace binding
- Execution timeout enforcement

**Container Lifecycle:**
```
1. Detect available runtime (docker/podman)
2. Pull image if needed
3. Create container with security constraints
4. Bind workspace volume (read-write)
5. Execute Python script
6. Stream output
7. Enforce timeout
8. Cleanup container
```

#### 5.2 `security.py` (133 LOC)
**Role:** Security policy enforcement

**Controls:**
- Resource limits (memory, CPU)
- Network policies (isolated by default)
- Filesystem access restrictions
- Execution timeout bounds
- Rootless enforcement

#### 5.3 `exceptions.py` (31 LOC)
**Role:** Sandbox-specific error types

**Exception Hierarchy:**
- `SandboxError` (base)
- `SandboxRuntimeError` (runtime not found)
- `SandboxExecutionError` (execution failure)
- `SandboxTimeoutError` (timeout exceeded)

---

## 3. Key Architectural Patterns

### 3.1 Progressive Disclosure Pattern

**Anthropic's Definition:** Load tool schemas only when needed, not upfront.

**Implementation:**
```
Phase 1: Discovery
- Agent: ls ./skills/
- Result: List of available workflow files

Phase 2: Introspection
- Agent: cat ./skills/simple_fetch.py
- Result: USAGE docstring with CLI arguments (110 tokens)

Phase 3: Execution
- Agent: uv run python -m runtime.harness skills/simple_fetch.py --url "..."
- Result: Execute workflow with parameters
```

**Token Comparison:**
- **Traditional (Load All):** 27,300 tokens (all tool schemas upfront)
- **Skills (Progressive):** 110 tokens (USAGE docstring only)
- **Reduction:** 99.6%

### 3.2 Lazy Loading Pattern

**Server Connections:**
- `initialize()`: Load config only, NO server connections
- `call_tool()`: Connect to server on first tool call
- Cache tools per server to avoid repeated `list_tools()` calls

**Benefits:**
- Faster startup (no upfront connection cost)
- Resource efficiency (unused servers never connect)
- Failure isolation (bad server configs don't break startup)

### 3.3 Dual-Mode Execution Pattern

**Direct Mode (Development):**
- Fast execution (no container overhead)
- Full system access
- Live code editing
- Ideal for: Development, testing, debugging

**Sandbox Mode (Production):**
- Secure isolation (container boundaries)
- Limited resources (memory, CPU, timeout)
- Network isolation
- Rootless execution
- Ideal for: Production, untrusted code, multi-tenant

**Mode Selection:**
```bash
# Direct mode (default)
uv run mcp-exec script.py

# Sandbox mode (--sandbox flag)
uv run mcp-exec script.py --sandbox
```

### 3.4 Type Safety Pattern

**Pydantic Everywhere:**
- Configuration: `ServerConfig`, `SandboxConfig`, `McpConfig`
- Tool Inputs: Auto-generated Pydantic models per tool
- Validation: Automatic field validation and type coercion
- Error Messages: Rich context from Pydantic validation errors

**Benefits:**
- Compile-time safety (mypy static checking)
- Runtime validation (Pydantic enforcement)
- Better error messages (field-level context)
- Self-documenting (models serve as documentation)

### 3.5 CLI-Immutable-Template Pattern (Skills)

**Problem:** Editing files to change parameters wastes tokens and time

**Solution:** Skills as CLI-based templates
- Logic is immutable (edit for bug fixes, not parameters)
- Parameters are mutable (change via CLI args)
- Discovery via filesystem (`ls`, `cat`)
- Execution via harness + args

**Pattern:**
```python
# DON'T do this (editing file to change URL):
url = "https://old-url.com"  # Change this line = file edit = tokens

# DO this (CLI argument):
parser.add_argument("--url", required=True)  # Change via CLI = no file edit
```

---

## 4. Data Flow Architecture

### 4.1 Skills Execution Flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Agent Discovery                                          │
│    Agent: ls ./skills/                                      │
│    System: Returns list of .py files                        │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. Agent Introspection                                      │
│    Agent: cat ./skills/simple_fetch.py                      │
│    System: Returns USAGE docstring (110 tokens)             │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. Runtime Harness Initialization                           │
│    Command: uv run python -m runtime.harness                │
│             skills/simple_fetch.py --url "..."              │
│                                                              │
│    Harness Actions:                                         │
│    - Set PYTHONPATH for generated wrappers                  │
│    - Initialize MCP client manager (UNINITIALIZED →         │
│      INITIALIZED)                                           │
│    - Parse CLI arguments from sys.argv                      │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. Skill Execution                                          │
│    - Import skill module dynamically                        │
│    - Call skill's main() async function                     │
│    - Skill calls MCP tools via generated wrappers           │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. Lazy MCP Connection (First Tool Call)                   │
│    - call_tool("serverName__toolName", params)              │
│    - Check if server connected                              │
│    - If not: _connect_to_server() (INITIALIZED →           │
│      CONNECTED)                                             │
│    - Cache tools from list_tools()                          │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 6. Tool Execution                                           │
│    - Find tool in cache                                     │
│    - Call session.call_tool()                               │
│    - Defensive unwrapping of response.value                 │
│    - Return result to skill                                 │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 7. Cleanup                                                  │
│    - Skill completes                                        │
│    - Harness cleanup()                                      │
│    - Close all MCP connections (CONNECTED →                │
│      UNINITIALIZED)                                         │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Wrapper Generation Flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Command: uv run mcp-generate                            │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. Load mcp_config.json                                     │
│    - Parse configuration                                    │
│    - Validate via Pydantic models                           │
│    - Filter disabled servers                                │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. For Each Server: Connect                                 │
│    - Detect transport type (stdio/sse/http)                 │
│    - Establish connection via MCP SDK                       │
│    - Initialize ClientSession                               │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. For Each Server: Introspect                              │
│    - Call session.list_tools()                              │
│    - Parse tool schemas (name, description, parameters)     │
│    - Extract JSON Schema for input parameters               │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. For Each Tool: Generate Wrapper                          │
│    - Create Pydantic model from JSON Schema                 │
│    - Generate async wrapper function                        │
│    - Add defensive unwrapping logic                         │
│    - Add type hints and docstrings                          │
│    - Write to servers/<server>/<tool>.py                    │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 6. Generate Barrel Exports                                  │
│    - Create servers/<server>/__init__.py                    │
│    - Import all tool wrappers                               │
│    - Re-export for clean imports                            │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 7. Cleanup Connections                                      │
│    - Close all MCP sessions                                 │
│    - Report generation summary                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Technology Stack

### 5.1 Core Dependencies

**Runtime:**
- `mcp>=1.0.0`: Model Context Protocol SDK
- `pydantic>=2.0.0`: Type validation and serialization
- `aiofiles>=23.0.0`: Async file I/O
- Python 3.11+ (3.14 not recommended)

**Development:**
- `black`: Code formatting
- `mypy`: Static type checking (strict mode)
- `ruff`: Fast linting
- `pytest>=8.0.0`: Testing framework
- `pytest-asyncio`: Async test support

**Optional:**
- `anthropic>=0.28.0`: For LLM-assisted test parameter generation
- Docker or Podman: For sandbox execution

### 5.2 Project Tooling

**Package Manager:** uv (fast Rust-based Python package manager)

**Scripts (pyproject.toml):**
- `mcp-exec`: Execute skills/scripts (`runtime.harness:main`)
- `mcp-generate`: Generate wrappers (`runtime.generate_wrappers:main`)
- `mcp-generate-discovery`: Generate test params with LLM
- `mcp-discover`: Execute safe tools and infer schemas

**Quality Checks:**
```bash
uv run mypy src/           # Type checking (strict)
uv run black src/ tests/   # Formatting
uv run ruff check src/     # Linting
uv run pytest              # 129 tests
```

---

## 6. Configuration Architecture

### 6.1 Primary Configuration: `mcp_config.json`

**Location:** Project root  
**Purpose:** Define MCP servers and sandbox settings

**Structure:**
```json
{
  "mcpServers": {
    "server_name": {
      "type": "stdio|sse|http",
      "command": "...",     // stdio only
      "args": [...],        // stdio only
      "env": {...},         // stdio only
      "url": "...",         // sse/http only
      "headers": {...},     // sse/http only
      "disabled": false
    }
  },
  "sandbox": {
    "enabled": false,
    "runtime": "auto|docker|podman",
    "image": "python:3.11-slim",
    "memory_limit": "512m",
    "cpu_limit": "1.0",
    "timeout": 30,
    "max_timeout": 120
  }
}
```

**Validation:** All fields validated by Pydantic models in `config.py`

### 6.2 Discovery Configuration: `discovery_config.json`

**Purpose:** Map tools to test parameters for schema discovery

**Structure:**
```json
{
  "server_name__tool_name": {
    "param1": "test_value",
    "param2": 123
  }
}
```

**Usage:**
```bash
uv run mcp-discover  # Execute safe tools, capture responses
```

### 6.3 Separation from Claude Code Configuration

**Important:** This project uses its own `mcp_config.json`, separate from Claude Code's global `~/.claude.json`.

**Conflict Avoidance:**
- Use different servers in each config, OR
- Disable overlapping servers in `~/.claude.json`

---

## 7. Security Architecture (Sandbox Layer)

### 7.1 Threat Model

**Threats Addressed:**
- Arbitrary code execution
- Resource exhaustion (memory, CPU)
- Network exfiltration
- Filesystem tampering
- Privilege escalation

### 7.2 Security Controls

**Container Isolation:**
- Rootless execution (no privileged mode)
- Network isolation (no network access by default)
- Filesystem isolation (workspace volume only)
- Resource limits (configurable memory/CPU)
- Execution timeout (prevents infinite loops)

**Default Settings:**
- Memory: 512MB (configurable)
- CPU: 1.0 core (configurable)
- Timeout: 30s (max 120s)
- Network: Disabled
- User: Non-root

### 7.3 Sandbox Modes

**Direct Mode (No Sandbox):**
- Fast (no container overhead)
- Full system access
- For: Development, trusted code

**Sandbox Mode (Containerized):**
- Slower (container startup ~2-3s)
- Isolated execution
- For: Production, untrusted code

**Mode Selection:**
```python
# In mcp_config.json
{
  "sandbox": {
    "enabled": true  # Enable sandbox globally
  }
}

# Or via CLI flag
uv run mcp-exec script.py --sandbox
```

---

## 8. Testing Architecture

### 8.1 Test Organization

**Location:** `tests/`  
**Total Tests:** 129  
**Coverage:** Comprehensive (all features)

**Structure:**
```
tests/
├── unit/              # Unit tests for individual modules
├── integration/       # Integration tests for workflows
├── sandbox/           # Sandbox-specific tests
└── fixtures/          # Test data and mocks
```

### 8.2 Test Categories

**Unit Tests:**
- Configuration validation
- MCP client state machine
- Wrapper generation logic
- Field normalization
- Error handling

**Integration Tests:**
- End-to-end skill execution
- Multi-tool workflows
- Sandbox execution
- Multi-transport connections

**Async Testing:**
- `pytest-asyncio` for async test support
- `asyncio_mode = "auto"` for automatic event loop management

---

## 9. Prior Art Integration

This project merges and enhances two existing MCP code execution approaches:

### 9.1 From `ipdelete/mcp-code-execution` (PRIMARY)

**Adopted:**
- ✅ Filesystem-based progressive disclosure
- ✅ Type-safe Pydantic wrappers
- ✅ Lazy server connections
- ✅ Schema discovery system
- ✅ 98.7% token reduction (script writing pattern)

**Pattern:** Write Python scripts that import MCP tools as typed functions

### 9.2 From `elusznik/mcp-server-code-execution-mode` (BRIDGE)

**Adopted:**
- ✅ Container sandboxing architecture
- ✅ Security controls and policies
- ✅ Production deployment patterns
- ✅ Resource isolation

**Pattern:** Execute MCP tools in isolated containers

### 9.3 Enhanced in This Project

**Novel Contributions:**
- ⭐ **Skills System:** CLI-based immutable templates (99.6% reduction)
- ⭐ **Multi-Transport:** stdio + SSE + HTTP support (100% server coverage)
- ⭐ **Dual-Mode:** Direct (fast) + Sandbox (secure) execution
- ⭐ **Python 3.11 Stable:** Avoiding 3.14 anyio compatibility issues
- ⭐ **Comprehensive Testing:** 129 tests covering all features
- ⭐ **Enhanced Documentation:** Complete guides for all features

---

## 10. File System Organization

### 10.1 Repository Structure

```
mcp-code-execution-enhanced/
├── src/
│   ├── mcp_execution/        # Package marker
│   ├── runtime/              # Core runtime modules
│   │   ├── config.py         # Configuration models
│   │   ├── mcp_client.py     # MCP client manager
│   │   ├── harness.py        # Execution harness
│   │   ├── generate_wrappers.py
│   │   ├── discover_schemas.py
│   │   ├── normalize_fields.py
│   │   ├── schema_utils.py
│   │   ├── schema_inference.py
│   │   ├── exceptions.py
│   │   └── sandbox/          # Sandbox subsystem
│   │       ├── container.py
│   │       ├── security.py
│   │       └── exceptions.py
│   └── prompts/              # LLM prompts for code generation
│
├── skills/                   # Skills framework
│   ├── simple_fetch.py       # Basic skill example
│   ├── multi_tool_pipeline.py
│   ├── README.md
│   └── SKILLS.md
│
├── examples/                 # Advanced examples
│   └── skills/               # 8 advanced workflow examples
│
├── servers/                  # Auto-generated (gitignored)
│   └── <server_name>/
│       ├── __init__.py
│       ├── <tool_name>.py
│       └── discovered_types.py
│
├── tests/                    # 129 comprehensive tests
│   ├── unit/
│   ├── integration/
│   └── sandbox/
│
├── docs/                     # Extended documentation
├── workspace/                # User scripts (gitignored)
│
├── mcp_config.json           # Primary configuration
├── discovery_config.json     # Schema discovery config
├── pyproject.toml            # Project metadata
├── uv.lock                   # Dependency lock file
│
├── README.md                 # Main documentation
├── CLAUDE.md                 # Claude Code operational guide
├── AGENTS.md.template        # Template for agent-specific guides
├── CONTRIBUTING.md
├── SECURITY.md
├── CHANGELOG.md
└── LICENSE
```

### 10.2 Generated Artifacts (Gitignored)

**`servers/` Directory:**
- Auto-generated by `uv run mcp-generate`
- Should NOT be committed to git
- Regenerated from `mcp_config.json` on setup
- Contains type-safe Python wrappers for MCP tools

**`workspace/` Directory:**
- User-created scripts
- Gitignored by default
- For experimentation and custom workflows

---

## 11. Key Innovations Summary

### 11.1 Skills-as-Immutable-CLI-Templates

**Innovation:** Workflows are templates executed with CLI args, not files edited per use

**Impact:**
- 99.6% token reduction (27,300 → 110)
- 96% time reduction (120s → 5s)
- Reusability across queries
- Immutable logic, mutable parameters

### 11.2 Multi-Transport MCP Support

**Innovation:** Single codebase supports stdio, SSE, and HTTP transports

**Impact:**
- 100% MCP server coverage
- Unified configuration format
- Automatic transport detection
- Seamless remote/local mixing

### 11.3 Dual-Mode Security Architecture

**Innovation:** Same code, two execution modes (direct/sandboxed)

**Impact:**
- Fast development (direct mode)
- Secure production (sandbox mode)
- Runtime mode selection
- No code duplication

### 11.4 Lazy Loading State Machine

**Innovation:** Explicit state machine for MCP client lifecycle

**Impact:**
- Faster startup (no upfront connections)
- Resource efficiency (unused servers never connect)
- Clear error messages (state validation)
- Debuggable lifecycle

### 11.5 Type Safety Throughout

**Innovation:** Pydantic models for configuration, inputs, and discovered schemas

**Impact:**
- Compile-time checks (mypy)
- Runtime validation (Pydantic)
- Better error messages
- Self-documenting code

---

## 12. Design Decisions & Trade-offs

### 12.1 Python 3.11 vs 3.14

**Decision:** Require Python 3.11+, recommend AGAINST 3.14

**Rationale:**
- anyio <4.9.0 has breaking changes in Python 3.14
- MCP SDK dependencies not yet compatible
- 3.11 is stable and well-tested

**Trade-off:** Miss 3.14 features, gain stability

### 12.2 Skills as Framework vs Library

**Decision:** Provide 2 generic examples, not opinionated workflows

**Rationale:**
- Skills are MCP server-specific
- Users have different server configs
- Framework > library for extensibility

**Trade-off:** Less "batteries included," more flexibility

### 12.3 Separate `mcp_config.json` vs Global Config

**Decision:** Project-local config, separate from Claude Code global config

**Rationale:**
- Avoid conflicts with Claude Code's config
- Project-specific server configurations
- Explicit over implicit

**Trade-off:** Duplication possible, clarity gained

### 12.4 Optional Sandbox vs Always Sandboxed

**Decision:** Sandbox is optional, not mandatory

**Rationale:**
- Development needs speed (direct mode)
- Production needs security (sandbox mode)
- Runtime context determines needs

**Trade-off:** Security not enforced by default, flexibility gained

### 12.5 Lazy Loading vs Eager Connection

**Decision:** Lazy loading (connect on first use)

**Rationale:**
- Faster startup
- Resource efficiency
- Failure isolation

**Trade-off:** First call slower, overall better UX

---

## 13. Future Architecture Extensibility

### 13.1 Transport Extensibility

**Current:** stdio, SSE, HTTP via MCP SDK

**Future Potential:**
- WebSocket transport
- gRPC transport
- Custom transport adapters

**Hook:** `_connect_to_server()` method in `mcp_client.py`

### 13.2 Sandbox Runtime Extensibility

**Current:** Docker, Podman (rootless)

**Future Potential:**
- Kubernetes pods
- AWS Lambda
- Cloud Run
- Firecracker microVMs

**Hook:** `SandboxExecutor` in `sandbox/container.py`

### 13.3 Code Generation Extensibility

**Current:** Python Pydantic wrappers

**Future Potential:**
- TypeScript wrappers
- Go wrappers
- OpenAPI schema generation

**Hook:** `generate_wrappers.py` templating logic

---

## Appendix A: Efficiency Metrics

### Token Reduction Comparison

| Approach | Tokens | Time | Use Case |
|----------|--------|------|----------|
| **Traditional (Load All)** | 27,300 | N/A | All tool schemas upfront |
| **Script Writing (ipdelete)** | 2,000 | 2 min | Novel workflows |
| **Skills (Enhanced)** | **110** | **5 sec** | Multi-step workflows (PREFERRED) |

**Skills Reduction:** 99.6% vs traditional (27,300 → 110)  
**Time Reduction:** 96% vs scripts (120s → 5s)

### Feature Comparison

| Feature | ipdelete (Original) | elusznik (Bridge) | Enhanced (This) |
|---------|---------------------|-------------------|-----------------|
| **Progressive Disclosure** | ✅ PRIMARY | ⚠️ ALTERNATIVE | ✅ PRIMARY |
| **Token Reduction** | 98.7% | ~95% | **99.6%** |
| **Type Safety** | ✅ Pydantic | ⚠️ Basic | ✅ Enhanced |
| **Sandboxing** | ❌ None | ✅ Required | ✅ Optional |
| **Multi-Transport** | ❌ stdio only | ❌ stdio only | ✅ stdio/SSE/HTTP |
| **Skills Framework** | ❌ None | ❌ None | ✅ CLI-based |
| **Test Coverage** | ⚠️ Partial | ⚠️ Partial | ✅ Comprehensive (129) |
| **Python Version** | ✅ 3.11+ | ⚠️ 3.12+ | ✅ 3.11 Stable |

---

## Appendix B: State Machine Diagram

### MCP Client Manager States

```
┌─────────────────┐
│ UNINITIALIZED   │ ← Manager created
└────────┬────────┘
         │
         │ initialize()
         │ (load config)
         ↓
┌─────────────────┐
│  INITIALIZED    │ ← Config loaded, no connections
└────────┬────────┘
         │
         │ call_tool() → _connect_to_server()
         │ (first tool call)
         ↓
┌─────────────────┐
│   CONNECTED     │ ← At least one server connected
└────────┬────────┘
         │
         │ cleanup()
         │ (close all connections)
         ↓
┌─────────────────┐
│ UNINITIALIZED   │ ← Back to initial state
└─────────────────┘
```

**State Validation:** All methods validate state before executing to prevent invalid transitions.

---

## Appendix C: CLI Commands Reference

### Primary Commands

```bash
# Generate wrappers from mcp_config.json
uv run mcp-generate

# Generate discovery config with LLM assistance
uv run mcp-generate-discovery

# Execute safe tools and infer schemas
uv run mcp-discover

# Execute a skill with CLI arguments
uv run mcp-exec skills/simple_fetch.py --url "https://example.com"

# Execute in sandbox mode
uv run mcp-exec skills/simple_fetch.py --url "..." --sandbox

# Execute a custom script
uv run mcp-exec workspace/my_script.py
```

### Development Commands

```bash
# Type checking
uv run mypy src/

# Code formatting
uv run black src/ tests/

# Linting
uv run ruff check src/ tests/

# Run tests
uv run pytest

# Install dependencies
uv sync
uv sync --all-extras  # Include dev dependencies
```

---

## Conclusion: Architectural Assessment

**Strengths:**
1. ✅ **Token Economy Champion:** 99.6% reduction is industry-leading
2. ✅ **Multi-Transport Leadership:** Only MCP runtime with stdio/SSE/HTTP
3. ✅ **Dual-Mode Flexibility:** Direct/sandbox covers dev and prod
4. ✅ **Type Safety Rigor:** Pydantic throughout, strict mypy
5. ✅ **Clear State Machine:** Debuggable lifecycle management
6. ✅ **Comprehensive Testing:** 129 tests, good coverage
7. ✅ **Excellent Documentation:** README, CLAUDE.md, SECURITY.md, examples

**Weaknesses:**
1. ⚠️ **Brand New (v3.0.0):** Only 5 commits, just released today
2. ⚠️ **Limited Field Testing:** No production battle scars yet
3. ⚠️ **Python 3.14 Incompatibility:** Blocks adoption of latest Python
4. ⚠️ **Skills Library Minimal:** Only 2 generic examples provided
5. ⚠️ **Sandbox Overhead:** 2-3s container startup latency

**Architectural Maturity:** 🌟🌟🌟🌟 (4/5)
- Solid design patterns
- Clear separation of concerns
- Extensibility hooks present
- Needs field validation

**Innovation Level:** 🚀🚀🚀🚀🚀 (5/5)
- Skills-as-Immutable-CLI-Templates is novel
- Multi-transport in single codebase is rare
- Dual-mode architecture is elegant
- State machine clarity is exemplary

**Recommendation:** High potential project with excellent architecture. Needs field testing and community contribution to realize full potential. Skills framework is transformative if adopted by Claude Code ecosystem.

---

**Analysis Complete:** 2025-11-20  
**Analyst:** GitHub Copilot (System Owner)  
**Next Steps:** Level 2 Decision Forensics + Anti-Library Extraction
