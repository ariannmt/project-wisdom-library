# Analysis Menu: Types and Methodologies

This document provides detailed guidance on each analysis type available in the Conceptual Distillation Workflow.

---

## 1. Hard Architecture Mapping

### Purpose
Map the technical architecture, dependencies, and structural patterns of a system.

### Methodology
- Identify system layers (presentation, business logic, data, infrastructure)
- Map component dependencies and interfaces
- Document technology stack and frameworks
- Identify integration points and external dependencies
- Analyze data flow and communication patterns
- Document architectural patterns (microservices, monolith, event-driven, etc.)

### Deliverables
- Architecture diagrams (component, deployment, sequence)
- Dependency graphs
- Technology inventory
- Integration point documentation
- Architectural pattern identification

### Best For
- New team members understanding system structure
- Planning refactoring or migrations
- Assessing technical debt
- Security audits requiring structural understanding

### Example Questions Answered
- "What are the major components and how do they interact?"
- "What technologies does this system depend on?"
- "Where are the critical integration points?"
- "What architectural patterns are in use?"

---

## 2. Decision Forensics

### Purpose
Investigate why specific decisions were made, tracing decision history and rationale.

### Methodology
- Review git history (commits, branches, tags)
- Analyze pull requests and code reviews
- Review issues, discussions, and documentation
- Identify decision points through code changes
- Trace trade-offs and alternatives considered
- Document implicit vs explicit decisions
- Interview artifacts (README changes, ADRs, comments)

### Deliverables
- Decision timeline
- Trade-off analysis
- Alternative approaches considered
- Rationale documentation
- Decision maker identification (where relevant)
- Impact assessment of key decisions

### Best For
- Understanding "why" behind current implementation
- Onboarding new team members
- Evaluating past decisions for current context
- Learning from project history
- Identifying decision patterns

### Example Questions Answered
- "Why was technology X chosen over Y?"
- "What alternatives were considered for this feature?"
- "When and why did the architecture change?"
- "What constraints influenced this decision?"

---

## 3. Anti-Library Extraction

### Purpose
Document discarded approaches, abandoned experiments, and "negative knowledge"—what doesn't work and why.

### Methodology
- Identify abandoned branches and features
- Review closed-without-merge pull requests
- Analyze reverted commits
- Extract "experiments" or "spike" work
- Document failed approaches from issues/discussions
- Catalog dead ends and their lessons
- Preserve context for why approaches were abandoned

### Deliverables
- Anti-library catalogue (what NOT to do)
- Failed experiment documentation
- Lessons learned from abandoned approaches
- Warning signs and red flags identified
- Alternative approaches tried and rejected

### Best For
- Preventing repeated mistakes
- Understanding constraints and limitations
- Preserving institutional knowledge
- Informing future architectural decisions
- Accelerating new team member learning

### Example Questions Answered
- "What approaches were tried and failed?"
- "Why didn't X work?"
- "What pitfalls should we avoid?"
- "What experiments were conducted?"

---

## 4. Vision Alignment

### Purpose
Assess alignment between stated goals/vision and actual implementation or behavior.

### Methodology
- Extract stated vision from documentation, README, mission statements
- Analyze actual implementation patterns
- Identify areas of drift or misalignment
- Map intended vs actual behavior
- Review user/stakeholder feedback for alignment gaps
- Assess feature priorities against stated goals
- Identify implicit vs explicit goals

### Deliverables
- Vision vs reality comparison
- Alignment gap analysis
- Drift identification and quantification
- Realignment recommendations
- Priority assessment
- Goal achievement metrics (where applicable)

### Best For
- Strategic planning and course correction
- Stakeholder communication
- Prioritization decisions
- Post-mortem analysis
- Mission/vision validation

### Example Questions Answered
- "Are we building what we said we would?"
- "Where have we drifted from our original vision?"
- "Do our actions match our stated priorities?"
- "What goals have we achieved vs missed?"

---

## 5. Sentiment Analysis

### Purpose
Analyze tone, emotion, and team dynamics through written communication.

### Methodology
- Analyze commit message tone and language
- Review issue/PR comment sentiment
- Identify friction points or frustration indicators
- Map emotional journey of project
- Detect collaboration patterns
- Identify areas of enthusiasm vs burnout signals
- Analyze response times and engagement levels

### Deliverables
- Sentiment timeline
- Friction point identification
- Team dynamics assessment
- Emotional health indicators
- Collaboration pattern analysis
- Risk areas (burnout, conflict, disengagement)

### Best For
- Team health assessment
- Project retrospectives
- Identifying support needs
- Understanding team dynamics
- Early warning for collaboration issues

### Example Questions Answered
- "Where are the pain points in this project?"
- "What areas generate the most frustration?"
- "How has team sentiment evolved over time?"
- "Are there signs of burnout or conflict?"

---

## 6. Meta-Pattern Synthesis

### Purpose
Identify recurring patterns across multiple investigations and synthesize higher-order insights.

### Methodology
- Review multiple analyses for common themes
- Identify patterns that transcend individual investigations
- Connect disparate findings into coherent framework
- Extract philosophical or strategic lessons
- Synthesize system-level insights
- Map relationships between patterns
- Generate predictive frameworks

### Deliverables
- Meta-pattern catalogue
- Higher-order insight documentation
- Pattern relationship maps
- Strategic framework synthesis
- Predictive models or principles
- Cross-investigation connections

### Best For
- Strategic planning
- Building organizational knowledge
- Identifying systemic issues or strengths
- Creating guiding principles
- Long-term learning and improvement

### Example Questions Answered
- "What patterns appear across our projects?"
- "What higher-level lessons can we extract?"
- "How do these patterns relate to each other?"
- "What principles should guide future work?"

---

## 7. Process Memory Mapping

### Purpose
Document strategic decisions, context, pivots, and learning moments as they occur.

### Methodology
- Capture real-time strategic context during analysis
- Document decision points and rationale
- Record uncertainties and how they were resolved
- Map context changes and pivots
- Preserve "why" behind investigation choices
- Link decisions to artifacts and outcomes
- Create living history of strategic thinking

### Deliverables
- Process memory entries (markdown + JSON)
- Decision timeline with context
- Strategic context documentation
- Uncertainty resolution log
- Ripple effect documentation
- Artifact linkage

### Best For
- Preserving institutional knowledge
- Enabling future AI agents to understand context
- Supporting strategic decision-making
- Creating learning resources
- Maintaining continuity across investigations

### Example Questions Answered
- "Why did we investigate this?"
- "What was the strategic context?"
- "How did our thinking evolve?"
- "What decisions shaped this investigation?"

### Special Note
Process memory can be requested as explicit output OR generated automatically when significant insights or decisions emerge during any other analysis type.

---

## 8. Backlog/Idea Capture

### Purpose
Extract and document improvement opportunities, technical debt, and future enhancements.

### Methodology
- Identify technical debt during investigation
- Document improvement opportunities
- Capture enhancement ideas
- Flag risks and concerns
- Prioritize findings
- Link to source analysis
- Categorize by type and impact

### Deliverables
- Backlog items with priority
- Idea notes with potential impact
- Risk documentation
- Improvement roadmap
- Technical debt inventory

### Best For
- Continuous improvement planning
- Prioritization discussions
- Resource allocation
- Risk management
- Innovation tracking

### Example Questions Answered
- "What could be improved?"
- "What technical debt exists?"
- "What opportunities were identified?"
- "What risks need attention?"

---

## 9. Custom Analysis

### Purpose
User-defined investigation type adapted to specific needs.

### Methodology
User specifies:
- Investigation focus and goals
- Methodology or approach
- Expected deliverables
- Success criteria

Agent adapts existing templates or creates custom approach.

### Deliverables
Varies based on user specification

### Best For
- Unique investigation needs
- Specialized domain analysis
- Novel synthesis approaches
- Experimental investigations

### Example Questions Answered
Whatever the user defines

---

## Analysis Combinations

Some analyses work particularly well together:

### Comprehensive System Understanding
- Hard Architecture Mapping
- Decision Forensics
- Anti-Library Extraction
→ Complete picture of current state and how it evolved

### Strategic Alignment Assessment
- Vision Alignment
- Sentiment Analysis
- Meta-Pattern Synthesis
→ Understand if you're building the right thing the right way

### Knowledge Preservation
- Decision Forensics
- Process Memory Mapping
- Anti-Library Extraction
→ Comprehensive institutional knowledge capture

### Health Check
- Sentiment Analysis
- Vision Alignment
- Backlog/Idea Capture
→ Assess project health and identify improvements

---

## Selecting the Right Analysis

### Ask Yourself:

**If you want to understand WHAT:**
→ Hard Architecture Mapping

**If you want to understand WHY:**
→ Decision Forensics

**If you want to understand WHAT NOT:**
→ Anti-Library Extraction

**If you want to understand IF (aligned):**
→ Vision Alignment

**If you want to understand HOW (people feel):**
→ Sentiment Analysis

**If you want to understand PATTERNS:**
→ Meta-Pattern Synthesis

**If you want to understand CONTEXT:**
→ Process Memory Mapping

**If you want to understand OPPORTUNITIES:**
→ Backlog/Idea Capture

**If you want to understand SOMETHING ELSE:**
→ Custom Analysis

---

## Analysis Type Decision Matrix

| Analysis Type | Time Required | Depth | Best For | Output Location |
|--------------|---------------|--------|----------|-----------------|
| Hard Architecture Mapping | Medium-High | Deep | Technical Understanding | `/analyses/` or `/distillations/` |
| Decision Forensics | Medium | Deep | Historical Context | `/atomic/` or `/distillations/` |
| Anti-Library Extraction | Medium | Medium | Risk Mitigation | `/analyses/` |
| Vision Alignment | Low-Medium | Medium | Strategic Planning | `/atomic/` or `/analyses/` |
| Sentiment Analysis | Low-Medium | Medium | Team Health | `/analyses/` |
| Meta-Pattern Synthesis | High | Very Deep | Strategic Insights | `/distillations/` |
| Process Memory Mapping | Low | Medium | Context Preservation | `/process_memory/` |
| Backlog/Idea Capture | Low | Shallow | Action Planning | `/backlog/` or `/ideas/` |
| Custom | Varies | Varies | Unique Needs | Varies |

---

## Evolution and Extension

This menu is not fixed. New analysis types can be added as needs emerge:

### Potential Future Analysis Types:
- **Performance Archaeology**: Understanding performance decisions and bottlenecks
- **Security Posture Assessment**: Security decision patterns and vulnerabilities
- **Dependency Health Check**: Third-party dependency management analysis
- **Documentation Gap Analysis**: Identifying documentation needs
- **Test Coverage Philosophy**: Understanding testing strategy and gaps
- **API Design Forensics**: API decision patterns and evolution
- **Error Handling Patterns**: How errors are handled and communicated

### Adding New Analysis Types:

1. Define purpose and methodology
2. Specify deliverables
3. Update this menu document
4. Create or adapt templates
5. Update `AGENT_PANEL_WORKFLOW.md`
6. Add examples to catalogue

---

**This analysis menu enables systematic, comprehensive investigation tailored to specific needs while maintaining consistency and quality across the wisdom library.**
