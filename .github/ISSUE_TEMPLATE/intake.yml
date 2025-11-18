name: Conceptual Investigation Intake
description: Request a new conceptual analysis or distillation using the automated agent workflow.
title: "[Intake]: "
labels: ["investigation"]
body:
  - type: markdown
    attributes:
      value: |
        ## Conceptual Investigation Intake
        Welcome to the Project Wisdom Library intake. Please fill out the details below to initiate the autonomous agent workflow.

  - type: dropdown
    id: analysis-type
    attributes:
      label: Analysis Type
      description: Is this a quick, focused check or a deep dive?
      options:
        - Atomic (Quick, focused)
        - Long-Form (Comprehensive distillation)
    validations:
      required: true

  - type: input
    id: subject
    attributes:
      label: Subject/Theme
      description: Short description of the project or topic (e.g., "Auth Service" or "Q4 Security Audit").
      placeholder: e.g., Payment Gateway Architecture
    validations:
      required: true

  - type: textarea
    id: context
    attributes:
      label: Strategic & Subjective Context
      description: The "Why". Describe your uncertainties, frustrations, vision, or strategic intent. This is critical for the agent!
      placeholder: "I am worried about the complexity of the token refresh logic. I want to know if it aligns with our mobile-first vision..."
    validations:
      required: true

  - type: checkboxes
    id: menu-items
    attributes:
      label: Requested Menu Items
      description: Which analysis methodologies should the agent apply?
      options:
        - label: Hard Architecture Mapping (Structure & Dependencies)
        - label: Decision Forensics (Why decisions were made)
        - label: Anti-Library Extraction (What failed & why)
        - label: Vision Alignment (Goals vs. Reality)
        - label: Sentiment Analysis (Team dynamics & friction)
        - label: Meta-Pattern Synthesis (Cross-project patterns)
        - label: Process Memory Mapping (Capture strategic decisions)
        - label: Backlog/Idea Capture (Improvements & Tech Debt)
        - label: Custom Analysis (Specify in notes)
    validations:
      required: true

  - type: textarea
    id: artifacts
    attributes:
      label: Artifacts & References
      description: Paste links to repositories, documents, or logs here.
      placeholder: "https://github.com/my-org/my-repo"

  - type: textarea
    id: special-requests
    attributes:
      label: Special Requests or Ideas
      description: Any specific focus areas or future enhancement ideas?
