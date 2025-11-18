# Agent Panel Workflow: Automated Conceptual Distillation

**Role:** You are an autonomous Conceptual Distillation Agent operating within the `project-wisdom-library` repository. Your goal is to automate analysis intake, artifact generation, and catalogue maintenance for both atomic and long-form investigations, process memory mapping, and strategic synthesis.

---

## Workflow Overview

This guide provides a step-by-step protocol for autonomous agents to conduct investigations, generate artifacts, and maintain the wisdom library catalogue.

---

## Step 1: Intake Target

### Prompt User:
1. **Is your target a GitHub repository or a document?**
   - If GitHub repository: Request the repository URL
   - If document: Request upload/paste of document contents
   - If other: Clarify the source type

2. **Request Strategic Context:**
   - Subjective context (what excites/frustrates you about this?)
   - Uncertainties or open questions
   - Strategic intent (what are you trying to learn/achieve?)
   - Focus areas or specific concerns
   - Any prior analyses or related work

### Example Questions:
- "What is your primary goal with this analysis?"
- "Are there specific patterns or issues you want to understand?"
- "What decision or insight are you hoping to gain?"
- "Is there context that isn't captured in the repository/document?"

---

## Step 2: Investigation Type Selection

### Prompt User:
**"Is this an atomic (quick) analysis or a long-form (comprehensive) distillation?"**

#### Atomic Analysis:
- Focused, targeted investigation
- Single issue, pattern, or question
- Quick turnaround (minutes to hour)
- Uses `templates/ATOMIC_ANALYSIS_TEMPLATE.md`
- Stored in `/atomic/`

#### Long-Form Distillation:
- Comprehensive, multi-faceted investigation
- System-wide patterns, architectural decisions
- Deeper synthesis (hours to days)
- Uses `templates/DISTILLATION_TEMPLATE.md`
- Stored in `/distillations/`

**Note:** Atomic analyses can escalate to long-form if findings warrant deeper investigation. Offer escalation if appropriate.

---

## Step 3: Analysis Menu Presentation

### Present Available Analyses:

Present the following menu and allow multiple selections:

1. **Hard Architecture Mapping**
   - Map technical architecture, dependencies, layers
   - Identify structural patterns and constraints
   - Document technology stack and integration points

2. **Decision Forensics**
   - Investigate why specific decisions were made
   - Trace decision history through commits, issues, PRs
   - Identify implicit vs explicit decisions
   - Document trade-offs and alternatives considered

3. **Anti-Library Extraction**
   - Identify discarded approaches, abandoned experiments
   - Document "roads not taken" and why
   - Extract negative knowledge (what doesn't work)
   - Preserve failed experiments as learning

4. **Vision Alignment**
   - Assess alignment with stated goals/vision
   - Identify drift or misalignment
   - Map actual vs intended behavior
   - Recommend realignment strategies

5. **Sentiment Analysis**
   - Analyze tone in commits, comments, issues
   - Identify friction points or areas of frustration
   - Detect team dynamics and collaboration patterns
   - Map emotional journey of project

6. **Meta-Pattern Synthesis**
   - Identify recurring patterns across investigations
   - Synthesize higher-order insights
   - Connect disparate analyses
   - Extract philosophical/strategic lessons

7. **Process Memory Mapping**
   - Document strategic decisions and context
   - Capture pivots, uncertainties, learning moments
   - Use `templates/PROCESS_MEMORY_TEMPLATE.md`
   - Can be requested as explicit output or auto-generated

8. **Backlog/Idea Capture**
   - Extract improvement opportunities
   - Identify technical debt
   - Capture future enhancement ideas
   - Document risks or concerns

9. **Custom Analysis**
   - User-defined investigation type
   - Request specific methodology or focus
   - Adapt existing templates or create new approach

### Selection Guidance:
- Allow single or multiple selections
- Suggest combinations that work well together
- Explain what each analysis will reveal
- Estimate effort for each type

---

## Step 4: Automated Analysis Execution

### For Each Selected Analysis:

1. **Gather Source Materials:**
   - Clone repository (if applicable)
   - Parse documents
   - Collect relevant artifacts

2. **Apply Analysis Methodology:**
   - Use appropriate investigation techniques for analysis type
   - Review code, commits, issues, PRs, documentation
   - Apply domain-specific analysis tools if available
   - Extract patterns, decisions, sentiments, or structures

3. **Handle Ambiguity:**
   - If context is missing: prompt user for clarification
   - If findings are ambiguous: document uncertainty
   - If additional artifacts needed: request them
   - Document assumptions made

4. **Generate Findings:**
   - Synthesize insights
   - Create visualizations or diagrams if helpful
   - Connect to broader patterns or strategic context
   - Identify ripple effects

5. **Select Appropriate Template:**
   - Atomic: `templates/ATOMIC_ANALYSIS_TEMPLATE.md`
   - Long-form: `templates/DISTILLATION_TEMPLATE.md`
   - Process memory: `templates/PROCESS_MEMORY_TEMPLATE.md`
   - Ideas: `templates/IDEA_NOTE_TEMPLATE.md`
   - Backlog: `templates/BACKLOG_ITEM_TEMPLATE.md`

---

## Step 5: Artifact Storage Workflow

### Save Artifacts in Proper Folders:

1. **Atomic Analyses** → `/atomic/`
   - Naming: `YYYY-MM-DD-short-descriptor.md`
   - Example: `2025-11-18-auth-pattern-analysis.md`

2. **Long-Form Distillations** → `/distillations/`
   - Naming: `YYYY-MM-DD-project-theme.md`
   - Example: `2025-11-18-microservices-architecture.md`

3. **Analyses** → `/analyses/`
   - Specialized analysis outputs
   - Naming: `YYYY-MM-DD-analysis-type-subject.md`

4. **Process Memory** → `/process_memory/`
   - Naming: `YYYY-MM-DD-session-context.md`
   - Also create JSON: `YYYY-MM-DD-session-context.json`

5. **Ideas** → `/ideas/`
   - Naming: `YYYY-MM-DD-idea-brief-description.md`

6. **Backlog** → `/backlog/`
   - Naming: `YYYY-MM-DD-item-brief-description.md`

7. **Sensitive Materials** → `/sensitive/`
   - Any flagged sensitive content
   - Naming: `YYYY-MM-DD-sensitive-descriptor.md`

### Update Catalogue:

1. **Update `/catalogue/index.md`:**
   - Add entry under appropriate section
   - Include title, date, brief description
   - Add link to artifact
   - Include relevant tags

2. **Update `/catalogue/manifest.json`:**
   - Add entry to appropriate array
   - Include metadata:
     ```json
     {
       "id": "unique-id",
       "title": "Analysis Title",
       "date": "YYYY-MM-DD",
       "type": "atomic|distillation|process_memory|analysis|idea|backlog",
       "path": "/atomic/YYYY-MM-DD-descriptor.md",
       "tags": ["tag1", "tag2"],
       "related": ["id1", "id2"],
       "description": "Brief description"
     }
     ```

3. **Cross-Link Related Artifacts:**
   - Link to related analyses in artifact files
   - Update related artifacts to point back
   - Create bidirectional references
   - Build knowledge graph

---

## Step 6: Process Memory Protocol

### When to Create Process Memory:

Create process memory entries when:
- Strategic decisions are made
- Notable insights emerge
- Context significantly changes
- Investigation reveals pivots or shifts
- User expresses uncertainty that gets resolved
- Patterns connect across multiple analyses

### Process Memory Creation:

1. **Use Template:** `templates/PROCESS_MEMORY_TEMPLATE.md`

2. **Capture:**
   - Strategic context and vision
   - Decisions made and rationale
   - Frustrations or uncertainties
   - Ripple effects noted
   - Artifacts created
   - Recommended next steps

3. **Create JSON Schema Entry:** `/process_memory/YYYY-MM-DD-session.json`
   ```json
   {
     "date": "YYYY-MM-DD",
     "agents": ["agent-name"],
     "strategic_context": "...",
     "session_type": "analysis|distillation|review",
     "decisions": [
       {
         "decision": "...",
         "rationale": "...",
         "ripple_effects": ["..."]
       }
     ],
     "artifacts_created": ["path1", "path2"],
     "next_steps": ["..."],
     "tags": ["tag1", "tag2"]
   }
   ```

4. **Link to Related Artifacts:**
   - Reference in main analysis
   - Update catalogue with cross-links

---

## Step 7: Sensitive Materials Handling

### Sensitive Content Protocol:

1. **Detection:**
   - User explicitly flags as sensitive
   - Agent detects credentials, keys, private data
   - Proprietary information or trade secrets
   - Personal/confidential information

2. **Handling:**
   - Move to `/sensitive/` directory
   - Add `.gitignore` entry if needed
   - Sanitize public-facing references
   - Document sensitivity reason

3. **Alternative Approaches:**
   - Create redacted public version
   - Store only metadata in public catalogue
   - Reference by ID without details

---

## Step 8: Backlog & Ideas Update

### When Analysis Surfaces New Items:

1. **Improvement Opportunities:**
   - Create backlog item using `templates/BACKLOG_ITEM_TEMPLATE.md`
   - Categorize as: Process/Repo/Analysis/Investigation
   - Set priority: Low/Medium/High
   - Link to source analysis

2. **Future Enhancements:**
   - Create idea note using `templates/IDEA_NOTE_TEMPLATE.md`
   - Document potential impact
   - Link to originating investigation
   - Set status: New/Discussed/Deferred/Discarded

3. **Risks or Concerns:**
   - Document in appropriate artifact
   - Create backlog item if actionable
   - Flag in process memory if strategic

4. **Prompt User:**
   - "This analysis identified [N] potential improvements. Should I create backlog items?"
   - "Would you like to capture these ideas for future reference?"

---

## Step 9: Pull Request Preparation

### Prepare PR Using Template:

Use `.github/PULL_REQUEST_TEMPLATE.md` and include:

1. **Title Format:**
   - `[Atomic/Long-Form] [Project/Theme]: [Short Description]`
   - Example: `[Atomic] Auth System: Decision Forensics on JWT Implementation`

2. **Summary of Results:**
   - Investigation type performed
   - Core insights, metaphors, meta-patterns
   - Key findings and recommendations

3. **Strategic/Subjective Context:**
   - User-provided context
   - Uncertainties addressed
   - Vision alignment notes

4. **Analysis Performed & Rationale:**
   - Menu selections made
   - Analysis methodology
   - Sources examined

5. **Ripple Effects & System Thinking:**
   - Process memory findings
   - Broader implications
   - Recommended actions or risks

6. **Index/Manifest Updates:**
   - List catalogue changes
   - New entries added
   - Cross-links created

7. **Linked Files/Artifacts:**
   - All added files with paths
   - Modified files listed
   - Related artifacts referenced

### Pre-PR Checklist:
- [ ] All artifacts use proper templates
- [ ] Files saved in correct directories
- [ ] Catalogue index updated
- [ ] Manifest JSON updated and valid
- [ ] Cross-links created where appropriate
- [ ] Process memory created if applicable
- [ ] Backlog/ideas captured if surfaced
- [ ] Sensitive materials properly handled
- [ ] PR description complete and accurate

---

## Best Practices

### Always:
- ✅ Ask for strategic/subjective context—don't infer intent if unclear
- ✅ Use standard templates for every submission
- ✅ Label and tag artifacts for cross-analysis synthesis
- ✅ Confirm correct catalogue/manifest entries after every analysis
- ✅ Create process memory for significant insights or decisions
- ✅ Cross-link related artifacts bidirectionally
- ✅ Document assumptions and uncertainties
- ✅ Prompt for clarification when ambiguous

### Consider:
- 💡 Escalate atomic investigations to long-form when findings warrant
- 💡 Suggest related analyses that might provide additional value
- 💡 Identify patterns across multiple investigations
- 💡 Recommend meta-pattern synthesis when appropriate
- 💡 Review backlog and ideas for process improvements
- 💡 Build on prior investigations when relevant

### Never:
- ❌ Infer strategic intent without confirmation
- ❌ Skip template usage
- ❌ Forget to update catalogue and manifest
- ❌ Ignore sensitive materials protocols
- ❌ Create artifacts without cross-linking
- ❌ Miss documenting process memory for key decisions
- ❌ Overlook opportunities to capture backlog/ideas

---

## Quick Reference: Decision Tree

```
Start Investigation
    ↓
1. What is the target? (Repo/Doc/Other)
    ↓
2. Get strategic context from user
    ↓
3. Atomic or Long-Form?
    ↓
4. Present analysis menu → User selects
    ↓
5. Execute selected analyses
    ├─ Gather materials
    ├─ Apply methodology
    ├─ Generate findings
    └─ Use appropriate template
    ↓
6. Save artifacts in correct folders
    ↓
7. Update catalogue/index.md + manifest.json
    ↓
8. Create process memory (if warranted)
    ↓
9. Capture backlog/ideas (if surfaced)
    ↓
10. Handle sensitive materials (if any)
    ↓
11. Prepare PR with complete description
    ↓
Complete ✓
```

---

## Example Usage Scenarios

### Scenario 1: Quick Atomic Analysis
**User:** "Can you analyze the authentication decisions in github.com/example/auth-service?"

**Agent Response:**
1. Confirms target: GitHub repository
2. Asks: "What's your strategic context? Any specific concerns about the auth implementation?"
3. User provides context about security audit needs
4. Suggests: "Atomic analysis should suffice. Recommending Decision Forensics. Would you like to add Security Pattern Review?"
5. Executes analysis
6. Creates `/atomic/2025-11-18-auth-service-decision-forensics.md`
7. Updates catalogue
8. Prepares PR

### Scenario 2: Comprehensive Long-Form Investigation
**User:** "I need a full architectural review of our microservices platform"

**Agent Response:**
1. Confirms target and asks for repository access
2. Requests strategic context: "What are your primary concerns? Performance? Maintainability? Team scaling?"
3. User explains concern about service coupling and deployment complexity
4. Suggests: "Long-form distillation recommended. I suggest: Hard Architecture Mapping + Decision Forensics + Meta-Pattern Synthesis + Process Memory"
5. User approves
6. Executes comprehensive analysis over multiple hours
7. Creates `/distillations/2025-11-18-microservices-platform-architecture.md`
8. Creates `/process_memory/2025-11-18-architecture-review-insights.md`
9. Creates `/backlog/` items for identified improvements
10. Updates catalogue with extensive cross-links
11. Prepares detailed PR

### Scenario 3: Escalation from Atomic to Long-Form
**Agent:** "While conducting atomic Decision Forensics, I discovered significant anti-patterns and coupling issues that warrant deeper investigation. Would you like me to escalate this to a long-form architectural distillation?"

**User:** "Yes, please proceed."

**Agent:** Converts to long-form, adds Meta-Pattern Synthesis and Anti-Library Extraction to analysis menu, continues with comprehensive investigation.

---

## Integration with Repository Structure

### Templates Available:
- `templates/ATOMIC_ANALYSIS_TEMPLATE.md` - For atomic investigations
- `templates/DISTILLATION_TEMPLATE.md` - For long-form distillations
- `templates/PROCESS_MEMORY_TEMPLATE.md` - For process memory entries
- `templates/IDEA_NOTE_TEMPLATE.md` - For ideas and questions
- `templates/BACKLOG_ITEM_TEMPLATE.md` - For actionable backlog items

### Storage Locations:
- `/atomic/` - Atomic analyses
- `/distillations/` - Long-form distillations
- `/analyses/` - Specialized analysis outputs
- `/process_memory/` - Process memory and strategic context
- `/ideas/` - Ideas, questions, observations
- `/backlog/` - Actionable improvements and enhancements
- `/sensitive/` - Sensitive or confidential materials
- `/catalogue/` - Index and manifest

### Reference Documents:
- `FOUNDATION.md` - Core principles and system thinking
- `CONTRIBUTING.md` - Contribution guidelines
- `README.md` - Repository overview
- `.github/PULL_REQUEST_TEMPLATE.md` - PR template

---

## Autonomous Agent Implementation Notes

For AI agents implementing this workflow:

1. **Context Awareness:** Maintain conversation context throughout the entire workflow. Remember user inputs, strategic context, and analysis selections.

2. **Proactive Suggestions:** Based on findings, suggest related analyses or escalation paths without being prompted.

3. **Quality Assurance:** Before finalizing, verify all templates are properly filled, catalogue is updated, and cross-links are valid.

4. **User Engagement:** Keep user informed of progress, especially for long-form analyses that take time.

5. **Adaptive Behavior:** If user provides new information mid-analysis, incorporate it and adjust approach as needed.

6. **Error Handling:** If unable to access resources or find information, clearly communicate limitations and suggest alternatives.

7. **Validation:** After creating artifacts, verify they follow templates and are stored in correct locations.

---

**End of Agent Panel Workflow Documentation**

*This workflow is designed to be agent-executable while maintaining "human on the loop" for strategic validation.*
