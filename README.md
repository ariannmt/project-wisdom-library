# Project Wisdom Library

Welcome to the **Project Wisdom Library**—a centralized, AI-driven archive for conceptual distillations, investigations, and epistemic history. This repository is designed for **Issue-Driven** autonomous agent operation, moving beyond simple data storage to capture the "Wisdom" and "Paradigm Shifts" of your projects.

## Core Principles
- **Holistic System Thinking:** We analyze connections, not just components.
- **Epistemic History:** We capture *why* decisions were made, not just *what* changed.
- **The Wisdom Ladder:** We systematically climb from Data (Level 1) to Wisdom (Level 4).

## How to Use This Library

### 1. Vision Owner (Human): Create the Mandate
**Do not browse folders manually.** Use the automated Intake Process.
1.  **Start:** Go to **Issues** $\to$ **New Issue**.
2.  **Select:** `[Intake]: Conceptual Investigation` or `[Task]: Backlog Task`.
3.  **Submit:** Fill out the form. This creates the "Trigger."

### 2. System Owner (Human + Agent): Execute the Mandate
*The system does not run automatically. You must invoke the Agent.*

1.  **Open your Agent Panel** (e.g., GitHub Copilot, Cursor, etc.).
2.  **Load Context:** Ensure the agent can read `docs/` and `prompts/`.
3.  **Paste the Driver:** Input the content of `prompts/AGENT_PANEL_PROMPT.md`.
4.  **Fire:** Give the command:
    > "Execute Phase 1 for Issue #[Number]"

### 2. For AI Agents (System Owners)
**Do not chat.** Execute the mandate.

1.  **Trigger:** Watch for new Issues with the label `investigation`.
2.  **Execution:** Follow the **[Automation Guide](docs/AUTOMATION_GUIDE.md)**.
    * Parse the Issue.
    * Establish the **Wisdom Ladder**.
    * Execute Analysis.
    * Generate Artifacts (Protocol Compliant).
    * Update Catalogue.
3.  **Delivery:** Submit a Pull Request with the results.

## Repository Structure

```
project-wisdom-library/
├── atomic/             # Level 1-2: Hard Facts & Forensics
├── distillations/      # Level 4: Wisdom & Paradigms
├── process_memory/     # Level 3: Epistemic History (JSON Protocol)
├── backlog/            # Strategic & Tactical Actions
├── catalogue/          # The Knowledge Graph (Manifest)
├── templates/          # Standardized Input Patterns
└── docs/               # The System Manual (Workflow & Schemas)
```

## Documentation Resources
- **[Automation Guide](docs/AUTOMATION_GUIDE.md):** The "Source of Truth" for Agent execution.
- **[Analysis Menu](docs/ANALYSIS_MENU.md):** The Wisdom Ladder definitions.
- **[Manifest Schema](docs/MANIFEST_SCHEMA.md):** The Data Structure & Mapping Protocol.
