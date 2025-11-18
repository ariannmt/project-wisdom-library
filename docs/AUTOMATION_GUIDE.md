# Automation Guide for Wisdom Library Agents

This guide provides implementation patterns and automation strategies for AI agents working with the Project Wisdom Library.

---

## Overview

The Wisdom Library is designed for **autonomous AI agent operation** with **human strategic oversight**. This guide helps agents implement efficient, consistent workflows.

---

## Core Automation Principles

### 1. Stateless Operation
Each agent invocation should be self-contained:
- Read current state from repository
- Perform operations
- Update state (manifest, index, artifacts)
- Commit changes atomically

### 2. Idempotency
Operations should be repeatable:
- File creation should check existence first
- Manifest updates should deduplicate
- Index regeneration should be deterministic
- IDs should be deterministic where possible

### 3. Validation
Always validate before committing:
- JSON schema validation for manifest
- Template compliance for artifacts
- Cross-reference integrity
- File path consistency

### 4. Graceful Degradation
Handle errors without breaking workflow:
- If catalogue update fails, still save artifact
- If cross-link fails, document in process memory
- If template is incomplete, flag for human review
- Always save work, even if imperfect

---

## Automated Workflows

### Workflow 1: Single Artifact Creation

```
1. Receive user input (target, context, analysis type)
2. Execute analysis
3. Generate artifact from template
4. Create unique ID
5. Save artifact to appropriate folder
6. Update manifest.json with new entry
7. Regenerate catalogue/index.md
8. Commit changes
9. Prepare PR description
```

**Implementation Pattern:**
```python
def create_artifact(analysis_data, artifact_type):
    # 1. Generate unique ID
    artifact_id = generate_id(analysis_data)
    
    # 2. Fill template
    artifact_content = fill_template(artifact_type, analysis_data)
    
    # 3. Save to file
    file_path = f"/{artifact_type}/{date}-{descriptor}.md"
    save_file(file_path, artifact_content)
    
    # 4. Update manifest
    manifest_entry = create_manifest_entry(artifact_id, analysis_data, file_path)
    add_to_manifest(artifact_type, manifest_entry)
    
    # 5. Update index
    regenerate_index()
    
    # 6. Return artifact info for PR
    return artifact_id, file_path
```

### Workflow 2: Multi-Artifact Investigation

```
1. Receive user input
2. Execute multiple analyses
3. Create primary artifact (atomic or distillation)
4. Create process memory entry
5. Create backlog items if needed
6. Create idea notes if needed
7. Update manifest for all artifacts
8. Cross-link all related artifacts
9. Regenerate index
10. Commit all changes
11. Prepare comprehensive PR
```

**Implementation Pattern:**
```python
def multi_artifact_investigation(user_input, analysis_types):
    artifacts_created = []
    
    # Primary analysis
    primary_artifact = create_artifact(primary_analysis_data, primary_type)
    artifacts_created.append(primary_artifact)
    
    # Process memory if warranted
    if has_strategic_insights(primary_analysis_data):
        pm_artifact = create_process_memory(primary_analysis_data, primary_artifact)
        artifacts_created.append(pm_artifact)
    
    # Backlog items
    for backlog_item in extract_backlog_items(primary_analysis_data):
        bl_artifact = create_backlog_item(backlog_item, primary_artifact)
        artifacts_created.append(bl_artifact)
    
    # Cross-link everything
    cross_link_artifacts(artifacts_created)
    
    # Update catalogue
    regenerate_index()
    
    return artifacts_created
```

### Workflow 3: Escalation (Atomic to Long-Form)

```
1. Detect escalation need during atomic analysis
2. Prompt user for confirmation
3. Create long-form distillation artifact
4. Link back to original atomic artifact (parent field)
5. Update original atomic artifact with child reference
6. Update manifest for both
7. Continue with expanded investigation
8. Regenerate index
9. Commit changes
```

**Implementation Pattern:**
```python
def escalate_to_longform(atomic_artifact_id, additional_analyses):
    # Load existing atomic artifact
    atomic_artifact = load_artifact(atomic_artifact_id)
    
    # Create longform distillation
    longform_id = f"{atomic_artifact_id}-expanded"
    longform_artifact = create_artifact(
        expanded_analysis_data,
        "distillation"
    )
    
    # Update relationships
    update_manifest_field(longform_id, "parent", atomic_artifact_id)
    update_manifest_field(atomic_artifact_id, "children", [longform_id])
    update_manifest_field(atomic_artifact_id, "status", "escalated")
    
    # Update file with cross-link
    add_cross_link(atomic_artifact, longform_id)
    
    regenerate_index()
    
    return longform_id
```

---

## Key Automation Functions

### ID Generation

```python
def generate_id(analysis_data):
    """
    Generate unique, deterministic ID for artifact
    Format: {analysis-type}-{descriptor}-{date}
    """
    analysis_type = analysis_data['analysis_type'].replace('_', '-')
    descriptor = slugify(analysis_data['title'])[:30]
    date = analysis_data['date']
    
    base_id = f"{analysis_type}-{descriptor}-{date}"
    
    # Ensure uniqueness
    counter = 1
    unique_id = base_id
    while id_exists(unique_id):
        unique_id = f"{base_id}-{counter}"
        counter += 1
    
    return unique_id
```

### Template Filling

```python
def fill_template(template_type, data):
    """
    Fill template with analysis data
    """
    template_path = f"templates/{template_type}_TEMPLATE.md"
    template = load_file(template_path)
    
    # Replace placeholders
    filled = template
    for key, value in data.items():
        placeholder = f"[{key.upper()}]"
        filled = filled.replace(placeholder, str(value))
    
    # Handle arrays (tags, linked artifacts)
    filled = fill_array_fields(filled, data)
    
    return filled
```

### Manifest Updates

```python
def add_to_manifest(artifact_type, entry):
    """
    Add entry to manifest.json
    """
    manifest = load_json("catalogue/manifest.json")
    
    # Validate entry
    validate_manifest_entry(entry)
    
    # Add to appropriate array
    manifest[artifact_type].append(entry)
    
    # Sort by date (newest first)
    manifest[artifact_type].sort(
        key=lambda x: x['date'],
        reverse=True
    )
    
    # Save manifest
    save_json("catalogue/manifest.json", manifest)
```

### Index Regeneration

```python
def regenerate_index():
    """
    Regenerate catalogue/index.md from manifest.json
    """
    manifest = load_json("catalogue/manifest.json")
    
    index_content = "# Index of Wisdom Artifacts\n\n"
    index_content += "*(Auto-generated)*\n\n"
    
    # For each category
    for category, items in manifest.items():
        index_content += f"## {category.title()}\n\n"
        
        if not items:
            index_content += "*No entries yet*\n\n"
            continue
        
        for item in items:
            # Format: - [Title](path) - date - tags
            tags_str = ", ".join(item.get('tags', [])[:5])
            index_content += f"- [{item['title']}]({item['path']}) "
            index_content += f"- {item['date']}"
            if tags_str:
                index_content += f" - `{tags_str}`"
            index_content += "\n"
        
        index_content += "\n"
    
    save_file("catalogue/index.md", index_content)
```

### Cross-Linking

```python
def cross_link_artifacts(artifact_ids):
    """
    Create bidirectional links between related artifacts
    """
    manifest = load_json("catalogue/manifest.json")
    
    # For each pair of artifacts
    for id1 in artifact_ids:
        for id2 in artifact_ids:
            if id1 == id2:
                continue
            
            # Add to related field if not present
            entry1 = find_manifest_entry(manifest, id1)
            if 'related' not in entry1:
                entry1['related'] = []
            if id2 not in entry1['related']:
                entry1['related'].append(id2)
    
    save_json("catalogue/manifest.json", manifest)
```

### Validation

```python
def validate_manifest_entry(entry):
    """
    Validate manifest entry against schema
    """
    required_fields = ['id', 'title', 'date', 'type', 'path']
    
    # Check required fields
    for field in required_fields:
        if field not in entry:
            raise ValueError(f"Missing required field: {field}")
        if not entry[field]:
            raise ValueError(f"Empty required field: {field}")
    
    # Validate date format
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', entry['date']):
        raise ValueError(f"Invalid date format: {entry['date']}")
    
    # Validate type
    valid_types = ['atomic', 'distillation', 'process_memory', 
                   'analysis', 'idea', 'backlog', 'sensitive']
    if entry['type'] not in valid_types:
        raise ValueError(f"Invalid type: {entry['type']}")
    
    # Validate path consistency
    expected_prefix = f"/{entry['type']}/"
    if not entry['path'].startswith(expected_prefix):
        raise ValueError(f"Path doesn't match type: {entry['path']}")
    
    return True
```

---

## Process Memory Automation

### When to Auto-Generate Process Memory

Automatically create process memory when:
- User expresses uncertainty that gets resolved
- Analysis reveals strategic pivot
- Decision point identified during investigation
- Multiple analyses connect in meaningful way
- User provides rich strategic context

```python
def should_create_process_memory(analysis_data, user_context):
    """
    Determine if process memory should be created
    """
    indicators = []
    
    # Check for strategic keywords in user context
    strategic_keywords = ['uncertain', 'decision', 'pivot', 'strategic', 
                         'critical', 'important', 'why']
    if any(kw in user_context.lower() for kw in strategic_keywords):
        indicators.append('strategic_context')
    
    # Check for decision points in analysis
    if 'decisions' in analysis_data and analysis_data['decisions']:
        indicators.append('decisions_made')
    
    # Check for ripple effects
    if 'ripple_effects' in analysis_data and len(analysis_data['ripple_effects']) > 2:
        indicators.append('significant_ripples')
    
    # Check for context change
    if 'context_change' in analysis_data:
        indicators.append('context_pivot')
    
    # Create if 2+ indicators present
    return len(indicators) >= 2
```

### Process Memory Generation

```python
def create_process_memory(analysis_data, primary_artifact_id):
    """
    Generate process memory entry
    """
    pm_data = {
        'date': analysis_data['date'],
        'agents': [analysis_data['author']],
        'strategic_context': extract_strategic_context(analysis_data),
        'session_type': 'analysis',
        'decisions': extract_decisions(analysis_data),
        'artifacts_created': [primary_artifact_id],
        'next_steps': generate_next_steps(analysis_data)
    }
    
    # Create markdown
    pm_md = fill_template('PROCESS_MEMORY', pm_data)
    pm_path = f"/process_memory/{pm_data['date']}-session.md"
    save_file(pm_path, pm_md)
    
    # Create JSON
    pm_json_path = f"/process_memory/{pm_data['date']}-session.json"
    save_json(pm_json_path, pm_data)
    
    # Update manifest
    pm_id = f"process-memory-{pm_data['date']}"
    manifest_entry = create_manifest_entry(pm_id, pm_data, pm_path)
    add_to_manifest('process_memory', manifest_entry)
    
    # Cross-link with primary artifact
    update_manifest_field(primary_artifact_id, 'process_memory_refs', [pm_id])
    
    return pm_id
```

---

## Backlog and Ideas Automation

### Extraction from Analysis

```python
def extract_backlog_items(analysis_data):
    """
    Extract actionable backlog items from analysis
    """
    backlog_items = []
    
    # Look for recommendations
    if 'recommendations' in analysis_data:
        for rec in analysis_data['recommendations']:
            if is_actionable(rec):
                backlog_items.append({
                    'title': extract_title(rec),
                    'description': rec,
                    'priority': estimate_priority(rec),
                    'source_analysis': analysis_data['id']
                })
    
    # Look for technical debt mentions
    if 'technical_debt' in analysis_data:
        for debt in analysis_data['technical_debt']:
            backlog_items.append({
                'title': f"Address: {extract_title(debt)}",
                'description': debt,
                'priority': 'medium',
                'type': 'technical-debt',
                'source_analysis': analysis_data['id']
            })
    
    return backlog_items

def extract_ideas(analysis_data):
    """
    Extract ideas and questions from analysis
    """
    ideas = []
    
    # Look for questions raised
    if 'questions' in analysis_data:
        for question in analysis_data['questions']:
            ideas.append({
                'title': question,
                'type': 'question',
                'source_analysis': analysis_data['id']
            })
    
    # Look for future enhancements mentioned
    if 'future_considerations' in analysis_data:
        for consideration in analysis_data['future_considerations']:
            ideas.append({
                'title': extract_title(consideration),
                'description': consideration,
                'type': 'enhancement',
                'source_analysis': analysis_data['id']
            })
    
    return ideas
```

---

## Error Handling Patterns

### Graceful Failure

```python
def safe_artifact_creation(analysis_data, artifact_type):
    """
    Create artifact with error handling
    """
    try:
        artifact_id = create_artifact(analysis_data, artifact_type)
        return {'success': True, 'artifact_id': artifact_id}
    except Exception as e:
        # Log error
        log_error(f"Artifact creation failed: {e}")
        
        # Save raw data for manual recovery
        save_recovery_file(analysis_data)
        
        # Return partial success
        return {
            'success': False,
            'error': str(e),
            'recovery_file': 'temp/recovery.json',
            'message': 'Analysis data saved for manual artifact creation'
        }
```

### Validation Failures

```python
def safe_manifest_update(entry):
    """
    Update manifest with validation
    """
    try:
        validate_manifest_entry(entry)
        add_to_manifest(entry['type'], entry)
        return {'success': True}
    except ValueError as e:
        # Attempt to fix common issues
        if 'date format' in str(e):
            entry['date'] = fix_date_format(entry['date'])
            return safe_manifest_update(entry)  # Retry
        
        # If can't auto-fix, save for manual review
        save_file('temp/invalid-manifest-entry.json', json.dumps(entry))
        return {
            'success': False,
            'error': str(e),
            'action': 'Manual review required'
        }
```

---

## Performance Optimizations

### Batch Operations

```python
def create_multiple_artifacts(analyses_data):
    """
    Create multiple artifacts efficiently
    """
    results = []
    manifest_updates = []
    
    # Create all artifacts
    for data in analyses_data:
        artifact = create_artifact(data, data['type'])
        results.append(artifact)
        manifest_updates.append(
            create_manifest_entry(artifact['id'], data, artifact['path'])
        )
    
    # Single manifest update
    manifest = load_json("catalogue/manifest.json")
    for update in manifest_updates:
        manifest[update['type']].append(update)
    save_json("catalogue/manifest.json", manifest)
    
    # Single index regeneration
    regenerate_index()
    
    return results
```

### Caching

```python
class ManifestCache:
    """Cache manifest to avoid repeated file I/O"""
    def __init__(self):
        self._manifest = None
        self._dirty = False
    
    def get(self):
        if self._manifest is None:
            self._manifest = load_json("catalogue/manifest.json")
        return self._manifest
    
    def update(self, updates):
        manifest = self.get()
        # Apply updates
        self._dirty = True
    
    def save(self):
        if self._dirty:
            save_json("catalogue/manifest.json", self._manifest)
            self._dirty = False
```

---

## Git Operations

### Atomic Commits

```python
def commit_artifact_creation(artifact_paths):
    """
    Commit new artifacts atomically
    """
    # Stage files
    for path in artifact_paths:
        git_add(path)
    
    # Stage catalogue updates
    git_add("catalogue/manifest.json")
    git_add("catalogue/index.md")
    
    # Commit with descriptive message
    artifact_count = len(artifact_paths)
    commit_message = f"Add {artifact_count} artifact(s): {', '.join(get_titles(artifact_paths))}"
    git_commit(commit_message)
```

### PR Description Generation

```python
def generate_pr_description(artifacts_created):
    """
    Generate PR description from template
    """
    template = load_file(".github/PULL_REQUEST_TEMPLATE.md")
    
    # Fill in sections
    pr_desc = template
    pr_desc = pr_desc.replace(
        "[Atomic/Long-Form]",
        artifacts_created[0]['type'].title()
    )
    
    # Add summary
    summary = "\n".join([
        f"- {a['title']}: {a['description']}"
        for a in artifacts_created
    ])
    pr_desc = pr_desc.replace(
        "- Core insights, metaphors, meta-patterns",
        summary
    )
    
    # Add linked files
    files = "\n".join([
        f"- [{a['path']}]({a['path']})"
        for a in artifacts_created
    ])
    pr_desc = pr_desc.replace(
        "- [All added/modified files with folder links]",
        files
    )
    
    return pr_desc
```

---

## Testing and Validation

### Pre-Commit Checks

```python
def pre_commit_validation():
    """
    Run validation before committing
    """
    checks = []
    
    # Validate manifest JSON
    checks.append(validate_json("catalogue/manifest.json"))
    
    # Check all referenced files exist
    checks.append(validate_file_references())
    
    # Check bidirectional links
    checks.append(validate_cross_references())
    
    # Validate all markdown files
    checks.append(validate_markdown_files())
    
    return all(checks)
```

### Integration Testing

```python
def test_full_workflow():
    """
    Test complete artifact creation workflow
    """
    # Mock user input
    user_input = {
        'target': 'https://github.com/example/repo',
        'context': 'Security audit needed',
        'analysis_type': 'decision-forensics',
        'investigation_type': 'atomic'
    }
    
    # Execute workflow
    result = execute_investigation(user_input)
    
    # Validate results
    assert result['success']
    assert os.path.exists(result['artifact_path'])
    assert artifact_in_manifest(result['artifact_id'])
    assert artifact_in_index(result['artifact_id'])
```

---

## Future Automation Opportunities

### Intelligent Analysis Selection
- ML model to suggest analysis types based on target and context
- Pattern recognition across historical analyses
- Automatic escalation triggers

### Enhanced Cross-Linking
- NLP-based semantic similarity for related artifacts
- Automatic tag generation from content
- Knowledge graph visualization

### Quality Metrics
- Artifact completeness scoring
- Template compliance checking
- Insight density measurement

### Search and Discovery
- Full-text search across all artifacts
- Tag-based filtering
- Timeline visualization
- Relationship graph exploration

---

**This automation guide enables efficient, consistent, and high-quality autonomous operation of the Wisdom Library system.**
