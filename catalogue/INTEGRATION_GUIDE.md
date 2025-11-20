# Step-by-Step Integration Guide for claude-agent-mcp-skills

## For Non-Technical Users

This guide provides **two options** for integrating the claude-agent-mcp-skills investigation:
1. **Option A (Recommended)**: One-shot automated script 
2. **Option B**: Manual step-by-step instructions

---

## ⚠️ Important: Pre-existing Manifest Errors

The `catalogue/manifest.json` file has **multiple pre-existing structural errors** that must be fixed before adding new content:
- Line 1497: Missing closing bracket after "wisdom-ladder"
- Line 1558: Missing structure after "special_focus"  
- And potentially more cascading errors

These errors existed BEFORE this investigation and prevent the manifest from being valid JSON.

---

## Option A: Automated One-Shot Script (RECOMMENDED)

This script automatically fixes all pre-existing errors AND integrates the new investigation.

### Step 1: Run the Integration Script

```bash
cd /home/runner/work/project-wisdom-library/project-wisdom-library
python3 catalogue/integrate_investigation.py
```

### Step 2: Review the Changes

```bash
git diff catalogue/manifest.json
```

### Step 3: Commit and Push

```bash
git add catalogue/manifest.json
git commit -m "Fix manifest errors and integrate claude-agent-mcp-skills investigation"
git push
```

**That's it!** The script handles everything automatically.

---

## Option B: Manual Integration (For Advanced Users)

If you prefer manual control or the script fails, follow these detailed steps.

### Prerequisites

You'll need a text editor that can handle large JSON files (VS Code, Sublime Text, or vim).

### Step 1: Backup the Current Manifest

```bash
cp catalogue/manifest.json catalogue/manifest.json.backup
```

### Step 2: Fix All Pre-existing Errors

The manifest has multiple structural errors. Here are ALL the fixes needed:

#### Fix 1: Line ~1497 - Missing closing bracket after "wisdom-ladder"

**Find this (around line 1490-1497):**
```json
          "local-first",
          "level-1",
          "wisdom-ladder"
    "atomic": [
```

**Replace with:**
```json
          "local-first",
          "level-1",
          "wisdom-ladder"
        ],
        "author": "GitHub Copilot",
        "status": "complete",
        "related": [],
        "strategic_context": "Skills-as-Infrastructure MCP implementation"
      }
    ],
    "atomic": [
```

#### Fix 2: Line ~1558 - Missing structure after "special_focus"

**Find this (around line 1554-1559):**
```json
            "Uvicorn"
          ],
          "special_focus": "Skills Patterns Extraction"
          "claude-code-plugins-plus-decision-forensics-2025-11-20"
        ],
```

**Replace with:**
```json
            "Uvicorn"
          ],
          "special_focus": "Skills Patterns Extraction"
        },
        "related": [
          "claude-code-plugins-plus-decision-forensics-2025-11-20"
        ],
```

### Step 3: Validate the Fixes

After applying BOTH fixes, validate:

```bash
python3 -c "import json; json.load(open('catalogue/manifest.json')); print('✓ manifest.json is now valid JSON')"
```

**Expected output:** `✓ manifest.json is now valid JSON`

If you see errors, review your changes carefully. The JSON must be perfectly formatted.

### Step 4: Add the New Investigation Entry

Once the manifest is valid, add the new investigation at the END of the array.

**Current end of file:**
```json
  },
  {
    "issue": "30",
    "target": "\"https://github.com/yusufkaraaslan/Skill_Seekers\"",
    "depth": "\"Long-Form (Deep distillation)\"",
    "intent": "\"\"",
    "artifact": "backlog/skill_seekers/2025-11-20-paradigm-shift-unknown.md",
    "created": "2025-11-20"
  }
]
```

**Change to (add comma after Issue 30):**
```json
  },
  {
    "issue": "30",
    "target": "\"https://github.com/yusufkaraaslan/Skill_Seekers\"",
    "depth": "\"Long-Form (Deep distillation)\"",
    "intent": "\"\"",
    "artifact": "backlog/skill_seekers/2025-11-20-paradigm-shift-unknown.md",
    "created": "2025-11-20"
  },
  {
    "issue": "38",
    "target": "https://github.com/dbbuilder/claude-agent-mcp-skills",
    "depth": "Long-Form (Deep distillation)",
    "intent": "",
    "created": "2025-11-20",
    "status": "complete",
    "analyses": [
      ... (copy entire content from catalogue/claude-agent-mcp-skills-manifest-entry.json)
    ]
  }
]
```

### Step 5: Final Validation

```bash
python3 -c "import json; data = json.load(open('catalogue/manifest.json')); print(f'✓ Valid JSON with {len(data)} entries'); print(f'✓ Last entry: Issue #{data[-1][\"issue\"]}')"
```

**Expected output:**
```
✓ Valid JSON with XX entries
✓ Last entry: Issue #38
```

### Step 6: Commit Changes

```bash
git add catalogue/manifest.json
git commit -m "Fix manifest errors and integrate claude-agent-mcp-skills investigation"
git push
```

---

## Verification Checklist

After integration (either option), verify:

- [ ] `manifest.json` is valid JSON (no parse errors)
- [ ] Last entry in manifest is Issue #38  
- [ ] Investigation has 8 artifacts (1 analysis, 3 atomic, 2 distillations, 1 process_memory, 1 backlog)
- [ ] No git conflicts
- [ ] Changes are committed and pushed

Quick verification:
```bash
python3 << 'EOF'
import json
data = json.load(open('catalogue/manifest.json'))
last = data[-1]
print(f"✓ Valid JSON with {len(data)} entries")
print(f"✓ Last entry: Issue #{last['issue']}")
print(f"✓ Analyses: {len(last.get('analyses', []))}")
print(f"✓ Atomic: {len(last.get('atomic', []))}")
print(f"✓ Distillations: {len(last.get('distillations', []))}")
print(f"✓ Process Memory: {len(last.get('process_memory', []))}")
print(f"✓ Backlog: {len(last.get('backlog', []))}")
EOF
```

Expected output shows all artifact counts.

---

## Troubleshooting

### Script Fails with "Validation failed"
**Cause:** Manifest has different errors than expected  
**Solution:** Use Option B (manual integration) instead

### "FileNotFoundError" for standalone entry
**Cause:** File `catalogue/claude-agent-mcp-skills-manifest-entry.json` missing  
**Solution:** Ensure you're in the correct directory and file exists

### JSON validation still fails after fixes
**Cause:** Typo in manual edits or missed a fix  
**Solution:** 
1. Restore from backup: `cp catalogue/manifest.json.backup catalogue/manifest.json`
2. Try automated script (Option A)
3. Or carefully re-apply manual fixes

### Git conflicts
**Cause:** Someone else modified manifest.json  
**Solution:**
1. Pull latest changes: `git pull`
2. Re-run the integration process
3. Resolve any conflicts manually

---

## Why This Approach?

The two-option approach provides:

1. **Safety**: Automated script includes validation at every step
2. **Flexibility**: Manual option for users who want full control  
3. **Transparency**: Both options clearly document what changes are made
4. **Robustness**: Handles pre-existing errors that must be fixed first

The split is necessary because:
- The manifest has pre-existing errors that MUST be fixed first
- Fixing errors + adding content in one operation is safest
- Manual option provides fallback if automation fails

---

## Support

**Files Created:**
- `catalogue/claude-agent-mcp-skills-manifest-entry.json` - The new investigation entry
- `catalogue/integrate_investigation.py` - Automated integration script  
- `catalogue/INTEGRATION_GUIDE.md` - This guide
- `catalogue/MANIFEST_INTEGRATION_STATUS.md` - Status documentation

**Investigation Artifacts:** All 8 files created in:
- `analyses/claude-agent-mcp-skills/`
- `atomic/claude-agent-mcp-skills/`
- `distillations/claude-agent-mcp-skills/`
- `process_memory/claude-agent-mcp-skills/`
- `backlog/claude-agent-mcp-skills/`

**Verification Commands:**
```bash
# Check all artifacts exist
find analyses/claude-agent-mcp-skills atomic/claude-agent-mcp-skills distillations/claude-agent-mcp-skills process_memory/claude-agent-mcp-skills backlog/claude-agent-mcp-skills -name "*.md" | wc -l
# Should return: 8

# Check standalone entry is valid
python3 -c "import json; json.load(open('catalogue/claude-agent-mcp-skills-manifest-entry.json')); print('✓ Valid')"

# Check current manifest state
python3 -c "import json; json.load(open('catalogue/manifest.json'))" 2>&1 | head -1
```

---

**Last Updated:** 2025-11-20  
**Investigation:** Issue #38 - claude-agent-mcp-skills  
**Status:** Ready for integration  
**Recommended Approach:** Option A (automated script)

