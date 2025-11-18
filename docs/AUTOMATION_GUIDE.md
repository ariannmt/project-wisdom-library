# Automation Guide: Issue-Driven Wisdom Workflow

This guide provides the implementation logic for the **System Owner Agent** to execute autonomous investigations triggered by the `intake.yml` Issue Form.

---

## Core Logic: The Autonomous Loop

The workflow is **Stateless** and **Atomic**. The agent reads the Issue, performs the work, and delivers the PR in one continuous execution.

### 1. Intake & Parsing Logic
*Instead of chatting, the agent parses the Issue Body.*

```python
def parse_issue_context(issue_body):
    # Extract the "Wisdom Ladder" parameters
    target = extract_field(issue_body, "Target")
    context = extract_field(issue_body, "Strategic & Subjective Context")
    menu_items = extract_checkboxes(issue_body, "Requested Menu Items")
    
    # Determine the Abstraction Level
    if "Meta-Pattern Synthesis" in menu_items:
        level = "Level 4 (Wisdom)"
    elif "Process Memory" in menu_items:
        level = "Level 3 (Knowledge)"
    else:
        level = "Level 1-2 (Data/Info)"
        
    return target, context, menu_items, level
```

### 2. The "Wisdom Ladder" Execution Strategy
*The agent must execute analyses in a specific dependency order.*

1.  **Establish Ground Truth (Level 1):**
    * Run `Hard Architecture Mapping` first.
    * *Output:* "The system *is* X."
2.  **Extract History (Level 2):**
    * Run `Decision Forensics` and `Anti-Library`.
    * *Output:* "The system became X because we rejected Y."
3.  **Synthesize Wisdom (Level 4):**
    * *Constraint:* You cannot define a "Paradigm" (Level 4) without citing a "Rejected Alternative" (Level 2).
    * *Output:* "The system values 'Speed' over 'Consistency'."

### 3. Protocol-to-Manifest Mapping
*Crucial: Translating Internal Memory to External Catalogue.*

When saving a `Process Memory` file, the agent must perform this transformation before updating `manifest.json`:

```python
def map_protocol_to_manifest(memory_json_block):
    manifest_entry = {
        "id": memory_json_block['id'],
        "title": memory_json_block['title'],
        "type": "process_memory", # Always generic in root
        "strategic_context": memory_json_block['rationale'], # Semantic Map
        "related": memory_json_block['links'],
        "metadata": {
            # Preserve granularity in metadata
            "protocol_type": memory_json_block['type'], # e.g. StrategicDecision
            "confidence": memory_json_block['confidence_level'],
            "phase": memory_json_block['phase']
        }
    }
    return manifest_entry
```

### 4. Strategic Backlog Generation
*Handling "Paradigm Shifts" as actionable items.*

If the analysis identifies a **Paradigm Shift** (e.g., "From Monolith to Microservices"):
1.  Do **NOT** use the standard bug template.
2.  Use `templates/STRATEGIC_BACKLOG_TEMPLATE.md`.
3.  Tag it as `paradigm-shift`.
4.  Link it to the **Process Memory** that justifies it.

---

## Error Handling & Resilience

* **Missing Context:** If the User left the "Strategic Context" blank in the Issue, the Agent must halt and comment on the Issue: *"Cannot proceed. Holistic System Thinking requires subjective context. Please update the Issue."*
* **Invalid JSON:** If the generated Process Memory JSON fails validation, the Agent must retry generation before saving.

---

**This guide ensures the Agent acts as a "System Owner," enforcing structure and meaning rather than just generating text.**
