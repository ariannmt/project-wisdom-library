# Manifest Schema Documentation

This document defines the schema for `/catalogue/manifest.json`, which serves as the machine-readable catalogue of all artifacts in the Project Wisdom Library.

---

## Purpose

The manifest provides:
- Structured metadata for all artifacts
- Cross-linking between related investigations
- Searchable and filterable catalogue
- JSON-based querying capabilities
- Automated index generation support

---

## Root Schema

```json
{
  "atomic": [],
  "distillations": [],
  "process_memory": [],
  "analyses": [],
  "ideas": [],
  "backlog": [],
  "sensitive": []
}
```

Each top-level key contains an array of artifact entries.

---

## Artifact Entry Schema

### Required Fields

```json
{
  "id": "string",
  "title": "string",
  "date": "YYYY-MM-DD",
  "type": "string",
  "path": "string"
}
```

### Full Schema with Optional Fields

```json
{
  "id": "unique-identifier",
  "title": "Human-readable title",
  "date": "YYYY-MM-DD",
  "type": "atomic|distillation|process_memory|analysis|idea|backlog|sensitive",
  "path": "/folder/YYYY-MM-DD-filename.md",
  "description": "Brief description of the artifact (1-2 sentences)",
  "tags": ["tag1", "tag2", "tag3"],
  "analysis_type": "decision-forensics|architecture-mapping|anti-library|vision-alignment|sentiment|meta-pattern|process-memory|backlog-idea|custom",
  "target": "Repository URL or Document Name",
  "target_type": "repository|document|other",
  "author": "Agent name or human contributor",
  "status": "complete|in-progress|escalated|requires-followup",
  "related": ["artifact-id-1", "artifact-id-2"],
  "parent": "artifact-id-for-escalated-analyses",
  "children": ["artifact-id-1", "artifact-id-2"],
  "process_memory_refs": ["pm-id-1", "pm-id-2"],
  "sensitivity": "public|internal|confidential",
  "strategic_context": "Brief note on strategic importance",
  "ripple_effects": ["effect-1", "effect-2"],
  "metadata": {
    "custom_field_1": "value",
    "custom_field_2": "value"
  }
}
```

---

## Field Definitions

### Core Fields

#### `id` (required)
- Type: `string`
- Format: `kebab-case-unique-identifier`
- Example: `"auth-service-decision-forensics-2025-11-18"`
- Purpose: Unique identifier for cross-referencing
- Generation: `{analysis-type}-{brief-descriptor}-{YYYY-MM-DD}` or custom

#### `title` (required)
- Type: `string`
- Example: `"Authentication Service: Decision Forensics on JWT Implementation"`
- Purpose: Human-readable display name
- Length: Recommended 50-100 characters

#### `date` (required)
- Type: `string`
- Format: `YYYY-MM-DD` (ISO 8601 date)
- Example: `"2025-11-18"`
- Purpose: Creation/completion date for temporal sorting

#### `type` (required)
- Type: `string`
- Enum: `atomic`, `distillation`, `process_memory`, `analysis`, `idea`, `backlog`, `sensitive`
- Purpose: Primary categorization matching folder structure

#### `path` (required)
- Type: `string`
- Format: Relative path from repository root
- Example: `"/atomic/2025-11-18-auth-decision-forensics.md"`
- Purpose: File location for retrieval

### Descriptive Fields

#### `description`
- Type: `string`
- Example: `"Analysis of JWT vs session-based authentication decision, examining trade-offs and implementation rationale."`
- Purpose: Brief summary for catalogue display
- Length: 1-3 sentences, ~100-200 characters

#### `tags`
- Type: `array` of `string`
- Example: `["authentication", "jwt", "security", "decision-forensics", "backend"]`
- Purpose: Categorization and searchability
- Format: lowercase, kebab-case for multi-word tags
- Recommended: 3-10 tags per artifact

#### `analysis_type`
- Type: `string`
- Enum: `decision-forensics`, `architecture-mapping`, `anti-library`, `vision-alignment`, `sentiment`, `meta-pattern`, `process-memory`, `backlog-idea`, `custom`, `other`
- Purpose: Specific methodology used
- Note: May differ from `type` (e.g., type=`atomic`, analysis_type=`decision-forensics`)

### Target Information

#### `target`
- Type: `string`
- Example: `"https://github.com/example/auth-service"` or `"System Architecture Document v2.3"`
- Purpose: Identifies what was analyzed

#### `target_type`
- Type: `string`
- Enum: `repository`, `document`, `codebase`, `system`, `other`
- Purpose: Categorizes target for filtering

### Authorship

#### `author`
- Type: `string`
- Example: `"Claude-3.5-Sonnet"` or `"GitHub Copilot"` or `"Human: John Doe"`
- Purpose: Attribution and provenance
- Format: `{agent-name}` or `Human: {name}`

#### `status`
- Type: `string`
- Enum: `complete`, `in-progress`, `escalated`, `requires-followup`, `archived`
- Purpose: Track investigation state
- Default: `complete`

### Relationship Fields

#### `related`
- Type: `array` of `string`
- Example: `["auth-architecture-mapping-2025-11-15", "security-audit-2025-11-10"]`
- Purpose: Bidirectional links to related artifacts
- Contains: Artifact IDs of related investigations

#### `parent`
- Type: `string` (artifact ID)
- Example: `"auth-atomic-analysis-2025-11-17"`
- Purpose: Link to parent investigation (for escalated analyses)
- Used when: Atomic investigation escalates to long-form

#### `children`
- Type: `array` of `string`
- Example: `["auth-deep-dive-2025-11-19", "auth-security-review-2025-11-20"]`
- Purpose: Link to child/follow-up investigations
- Inverse of `parent` field

#### `process_memory_refs`
- Type: `array` of `string`
- Example: `["strategic-session-2025-11-18", "pivot-decision-2025-11-17"]`
- Purpose: Link to associated process memory entries
- Contains: Process memory artifact IDs

### Strategic Fields

#### `sensitivity`
- Type: `string`
- Enum: `public`, `internal`, `confidential`
- Default: `public`
- Purpose: Access control and handling guidance

#### `strategic_context`
- Type: `string`
- Example: `"Critical for Q4 security certification"`
- Purpose: Capture strategic importance or urgency

#### `ripple_effects`
- Type: `array` of `string`
- Example: `["May require API changes", "Team training needed", "Documentation update required"]`
- Purpose: Document downstream impacts or considerations

### Extension Field

#### `metadata`
- Type: `object`
- Purpose: Custom fields for specific use cases
- Example:
  ```json
  "metadata": {
    "repository_stars": 1234,
    "investigation_duration_hours": 3.5,
    "stakeholder": "Engineering Leadership",
    "milestone": "Q4-Security-Audit"
  }
  ```

---

## Example Entries

### Atomic Analysis Entry

```json
{
  "id": "auth-jwt-decision-forensics-2025-11-18",
  "title": "Authentication Service: JWT Implementation Decision Forensics",
  "date": "2025-11-18",
  "type": "atomic",
  "path": "/atomic/2025-11-18-auth-jwt-decision-forensics.md",
  "description": "Investigation of why JWT was chosen over session-based authentication, examining trade-offs and implementation considerations.",
  "tags": ["authentication", "jwt", "security", "decision-forensics", "api"],
  "analysis_type": "decision-forensics",
  "target": "https://github.com/example/auth-service",
  "target_type": "repository",
  "author": "Claude-3.5-Sonnet",
  "status": "complete",
  "related": ["auth-architecture-map-2025-11-15"],
  "process_memory_refs": ["security-audit-session-2025-11-18"],
  "strategic_context": "Part of Q4 security certification preparation",
  "ripple_effects": ["Token refresh strategy needs documentation", "Mobile app impact noted"]
}
```

### Long-Form Distillation Entry

```json
{
  "id": "microservices-architecture-comprehensive-2025-11-18",
  "title": "Microservices Platform: Comprehensive Architectural Distillation",
  "date": "2025-11-18",
  "type": "distillation",
  "path": "/distillations/2025-11-18-microservices-architecture-comprehensive.md",
  "description": "Full architectural review covering service coupling, deployment complexity, data flow patterns, and strategic recommendations for platform evolution.",
  "tags": ["microservices", "architecture", "kubernetes", "system-design", "technical-debt"],
  "analysis_type": "architecture-mapping",
  "target": "https://github.com/example/platform",
  "target_type": "repository",
  "author": "Claude-3.5-Sonnet",
  "status": "complete",
  "related": ["service-mesh-analysis-2025-11-10", "deployment-pain-points-2025-11-12"],
  "children": ["service-coupling-deep-dive-2025-11-20"],
  "process_memory_refs": ["architecture-review-insights-2025-11-18"],
  "strategic_context": "Platform scaling challenges for 10x growth in 2026",
  "ripple_effects": [
    "Service mesh adoption recommended",
    "Team structure may need realignment",
    "Observability improvements critical"
  ],
  "metadata": {
    "service_count": 47,
    "investigation_duration_hours": 12,
    "stakeholder": "CTO"
  }
}
```

### Process Memory Entry

```json
{
  "id": "architecture-review-insights-2025-11-18",
  "title": "Process Memory: Architecture Review Strategic Insights",
  "date": "2025-11-18",
  "type": "process_memory",
  "path": "/process_memory/2025-11-18-architecture-review-insights.md",
  "description": "Strategic decisions and insights from microservices architecture review, documenting pivots in understanding and key recommendations.",
  "tags": ["process-memory", "architecture", "strategic-decisions"],
  "analysis_type": "process-memory",
  "author": "Claude-3.5-Sonnet",
  "status": "complete",
  "related": ["microservices-architecture-comprehensive-2025-11-18"],
  "strategic_context": "Captured major pivot in deployment strategy understanding",
  "ripple_effects": ["Changed approach to service mesh evaluation"]
}
```

### Backlog Item Entry

```json
{
  "id": "implement-service-mesh-backlog-2025-11-18",
  "title": "Backlog: Implement Service Mesh for Observability",
  "date": "2025-11-18",
  "type": "backlog",
  "path": "/backlog/2025-11-18-implement-service-mesh.md",
  "description": "Action item to evaluate and implement service mesh for improved observability and traffic management across microservices.",
  "tags": ["backlog", "service-mesh", "observability", "infrastructure"],
  "analysis_type": "backlog-idea",
  "author": "Claude-3.5-Sonnet",
  "status": "open",
  "related": ["microservices-architecture-comprehensive-2025-11-18"],
  "strategic_context": "High priority for Q1 2026",
  "metadata": {
    "priority": "high",
    "estimated_effort": "6-8 weeks",
    "dependencies": ["kubernetes-upgrade"]
  }
}
```

### Idea Entry

```json
{
  "id": "api-gateway-consolidation-idea-2025-11-18",
  "title": "Idea: Consolidate API Gateways",
  "date": "2025-11-18",
  "type": "idea",
  "path": "/ideas/2025-11-18-api-gateway-consolidation.md",
  "description": "Consideration to consolidate three separate API gateways into unified platform for simplified management.",
  "tags": ["idea", "api-gateway", "simplification", "architecture"],
  "analysis_type": "backlog-idea",
  "author": "Claude-3.5-Sonnet",
  "status": "new",
  "related": ["microservices-architecture-comprehensive-2025-11-18"],
  "strategic_context": "Potential simplification opportunity",
  "metadata": {
    "potential_impact": "medium",
    "risk_level": "medium"
  }
}
```

---

## Validation Rules

### Required Field Validation
- All required fields must be present
- No null values for required fields
- Empty strings not allowed for required fields

### Type Constraints
- `date` must match `YYYY-MM-DD` format
- `type` must be one of allowed enum values
- `path` must start with `/` and end with `.md` (or `.json` for process memory JSON)
- `tags` array must contain at least 1 tag
- `related`, `children`, `process_memory_refs` must be arrays (can be empty)

### ID Uniqueness
- Each `id` must be unique across entire manifest
- Recommended format: `{descriptor}-{date}` for uniqueness

### Relationship Integrity
- IDs referenced in `related`, `parent`, `children`, `process_memory_refs` should exist in manifest
- Bidirectional links should be maintained (if A references B, B should reference A)

### Path Consistency
- `path` should match `type` folder:
  - `type: "atomic"` → `path: "/atomic/..."`
  - `type: "distillation"` → `path: "/distillations/..."`
  - etc.

---

## Automated Maintenance

### On Artifact Creation
1. Generate unique ID
2. Populate required fields
3. Add entry to appropriate array in manifest
4. Update `related` artifacts to reference new artifact
5. Validate JSON schema
6. Regenerate `/catalogue/index.md`

### On Artifact Update
1. Update manifest entry
2. Maintain ID (never change)
3. Update date if substantial changes
4. Update relationships if needed
5. Validate JSON schema

### On Artifact Deletion
1. Remove manifest entry
2. Update all `related` references in other artifacts
3. Consider archiving rather than deleting

---

## Query Examples

### Find all atomic analyses on authentication:
```javascript
manifest.atomic.filter(item => 
  item.tags.includes('authentication')
)
```

### Find all artifacts related to a specific analysis:
```javascript
const id = 'auth-jwt-decision-forensics-2025-11-18';
Object.values(manifest).flat().filter(item =>
  item.related && item.related.includes(id)
)
```

### Find all incomplete investigations:
```javascript
Object.values(manifest).flat().filter(item =>
  item.status && item.status !== 'complete'
)
```

### Find all artifacts from last 7 days:
```javascript
const cutoff = new Date();
cutoff.setDate(cutoff.getDate() - 7);
const cutoffStr = cutoff.toISOString().split('T')[0];

Object.values(manifest).flat().filter(item =>
  item.date >= cutoffStr
)
```

---

## Schema Evolution

### Adding New Fields
- Add to optional fields section
- Document purpose and format
- Update examples
- Maintain backward compatibility

### Deprecating Fields
- Mark as deprecated in documentation
- Maintain in schema for compatibility
- Provide migration guidance
- Set removal timeline

### Version Management
Consider adding schema version:
```json
{
  "schema_version": "1.0.0",
  "atomic": [],
  ...
}
```

---

## Best Practices

1. **Consistency**: Use consistent naming patterns for IDs and tags
2. **Completeness**: Fill optional fields when information is available
3. **Relationships**: Always maintain bidirectional links
4. **Tags**: Use 3-10 relevant tags per artifact
5. **Descriptions**: Write clear, concise descriptions (100-200 chars)
6. **Validation**: Validate JSON before committing
7. **Updates**: Keep manifest synchronized with file system
8. **Documentation**: Update this schema doc when adding custom fields

---

## Tools and Scripts

### Recommended Tools
- JSON schema validators
- Automated manifest generators
- Cross-reference checkers
- Duplicate ID detectors
- Broken link identifiers

### Future Automation
- Pre-commit hooks for validation
- CI/CD checks for schema compliance
- Automated relationship discovery
- Index generation from manifest
- Search/filter web interface

---

**This schema enables rich, queryable metadata while maintaining simplicity and flexibility for diverse artifact types.**
