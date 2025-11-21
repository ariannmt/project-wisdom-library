# Hard Architecture Mapping: Agent Control Plane (ACP)

**Date:** 2025-11-20  
**Level:** 1 (Data & Reality)  
**Methodology:** Hard Architecture Mapping  
**Target:** https://github.com/humanlayer/agentcontrolplane  
**Codebase Size:** ~32,000 lines of Go code  

---

## Executive Summary

Agent Control Plane (ACP) is a **Kubernetes-native orchestrator for AI Agents** built as a Kubernetes Operator using the controller-runtime pattern. The system implements **durable, asynchronous agent execution** by checkpointing conversation state at every tool call, enabling reliable long-running agentic workflows that survive failures, incorporate human feedback, and delegate work across distributed systems.

**Core Paradigm:** The entire agent "call stack" is expressed as a rolling context window—no separate execution state required. This is **Infrastructure-as-Conversations**: Kubernetes etcd becomes the durable message queue, and CRDs become the API for orchestrating AI conversations.

---

## 1. Core Architecture Pattern: Kubernetes Operator

### 1.1 Operator Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Kubernetes API Server                     │
│                         (etcd)                               │
└────────────────┬────────────────────────────────────────────┘
                 │
                 │ Watch & Reconcile
                 ▼
┌─────────────────────────────────────────────────────────────┐
│              ACP Operator (Controller Manager)               │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │     LLM      │  │    Agent     │  │     Task     │     │
│  │  Controller  │  │  Controller  │  │  Controller  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   ToolCall   │  │  MCPServer   │  │ContactChannel│     │
│  │  Controller  │  │  Controller  │  │  Controller  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                 │
                 │ Call External Services
                 ▼
┌─────────────────────────────────────────────────────────────┐
│        ┌─────────────┐   ┌─────────────┐                   │
│        │  LLM APIs   │   │  MCP Tools  │                   │
│        │ (OpenAI,    │   │  (stdio/    │                   │
│        │  Anthropic) │   │   http)     │                   │
│        └─────────────┘   └─────────────┘                   │
│        ┌─────────────────────────────────┐                 │
│        │      HumanLayer API             │                 │
│        │  (Human Approval/Input)         │                 │
│        └─────────────────────────────────┘                 │
└─────────────────────────────────────────────────────────────┘
```

**Design Principles:**
- **Kubernetes-Native**: Everything is a CRD (Custom Resource Definition)
- **Declarative**: Desired state vs. current state reconciliation
- **Observable**: All state changes emit Kubernetes Events
- **Durable**: State persisted in etcd, survives pod restarts
- **Scalable**: Multiple controller replicas with distributed locking

---

## 2. Custom Resource Definitions (CRDs)

### 2.1 Core CRDs Overview

| CRD | Purpose | Key Fields | Status States |
|-----|---------|-----------|---------------|
| **LLM** | LLM provider configuration | `provider`, `model`, `apiKeyFrom`, `parameters` | Ready, Error, Pending |
| **Agent** | Agent definition | `llmRef`, `system`, `mcpServers`, `subAgents` | Ready, Error, Pending |
| **Task** | Conversation instance | `agentRef`, `userMessage`, `contextWindow` | Initializing, SendingToLLM, ToolCallsPending, FinalAnswer, Error |
| **ToolCall** | Tool execution unit | `taskRef`, `toolRef`, `arguments`, `result` | Pending, Executing, AwaitingHumanApproval, Succeeded, Failed |
| **MCPServer** | MCP tool server | `transport`, `command`, `args`, `url` | Ready, Error, Connecting |
| **ContactChannel** | Human contact channel | `type`, `slack`/`email`, `apiKeyFrom` | Ready, Error, Validating |

### 2.2 Resource Dependency Graph

```
┌─────────┐
│ Secret  │────────┐
└─────────┘        │
                   │ apiKeyFrom
                   ▼
              ┌─────────┐
              │   LLM   │
              └─────────┘
                   │ llmRef
                   ▼
              ┌─────────┐          ┌──────────────┐
              │  Agent  │◄─────────│  MCPServer   │
              └─────────┘ mcpServers└──────────────┘
                   │                ┌──────────────────┐
                   │ subAgents      │ ContactChannel   │
                   │◄───────────────┴──────────────────┘
                   │ humanContactChannels
                   │ agentRef
                   ▼
              ┌─────────┐
              │  Task   │
              └─────────┘
                   │ taskRef
                   ▼
              ┌─────────┐
              │ToolCall │
              └─────────┘
```

---

## 3. Feature/Functionality/Capability Matrices

### 3.1 LLM Provider Support Matrix

| Provider | Status | Auth Method | Parameters | Special Features |
|----------|--------|-------------|------------|------------------|
| **OpenAI** | ✅ Alpha | API Key | `model`, `temperature`, `maxTokens`, `topP`, `frequencyPenalty`, `presencePenalty` | Organization ID, Azure support (OPEN_AI/AZURE/AZURE_AD) |
| **Anthropic** | ✅ Alpha | API Key | `model`, `temperature`, `maxTokens`, `topP`, `topK` | `anthropicBetaHeader` for extended features |
| **Vertex AI** | ✅ Alpha | GCP Credentials | `model`, `temperature`, `maxTokens`, `topP`, `topK` | `cloudProject`, `cloudLocation` |
| **Mistral AI** | ✅ Alpha | API Key | `model`, `temperature`, `maxTokens`, `topP` | Standard parameters |

**Validation:** All providers support API key validation on LLM resource creation.

### 3.2 MCP (Model Context Protocol) Integration Matrix

| Feature | Stdio | HTTP | Status |
|---------|-------|------|--------|
| **Transport** | ✅ | ✅ | Alpha |
| **Tool Discovery** | ✅ | ✅ | Alpha |
| **Tool Execution** | ✅ | ✅ | Alpha |
| **Environment Variables** | ✅ | N/A | Alpha |
| **Secret Injection** | ✅ (via `secretKeyRef`) | ✅ | Alpha |
| **Resource Limits** | ✅ (CPU/Memory) | N/A | Alpha |
| **Approval Workflow** | ✅ | ✅ | Alpha |
| **Connection Pooling** | ❌ | 🗺️ Planned | - |
| **Better Scheduling** | 🗺️ Planned | 🗺️ Planned | - |

**Example MCP Servers Tested:**
- `mcp-server-fetch` (stdio): Web content fetching
- Custom HTTP MCP servers

### 3.3 Human-in-the-Loop Capabilities Matrix

| Capability | Approval | Human-as-Tool | Channel Types | Status |
|------------|----------|---------------|---------------|--------|
| **Request Human Approval** | ✅ | N/A | Slack, Email | Alpha |
| **Request Human Input** | N/A | ✅ | Slack, Email | ✅ Alpha |
| **Tiered Approval** (once/task/always) | 🗺️ Planned | N/A | - | Planned |
| **Channel Context** | ✅ | ✅ | All | Alpha |
| **Allowed Responders** | ✅ (Slack) | ✅ (Slack) | Slack | Alpha |
| **Custom Subject** | ✅ | ✅ | Email | Alpha |
| **Thread Continuity** | ✅ (v1beta3) | ✅ (v1beta3) | All | Alpha |

**HumanLayer Integration:**
- External service: `humanlayer.dev`
- API version: v1beta3 (with `thread_id` support)
- Authentication: Per-project or per-channel API keys

### 3.4 Agent Composition & Delegation Matrix

| Feature | Capability | Implementation | Status |
|---------|-----------|----------------|--------|
| **Sub-Agent References** | Agent can reference other Agents | `spec.subAgents[]` | ✅ Alpha |
| **Delegate Tool** | LLM can call `delegate__<agent-name>` | Auto-generated tool per sub-agent | 🚧 In Progress |
| **Parent-Child Task Linking** | Delegation creates child Task | `spec.parentTaskRef` | 🚧 In Progress |
| **Agent Description** | Context for delegation | `spec.description` | ✅ Alpha |
| **Recursive Delegation** | Sub-agents can have sub-agents | Supported by design | ✅ Alpha |

### 3.5 Task Execution Lifecycle Matrix

| Phase | Description | Trigger | Next States | Observable Via |
|-------|-------------|---------|-------------|----------------|
| **Initializing** | Validation & setup | Task created | SendingToLLM, Error | Event: ValidationSucceeded |
| **SendingToLLM** | Sending context window | Validation passed or tools completed | ToolCallsPending, FinalAnswer, Error | Event: SendingContextWindowToLLM |
| **ToolCallsPending** | LLM requested tool calls | LLM response with tool_calls | Executing (per ToolCall) | Event: ToolCallCreated |
| **Executing** | Tools running | ToolCall created | AwaitingHumanApproval, Succeeded, Failed | ToolCall Status |
| **AwaitingHumanApproval** | Waiting for human | Approval required | Succeeded, Failed | Event: AwaitingHumanApproval |
| **FinalAnswer** | LLM provided answer | LLM response without tool_calls | (Terminal) | Event: LLMFinalAnswer |
| **Error** | Failure occurred | Any error | (Terminal) | Event: Error, status.statusDetail |

**Key Insight:** Each phase transition is observable via Kubernetes Events, enabling real-time debugging.

### 3.6 Observability & Telemetry Matrix

| Feature | Implementation | Status | Details |
|---------|----------------|--------|---------|
| **OpenTelemetry Traces** | 🚧 In Progress | Partial | Trace & Span IDs in Task.status.spanContext |
| **OpenTelemetry Logs** | 🗺️ Planned | - | - |
| **OpenTelemetry Metrics** | 🗺️ Planned | - | - |
| **Token Counts in Traces** | 🗺️ Planned | - | LLM usage tracking |
| **Kubernetes Events** | ✅ Alpha | Complete | All state transitions emit events |
| **Status Fields** | ✅ Alpha | Complete | `ready`, `status`, `statusDetail` on all CRDs |
| **Context Window Inspection** | ✅ Alpha | Complete | Full conversation in `status.contextWindow` |
| **Grafana + Tempo** | ✅ Alpha | Example | `acp-example/otel/` |

**Observability Stack (acp-example):**
- Grafana (visualization)
- Tempo (distributed tracing)
- Loki (log aggregation)
- Prometheus (metrics)

---

## 4. Technical Architecture Layers

### 4.1 Layer 1: Kubernetes Foundation

**Technologies:**
- Go 1.21+
- Kubebuilder v3 (Operator framework)
- controller-runtime (reconciliation engine)
- Kubernetes API Machinery

**Key Patterns:**
- **State Machine Controllers**: Each CRD has a state machine for reconciliation
- **Distributed Locking**: Kubernetes Lease-based coordination for multi-pod deployments
- **Event-Driven**: All state changes emit Kubernetes Events
- **Idempotent Reconciliation**: Controllers can re-process same state safely

### 4.2 Layer 2: Custom Resource Layer

**CRD Implementation Details:**

| CRD | File Path | Lines of Code | Key Structs |
|-----|-----------|---------------|-------------|
| Agent | `api/v1alpha1/agent_types.go` | ~150 | `AgentSpec`, `AgentStatus`, `ResolvedMCPServer` |
| Task | `api/v1alpha1/task_types.go` | ~200 | `TaskSpec`, `TaskStatus`, `Message`, `SpanContext` |
| LLM | `api/v1alpha1/llm_types.go` | ~250 | `LLMSpec`, `LLMStatus`, `BaseConfig`, provider configs |
| ToolCall | `api/v1alpha1/toolcall_types.go` | ~150 | `ToolCallSpec`, `ToolCallStatus`, `ToolCallPhase` |
| MCPServer | `api/v1alpha1/mcpserver_types.go` | ~180 | `MCPServerSpec`, `MCPServerStatus`, `EnvVar` |
| ContactChannel | `api/v1alpha1/contactchannel_types.go` | ~150 | `ContactChannelSpec`, `SlackChannelConfig`, `EmailChannelConfig` |

**Total CRD Code:** ~1,080 lines

### 4.3 Layer 3: Controller Layer

**Controller Architecture:**

Each controller follows the pattern:
```go
func (r *Reconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    // 1. Fetch resource
    // 2. Determine state
    // 3. Execute state transition
    // 4. Update status
    // 5. Emit events
    return ctrl.Result{}, nil
}
```

**Controller Files:**

| Controller | File | Lines | State Machine | Key Responsibilities |
|------------|------|-------|---------------|----------------------|
| **LLM** | `internal/controller/llm/llm_controller.go` | ~400 | `state_machine.go` | Validate API keys, test connections |
| **Agent** | `internal/controller/agent/agent_controller.go` | ~500 | `state_machine.go` | Resolve LLM/MCP/SubAgent refs, validate dependencies |
| **Task** | `internal/controller/task/task_controller.go` | ~800 | `state_machine.go` | Orchestrate LLM calls, manage context window, create ToolCalls |
| **ToolCall** | `internal/controller/toolcall/toolcall_controller.go` | ~600 | `state_machine.go` | Execute MCP tools, handle human approval, update results |
| **MCPServer** | `internal/controller/mcpserver/mcpserver_controller.go` | ~400 | `state_machine.go` | Start stdio servers, discover tools, validate connections |
| **ContactChannel** | `internal/controller/contactchannel/contactchannel_controller.go` | ~350 | `state_machine.go` | Validate HumanLayer API keys, register channels |

**Total Controller Code:** ~3,050 lines

**State Machine Pattern:**
```go
// state_machine.go (example)
type State string

const (
    StateInitializing State = "Initializing"
    StateRunning      State = "Running"
    StateCompleted    State = "Completed"
    StateError        State = "Error"
)

func (r *Reconciler) determineNextState(resource *v1alpha1.Resource) State {
    // State transition logic
}
```

### 4.4 Layer 4: Integration Layer

**External Service Integrations:**

#### 4.4.1 LLM Provider Integrations

| Provider | Client Library | File | Integration Approach |
|----------|----------------|------|----------------------|
| OpenAI | `github.com/sashabaranov/go-openai` | `internal/llm/openai.go` | Native Go client |
| Anthropic | `github.com/anthropics/anthropic-sdk-go` | `internal/llm/anthropic.go` | Official SDK |
| Vertex AI | `cloud.google.com/go/vertexai/genai` | `internal/llm/vertex.go` | Google Cloud SDK |
| Mistral | `github.com/gage-technologies/mistral-go` | `internal/llm/mistral.go` | Community SDK |

**Common Interface Pattern:**
```go
type LLMClient interface {
    CreateChatCompletion(ctx context.Context, messages []Message) (*CompletionResponse, error)
}
```

#### 4.4.2 MCP (Model Context Protocol) Integration

**MCP Client Implementation:**
- **Stdio Transport**: Start subprocess, communicate via stdin/stdout with JSON-RPC
- **HTTP Transport**: Standard HTTP client for RESTful MCP servers
- **Tool Discovery**: Query server for available tools on connection
- **Tool Execution**: Call tools with JSON arguments, return results

**Key Files:**
- `internal/mcp/client.go`: MCP client interface
- `internal/mcp/stdio.go`: Stdio transport implementation
- `internal/mcp/http.go`: HTTP transport implementation

#### 4.4.3 HumanLayer API Integration

**HumanLayer Client:**
- **File**: `hack/humanlayer_client.go` + `internal/humanlayerapi/`
- **API Version**: v1beta3 (supports `thread_id`)
- **Authentication**: Project-level or channel-level API keys
- **Endpoints**:
  - `/v1beta3/function-calls` (POST): Request approval/input
  - `/v1beta3/function-calls/{id}` (GET): Poll for response
  - `/v1beta3/contact-channels` (POST): Register channels

**Generated OpenAPI Client:** `internal/humanlayerapi/` (~2,500 lines)

### 4.5 Layer 5: Infrastructure Layer

**Deployment & Release:**

| Component | Location | Purpose |
|-----------|----------|---------|
| **Operator Deployment** | `config/manager/manager.yaml` | Pod spec for operator |
| **CRD Definitions** | `config/crd/bases/*.yaml` | Kubernetes CRD schemas |
| **Release Manifests** | `config/release/` | Combined YAML for installation |
| **RBAC** | `config/rbac/` | ServiceAccount, Roles, RoleBindings |
| **Kustomize** | `config/kustomization.yaml` | Configuration management |

**Installation Methods:**
1. **Latest Release**: `kubectl apply -f https://.../latest.yaml`
2. **Specific Version**: `kubectl apply -f https://.../v0.1.0.yaml`
3. **CRDs Only**: `kubectl apply -f https://.../latest-crd.yaml`

**Container Image:**
- Registry: (Not specified in repo)
- Built via `make docker-build`
- Multi-arch support: Likely amd64/arm64

---

## 5. Data Flow Diagrams

### 5.1 Task Execution Flow

```
1. User creates Task (kubectl apply)
   │
   ▼
2. Task Controller: Reconcile
   │
   ├─► Validate Task
   │   - Check Agent exists
   │   - Check Agent is Ready
   │   - Initialize context window
   │
   ▼
3. Send Context Window to LLM
   │
   ├─► Build messages array
   │   - System prompt from Agent
   │   - User message
   │   - Tool definitions (from MCP servers + human channels + sub-agents)
   │
   ▼
4. LLM Response
   │
   ├─► Case A: Tool calls requested
   │   │
   │   ├─► For each tool call:
   │   │   - Create ToolCall CRD
   │   │   - ToolCall Controller reconciles
   │   │   - Execute tool (MCP/Human/Delegate)
   │   │   - Update ToolCall.status.result
   │   │
   │   └─► Task Controller: Wait for all ToolCalls
   │       - Append tool results to context window
   │       - Go to step 3 (send to LLM again)
   │
   └─► Case B: Final answer
       - Set Task.status.output
       - Set Task.status.phase = "FinalAnswer"
       - Emit event: LLMFinalAnswer
```

### 5.2 MCP Tool Call Flow

```
ToolCall Created
   │
   ▼
ToolCall Controller: Reconcile
   │
   ├─► Fetch ToolCall
   │
   ├─► Fetch referenced MCPServer
   │
   ├─► Check if approval required
   │   │
   │   ├─► YES: approvalContactChannel set
   │   │   │
   │   │   ├─► Call HumanLayer API
   │   │   │   - Create function call request
   │   │   │   - Set phase = "AwaitingHumanApproval"
   │   │   │
   │   │   └─► Poll for approval
   │   │       - Requeue every 10s
   │   │       - When approved: continue
   │   │
   │   └─► NO: proceed
   │
   ├─► Execute MCP Tool
   │   │
   │   ├─► Stdio: Call subprocess
   │   │   - Send JSON-RPC request to stdin
   │   │   - Read JSON-RPC response from stdout
   │   │
   │   └─► HTTP: Call endpoint
   │       - POST to MCP server URL
   │       - Parse JSON response
   │
   ├─► Update ToolCall.status.result
   │
   └─► Update ToolCall.status.phase = "Succeeded"
```

### 5.3 Human-in-the-Loop Flow

```
Task requests human input (via humanContactChannels)
   │
   ▼
Task Controller: Create ToolCall for human contact
   │
   ▼
ToolCall Controller: Reconcile
   │
   ├─► Call HumanLayer API
   │   - POST /v1beta3/function-calls
   │   - Payload: question, contact channel, thread_id
   │
   ├─► Set phase = "AwaitingHumanInput"
   │
   ├─► Poll for response
   │   - GET /v1beta3/function-calls/{id}
   │   - Requeue every 10s
   │
   ├─► Human responds via Slack/Email
   │   - HumanLayer receives response
   │   - Stores in their backend
   │
   ├─► ToolCall Controller: Fetch response
   │   - GET returns status = "approved" + response
   │
   └─► Update ToolCall.status.result = human's answer
       - Set phase = "Succeeded"
       - Task Controller appends to context window
```

---

## 6. Code Statistics & Complexity Metrics

### 6.1 Codebase Breakdown

| Category | Files | Total Lines | Avg Lines/File |
|----------|-------|-------------|----------------|
| **CRD Types** | 8 | ~1,500 | 188 |
| **Controllers** | 36 | ~4,500 | 125 |
| **LLM Integrations** | ~8 | ~2,000 | 250 |
| **MCP Client** | ~5 | ~1,500 | 300 |
| **HumanLayer Client** | ~20 | ~2,500 | 125 |
| **Test Files** | ~20 | ~5,000 | 250 |
| **Examples** | ~10 | ~1,000 | 100 |
| **Config/Manifests** | ~50 | ~5,000 | 100 |
| **Generated Code** | ~5 | ~2,000 | 400 |
| **Utilities** | ~15 | ~2,000 | 133 |
| **Docs (code comments)** | - | ~5,000 | - |

**Total:** ~32,000 lines of Go code across ~180 files

### 6.2 Dependency Analysis

**Direct Dependencies (go.mod):**
- `k8s.io/apimachinery` (Kubernetes core)
- `k8s.io/client-go` (Kubernetes client)
- `sigs.k8s.io/controller-runtime` (Operator framework)
- `github.com/sashabaranov/go-openai` (OpenAI)
- `github.com/anthropics/anthropic-sdk-go` (Anthropic)
- `cloud.google.com/go/vertexai` (Vertex AI)
- `github.com/gage-technologies/mistral-go` (Mistral)
- `go.opentelemetry.io/otel` (Telemetry)

**Architecture Constraint:** The operator is stateless—all state lives in etcd via Kubernetes API.

---

## 7. Key Design Decisions & Constraints

### 7.1 Architectural Constraints

| Constraint | Rationale | Implication |
|------------|-----------|-------------|
| **Kubernetes-Only** | Leverage etcd for durability, API for orchestration | Cannot run standalone |
| **Single Namespace** | LocalObjectReference pattern | Cross-namespace references not supported |
| **Eventual Consistency** | Async reconciliation loops | State updates may lag |
| **No Direct State Mutation** | Only via Kubernetes API | Slower than in-memory state |
| **Context Window as State** | Simplicity | Entire conversation in CRD (size limits) |

### 7.2 Scalability Considerations

| Dimension | Current State | Limitation | Mitigation |
|-----------|---------------|------------|------------|
| **Task Size** | Context window stored in etcd | etcd object size limit (~1.5MB) | Use external storage for large contexts (not implemented) |
| **Concurrent Tasks** | No hard limit | etcd write throughput (~10k writes/sec) | Kubernetes API rate limiting |
| **Tool Call Concurrency** | Serial execution per Task | Each tool call waits for previous | Parallelization possible (not implemented) |
| **MCP Server Pooling** | New process per call | High resource usage | Connection pooling planned |

---

## 8. Security Architecture

### 8.1 Secret Management

**Pattern:** All sensitive data stored in Kubernetes Secrets

| Secret Type | Usage | Reference Pattern |
|-------------|-------|-------------------|
| **LLM API Keys** | OpenAI, Anthropic, etc. | `spec.apiKeyFrom.secretKeyRef` |
| **HumanLayer Tokens** | Human-in-the-loop | `spec.apiKeyFrom.secretKeyRef` or `spec.channelApiKeyFrom` |
| **MCP Environment Vars** | Tool credentials | `spec.env[].valueFrom.secretKeyRef` |

**Security Features:**
- No secrets in CRD spec (only references)
- RBAC controls who can read secrets
- Secrets injected at runtime, not logged

### 8.2 RBAC Model

**ServiceAccount:** `acp-controller-manager`

**Permissions (ClusterRole):**
- **Full CRUD** on all ACP CRDs (`agents`, `tasks`, `llms`, etc.)
- **Read** on `secrets` (for API key injection)
- **Create** on `events` (for observability)
- **Create/Update** on `leases` (for distributed locking)

**User Permissions:** Users need RBAC to:
- Create/Read Tasks (to run agents)
- Create/Read Agents (to define agents)
- Create LLMs, MCPServers, ContactChannels (to configure tools)

---

## 9. Deployment & Operations

### 9.1 Installation Methods

| Method | Command | Use Case |
|--------|---------|----------|
| **Latest** | `kubectl apply -f .../latest.yaml` | Production (rolling) |
| **Pinned Version** | `kubectl apply -f .../v0.1.0.yaml` | Production (stable) |
| **CRDs Only** | `kubectl apply -f .../latest-crd.yaml` | Custom deployments |
| **Local Dev** | `make install && make run` | Development |

### 9.2 Observability Stack (acp-example)

**Included in `acp-example/` directory:**

| Component | Purpose | Helm Chart | Access |
|-----------|---------|-----------|--------|
| **Grafana** | Visualization | `acp-example/grafana/` | Port-forward 3000 |
| **Tempo** | Distributed tracing | `acp-example/otel/` | Via Grafana |
| **Loki** | Log aggregation | `acp-example/loki/` | Via Grafana |
| **Prometheus** | Metrics | `acp-example/prometheus/` | Port-forward 9090 |

**Setup:** `make -C acp-example otel-stack`

---

## 10. Testing Infrastructure

### 10.1 Test Coverage

| Test Type | Files | Coverage Focus |
|-----------|-------|----------------|
| **Unit Tests** | `*_test.go` in each controller | State machine logic, validation |
| **Integration Tests** | `task_humanlayerapi_integration_test.go` | HumanLayer API interactions |
| **E2E Tests** | `.github/workflows/test-e2e.yml` | Full workflow testing |

**Test Frameworks:**
- `sigs.k8s.io/controller-runtime/pkg/envtest` (Kubernetes test environment)
- Standard Go testing

### 10.2 CI/CD Pipeline

**GitHub Actions Workflows:**

| Workflow | File | Trigger | Purpose |
|----------|------|---------|---------|
| **Test** | `.github/workflows/test.yml` | PR, push to main | Run unit tests |
| **E2E Test** | `.github/workflows/test-e2e.yml` | PR, push to main | End-to-end testing |
| **Lint** | `.github/workflows/lint.yml` | PR, push to main | Code quality checks |

**Linting:** `.golangci.yml` configured with:
- gofmt
- govet
- staticcheck
- errcheck

---

## 11. Feature Completeness vs. Roadmap

### 11.1 Implemented Features (Alpha ✅)

| Feature | Status | Quality |
|---------|--------|---------|
| Durable task execution | ✅ Alpha | Core functionality |
| OpenAI support | ✅ Alpha | Production-ready |
| Anthropic support | ✅ Alpha | Production-ready |
| Vertex AI support | ✅ Alpha | Production-ready |
| Mistral AI support | ✅ Alpha | Production-ready |
| MCP stdio support | ✅ Alpha | Working |
| MCP HTTP support | ✅ Alpha | Working |
| Human approval for tools | ✅ Alpha | Working |
| Human as tool | ✅ Alpha | Working |
| Kubernetes Events | ✅ Alpha | Complete |
| OpenTelemetry traces | 🚧 In Progress | Partial (span context only) |

### 11.2 Planned Features (Roadmap 🗺️)

| Feature | Priority | Complexity |
|---------|----------|------------|
| Better MCP scheduling | Medium | Medium |
| Delegation to sub-agents | High | High (In Progress 🚧) |
| Tiered approval (once/task/always) | Medium | Medium |
| OTel logs | Low | Low |
| OTel metrics | Low | Low |
| Token counts in traces | Medium | Medium |
| Webhook triggers | High | High |
| Slack/Email inbound triggers | High | High |
| ACP UI | High | Very High |
| ACP CLI | High | Medium |

---

## 12. Strengths & Innovations

### 12.1 Novel Design Patterns

1. **Infrastructure-as-Conversations**
   - Treating conversations as durable, orchestrated workflows
   - Context window = execution state

2. **Async/Await at Infrastructure Level**
   - Tool calls checkpoint state automatically
   - Survives pod restarts, network failures

3. **Declarative AI Orchestration**
   - YAML-based agent definitions
   - GitOps-compatible

4. **Observable by Default**
   - Every state transition = Kubernetes Event
   - Full audit trail

5. **Composable Agent Architecture**
   - Agents as tools for other agents
   - Recursive delegation supported

### 12.2 Architectural Strengths

| Strength | Benefit |
|----------|---------|
| **Kubernetes-Native** | Leverage battle-tested orchestration |
| **State Machine Controllers** | Clear, debuggable state transitions |
| **Durable State** | Survive failures, long-running workflows |
| **Extensible via CRDs** | Add new resource types easily |
| **Observable** | Events + OTel for full visibility |

---

## 13. Limitations & Trade-offs

### 13.1 Current Limitations

| Limitation | Impact | Workaround |
|------------|--------|------------|
| **Context window size** | Large conversations may exceed etcd limits (~1.5MB) | Not implemented yet |
| **Serial tool execution** | Slow for parallel-capable tools | Could parallelize |
| **No MCP connection pooling** | High resource usage for stdio MCPs | Planned |
| **Single namespace only** | No cross-namespace agent delegation | Design constraint |
| **No streaming LLM responses** | Higher latency for long responses | Could add streaming |

### 13.2 Trade-offs Made

| Trade-off | Decision | Reasoning |
|-----------|----------|-----------|
| **Kubernetes dependency** | Require K8s | Durability + orchestration for free |
| **Eventual consistency** | Accept async delays | Necessary for distributed system |
| **CRD size limits** | Store context in etcd | Simplicity > optimization |
| **No local mode** | Require K8s cluster | Focus on production use case |

---

## 14. Competitor/Alternative Analysis Context

### 14.1 Unique Positioning

**What ACP does differently:**

| Aspect | ACP | Typical Agent Frameworks |
|--------|-----|--------------------------|
| **Durability** | Kubernetes etcd | In-memory or DB |
| **Orchestration** | Kubernetes operators | Custom schedulers |
| **Scalability** | Kubernetes scaling | Manual scaling |
| **Observability** | K8s Events + OTel | Custom logging |
| **State Management** | CRDs (declarative) | Imperative code |
| **Agent Composition** | Native (sub-agents as CRDs) | Often limited |

**Target Use Case:** Production-grade, long-running, durable agentic workflows that need to survive failures and scale across infrastructure.

---

## 15. Technical Debt & Future Refactoring Opportunities

### 15.1 Identified Technical Debt

1. **MCP Client Efficiency**
   - **Issue:** New process per stdio MCP call
   - **Impact:** High CPU/memory usage
   - **Refactor:** Connection pooling + process reuse

2. **Context Window Storage**
   - **Issue:** Full conversation in CRD
   - **Impact:** etcd size limits
   - **Refactor:** External storage for large contexts

3. **Tool Call Parallelization**
   - **Issue:** Serial execution
   - **Impact:** Slower than necessary
   - **Refactor:** Parallel ToolCall execution where safe

4. **Error Handling Consistency**
   - **Issue:** Some controllers have different error patterns
   - **Impact:** Harder to debug
   - **Refactor:** Standardize error handling + retry logic

### 15.2 Code Smells

- **Large Controller Functions:** Some reconcile functions >200 lines
- **Repeated Validation Logic:** Could extract to shared validators
- **Generated Code Bloat:** HumanLayer API client is ~2,500 lines (acceptable, auto-generated)

---

## 16. Integration Points & External Dependencies

### 16.1 External Service Dependencies

| Service | Purpose | Failure Impact | Mitigation |
|---------|---------|----------------|------------|
| **LLM APIs** | Core functionality | Tasks fail | Retry logic + status reporting |
| **HumanLayer API** | Human-in-the-loop | Human interactions fail | Timeout + error handling |
| **MCP Servers** | Tool execution | Tool calls fail | Per-tool error handling |
| **etcd** (via K8s) | State storage | Operator cannot function | Kubernetes HA |

### 16.2 Network Boundaries

```
┌─────────────────────────────────────────────────┐
│              Kubernetes Cluster                 │
│  ┌───────────────────────────────────────────┐ │
│  │         ACP Operator Pod(s)               │ │
│  │                                           │ │
│  │  ┌─────────────────────────────────────┐ │ │
│  │  │       Controller Manager            │ │ │
│  │  │  (Reconciliation Loops)             │ │ │
│  │  └─────────────────────────────────────┘ │ │
│  │         │           │           │         │ │
│  └─────────┼───────────┼───────────┼─────────┘ │
│            │           │           │           │
│  ┌─────────▼───────────▼───────────▼─────────┐ │
│  │      Kubernetes API Server (etcd)         │ │
│  └───────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
          │           │           │
          │           │           │ Network Egress
          │           │           │
          ▼           ▼           ▼
  ┌─────────┐  ┌─────────┐  ┌─────────┐
  │LLM APIs │  │HumanLayer│  │MCP Srvs │
  │(OpenAI, │  │   API    │  │(External│
  │Anthropic│  │          │  │ or Local)│
  │ etc.)   │  │          │  │         │
  └─────────┘  └─────────┘  └─────────┘
```

---

## 17. Glossary of Key Terms

| Term | Definition |
|------|------------|
| **CRD** | Custom Resource Definition—Kubernetes' extension mechanism |
| **Reconcile** | Process of making current state match desired state |
| **Context Window** | The rolling conversation history sent to the LLM |
| **MCP** | Model Context Protocol—standard for tool integration |
| **HumanLayer** | External service for human approval/input workflows |
| **ToolCall** | A single invocation of a tool (MCP, human, or sub-agent) |
| **Sub-Agent** | An Agent that can be delegated to by another Agent |
| **Stdio Transport** | Communication via stdin/stdout (for MCP) |
| **Approval Workflow** | Requiring human approval before tool execution |
| **Durable Execution** | Surviving failures by checkpointing state |

---

## 18. Architecture Diagrams Summary

### 18.1 High-Level System Architecture

```
┌────────────────────────────────────────────────────────────┐
│                     User / Developer                        │
│                                                             │
│  kubectl apply -f agent.yaml                               │
│  kubectl apply -f task.yaml                                │
│  kubectl get task my-task -o jsonpath='{.status.output}'  │
└────────────────────────────┬───────────────────────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────────┐
│              Kubernetes API Server (etcd)                   │
│                                                             │
│  ┌─────┐  ┌─────┐  ┌─────┐  ┌────────┐  ┌──────────┐    │
│  │ LLM │  │Agent│  │Task │  │ToolCall│  │MCPServer │    │
│  │     │  │     │  │     │  │        │  │ContactCh.│    │
│  └─────┘  └─────┘  └─────┘  └────────┘  └──────────┘    │
│     ▲        ▲        ▲          ▲            ▲           │
│     │        │        │          │            │           │
│     └────────┴────────┴──────────┴────────────┘           │
│                       │ Watch & Reconcile                  │
└───────────────────────┼────────────────────────────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────────────┐
│               ACP Operator (Controller Manager)             │
│                                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                │
│  │   LLM    │  │  Agent   │  │   Task   │                │
│  │Controller│  │Controller│  │Controller│                │
│  └──────────┘  └──────────┘  └──────────┘                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                │
│  │ ToolCall │  │MCPServer │  │ Contact  │                │
│  │Controller│  │Controller│  │Controller│                │
│  └──────────┘  └──────────┘  └──────────┘                │
│         │              │              │                    │
└─────────┼──────────────┼──────────────┼────────────────────┘
          │              │              │ External Calls
          ▼              ▼              ▼
┌────────────────────────────────────────────────────────────┐
│                   External Services                         │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │  OpenAI API  │  │ Anthropic    │  │  Vertex AI   │    │
│  │              │  │     API      │  │     API      │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
│  ┌──────────────────────────────────────────────────┐    │
│  │            HumanLayer API                         │    │
│  │   (Human Approval / Human as Tool)                │    │
│  └──────────────────────────────────────────────────┘    │
│  ┌──────────────────────────────────────────────────┐    │
│  │              MCP Servers                          │    │
│  │   (stdio subprocess or HTTP endpoints)            │    │
│  └──────────────────────────────────────────────────┘    │
└────────────────────────────────────────────────────────────┘
```

---

## 19. Conclusion

Agent Control Plane (ACP) represents a **paradigm shift** in AI agent orchestration by treating **conversations as durable, observable, Kubernetes-native workflows**. The system's architecture demonstrates:

1. **Infrastructure-as-Conversations**: Kubernetes etcd becomes the durable message queue for agent interactions
2. **Async/Await at Infrastructure Level**: Checkpointing at every tool call enables long-running, failure-resistant workflows
3. **Declarative AI Orchestration**: YAML-based agent definitions enable GitOps workflows
4. **Composable Agent Architecture**: Sub-agents as first-class resources enable hierarchical delegation
5. **Observable by Default**: Kubernetes Events + OpenTelemetry provide full visibility

**Architectural Maturity:** Alpha—core functionality working, production features (OTel, UI, CLI) in development.

**Target Use Case:** Production-grade, durable, long-running agentic workflows that need to survive failures, incorporate human feedback, and scale across distributed systems.

**Special Note on Matrices:** As requested, this analysis includes comprehensive **Feature/Functionality/Capability Matrices** in Section 3, covering LLM providers, MCP integration, human-in-the-loop capabilities, agent composition, task execution lifecycle, and observability—providing a tabular view of the system's capabilities across multiple dimensions.

---

**End of Level 1 Analysis**
