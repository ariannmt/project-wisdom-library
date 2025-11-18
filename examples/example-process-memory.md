# Example: Process Memory & Epistemic History

## 1. Session Context
**Date:** 2025-11-18
**Agents Active:** Claude-3.5-Sonnet
**Strategic Context:** Q4 Security Certification; User is worried that the current JWT complexity is "technical debt" we should abandon.
**Frustrations/Uncertainties:** - Team believes JWT refresh logic is "too hard" to maintain.
- Uncertainty if we originally chose JWT for a good reason or just followed a trend.

## 2. Epistemic History (The Narrative)

### The Evolution of Thought
- **Initial State:** We entered the session assuming the JWT implementation was "legacy bloat" that should be replaced with simple Session Cookies.
- **The Pivot/Insight:** Analysis of `git blame` and old PRs (#145) revealed that **Mobile App requirements** were the hard constraint. Cookies don't work well for the React Native app.
- **Final State:** We validated that the complexity is *necessary* for the Mobile requirement. The frustration isn't "bad code," it's "missing documentation" on *why* it exists.

### The Roads Not Taken (Negative Knowledge)
- **Option A (Session Cookies):** Discarded. While simpler for Web, it would require a separate auth stack for Mobile, doubling maintenance.
- **Option B (Auth0/Third-party):** Discarded in 2024 due to cost constraints at scale (100k+ MAU).

## 3. Structured Memory Record (Protocol Compliance)
*Agent: Generate the JSON object below based on the Narrative above, strictly adhering to the Project Wisdom Memory Schema.*

```json
{
  "id": "jwt-decision-validation-2025-11-18",
  "type": "StrategicDecision",
  "title": "Validate JWT Architecture for Mobile Support",
  "summary": "Confirmed JWT architecture is required for Mobile support; rejected pivot to Session Cookies.",
  "rationale": "Switching to Session Cookies would break the React Native app or force a dual-stack auth system. Current complexity is a trade-off for Unified Auth.",
  "source_adr": "[https://github.com/example/auth-service/blob/main/docs/adr/003-jwt-auth.md](https://github.com/example/auth-service/blob/main/docs/adr/003-jwt-auth.md)",
  "related_concepts": ["Mobile-First", "Stateless Auth", "Unified Architecture"],
  "timestamp_created": "2025-11-18T14:30:00Z",
  "confidence_level": 0.95,
  "phase": "Review",
  "provenance": {
    "author": "Claude-3.5-Sonnet",
    "trigger": "Security Audit Issue #42"
  },
  "links": ["auth-jwt-decision-forensics-2025-11-18"],
  "tags": ["authentication", "jwt", "mobile", "decision-forensics"]
}
```
