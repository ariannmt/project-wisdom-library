# Example Manifest Entries

This file demonstrates proper manifest.json entries for the example artifacts.

## Example Atomic Analysis Entry

```json
{
  "id": "auth-jwt-decision-forensics-2025-11-18",
  "title": "Authentication Service: JWT Implementation Decision Forensics",
  "date": "2025-11-18",
  "type": "atomic",
  "path": "/atomic/2025-11-18-auth-jwt-decision-forensics.md",
  "description": "Investigation of why JWT was chosen over session-based authentication, examining trade-offs and implementation rationale with focus on mobile requirements.",
  "tags": ["authentication", "jwt", "decision-forensics", "security", "architecture", "mobile", "scalability"],
  "analysis_type": "decision-forensics",
  "target": "https://github.com/example/auth-service",
  "target_type": "repository",
  "author": "Claude-3.5-Sonnet",
  "status": "complete",
  "related": ["architecture-mapping-auth-service-2025-11-15"],
  "process_memory_refs": ["security-audit-session-2025-11-18"],
  "strategic_context": "Part of Q4 security certification preparation",
  "ripple_effects": [
    "Token refresh complexity identified as expected trade-off",
    "Documentation gap creates risk of future questioning",
    "Monitoring capabilities need enhancement"
  ]
}
```

## Example Process Memory Entry

```json
{
  "id": "security-audit-session-2025-11-18",
  "title": "Process Memory: Security Audit Session - JWT Analysis",
  "date": "2025-11-18",
  "type": "process_memory",
  "path": "/process_memory/2025-11-18-security-audit-session.md",
  "description": "Strategic decisions and insights from JWT authentication analysis, documenting team uncertainties resolved and knowledge management patterns identified.",
  "tags": ["process-memory", "authentication", "knowledge-management", "strategic-decisions"],
  "analysis_type": "process-memory",
  "author": "Claude-3.5-Sonnet",
  "status": "complete",
  "related": ["auth-jwt-decision-forensics-2025-11-18"],
  "strategic_context": "Q4 security certification; revealed institutional knowledge risk",
  "ripple_effects": [
    "Identified pattern: ADRs miss implementation context",
    "Need for similar forensics on other decisions",
    "Knowledge transfer gap when architects leave"
  ]
}
```

## Example Backlog Item Entry

```json
{
  "id": "update-adr-003-jwt-context-2025-11-18",
  "title": "Backlog: Update ADR-003 with Full JWT Decision Context",
  "date": "2025-11-18",
  "type": "backlog",
  "path": "/backlog/2025-11-18-update-adr-003-jwt-context.md",
  "description": "Enhance ADR-003 with complete context from PR discussions and issues to preserve architectural rationale for future team members.",
  "tags": ["backlog", "documentation", "adr", "knowledge-management"],
  "analysis_type": "backlog-idea",
  "author": "Claude-3.5-Sonnet",
  "status": "open",
  "related": ["auth-jwt-decision-forensics-2025-11-18"],
  "strategic_context": "High priority for knowledge preservation",
  "metadata": {
    "priority": "high",
    "estimated_effort": "2-4 hours",
    "type": "documentation"
  }
}
```

## Example Idea Entry

```json
{
  "id": "mobile-architecture-influence-study-2025-11-18",
  "title": "Idea: Study Mobile-First Architecture Influence Patterns",
  "date": "2025-11-18",
  "type": "idea",
  "path": "/ideas/2025-11-18-mobile-architecture-influence-study.md",
  "description": "Investigate how mobile app requirements have influenced backend architecture decisions across the codebase, potentially revealing system-wide patterns.",
  "tags": ["idea", "mobile", "architecture", "meta-pattern"],
  "analysis_type": "custom",
  "author": "Claude-3.5-Sonnet",
  "status": "new",
  "related": ["auth-jwt-decision-forensics-2025-11-18"],
  "strategic_context": "Could reveal architectural principles for future decisions",
  "metadata": {
    "potential_impact": "medium-high",
    "investigation_type": "meta-pattern-synthesis"
  }
}
```

## Full Manifest Structure Example

```json
{
  "atomic": [
    {
      "id": "auth-jwt-decision-forensics-2025-11-18",
      "title": "Authentication Service: JWT Implementation Decision Forensics",
      "date": "2025-11-18",
      "type": "atomic",
      "path": "/atomic/2025-11-18-auth-jwt-decision-forensics.md",
      "description": "Investigation of why JWT was chosen over session-based authentication.",
      "tags": ["authentication", "jwt", "decision-forensics", "security"],
      "analysis_type": "decision-forensics",
      "target": "https://github.com/example/auth-service",
      "target_type": "repository",
      "author": "Claude-3.5-Sonnet",
      "status": "complete",
      "related": [],
      "process_memory_refs": ["security-audit-session-2025-11-18"]
    }
  ],
  "distillations": [],
  "process_memory": [
    {
      "id": "security-audit-session-2025-11-18",
      "title": "Process Memory: Security Audit Session - JWT Analysis",
      "date": "2025-11-18",
      "type": "process_memory",
      "path": "/process_memory/2025-11-18-security-audit-session.md",
      "description": "Strategic decisions and insights from JWT authentication analysis.",
      "tags": ["process-memory", "authentication", "knowledge-management"],
      "analysis_type": "process-memory",
      "author": "Claude-3.5-Sonnet",
      "status": "complete",
      "related": ["auth-jwt-decision-forensics-2025-11-18"]
    }
  ],
  "analyses": [],
  "ideas": [
    {
      "id": "mobile-architecture-influence-study-2025-11-18",
      "title": "Idea: Study Mobile-First Architecture Influence Patterns",
      "date": "2025-11-18",
      "type": "idea",
      "path": "/ideas/2025-11-18-mobile-architecture-influence-study.md",
      "description": "Investigate how mobile requirements influenced backend decisions.",
      "tags": ["idea", "mobile", "architecture", "meta-pattern"],
      "analysis_type": "custom",
      "author": "Claude-3.5-Sonnet",
      "status": "new",
      "related": ["auth-jwt-decision-forensics-2025-11-18"]
    }
  ],
  "backlog": [
    {
      "id": "update-adr-003-jwt-context-2025-11-18",
      "title": "Backlog: Update ADR-003 with Full JWT Decision Context",
      "date": "2025-11-18",
      "type": "backlog",
      "path": "/backlog/2025-11-18-update-adr-003-jwt-context.md",
      "description": "Enhance ADR-003 with complete context for future reference.",
      "tags": ["backlog", "documentation", "adr"],
      "analysis_type": "backlog-idea",
      "author": "Claude-3.5-Sonnet",
      "status": "open",
      "metadata": {
        "priority": "high"
      }
    }
  ],
  "sensitive": []
}
```

## Notes on These Examples

### Cross-Linking Demonstrated
- Atomic analysis references process memory entry
- Process memory references atomic analysis (bidirectional)
- Backlog and idea items reference originating analysis
- All maintain referential integrity

### Metadata Usage
- Backlog items include priority and effort estimates
- Ideas include potential impact and investigation type
- All entries include strategic context where relevant

### Tag Patterns
- Mix of type tags (authentication, jwt) and methodology tags (decision-forensics)
- Process memory includes "process-memory" tag for easy filtering
- Consistent lowercase, hyphenated format

### Status Tracking
- Completed investigations marked as "complete"
- Backlog items marked as "open"
- Ideas marked as "new"
- Enables workflow management

These examples demonstrate the complete artifact lifecycle from investigation through process memory capture and actionable follow-up items.
