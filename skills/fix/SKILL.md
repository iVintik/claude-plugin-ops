---
name: fix
description: "Fix open issues tracked in a plugin's ISSUES.md with non-regression safety. Use when the user asks to \"fix plugin issues\", \"resolve plugin bugs\", \"fix this issue\", \"handle this bug\", \"implement the fix\", or mentions fixing tracked plugin problems. Works with ISSUES.md entries created by /plugin-ops:issues."
argument-hint: "[plugin-path] [--issue ISSUE-NNN] [--all-open] [--dry-run]"
---

# Plugin Issue Fix

Fix tracked issues from ISSUES.md with non-regression guarantees.

## Parse Arguments

Parse `$ARGUMENTS`:
- **First positional** (optional): Path to plugin directory. Default: current working directory.
- `--issue ISSUE-NNN`: Fix a specific issue.
- `--all-open`: Fix all open issues (severity order: critical → major → minor → enhancement).
- `--dry-run`: Analyze and propose fixes without applying.

If neither `--issue` nor `--all-open`, list open issues and ask which to fix.

**Cache guard**: `~/.claude/plugins/cache/` is READ-ONLY. Resolve to the real git repo via atlas: `atlas_search_projects(query="plugin-name")`.

## Non-Regression Protocol (mandatory)

Read `knowledge/lifecycle-formats.md` for the full protocol.

1. Read ISSUES.md — collect all resolved issues with ID, title, resolution, files
2. This "protected set" must remain intact after fixes

## For Each Issue

### 1. Understand
Read the ISSUES.md entry: description, context, severity, notes.

### 2. Investigate
Read relevant files, identify root cause, determine what needs to change.

### 3. Plan
For each proposed change, check against protected set:
- Touches resolved fix → **SKIP**, explain conflict
- Same file but different section → proceed with caution
- No overlap → proceed

### 4. Apply (unless --dry-run)
Minimal, focused changes. Edit tool for modifications, Write only for new files.

### 5. Verify
Re-read files for all resolved issues. If regression detected: revert the change, report conflict, do NOT mark current issue resolved.

### 6. Update ISSUES.md
Success: status → `resolved`, set date, write resolution.
Blocked: add note with date explaining blocker.

## Post-Fix

Prepend fix entry to REFLECTIONS.md (format from `knowledge/lifecycle-formats.md`).

## Output

```
Fix results for {plugin-name} v{version}

ISSUE-{NNN} ({severity}): {title}
  Status: resolved | blocked | skipped
  {resolution or reason}

Non-regression: {N} resolved issues verified — {all intact | M regressions}
```

For multi-file fixes: break into steps, verify non-regression after each step, revert on regression, update status to `in-progress` with partial progress notes.
