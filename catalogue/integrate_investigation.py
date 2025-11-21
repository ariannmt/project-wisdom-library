#!/usr/bin/env python3
"""
One-shot integration script for claude-agent-mcp-skills investigation

This script:
1. Fixes the pre-existing error in manifest.json (line 1497)
2. Validates the fix
3. Integrates the new investigation entry
4. Validates the final result

Usage:
    python3 catalogue/integrate_investigation.py
"""
import json
import sys
from pathlib import Path

def main():
    repo_root = Path("/home/runner/work/project-wisdom-library/project-wisdom-library")
    manifest_path = repo_root / "catalogue" / "manifest.json"
    entry_path = repo_root / "catalogue" / "claude-agent-mcp-skills-manifest-entry.json"
    
    print("=" * 70)
    print("  Claude Agent MCP Skills - Manifest Integration Script")
    print("=" * 70)
    print()
    
    # Step 1: Read the manifest
    print("📖 Step 1: Reading manifest.json...")
    try:
        with open(manifest_path, 'r') as f:
            content = f.read()
        print(f"   ✓ Read {len(content)} characters from manifest.json")
    except FileNotFoundError:
        print(f"   ✗ Error: {manifest_path} not found")
        return 1
    
    # Step 2: Fix the pre-existing errors
    print("\n🔧 Step 2: Fixing pre-existing errors in manifest...")
    
    fixes_applied = []
    
    # Fix 1: Missing closing bracket and metadata after "wisdom-ladder" (line ~1497)
    old_pattern_1 = '''          "wisdom-ladder"
    "atomic": ['''
    
    new_pattern_1 = '''          "wisdom-ladder"
        ],
        "author": "GitHub Copilot",
        "status": "complete",
        "related": [],
        "strategic_context": "Skills-as-Infrastructure MCP implementation"
      }
    ],
    "atomic": ['''
    
    if old_pattern_1 in content:
        content = content.replace(old_pattern_1, new_pattern_1)
        fixes_applied.append("Line ~1497: Added missing closing bracket and metadata")
    
    # Fix 2: Missing closing bracket and related array after "special_focus" (line ~1558)
    old_pattern_2 = '''          "special_focus": "Skills Patterns Extraction"
          "claude-code-plugins-plus-decision-forensics-2025-11-20"
        ],'''
    
    new_pattern_2 = '''          "special_focus": "Skills Patterns Extraction"
        },
        "related": [
          "claude-code-plugins-plus-decision-forensics-2025-11-20"
        ],'''
    
    if old_pattern_2 in content:
        content = content.replace(old_pattern_2, new_pattern_2)
        fixes_applied.append("Line ~1558: Added missing closing bracket and related array")
    
    # Fix 3: Missing closing bracket after "wisdom-ladder" before "id" (line ~1605-1613)
    old_pattern_3 = '''          "wisdom-ladder"
        "id":'''
    
    new_pattern_3 = '''          "wisdom-ladder"
        ]
      },
      {
        "id":'''
    
    if old_pattern_3 in content:
        content = content.replace(old_pattern_3, new_pattern_3)
        fixes_applied.append("Line ~1605-1613: Added missing closing bracket before new object")
    
    # Fix 4: Missing closing bracket after "wisdom-ladder" before string (line ~1651-1664)
    # This is for entries where there's a related array that starts with a string
    old_pattern_4 = '''          "wisdom-ladder"
          "claude-code-plugins-plus-paradigm-extraction-2025-11-20"
        ],'''
    
    new_pattern_4 = '''          "wisdom-ladder"
        ],
        "related": [
          "claude-code-plugins-plus-paradigm-extraction-2025-11-20"
        ],'''
    
    if old_pattern_4 in content:
        content = content.replace(old_pattern_4, new_pattern_4)
        fixes_applied.append("Line ~1651-1664: Added missing closing bracket and related array")
    
    # Fix 5: Missing closing bracket after "level-1-4" before "id" (line ~1708-1712)
    old_pattern_5 = '''          "level-1-4"
        "id":'''
    
    new_pattern_5 = '''          "level-1-4"
        ]
      },
      {
        "id":'''
    
    if old_pattern_5 in content:
        content = content.replace(old_pattern_5, new_pattern_5)
        fixes_applied.append("Line ~1708-1712: Added missing closing bracket before new object")
    
    # Fix 6: Missing closing brace for metadata before string (line ~1699-1700)
    old_pattern_6 = '''          "applicability": "AI systems, web apps, APIs, distributed systems"
          "claude-code-plugins-plus-meta-patterns-2025-11-20"
        ],'''
    
    new_pattern_6 = '''          "applicability": "AI systems, web apps, APIs, distributed systems"
        }
      },
      {
        "id": "claude-code-plugins-plus-paradigm-extraction-2025-11-20",
        "title": "Paradigm Extraction: Claude Code Plugins Plus",
        "date": "2025-11-20",
        "type": "distillation",
        "path": "/distillations/claude-code-plugins-plus/2025-11-20-paradigm-extraction.md",
        "description": "7 fundamental paradigm shifts",
        "tags": ["paradigm-extraction", "worldview-shifts"],
        "author": "GitHub Copilot",
        "status": "complete",
        "related": [
          "claude-code-plugins-plus-meta-patterns-2025-11-20"
        ],'''
    
    if old_pattern_6 in content:
        content = content.replace(old_pattern_6, new_pattern_6)
        fixes_applied.append("Line ~1699-1700: Added missing closing brace and restructured entry")
    
    if fixes_applied:
        for fix in fixes_applied:
            print(f"   ✓ Fixed: {fix}")
    else:
        print("   ⚠️  Warning: Expected patterns not found")
        print("   Errors may have been fixed already or are different")
        print("   Continuing with validation...")

    
    # Step 3: Validate the fix
    print("\n✅ Step 3: Validating fix...")
    try:
        data = json.loads(content)
        print(f"   ✓ Manifest is now valid JSON")
        print(f"   ✓ Contains {len(data)} investigation entries")
    except json.JSONDecodeError as e:
        print(f"   ✗ Validation failed at line {e.lineno}, column {e.colno}")
        print(f"   ✗ Error: {e.msg}")
        print("\n   Cannot proceed. Please fix the JSON error manually.")
        return 1
    
    # Step 4: Read the new investigation entry
    print("\n📖 Step 4: Reading new investigation entry...")
    try:
        with open(entry_path, 'r') as f:
            new_entry = json.load(f)
        print(f"   ✓ Loaded entry for Issue #{new_entry['issue']}")
        print(f"   ✓ Investigation: {new_entry['target']}")
    except FileNotFoundError:
        print(f"   ✗ Error: {entry_path} not found")
        return 1
    except json.JSONDecodeError as e:
        print(f"   ✗ Error: Entry file is not valid JSON")
        return 1
    
    # Check if entry already exists
    existing_issues = [str(entry.get('issue', '')) for entry in data]
    if '38' in existing_issues:
        print("   ⚠️  Warning: Issue #38 already exists in manifest")
        print("   Skipping addition to avoid duplicates")
        print("\n✅ Manifest is already integrated!")
        return 0
    
    # Step 5: Add the new entry
    print("\n➕ Step 5: Adding new investigation entry...")
    data.append(new_entry)
    print(f"   ✓ Added Issue #{new_entry['issue']} to manifest")
    print(f"   ✓ Total entries now: {len(data)}")
    
    # Step 6: Write back the updated manifest
    print("\n💾 Step 6: Writing updated manifest...")
    try:
        with open(manifest_path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"   ✓ Wrote updated manifest to {manifest_path}")
    except Exception as e:
        print(f"   ✗ Error writing manifest: {e}")
        return 1
    
    # Step 7: Final validation
    print("\n✅ Step 7: Final validation...")
    try:
        with open(manifest_path, 'r') as f:
            final_data = json.load(f)
        print(f"   ✓ Final manifest is valid JSON")
        print(f"   ✓ Total entries: {len(final_data)}")
        print(f"   ✓ Last entry: Issue #{final_data[-1]['issue']}")
        
        # Verify the new entry
        last_entry = final_data[-1]
        if last_entry.get('issue') == '38':
            print(f"   ✓ Issue #38 successfully integrated")
            print(f"   ✓ Artifacts: {len(last_entry.get('analyses', []))} analyses, "
                  f"{len(last_entry.get('atomic', []))} atomic, "
                  f"{len(last_entry.get('distillations', []))} distillations")
        else:
            print(f"   ⚠️  Warning: Last entry is Issue #{last_entry.get('issue')}, not #38")
    except Exception as e:
        print(f"   ✗ Final validation failed: {e}")
        return 1
    
    print("\n" + "=" * 70)
    print("✅ Integration Complete!")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Review changes: git diff catalogue/manifest.json")
    print("2. Stage changes: git add catalogue/manifest.json")
    print("3. Commit: git commit -m 'Integrate claude-agent-mcp-skills investigation'")
    print("4. Push: git push")
    print()
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
