# Example Manifest Entries

This file demonstrates how to map the internal **Process Memory Protocol** and **Wisdom Ladder** artifacts into the `manifest.json` schema.

## 1. Process Memory Entry (Mapped)
*Note how `type` is "StrategicDecision" in metadata, but "process_memory" in the root type.*

```json
{
  "id": "jwt-decision-validation-2025-11-18",
  "title": "Validate JWT Architecture for Mobile Support",
  "date": "2025-11-18",
  "type": "process_memory",
  "path": "/process_memory/2025-11-18-jwt-decision-validation.md",
  "description": "Confirmed JWT architecture is required for Mobile support; rejected pivot to Session Cookies.",
  "tags": ["authentication", "jwt", "mobile", "decision-forensics"],
  "author": "Claude-3.5-Sonnet",
  "status": "complete",
  "related": ["auth-jwt-decision-forensics-2025-11-18"],
  "strategic_context": "Switching to Session Cookies would break the React Native app or force a dual-stack auth system.",
  "metadata": {
    "protocol_type": "StrategicDecision",
    "confidence": 0.95,
    "phase": "Review",
    "source_adr": "[https://github.com/example/auth-service/blob/main/docs/adr/003-jwt-auth.md](https://github.com/example/auth-service/blob/main/docs/adr/003-jwt-auth.md)"
  }
}
```

## 2. Strategic Backlog Entry (Paradigm Shift)
*Used for capturing Cultural or Mental Model shifts.*

```json
{
  "id": "paradigm-shift-documentation-2025-11-18",
  "title": "Strategic Shift: From 'Code is Self-Documenting' to 'Context is King'",
  "date": "2025-11-18",
  "type": "backlog",
  "path": "/backlog/2025-11-18-paradigm-shift-documentation.md",
  "description": "Initiative to mandate 'Why' documentation (ADRs/Context) alongside code, as 'Self-Documenting' code failed to explain the JWT constraint.",
  "tags": ["paradigm-shift", "culture", "documentation", "knowledge-management"],
  "author": "Claude-3.5-Sonnet",
  "status": "open",
  "related": ["jwt-decision-validation-2025-11-18"],
  "strategic_context": "The team wasted 3 days debating JWT because the 'Why' wasn't documented. We must shift culture to value Context over Brevity.",
  "metadata": {
    "type": "Strategic Realignment",
    "priority": "High",
    "target_paradigm": "Context is King"
  }
}
```

## 3. Long-Form Distillation (Wisdom Ladder)
*Shows a Level 4 analysis entry.*

```json
{
  "id": "auth-service-philosophy-2025-11-18",
  "title": "Conceptual Distillation: The Philosophy of Auth Service",
  "date": "2025-11-18",
  "type": "distillation",
  "path": "/distillations/2025-11-18-auth-service-philosophy.md",
  "description": "Comprehensive distillation of the Auth Service, identifying the 'Mobile-First' root metaphor and the 'Stateless' mental model.",
  "tags": ["distillation", "wisdom", "auth", "philosophy"],
  "author": "Claude-3.5-Sonnet",
  "status": "complete",
  "related": ["jwt-decision-validation-2025-11-18", "auth-architecture-map-2025-11-18"],
  "strategic_context": "Needed to align new team members with the hidden constraints of the system.",
  "metadata": {
    "investigation_level": "Level 4 (Wisdom)",
    "root_metaphor": "The Gatekeeper",
    "archetypes_identified": ["Shifting the Burden"]
  }
}
```
