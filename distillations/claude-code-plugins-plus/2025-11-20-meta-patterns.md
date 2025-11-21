# Meta-Pattern Synthesis: Claude Code Plugins Plus

**Investigation ID:** `claude-code-plugins-plus-meta-patterns-2025-11-20`
**Date:** 2025-11-20
**Level:** 4 (Wisdom/Abstraction - Universal Principles)
**Methodology:** Meta-Pattern Synthesis
**Target:** https://github.com/jeremylongshore/claude-code-plugins-plus
**Dependencies:** Levels 1-3 complete (Architecture, Forensics, Anti-Library, Vision, Process Memory)

---

## Executive Summary

Synthesizing findings across all investigation levels reveals **12 universal meta-patterns** applicable beyond Claude Code plugins to any AI-native system, platform ecosystem, or standards-driven market. These patterns cluster around three themes: **(1) Linguistic Interfaces**, **(2) Constraint-Driven Architecture**, and **(3) Quality-as-Infrastructure**. The key abstraction: **In AI-native systems, documentation IS the primary execution artifact—not supplementary but foundational.**

**Universal Insight:** The repository demonstrates that **form (how you structure) determines function (what emerges)** more than explicit programming. Patterns extracted are transferable to agent systems, distributed architectures, open-source projects, and platform ecosystems.

---

## Meta-Pattern 1: **Documentation-as-Executable-Specification**

### Pattern Definition
In AI-native systems, documentation files (e.g., SKILL.md) serve as **executable specifications** that AI agents interpret as instructions, not merely reference material.

### Evidence from Investigation
- **SKILL.md structure:** Frontmatter (YAML) + narrative description = complete program
- **Trigger phrases:** Act as function signatures in linguistic space
- **Tool permissions:** Type declarations (capability boundaries)
- **Version tracking:** Semantic versioning of "prompts as code"

### Universal Application

| Domain | Implementation | Benefit |
|--------|----------------|---------|
| **API Documentation** | OpenAPI specs auto-generate client SDKs | Docs → Code (reversed) |
| **Infrastructure** | Terraform configs = declarative infrastructure | Docs = Executable |
| **Testing** | BDD scenarios (Gherkin) = executable tests | Specs → Tests |
| **AI Agents** | System prompts = agent behavior specifications | Prompts → Programs |

### Abstraction Principle
> **"In AI-native systems, write documentation first—it IS the program."**

Traditional: Code → (optionally) Docs
AI-Native: Docs → (automatically) Behavior

### Cross-Domain Transfer

**Healthcare AI:** Patient care guidelines written as FHIR-compliant markdown → AI follows protocols
**Legal Tech:** Contract templates as structured text → AI generates/validates contracts
**Education:** Curriculum as competency YAML → AI personalizes learning paths

### Key Insight
When AI is the consumer, **clarity matters more than brevity**. Verbose, explicit documentation isn't overhead—it's executable precision.

---

## Meta-Pattern 2: **Linguistic API Design**

### Pattern Definition
Natural language descriptions serve as API surfaces, where **semantic matching** (not exact syntax) determines invocation.

### Evidence from Investigation
- **Trigger phrases:** "monitor CPU", "analyze performance", "optimize code"
- **Soft matching:** Variations accepted ("check CPU load" ≈ "monitor CPU usage")
- **Context-aware:** Same phrase may activate different skills based on conversation context
- **Silent activation:** No explicit `/command` required—intent suffices

### Universal Application

| System Type | Linguistic API | Traditional API |
|-------------|---------------|-----------------|
| **Claude Code Skills** | "scan for vulnerabilities" | `security.scan({target: 'code'})` |
| **Voice Assistants** | "turn on the lights" | `smart_home.light.power(state=True)` |
| **Search Engines** | "restaurants near me" | `search.query(type='restaurant', location='current')` |
| **Chatbots** | "cancel my subscription" | `account.subscription.cancel()` |

### Abstraction Principle
> **"Make intent the interface, not syntax."**

Users shouldn't learn function names—they should **express goals** and system infers methods.

### Design Guidelines

**For Linguistic APIs:**
1. **Multiple Invocation Patterns:** Accept variations ("find bugs" = "detect issues" = "scan problems")
2. **Explicit Triggers:** Document activation phrases (makes implicit explicit)
3. **Semantic Categories:** Group by intent (security, performance, testing) not implementation
4. **Contextual Disambiguation:** Same phrase → different actions based on conversation state

### Key Insight
Linguistic APIs trade **precision** (exact syntax) for **accessibility** (natural expression). In human-AI interaction, accessibility wins.

---

## Meta-Pattern 3: **Tool Permissions as Architectural Declarations**

### Pattern Definition
Permission lists (e.g., `allowed-tools: Read, Grep, Bash`) serve as **architectural declarations** that document capability boundaries, not runtime enforcement.

### Evidence from Investigation
- **5 Categories:** Read-only, Code Editing, Web Research, Database, Testing
- **Principle of Least Privilege:** Request minimal tools for purpose
- **Documentation Value:** Users know what skill CAN do before activation
- **Not Enforcement:** Claude reads as guidance, not hard constraint

### Universal Application

| System | Permission Declaration | Purpose |
|--------|------------------------|---------|
| **Docker** | `capabilities: [NET_ADMIN, SYS_TIME]` | Document container privileges |
| **Kubernetes** | `securityContext: {runAsUser: 1000}` | Declare pod security posture |
| **OAuth** | `scopes: [read:user, write:repo]` | Specify app permissions |
| **SELinux** | `type: httpd_sys_content_t` | Label resource access policies |

### Abstraction Principle
> **"Permissions aren't gates—they're specifications."**

In trust-based systems, declarations **communicate intent** rather than enforce boundaries.

### Design Guidelines

**For Permission Systems:**
1. **Declarative:** State what's allowed (not how enforcement works)
2. **Minimal:** Request least privilege (documents true needs)
3. **Categorized:** Group into semantic sets (easier to reason about)
4. **Auditable:** Visible to consumers before use (builds trust)

### Key Insight
When enforcement is impractical (AI reading prompts), **documented constraints shape behavior** through context. Trust model over enforcement model.

---

## Meta-Pattern 4: **Silent Ambient Intelligence**

### Pattern Definition
Capabilities activate **without notification**, creating invisible assistance layer that users detect through outcome quality, not explicit invocation.

### Evidence from Investigation
- **Skills activate silently:** No "skill X is now active" message
- **Detection through behavior:** Claude uses domain language, follows workflows
- **User guide teaches detection:** "How to know if skill activated" section
- **UX Philosophy:** Interruption-free assistance

### Universal Application

| Domain | Silent Activation Example | Detection Method |
|--------|---------------------------|------------------|
| **Autocorrect** | Typo fixed without prompt | See corrected text |
| **Spam Filtering** | Email silently moved | Inbox stays clean |
| **Anti-virus** | Threat quarantined | No infection occurs |
| **Smart Home** | Lights adjust to time | Room lighting changes |
| **AI Assistants** | Context carried across turns | Coherent conversation |

### Abstraction Principle
> **"The best assistance is invisible until needed."**

Ambient intelligence: Always available, never intrusive.

### Design Considerations

**When to Use Silent Activation:**
✅ High-frequency actions (interruption cost high)
✅ Predictable user intent (low error rate)
✅ Non-destructive operations (mistakes recoverable)

**When to Require Explicit Invocation:**
⚠️ Irreversible actions (delete, publish)
⚠️ Ambiguous intent (multiple interpretations)
⚠️ Learning phase (user needs feedback)

### Key Insight
Silent activation trades **awareness** (user knows capability fired) for **flow** (uninterrupted experience). Choose based on operation criticality.

---

## Meta-Pattern 5: **Constraint-Driven Design Excellence**

### Pattern Definition
External constraints (platform schemas, standards, resource limits) **force creative solutions** that wouldn't emerge with unlimited freedom.

### Evidence from Investigation
- **Claude CLI schema → Dual-catalog architecture** (elegant workaround)
- **2025 standard → 100% compliance strategy** (competitive positioning)
- **No dependencies → Simple plugins** (maintainability win)
- **Single maintainer → Automation investment** (forced scalability)

### Universal Application

| Constraint | Forced Solution | Emergent Benefit |
|------------|-----------------|------------------|
| **Twitter's 140 chars** | Concise writing | Clarity, viral spread |
| **Mobile screen size** | Touch-first UI | Accessibility improvement |
| **Serverless cold starts** | Fast initialization | Efficient architecture |
| **SQLite file-based** | No server setup | Portable, simple deployment |

### Abstraction Principle
> **"Constraints aren't limitations—they're design specifications."**

Limits shape creativity: Haiku (17 syllables), Sonnet (14 lines), Unix pipes (text streams).

### Design Strategy

**Embrace Constraints:**
1. **Identify non-negotiables** (platform limits, standards, budgets)
2. **Design within bounds** (don't fight constraints, work with them)
3. **Extract advantages** (constraints create focus, simplicity)
4. **Communicate constraints** (make them visible to users/developers)

### Key Insight
**Freedom paralyzes** (infinite options = decision fatigue). **Constraints liberate** (finite options = creative solutions).

---

## Meta-Pattern 6: **Standards-as-Competitive-Strategy**

### Pattern Definition
In standards-driven markets, **perfect conformance** differentiates more than novel features—being the "reference implementation" creates defensible position.

### Evidence from Investigation
- **100% 2025 schema compliance** marketed as "industry-first"
- **Competitor research:** Others 0-10% compliant
- **3-day migration investment** prioritized over new features
- **Quality leadership** positioning through standards adherence

### Universal Application

| Market | Standard | Compliance Strategy |
|--------|----------|---------------------|
| **Web Browsers** | W3C HTML/CSS specs | Chrome, Firefox compete on standards |
| **Cloud Platforms** | CNCF Kubernetes | AWS EKS, Azure AKS claim compliance |
| **Accessibility** | WCAG 2.1 | Companies tout AA/AAA certification |
| **Security** | ISO 27001, SOC 2 | Audit compliance as trust signal |

### Abstraction Principle
> **"When everyone has features, conformance becomes the feature."**

Crowded markets: Differentiate through **quality signals** (standards) not quantity (features).

### Strategic Framework

**Standards-First Strategy:**
1. **Identify target standard** (e.g., Anthropic 2025 schema)
2. **Audit current state** (measure compliance gap)
3. **Achieve 100%** (invest in full conformance)
4. **Market leadership** ("first", "only", "most compliant")
5. **Maintain** (standards evolve, stay current)

### Key Insight
**Innovation ≠ only novel features.** Being first to **fully implement external standards** is strategic innovation (execution excellence).

---

## Meta-Pattern 7: **Evidence-First Scaling**

### Pattern Definition
Make scaling decisions based on **quantified gaps** (not assumptions), then apply systematic fixes—measure, act, validate cycle.

### Evidence from Investigation
- **96% non-compliance measured** → triggered migration
- **120 missing LICENSEs counted** → bulk remediation
- **261 missing assets quantified** → automated generation
- **No "we should improve"** → "Gap is X, fix is Y"

### Universal Application

| Domain | Evidence-First Practice | Reactive Alternative |
|--------|------------------------|----------------------|
| **Performance** | Profile first, then optimize | Premature optimization |
| **Security** | Audit logs, then fix vulns | Assume security |
| **Testing** | Measure coverage, add tests | "Feels tested enough" |
| **Quality** | Static analysis, fix issues | Code review alone |

### Abstraction Principle
> **"Quantify before acting. Speculation is expensive."**

Data-driven decisions: Measure → Diagnose → Fix → Validate

### Implementation Pattern

```
1. AUDIT: Count/measure current state
2. QUANTIFY GAP: Calculate delta from target
3. PRIORITIZE: Rank by impact × effort
4. SYSTEMATIC FIX: Script solution, apply at scale
5. VALIDATE: Re-measure, confirm gap closed
```

### Key Insight
**"We should improve quality"** = vague → ignored
**"96% non-compliant"** = specific → actionable

---

## Meta-Pattern 8: **Dual-Persistence Architecture**

### Pattern Definition
Maintain **source of truth** (rich representation) + **derived views** (constrained representations) to serve different consumers with incompatible requirements.

### Evidence from Investigation
- **marketplace.extended.json** (source): Full metadata for website
- **marketplace.json** (derived): Sanitized for CLI compatibility
- **Sync script** bridges: Strips extra fields, maintains core data
- **Edit workflow:** Always modify source, regenerate derived

### Universal Application

| System | Source of Truth | Derived View | Reason |
|--------|----------------|--------------|--------|
| **Databases** | Normalized tables | Denormalized reports | Query performance |
| **APIs** | Internal format | Public schema | Backward compatibility |
| **Configs** | YAML (human) | JSON (machine) | Tooling requirements |
| **Documentation** | Markdown (source) | HTML (rendered) | Display format |

### Abstraction Principle
> **"Never constrain richest representation to meet strictest consumer."**

Keep full fidelity, then transform for contexts.

### Design Guidelines

**For Dual-Persistence:**
1. **Single Source of Truth:** One authoritative representation
2. **Automated Derivation:** Script transformation (no manual sync)
3. **CI Validation:** Fail if derived out of sync
4. **Clear Ownership:** Edit source, regenerate derived

### Key Insight
When consumers have **incompatible requirements**, separate storage beats compromise. Don't dumb down source—transform for target.

---

## Meta-Pattern 9: **Quality-as-Automated-Infrastructure**

### Pattern Definition
Enforce quality standards through **automated tooling** (validators, generators, CI checks)—not documentation or manual review. Quality infrastructure, not quality aspiration.

### Evidence from Investigation
- **claude-plugin-validator package:** Automated checks + auto-fix
- **Python validation scripts:** Schema enforcement
- **GitHub Actions CI:** Quality gates in pipeline
- **Generation includes validation:** Quality by default

### Universal Application

| Domain | Quality Tool | Manual Alternative (Fails at Scale) |
|--------|--------------|-------------------------------------|
| **Code** | Linters (ESLint, Pylint) | Code review comments |
| **Security** | SAST scanners (Snyk, Checkmarx) | Manual audits |
| **Testing** | Coverage tools (Istanbul, JaCoCo) | Developer discretion |
| **Documentation** | Spell checkers, link validators | Proofreading |

### Abstraction Principle
> **"Automate quality gates or they won't be enforced."**

Humans are inconsistent, tools are reliable.

### Implementation Strategy

```
1. DEFINE STANDARD: What is "quality"? (e.g., 100% schema compliant)
2. BUILD VALIDATOR: Tool that checks compliance
3. INTEGRATE CI: Fail builds on violations
4. ADD AUTO-FIX: Where possible, remediate automatically
5. MEASURE METRICS: Track compliance over time
```

### Key Insight
**"Follow quality standards"** = suggestion (ignored under pressure)
**Validator package + CI** = infrastructure (enforced automatically)

---

## Meta-Pattern 10: **Recursive AI Development**

### Pattern Definition
Use AI to create **AI-consumable artifacts** (docs, configs, prompts) that other AI agents read to extend capabilities—self-referential development loop.

### Evidence from Investigation
- **Human writes plugin docs** (for humans)
- **AI generates SKILL.md** (for AI, from human docs)
- **Claude reads SKILL.md** (AI reads AI-generated specs)
- **Usage patterns inform docs** (closes loop)

### Universal Application

| Domain | Recursive Pattern | Benefit |
|--------|------------------|---------|
| **Code Generation** | AI writes code → AI reviews code → Improves | Self-improving systems |
| **Documentation** | AI generates docs → AI answers questions from docs | Consistency |
| **Testing** | AI writes tests → AI runs tests → Refines | Automated QA |
| **Training Data** | AI labels data → AI trains on labels → Better labeling | Bootstrap learning |

### Abstraction Principle
> **"When AI is both producer and consumer, optimize for machine clarity."**

Not "readable by humans" but "parseable by AI."

### Design Considerations

**For Recursive Systems:**
✅ **Explicit structure:** YAML frontmatter > prose
✅ **Validation loops:** AI-generated → validated → used
✅ **Version control:** Track AI-generated artifacts (audit trail)

**Risks:**
⚠️ **Error amplification:** AI mistakes propagate if not validated
⚠️ **Opacity:** Hard to debug AI → AI interactions
⚠️ **Brittleness:** Schema changes break entire chain

### Key Insight
Recursive AI development **scales expertise** (one human → many AI-generated artifacts) but requires **validation infrastructure** (errors compound).

---

## Meta-Pattern 11: **Progressive Disclosure Through Structure**

### Pattern Definition
Use **physical organization** (file/directory structure) to mirror **cognitive progression** (beginner → intermediate → advanced), revealing complexity gradually.

### Evidence from Investigation
- **SKILL.md:** Core (always visible)
- **scripts/:** Automation (for advanced users)
- **references/:** Deep dives (optional)
- **assets/:** Customization (experts)

User sees complexity **when ready**, not all at once.

### Universal Application

| System | Progressive Layers | User Journey |
|--------|-------------------|--------------|
| **Documentation** | README → Getting Started → API Reference → Internals | Beginner → Expert |
| **Software** | GUI → CLI → API → Source Code | User → Developer |
| **Learning** | Tutorial → Exercises → Projects → Mastery | Student → Practitioner |
| **Games** | Tutorial → Campaign → Challenges → Mods | Player → Creator |

### Abstraction Principle
> **"Match information density to user readiness."**

Don't overwhelm beginners, don't bore experts.

### Design Strategy

**Layered Information Architecture:**
```
Layer 1 (Always Visible): Core function, simple example
Layer 2 (Easy to Find): Common use cases, best practices
Layer 3 (Discoverable): Advanced features, customization
Layer 4 (Deep Dive): Internals, architecture, theory
```

### Key Insight
**Flat structure** = paralysis (too much at once)
**Layered structure** = progression (complexity emerges as understanding grows)

---

## Meta-Pattern 12: **Quantifiable Trust Building**

### Pattern Definition
Build trust through **measurable, verifiable claims** (counts, percentages, audits) rather than subjective adjectives ("high quality", "comprehensive").

### Evidence from Investigation
- **"254 plugins"** (countable)
- **"100% compliant"** (auditable)
- **"185 Skills"** (measurable)
- **"96% non-compliant"** (honest gap reporting)

vs. vague claims like "many plugins", "quality plugins"

### Universal Application

| Vague Claim | Quantifiable Alternative | Verification |
|-------------|-------------------------|--------------|
| "Fast performance" | "< 100ms p99 latency" | Benchmark |
| "Secure system" | "SOC 2 Type II certified" | Audit report |
| "Comprehensive tests" | "95% code coverage" | Coverage tool |
| "Active community" | "1,200 contributors" | GitHub stats |

### Abstraction Principle
> **"Measurable > Adjectives for credibility."**

Subjective = debatable, Objective = verifiable.

### Implementation Guidelines

**For Trust Building:**
1. **Quantify claims:** Convert adjectives to numbers
2. **Provide evidence:** Link to audits, reports, metrics
3. **Admit gaps:** Honest reporting > exaggeration
4. **Show progress:** Before/after measurements

**Example Transformation:**
- ❌ "Our marketplace has high-quality plugins"
- ✅ "Our marketplace has 254 plugins, 100% schema-compliant (verified by automated validator)"

### Key Insight
**Trust emerges from verification**, not assertion. Users trust what they can **independently confirm**.

---

## Cross-Cutting Themes

### Theme 1: **AI-Native ≠ AI-Powered**

**AI-Powered:** AI assists human workflows (copilot model)
**AI-Native:** Systems designed for AI operation (docs = execution, linguistic APIs, silent activation)

**Shift:** From "AI helps humans code" → "AI reads docs to extend capabilities"

---

### Theme 2: **Form Determines Function**

**Traditional:** Write code, then optimize
**Pattern-Driven:** Structure system, behavior emerges

**Examples:**
- Dual-catalog → clean separation (form = structure, function = separation)
- Tool permissions → capability docs (form = YAML list, function = documentation)
- Trigger phrases → activation logic (form = description text, function = invocation)

---

### Theme 3: **Constraint Is Specification**

**Observation:** Every constraint in investigation forced better design
- CLI schema strictness → dual-catalog elegance
- 2025 standard → competitive positioning
- Resource limits → automation investment

**Principle:** **Constraints aren't problems to solve—they're parameters to design within.**

---

## Transferability Matrix

| Pattern | AI Systems | Platform Ecosystems | Open Source | Enterprise |
|---------|-----------|---------------------|-------------|------------|
| Documentation-as-Executable | ⭐⭐⭐⭐⭐ High | ⭐⭐⭐ Moderate | ⭐⭐⭐⭐ High | ⭐⭐⭐ Moderate |
| Linguistic APIs | ⭐⭐⭐⭐⭐ High | ⭐⭐⭐ Moderate | ⭐⭐ Low | ⭐⭐⭐⭐ High |
| Tool Permissions as Declarations | ⭐⭐⭐⭐ High | ⭐⭐⭐⭐ High | ⭐⭐⭐ Moderate | ⭐⭐⭐⭐⭐ High |
| Silent Ambient Intelligence | ⭐⭐⭐⭐⭐ High | ⭐⭐ Low | ⭐ Low | ⭐⭐⭐ Moderate |
| Constraint-Driven Design | ⭐⭐⭐⭐⭐ Universal | ⭐⭐⭐⭐⭐ Universal | ⭐⭐⭐⭐⭐ Universal | ⭐⭐⭐⭐⭐ Universal |
| Standards-as-Strategy | ⭐⭐⭐ Moderate | ⭐⭐⭐⭐⭐ High | ⭐⭐⭐⭐ High | ⭐⭐⭐⭐⭐ High |
| Evidence-First Scaling | ⭐⭐⭐⭐⭐ Universal | ⭐⭐⭐⭐⭐ Universal | ⭐⭐⭐⭐⭐ Universal | ⭐⭐⭐⭐⭐ Universal |
| Dual-Persistence | ⭐⭐⭐ Moderate | ⭐⭐⭐⭐⭐ High | ⭐⭐⭐ Moderate | ⭐⭐⭐⭐ High |
| Quality-as-Infrastructure | ⭐⭐⭐⭐⭐ Universal | ⭐⭐⭐⭐⭐ Universal | ⭐⭐⭐⭐⭐ Universal | ⭐⭐⭐⭐⭐ Universal |
| Recursive AI Development | ⭐⭐⭐⭐⭐ High | ⭐⭐ Low | ⭐⭐⭐ Moderate | ⭐⭐⭐⭐ High |
| Progressive Disclosure | ⭐⭐⭐⭐⭐ Universal | ⭐⭐⭐⭐ High | ⭐⭐⭐⭐⭐ High | ⭐⭐⭐⭐ High |
| Quantifiable Trust | ⭐⭐⭐⭐⭐ Universal | ⭐⭐⭐⭐⭐ Universal | ⭐⭐⭐⭐⭐ Universal | ⭐⭐⭐⭐⭐ Universal |

**Universal Patterns** (apply everywhere): Constraint-Driven Design, Evidence-First Scaling, Quality-as-Infrastructure, Quantifiable Trust, Progressive Disclosure

**Domain-Specific Patterns** (high value in specific contexts): Linguistic APIs (AI systems), Standards-as-Strategy (platform ecosystems), Recursive AI Development (AI-native systems)

---

## Conclusion: The Meta-Wisdom

Claude Code Plugins Plus demonstrates that **architecture emerges from patterns, not plans**. The 12 meta-patterns extracted are not just "how this project works"—they're **transferable principles** for:

1. **AI-Native Systems:** Documentation-as-executable, linguistic APIs, silent activation
2. **Platform Ecosystems:** Standards-as-strategy, dual-persistence, constraint-driven design
3. **Quality at Scale:** Evidence-first scaling, quality-as-infrastructure, quantifiable trust
4. **Any Software:** Progressive disclosure, recursive development (when AI involved)

**The Ultimate Abstraction:**
> **"Systems shaped by good patterns are robust to change. Patterns > Code."**

Patterns outlive implementations. These 12 principles will remain relevant as AI models evolve, platforms change, and technologies shift.

**Next Steps:** Paradigm Extraction will identify the fundamental worldview shifts these patterns represent.

---

## Artifact Metadata

```json
{
  "id": "claude-code-plugins-plus-meta-patterns-2025-11-20",
  "type": "distillation",
  "level": 4,
  "methodology": "Meta-Pattern Synthesis",
  "target": "https://github.com/jeremylongshore/claude-code-plugins-plus",
  "patterns_identified": 12,
  "themes_extracted": 3,
  "transferability": "cross-domain",
  "universal_patterns": 5,
  "domain_specific_patterns": 7,
  "confidence": 0.90,
  "wisdom_level": 4,
  "strategic_context": "Extract portable wisdom applicable beyond this project—patterns that can guide AI-native development, platform ecosystems, and quality-driven engineering",
  "related": [
    "claude-code-plugins-plus-architecture-2025-11-20",
    "claude-code-plugins-plus-decision-forensics-2025-11-20",
    "claude-code-plugins-plus-anti-library-2025-11-20",
    "claude-code-plugins-plus-vision-alignment-2025-11-20",
    "claude-code-plugins-plus-process-memory-2025-11-20"
  ]
}
```
