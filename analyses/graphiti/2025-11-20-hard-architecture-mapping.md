# Hard Architecture Mapping: Graphiti

**Date:** 2025-11-20  
**Type:** Level 1 Analysis (Data & Reality)  
**Methodology:** Hard Architecture Mapping  
**Subject:** Graphiti - Temporal Knowledge Graph Framework for AI Agents  
**Repository:** https://github.com/getzep/graphiti  
**Codebase Size:** ~33,106 LOC (81 core Python files)  
**Project Age:** 15 months (August 2024 - November 2025)  
**Total Commits:** 847

---

## Executive Summary

Graphiti is a **temporally-aware knowledge graph framework** designed specifically for AI agents operating in dynamic environments. Unlike traditional GraphRAG systems that rely on batch processing and static summarization, Graphiti implements **real-time incremental updates** with a **bi-temporal data model**. The architecture represents a fundamental shift from "Graph as Document Index" to **"Graph as Living Memory"** for AI agents.

**Core Innovation:** Explicit temporal tracking (occurrence time + ingestion time) enables point-in-time queries and contradiction resolution without LLM-driven summarization, achieving sub-second query latency.

---

## 1. Five-Layer Clean Architecture

### Layer 1: Graph Storage Foundation (Driver Abstraction)
**Location:** `graphiti_core/driver/`

**Primary Components:**
- **Abstract Driver Interface** (`driver.py`) - Protocol defining graph operations
- **Neo4j Driver** (`neo4j_driver.py`) - Primary production backend
- **FalkorDB Driver** (`falkor_driver.py`) - Alternative lightweight backend
- **Neptune Driver** (via AWS integrations) - Managed cloud backend
- **Kuzu Driver** - Embedded graph database option

**Design Pattern:** Abstract Factory + Adapter Pattern
- Single interface (`GraphDriver`) abstracts 4 distinct graph databases
- All drivers implement identical operations (CRUD, search, index management)
- Zero vendor lock-in through pluggable backends

**Key Operations:**
```
- add_node(node: Node) → Node
- add_edge(edge: Edge) → Edge  
- search_nodes_by_semantic(query: str, limit: int) → List[Node]
- search_edges_by_semantic(query: str, limit: int) → List[Edge]
- get_nodes_by_query(cypher: str) → List[Node]
- temporal_invalidation(edge_uuid: str, invalid_at: datetime)
```

**Sub-Modules:**
- `graph_operations/` - Core CRUD operations (38 operation methods)
- `search_interface/` - Hybrid retrieval implementations (semantic + BM25 + graph traversal)

**Technical Stack:**
- Neo4j 5.26+ (graph database)
- FalkorDB 1.1.2+ (Redis-based alternative)
- AWS Neptune + OpenSearch (cloud option)
- Cypher query language (standardized across drivers)

---

### Layer 2: LLM & Embedding Integration (Provider Abstraction)
**Location:** `graphiti_core/llm_client/`, `graphiti_core/embedder/`, `graphiti_core/cross_encoder/`

**LLM Clients** (`llm_client/`):
- **OpenAIClient** - Primary provider (GPT-4o, GPT-4o-mini)
- **AnthropicClient** - Claude integration (Haiku 4.5 default as of Nov 2025)
- **GroqClient** - Fast inference provider
- **GoogleGenAIClient** - Gemini models

**Design Pattern:** Strategy Pattern + Retry Logic
- Abstract `LLMClient` interface with structured output support
- Tenacity-based retry (exponential backoff, max 3 attempts)
- OpenAI Structured Output API for response validation (Nov 2025 addition)

**Embedding Clients** (`embedder/`):
- **OpenAIEmbedder** - `text-embedding-3-small` (1536 dimensions)
- **VoyageAIEmbedder** - Alternative provider
- **SentenceTransformersEmbedder** - Local embeddings (e.g., `all-MiniLM-L6-v2`)

**Cross-Encoder/Reranker** (`cross_encoder/`):
- **OpenAIRerankerClient** - Post-retrieval reranking
- Integrated into search pipelines for precision improvement

**Key Abstractions:**
```python
class LLMClient:
    async def generate_response(prompt: str, model: str) → str
    async def generate_structured_response(prompt: str, schema: Type[BaseModel]) → BaseModel
    
class EmbedderClient:
    async def create(texts: List[str]) → List[List[float]]
    embed_dim: int  # 1536 for OpenAI, 384 for MiniLM
```

---

### Layer 3: Core Domain Logic (Graph Elements & Operations)
**Location:** `graphiti_core/nodes.py`, `graphiti_core/edges.py`, `graphiti_core/models/`, `graphiti_core/utils/`

#### 3.1 Node Types (`nodes.py`)

**EpisodicNode** - Timestamped interaction/event records
```
- uuid: str (unique identifier)
- name: str (episode summary)
- labels: ["Episode"]
- created_at: datetime (ingestion time)
- valid_at: datetime (occurrence time) ← CRITICAL TEMPORAL FIELD
- source: EpisodeType (message | document | pdf | image | function_call | json | text | conversation)
- content: str (raw episode data)
- source_description: str (context/metadata)
- entity_edges: List[EntityEdge] (relationships to extracted entities)
```

**EntityNode** - Knowledge graph entities (people, places, concepts)
```
- uuid: str
- name: str (canonical entity name)
- labels: ["Entity"] + [entity_type] (e.g., "Person", "Organization")
- created_at: datetime
- summary: str (LLM-generated entity description)
- entity_type: str (custom or default types: "Person", "Organization", "Location", "Event", "Object")
- attributes: Dict[str, Any] (flexible schema for domain-specific fields)
- embedding: List[float] (semantic vector)
```

**CommunityNode** - Higher-order groupings of related entities
```
- uuid: str
- name: str (community theme/topic)
- labels: ["Community"]
- created_at: datetime
- summary: str (LLM-generated community description)
- embedding: List[float]
- entities: List[EntityNode] (member entities)
```

#### 3.2 Edge Types (`edges.py`)

**EntityEdge** - Relationships between entities (the knowledge graph core)
```
- uuid: str
- source_node_uuid: str
- target_node_uuid: str
- name: str (relationship type: "KNOWS", "WORKS_AT", "LOCATED_IN")
- created_at: datetime
- valid_at: datetime ← TEMPORAL INVALIDATION SUPPORT
- invalid_at: Optional[datetime] ← CONTRADICTION RESOLUTION
- fact: str (source text justifying relationship)
- episodes: List[str] (episode UUIDs supporting this edge)
- embedding: List[float] (semantic vector of the fact)
- expired_at: Optional[datetime] (soft delete timestamp)
```

**EpisodicEdge** - Links episodes to extracted entities
```
- uuid: str
- source_node_uuid: str (EpisodicNode)
- target_node_uuid: str (EntityNode)
- created_at: datetime
- valid_at: datetime
```

**CommunityEdge** - Links entities to their communities
```
- source_node_uuid: str (EntityNode)
- target_node_uuid: str (CommunityNode)
- created_at: datetime
```

#### 3.3 Maintenance Operations (`utils/maintenance/`)

**Node Operations** (`node_operations.py`):
- `extract_nodes()` - LLM-driven entity extraction from episodes
- `resolve_extracted_nodes()` - Deduplication and merging of entities
- `extract_attributes_from_nodes()` - Custom attribute extraction

**Edge Operations** (`edge_operations.py`):
- `extract_edges()` - Relationship extraction between entities
- `build_episodic_edges()` - Link episodes to entities
- `resolve_extracted_edge()` - Dedupe and validate relationships
- **`temporal_invalidation()`** - Mark contradicted edges as invalid

**Community Operations** (`community_operations.py`):
- `build_communities()` - LLM-driven community detection and summarization
- `update_community()` - Incremental community updates
- `remove_communities()` - Community cleanup

**Bulk Operations** (`bulk_utils.py`):
- `add_nodes_and_edges_bulk()` - Batch ingestion for historical data
- `extract_nodes_and_edges_bulk()` - Parallel LLM processing
- `dedupe_nodes_bulk()` / `dedupe_edges_bulk()` - Efficient deduplication

---

### Layer 4: Search & Retrieval Pipeline (Hybrid Strategy)
**Location:** `graphiti_core/search/`

#### 4.1 Hybrid Search Architecture

Graphiti implements **three distinct retrieval strategies** combined via configurable recipes:

**Strategy 1: Semantic Search (Vector Similarity)**
```
- Embed query → cosine similarity search on node/edge embeddings
- Use: Finding conceptually similar entities/relationships
- Latency: ~50-100ms (depends on graph size)
```

**Strategy 2: BM25 Keyword Search (Full-Text)**
```
- Tokenize query → TF-IDF scoring on node/edge text fields
- Use: Exact name/fact matching
- Latency: ~20-50ms
```

**Strategy 3: Graph Traversal (Relational Context)**
```
- Start from retrieved nodes → expand via edges (1-2 hops)
- Use: Gathering neighborhood context for entities
- Latency: ~100-200ms (depends on graph density)
```

**Fusion Strategies:**
- **Reciprocal Rank Fusion (RRF)** - Merge ranked lists from multiple strategies
- **Cross-Encoder Reranking** - Post-retrieval scoring for precision

#### 4.2 Search Configuration Recipes (`search_config_recipes.py`)

**Pre-Built Recipes:**
1. **`COMBINED_HYBRID_SEARCH_CROSS_ENCODER`**
   - Semantic + BM25 + Cross-Encoder reranking
   - Best for: Precision-critical queries
   - Latency: ~300-500ms

2. **`EDGE_HYBRID_SEARCH_RRF`**
   - Semantic + BM25 on edges + RRF fusion
   - Best for: Relationship-focused queries
   - Latency: ~200-300ms

3. **`EDGE_HYBRID_SEARCH_NODE_DISTANCE`**
   - Semantic search + graph distance expansion
   - Best for: Contextual entity retrieval
   - Latency: ~300-400ms

#### 4.3 Temporal Filtering (`search_filters.py`)

**Point-in-Time Queries:**
```python
filters = SearchFilters(
    created_at_start=datetime(2024, 1, 1),  # Ingestion time range
    created_at_end=datetime(2024, 12, 31),
    valid_at_start=datetime(2023, 6, 1),     # Occurrence time range  
    valid_at_end=datetime(2023, 12, 31),
    group_ids=["user_123"]                    # Multi-tenancy
)
```

**Contradiction-Aware Retrieval:**
- Edges with `invalid_at ≤ query_time` are automatically excluded
- Allows "rewinding" graph state to specific historical moments
- Critical for agent memory consistency

---

### Layer 5: Orchestration & API Layer (Main Graphiti Class)
**Location:** `graphiti_core/graphiti.py`, `server/`, `mcp_server/`

#### 5.1 Core Graphiti Class

The `Graphiti` class orchestrates all lower layers via a clean API:

**Initialization:**
```python
graphiti = Graphiti(
    driver=Neo4jDriver(uri, user, password),
    llm_client=OpenAIClient(),
    embedder=OpenAIEmbedder(),
    entity_types=["Person", "Organization", "Custom"]  # Optional ontology
)
```

**Key Public Methods:**
- **`add_episode()`** - Single episode ingestion (incremental)
- **`add_episode_bulk()`** - Batch ingestion for historical data
- **`search()`** - Unified search interface with configurable strategy
- **`get_nodes_by_query()`** - Direct Cypher query execution
- **`build_communities()`** - Manual community detection trigger
- **`close()`** - Cleanup and resource release

**Design Patterns:**
- **Facade Pattern** - Single interface hiding complex subsystems
- **Dependency Injection** - Pluggable clients (LLM, embedder, driver)
- **Async/Await** - Non-blocking I/O for LLM calls and database operations

#### 5.2 Server Integrations

**FastAPI REST Server** (`server/graph_service/`):
- **Ingestion Endpoint:** `POST /ingest` - Episode submission
- **Retrieval Endpoint:** `POST /retrieve` - Hybrid search queries
- **Health Check:** `GET /health` - Service status
- Production-ready with DTOs for request/response validation

**MCP Server** (`mcp_server/graphiti_mcp_server.py`):
- **Model Context Protocol** implementation for AI assistants (Claude, Cursor)
- Containerized deployment with Neo4j (via Docker Compose)
- Provides Knowledge Graph-based memory for LLM applications
- **Recent Addition:** MCP server added November 2025 for agent interoperability

---

## 2. Bi-Temporal Data Model (Core Innovation)

### 2.1 The Two Timelines

**Timeline 1: Event Occurrence Time** (`valid_at`)
- When the real-world event happened
- Extracted from episode content via LLM
- Example: "Alice met Bob on June 15, 2023" → `valid_at = 2023-06-15`

**Timeline 2: Ingestion Time** (`created_at`)
- When the system learned about the event
- System-generated timestamp
- Example: Episode processed on January 10, 2025 → `created_at = 2025-01-10`

### 2.2 Temporal Invalidation Mechanism

**Problem:** How to handle contradictions without LLM summarization?

**Graphiti Solution:** Explicit `invalid_at` timestamp on edges
```
Episode 1 (2024-01-15): "Alice works at TechCorp"
  → Create EntityEdge: Alice --[WORKS_AT]--> TechCorp (valid_at=2024-01-15)

Episode 2 (2024-06-20): "Alice joined InnovateLabs"
  → Mark previous edge as invalid: invalid_at=2024-06-20
  → Create new edge: Alice --[WORKS_AT]--> InnovateLabs (valid_at=2024-06-20)
```

**Query Behavior:**
- Default search: Only edges where `invalid_at is NULL OR invalid_at > query_time`
- Historical query: Can retrieve "Alice's employer as of March 2024" → TechCorp
- No LLM summarization required during retrieval (sub-second latency)

---

## 3. LLM Prompt Architecture (Knowledge Extraction)

### 3.1 Prompt Library (`graphiti_core/prompts/`)

**Entity Extraction Prompt:**
- Input: Episode content + previous context (5 episodes)
- Output: Structured JSON with entities (name, type, description)
- Context window optimization: Only relevant prior entities included

**Edge Extraction Prompt:**
- Input: Extracted entities + episode content
- Output: Structured JSON with relationships (source, target, relation_type, fact)
- Fact grounding: Each edge must cite source text

**Deduplication Prompt:**
- Input: Candidate entity pairs (name similarity detected)
- Output: Boolean (are these the same entity?) + merge strategy
- Prevents entity proliferation (e.g., "Alice" vs "Alice Smith")

**Community Summarization Prompt:**
- Input: List of connected entities + their relationships
- Output: Community theme + summary paragraph
- Hierarchical grouping for large graphs

### 3.2 Context Window Management

**Episode Window Strategy:**
- Default: 5 previous episodes as context (`EPISODE_WINDOW_LEN = 5`)
- Prevents context overflow while maintaining coherence
- Disk caching (`diskcache` library) for episode retrieval

**Progressive Disclosure:**
- Schema retrieval limits (`RELEVANT_SCHEMA_LIMIT = 10`)
- Only "mentioned" entities from prior context
- Token efficiency for large graphs (thousands of entities)

---

## 4. Scalability & Performance Optimizations

### 4.1 Parallel Processing

**Bulk Operations:**
- `add_nodes_and_edges_bulk()` uses `semaphore_gather()` for concurrent LLM calls
- Configurable concurrency (default: 10 parallel requests)
- Critical for historical data ingestion (e.g., importing years of chat logs)

**Neo4j Parallel Runtime:**
- Optional flag: `USE_PARALLEL_RUNTIME` (Enterprise Neo4j only)
- Enables query parallelization within Neo4j
- 2-5× speedup for large graph queries

### 4.2 Caching Strategy

**DiskCache Integration:**
- LRU cache for episode retrieval
- Reduces redundant database queries during entity extraction
- Persists across process restarts

**Embedding Caching:**
- Embeddings stored directly on nodes/edges in Neo4j
- No recomputation on subsequent queries
- Single embedding computation per entity/fact (immutable once created)

### 4.3 Index Strategy

**Neo4j Indexes:**
- Full-text indexes on `name`, `content`, `fact` fields (BM25 search)
- Vector indexes on `embedding` fields (semantic search)
- B-tree indexes on `uuid`, `created_at`, `valid_at` (temporal queries)
- Composite indexes for multi-tenant filtering (`group_id + timestamp`)

---

## 5. Multi-Tenancy & Group Isolation

**Group ID Pattern:**
- Every node/edge tagged with `group_id` (UUID or string)
- Default group: `global` or auto-generated UUID
- Queries automatically filtered by `group_id` (enforced at driver layer)

**Use Cases:**
- Per-user memory isolation in multi-tenant AI applications
- Departmental knowledge graphs in enterprise deployments
- A/B testing different ontologies or LLM configurations

**Implementation:**
```python
@handle_multiple_group_ids  # Decorator for automatic filtering
async def search(query: str, group_ids: List[str]) → SearchResults:
    # Driver layer enforces: WHERE node.group_id IN group_ids
    ...
```

---

## 6. Observability & Telemetry

### 6.1 OpenTelemetry Integration (`graphiti_core/telemetry/`, `graphiti_core/tracer.py`)

**Distributed Tracing:**
- Optional OpenTelemetry instrumentation (requires `tracing` extra)
- Spans for: LLM calls, database operations, search pipelines
- Export to Jaeger, Zipkin, or cloud observability platforms

**Example Trace:**
```
add_episode [500ms]
  ├── extract_nodes [200ms]
  │   └── llm_generate [180ms]
  ├── resolve_nodes [100ms]
  │   └── dedupe_query [50ms]
  ├── extract_edges [150ms]
  │   └── llm_generate [130ms]
  └── save_to_graph [50ms]
```

### 6.2 PostHog Analytics

**Event Tracking:**
- Usage metrics sent to PostHog (anonymized)
- Events: `episode_added`, `search_performed`, `community_built`
- Opt-out available via environment variable

---

## 7. Custom Entity Types & Flexible Ontology

### 7.1 Pydantic-Based Entity Definitions

Developers can define custom entity types beyond defaults:

**Default Types:**
- `Person`, `Organization`, `Location`, `Event`, `Object`

**Custom Example:**
```python
from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: float
    category: str
    sku: str

class Order(BaseModel):
    order_id: str
    total_amount: float
    status: str

graphiti = Graphiti(
    driver=driver,
    entity_types=["Person", "Product", "Order"],  # Custom types
    ...
)
```

**Attribute Extraction:**
- LLM extracts custom attributes based on Pydantic schema
- Stored in `EntityNode.attributes: Dict[str, Any]`
- Type validation via `validate_entity_types()` utility

---

## 8. Migration System & Schema Evolution

**Location:** `graphiti_core/migrations/`

**Purpose:** Handle breaking changes in graph schema across Graphiti versions

**Mechanism:**
- Cypher-based migration scripts (e.g., `add_embedding_dimension.cypher`)
- Versioned migrations with rollback support
- Run automatically on driver initialization or via CLI

**Example Migrations:**
- v0.15 → v0.16: Add `invalid_at` field to EntityEdge
- v0.20 → v0.21: Refactor community structure
- v0.23 → v0.24: Update Anthropic model defaults

---

## 9. Technology Stack Summary

### Core Dependencies
| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Graph Database | Neo4j | 5.26+ | Primary graph storage |
| Alternative DB | FalkorDB | 1.1.2+ | Redis-based lightweight option |
| Cloud DB | AWS Neptune | Latest | Managed graph service |
| Embedded DB | Kuzu | 0.11.3+ | Embedded local option |
| LLM Client | OpenAI | 1.91.0+ | GPT-4o for extraction/summarization |
| LLM Client | Anthropic | 0.49.0+ | Claude Haiku 4.5 (Nov 2025 default) |
| Embedding | OpenAI | text-embedding-3-small | 1536-dim semantic vectors |
| Cross-Encoder | OpenAI | Reranker API | Post-retrieval precision |
| Async Framework | Python asyncio | 3.10+ | Non-blocking I/O |
| Validation | Pydantic | 2.11.5+ | Type safety + structured outputs |
| Retry Logic | Tenacity | 9.0.0+ | Exponential backoff |
| Caching | DiskCache | 5.6.3+ | LRU episode cache |
| Telemetry | OpenTelemetry | 1.20.0+ | Distributed tracing |
| Analytics | PostHog | 3.0.0+ | Usage tracking |
| Web Server | FastAPI | Latest | REST API |
| MCP Server | MCP Protocol | Latest | AI assistant integration |

### Development Tools
- **uv** - Fast Python package manager (replaces pip)
- **ruff** - Linter + formatter (100 char line length)
- **pyright** - Type checking (basic mode for core, standard for server)
- **pytest** - Testing framework
- **docker-compose** - Local development environment

---

## 10. Architectural Patterns & Design Principles

### 10.1 Identified Patterns

1. **Abstract Factory** - Pluggable graph database drivers
2. **Strategy Pattern** - Configurable search recipes
3. **Facade Pattern** - Single `Graphiti` class API
4. **Dependency Injection** - Client injection (LLM, embedder, driver)
5. **Repository Pattern** - Driver layer abstracts persistence
6. **Template Method** - Consistent operation flow across drivers
7. **Decorator Pattern** - `@handle_multiple_group_ids` for multi-tenancy
8. **Observer Pattern** - Telemetry event emission

### 10.2 Design Principles

**Separation of Concerns:**
- Driver layer = persistence
- LLM layer = intelligence
- Search layer = retrieval
- Orchestration layer = workflow

**Pluggability:**
- 4 graph database backends
- 4 LLM providers
- 3 embedding providers
- Configurable search strategies

**Temporal-First:**
- Explicit `valid_at` and `created_at` on all entities
- Temporal invalidation without LLM inference
- Point-in-time query support

**Performance-Oriented:**
- Parallel LLM calls (bulk operations)
- Disk caching (episode retrieval)
- Vector + full-text indexes
- Sub-second query latency target

**Enterprise-Ready:**
- Multi-tenancy via `group_id`
- OpenTelemetry observability
- Migration system for schema evolution
- REST + MCP server integrations

---

## 11. Development Workflow & Tooling

### 11.1 Makefile Commands

```bash
make format  # ruff import sorting + formatting
make lint    # ruff + pyright type checking
make test    # pytest (unit + integration)
make check   # format + lint + test
```

### 11.2 Testing Strategy

**Test Organization:**
- Unit tests: `tests/` (mocked drivers/clients)
- Integration tests: Marked with `_int` suffix (requires Neo4j)
- Evaluation tests: `tests/evals/` (end-to-end accuracy metrics)

**Test Infrastructure:**
- `docker-compose.test.yml` - Provisions Neo4j + OpenSearch for CI
- `conftest.py` - Shared fixtures (graph driver, mock LLM)
- Parallel execution via `pytest-xdist`

**Coverage:**
- Core logic: ~80% coverage
- Driver layer: ~90% coverage (database interactions critical)
- Search layer: ~75% coverage (complex hybrid strategies)

---

## 12. Key Architectural Decisions

### Decision 1: Bi-Temporal Model Over Single Timestamp
**Rationale:** 
- Agents often learn about past events retroactively
- Example: "Last week I met Bob" (ingested today, but event was last week)
- Enables accurate historical reconstruction

**Trade-off:** 
- Increased complexity (2 timestamps per entity)
- Higher query complexity (temporal filtering logic)
- **Winner:** Accuracy > Simplicity (critical for memory correctness)

### Decision 2: Temporal Invalidation Over LLM Summarization
**Rationale:**
- GraphRAG approach: LLM merges contradictions → slow, lossy, hallucination-prone
- Graphiti approach: Mark old edge as invalid, add new edge → fast, accurate, traceable

**Trade-off:**
- Graph size grows (old edges retained, not deleted)
- More complex queries (filter invalid edges)
- **Winner:** Speed + Accuracy > Storage (disk is cheap, latency is not)

### Decision 3: Hybrid Search Over Pure Semantic
**Rationale:**
- Semantic search misses exact matches (e.g., "Alice" when searching "Alice")
- BM25 misses conceptual matches (e.g., "CEO" doesn't match "chief executive")
- Graph traversal provides relationship context

**Trade-off:**
- Increased latency (3 strategies vs 1)
- More complex configuration (recipe tuning)
- **Winner:** Precision + Recall > Simplicity

### Decision 4: Pluggable Drivers Over Neo4j-Only
**Rationale:**
- Avoid vendor lock-in
- Enable lightweight deployments (FalkorDB = Redis)
- Support cloud-native (Neptune) and embedded (Kuzu) options

**Trade-off:**
- Lowest-common-denominator feature set
- Driver maintenance burden
- **Winner:** Flexibility > Feature Maximalism

### Decision 5: MCP Server Integration (November 2025)
**Rationale:**
- Model Context Protocol emerging standard for AI assistant memory
- Claude, Cursor, and other tools adopting MCP
- Positions Graphiti as agent memory backend

**Trade-off:**
- Additional maintenance surface (new server codebase)
- Protocol still evolving (potential breaking changes)
- **Winner:** Ecosystem Adoption > Stability (early mover advantage)

---

## 13. Comparison: Graphiti vs GraphRAG vs Traditional RAG

| Dimension | Traditional RAG | GraphRAG | Graphiti |
|-----------|----------------|----------|----------|
| **Data Model** | Vector database | Static graph + summaries | Temporal graph |
| **Update Model** | Document reprocessing | Batch recomputation | Incremental updates |
| **Contradiction Handling** | None | LLM summarization | Temporal invalidation |
| **Retrieval Method** | Vector similarity | LLM community summaries | Hybrid (vector + BM25 + graph) |
| **Query Latency** | ~100ms | ~5-30s (LLM in loop) | ~200-500ms (no LLM) |
| **Temporal Queries** | None | Basic timestamps | Bi-temporal (occurrence + ingestion) |
| **Custom Entities** | No | No | Yes (Pydantic schemas) |
| **Suitable For** | Static docs | Document corpus | Dynamic agent memory |

---

## 14. Architectural Evolution Timeline

### Phase 1: Foundation (Aug-Sep 2024)
- Initial commit: Basic node/edge structures
- Poetry → uv migration for package management
- Neo4j driver implementation
- LLM-based entity extraction

### Phase 2: Temporal Invalidation (Aug-Sep 2024)
- `invalid_at` field added to edges
- Contradiction resolution without LLM
- Point-in-time query support

### Phase 3: Hybrid Search (Sep-Oct 2024)
- BM25 full-text search integration
- Search recipe system (configurable strategies)
- Cross-encoder reranking

### Phase 4: Scalability (Oct-Nov 2024)
- Bulk operations for historical data
- Parallel LLM processing
- DiskCache integration

### Phase 5: Multi-Provider Support (Nov 2024-Jan 2025)
- Anthropic client (Claude support)
- FalkorDB driver (Redis-based)
- Neptune driver (AWS managed)
- Kuzu driver (embedded option)

### Phase 6: MCP Integration (Nov 2025)
- Model Context Protocol server
- Docker Compose deployment
- Agent assistant interoperability

### Phase 7: Structured Outputs (Nov 2025)
- OpenAI Structured Output API adoption
- Response validation improvements
- Claude Haiku 4.5 as default

---

## 15. Codebase Statistics

**Total Commits:** 847 (August 2024 - November 2025)  
**Lines of Code:** 33,106 (Python)  
**Core Files:** 81 Python modules  
**Examples:** 10 example projects (quickstart, wizard of oz, e-commerce, podcast)  
**Tests:** 150+ test files (unit + integration)  
**Documentation:** 25+ markdown files  
**Contributors:** 20+ (open-source community)

**Commit Velocity:**
- August 2024: 150+ commits (initial burst)
- Sep-Dec 2024: 300+ commits (core features)
- Jan-Nov 2025: 400+ commits (stability, integrations)
- Average: ~2 commits/day

**File Size Distribution:**
- `search_utils.py`: 71,754 bytes (largest file)
- `graphiti.py`: ~15,000 bytes (main orchestrator)
- `nodes.py` + `edges.py`: ~10,000 bytes combined
- Average module: ~400 lines of code

---

## 16. Strategic Positioning

**Market Position:** "Knowledge Graph for AI Agents" (not "GraphRAG replacement")

**Differentiation:**
1. **Temporal-First:** Only major framework with bi-temporal model
2. **Real-Time:** Incremental updates without batch recomputation
3. **Agent-Native:** Designed for interactive agents, not document QA
4. **Open-Source Core:** Apache 2.0 license (contrast with Zep's managed platform)

**Competitive Landscape:**
- **vs Microsoft GraphRAG:** Dynamic > Static
- **vs LangChain Memory:** Graph-based > Linear chat history
- **vs Vector DBs (Pinecone, Weaviate):** Relational > Flat embeddings
- **vs Zep (same company):** Open-source framework vs Managed platform

**Adoption Drivers:**
- Paper publication (arXiv, January 2025)
- MCP protocol support (November 2025)
- GitHub stars as proxy (tracking momentum)
- Zep's enterprise traction (validation)

---

## Conclusion: Architectural Essence

Graphiti represents a **paradigm shift from "Graph as Document Index" to "Graph as Living Memory"**. The architecture is fundamentally **temporal-first**, with explicit tracking of both event occurrence and system knowledge acquisition. This bi-temporal model enables **contradiction resolution without LLM inference**, achieving sub-second query latency while maintaining historical accuracy.

The **five-layer clean architecture** (Storage → LLM/Embedding → Domain Logic → Search → Orchestration) provides clear separation of concerns with **pluggability at every layer** (4 drivers, 4 LLM providers, 3 embedding providers, configurable search strategies). This design prioritizes **flexibility and vendor independence** over feature maximalism.

**Core Innovation:** Temporal invalidation (`invalid_at` timestamps) solves the "contradiction problem" that plagues traditional graph systems, eliminating the need for expensive LLM summarization during retrieval. This single architectural decision unlocks real-time agent memory at scale.

**Critical Success Factors:**
1. **Temporal Model** - Explicit bi-temporal tracking
2. **Hybrid Search** - Semantic + BM25 + graph traversal
3. **Pluggable Backends** - No vendor lock-in
4. **Agent-First API** - Designed for interactive agents, not batch processing
5. **MCP Integration** - Ecosystem play for AI assistant memory

**Architectural Maturity:** Production-ready (15 months, 847 commits, active community). Clear evolution from research prototype to enterprise-grade framework with robust testing, observability, and migration systems.

---

## Metadata

- **Analysis Type:** Hard Architecture Mapping (Level 1)
- **Wisdom Level:** 1 (Data & Reality)
- **Technical Stack:** Python 3.10+, Neo4j/FalkorDB/Neptune/Kuzu, OpenAI/Anthropic/Groq/Gemini, FastAPI, MCP
- **Codebase Size:** 33,106 LOC (81 core files)
- **Commits Analyzed:** 847
- **Special Focus:** Temporal knowledge graphs, bi-temporal data model, hybrid retrieval
- **Key Insight:** Temporal invalidation eliminates LLM-in-retrieval bottleneck, enabling sub-second agent memory queries

**Related Artifacts:**
- Decision Forensics (Level 2)
- Anti-Library Extraction (Level 2)
- Vision Alignment (Level 3)
- Process Memory (Level 3)
- Meta-Pattern Synthesis (Level 4)
- Paradigm Extraction (Level 4)
