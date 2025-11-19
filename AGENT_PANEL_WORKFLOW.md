# Agent Panel Workflow: Issue-Driven Autonomous Distillation (Robust Copilot Edition)

**Role:** System Owner Agent (GitHub Copilot)  
**Context:** Project Wisdom Library  
**Activation:** Assignment to a GitHub Issue created by an approved template.

---

## I. Robust Protocol Activation & Payload Extraction

### 1. Trigger Sequence
> **When assigned to an Issue, begin at once.**

- **Scan:** Read the full Issue for a code block labeled `agent_prompt` (YAML payload).

### 2. Error Handling & Diagnostics

- **If no `agent_prompt` block is found:**  
    - Comment on the Issue:  
      *"Activation failed. No agent_prompt block detected. Please ensure your Issue is created from an approved template and includes the agent payload."*  
    - Halt processing.  
- **If YAML is malformed or unreadable:**  
    - Comment on the Issue:  
      *"Agent activation failed. agent_prompt payload is malformed or contains errors. Please validate YAML syntax."*  
    - Halt processing.
- **If required fields (like `action`) are missing:**  
    - Comment:  
      *"Agent activation failed. Required fields (`action`, scenario inputs) missing from payload. Please check and resubmit."*  
    - Halt processing.

---

## II. Scenario Routing & Fallback Logic

> **Use the `action` field in the payload to select a scenario. If ambiguous or missing, comment with a diagnostic message and halt.**

---

### A. Investigation ("Execute Wisdom Ladder Protocol")

#### Error Handling & Fallbacks

- **If `target` or other required input (`depth`, `tools`) is missing/invalid:**  
    - Comment with what’s missing and pause until provided.
    - If `intent` is blank, proceed to inference as usual.

- **If selected tool/menu item is unrecognized:**  
    - Log uncertainty in Process Memory and comment for user review.
    - Proceed with recognized tools only.

- **If a tool/template is missing:**  
    - Use a minimal Markdown stub.
    - Log and comment:  
        *"Template for [tool] missing, used minimal stub. Please review."*

#### Robust Execution Sequence

1. **Profile Target:**  
    - If no valid repo URL, halt and request correction.

2. **Generate `subject_slug`:**  
    - If generation fails, fallback to date-based slug: `unknown-subject-YYYYMMDD-HHMMSS`.

3. **Tool/Application Loop:**  
    - For each recognized selected tool, execute corresponding analysis.
    - Log skipped/unimplemented tools in Process Memory and comment on Issue.

4. **Intent Inference:**  
    - If `intent` is blank, attempt inference; if unable, set as `"(unknown)"` and log.

5. **Artifact Generation:**  
    - If output file exists, add numeric suffix (e.g., `-2.md`).
    - On write errors or file access fail, create fallback in `/errors/` with timestamp.
    - Always use `[subject_slug]` subfolder; if unavailable, use `/atomic/unknown-subject/`.

6. **Process Memory:**  
    - Always produce or update, even if investigation incomplete or aborts.

7. **Sensitive Materials/Paradigm Shifts:**  
    - If possible, isolate; else, comment and skip with log.

8. **System Maintenance:**  
    - On manifest/index write error, create `/catalogue/errors/manifest-FAILED-YYYYMMDD-HHMMSS.json`, log failure, and comment on Issue.

9. **Pull Request/Delivery:**  
    - If PR creation or file push fails, comment with diagnostics and log in Process Memory.

---

### B. Task Filing ("Execute Task Filing Protocol")

- **Missing/invalid `title`, `description`, etc.:**  
    - Comment, log, halt.
    - If slug fails, use fallback: `unknown-task-YYYYMMDD-HHMMSS.md`.

- **Template/file errors:**  
    - Use minimal stub and comment/log.

- **Manifest errors:**  
    - Save to `/catalogue/errors/` and notify via Issue comment.

---

### C. Idea Filing ("Execute Idea Filing Protocol")

- **Missing/invalid `subject`, `observation`, or `impact`:**  
    - Comment, log, halt.
    - Generate fallback slug if necessary.

- **Template/file errors:**  
    - Use stub, log, comment.

- **Manifest/index issues:**  
    - Same as above (errors folder, diagnostics comment).

---

## III. General Operational Rules & Resilience

- **File Placement:** All artifacts use `[subject_slug]` subfolders; fallback to `/unknown-subject/` if slug not possible.
- **Template Usage:** On missing template, always use generic stub and log.
- **Catalogue Compliance:** Any cataloging error routes files to `/catalogue/errors/` with diagnostic notes.
- **Process Memory & Cross-linking:** Always update Process Memory (even on failure) and reference Issue/report context.
- **Diagnostics:** On any failure, a comment is left in the Issue detailing what happened and what remediation is needed.
- **Never Close on Partial Failure:** Do not close an Issue unless all artifacts are successfully generated and cataloged.
- **Language/Encoding Issues:** If fields are not in English or are unreadable, note in Process Memory and comment on Issue.

---

## IV. Example Output Structure

```
project-wisdom-library/
├── atomic/
│   └── auth-service/
│       ├── 2025-11-19-jwt-forensics.md
│       └── unknown-subject-20251119-010124.md
├── distillations/
│   └── auth-service/
│       └── 2025-11-19-auth-architecture.md
├── analyses/
│   └── auth-service/
│       └── 2025-11-19-hard-map-diagram.md
├── process_memory/
│   └── auth-service/
│       └── 2025-11-19-jwt-forensics.md
│       └── unknown-subject-20251119-010124.md
├── backlog/
│   └── auth-service/
│       └── 2025-11-19-shift-stateless.md
├── sensitive/
│   └── auth-service/
│       └── 2025-11-19-legacy-keys.md
├── ideas/
│   └── 2025-11-19-auth-service-drift.md
├── catalogue/
│   ├── manifest.json
│   ├── index.md
│   └── errors/
│        └── manifest-FAILED-20251119-010124.json
├── errors/
│   └── atomic/
│       └── unknown-subject-20251119-010124.md
└── README.md
```

---

## V. Quick Reference: What Happens When
| **If…**                                              | **Copilot will…**                                                                               |
|------------------------------------------------------|--------------------------------------------------------------------------------------------------|
| No agent_prompt payload or malformed YAML            | Comment diagnostic & halt                                                                       |
| Required scenario field missing/ambiguous            | Comment diagnostic & halt                                                                       |
| Tool or template missing/unrecognized                | Warn user, use basic stub, record in Process Memory, continue                                   |
| Manifest or index update fails                       | Save to errors folder, comment on issue                                                         |
| Slug or filename fails                               | Use fallback (unknown-subject/timestamp), continue                                              |
| Any file push, PR, or artifact creation fails        | Comment on Issue, log in Process Memory, continue when possible                                 |
| Language/unreadable input                            | Note in diagnostics, comment, continue                                                          |
| Multiple failures                                    | Record all in diagnostics, never close unless all steps complete                                 |

---

**This workflow ensures that every failure is reported, documented, and visible, making Copilot reliable, resilient, and always accountable.**

If you'd like this adapted for any specific templates, or need sample error comments/diagnostics, let me know!
