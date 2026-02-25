---
name: fix
description: Fix open issues in a Claude Code plugin with non-regression checks. Use when the user asks to fix plugin issues, resolve plugin bugs, implement fixes for tracked issues, or debug a plugin problem.
argument-hint: "[plugin-path] [--issue ISSUE-NNN] [--all-open] [--dry-run]"
---

# Plugin Issue Fix

Fix tracked issues from ISSUES.md with non-regression guarantees.

## Parse Arguments

Parse `$ARGUMENTS`:
- **First positional argument** (optional): Path to plugin directory. If omitted, use current working directory.
- `--issue ISSUE-NNN`: Fix a specific issue
- `--all-open`: Attempt to fix all open issues (process in severity order: critical → major → minor → enhancement)
- `--dry-run`: Analyze and propose fixes without applying them

If neither `--issue` nor `--all-open` is specified, list open issues and ask the user which to fix.

## Locate Plugin

**CRITICAL: Cache vs Repo**
- `~/.claude/plugins/cache/` contains READ-ONLY installed copies — NEVER edit these
- Always resolve to the real git repo before editing. Use atlas: `atlas_search_projects(query="plugin-name")` to find the repo path
- If the plugin-path points into `~/.claude/plugins/cache/`, STOP and find the real repo first

1. Verify `.claude-plugin/plugin.json` exists at the resolved repo path
2. Read plugin name and version

## Non-Regression Protocol

**This step is MANDATORY before making any changes.**

Read `knowledge/lifecycle-formats.md` for the non-regression protocol.

1. **Read ISSUES.md** — collect ALL resolved issues
2. For each resolved issue, record:
   - Issue ID, title, and resolution
   - Files and code sections mentioned
   - Date resolved
3. This is the "protected set" — must remain intact after fixes

## For Each Issue to Fix

### 1. Understand the Issue

Read the issue entry from ISSUES.md:
- Description: What is wrong
- Context: How it was discovered
- Notes: Any additional observations
- Severity: Determines priority

### 2. Investigate

Based on the issue description:
- Read the relevant files mentioned or implied
- Understand the current state of the code/content
- Identify the root cause
- Determine what needs to change

### 3. Plan the Fix

For each proposed change:
1. **Check against protected set** — will this change touch any file/section involved in a resolved issue?
   - If YES and the change would modify the resolved fix: **SKIP** and explain the conflict
   - If YES but the change is in a different section of the same file: proceed with caution
   - If NO: proceed normally

2. Describe the fix clearly

### 4. Apply the Fix (unless --dry-run)

- Use Edit tool for file modifications
- Use Write tool only for new files
- Make minimal, focused changes — fix only what the issue describes

### 5. Verify Non-Regression

After applying the fix:
1. Re-read files involved in ALL resolved issues
2. Verify each resolved fix is still present and functional
3. If any regression detected:
   - REVERT the change that caused it
   - Report the conflict to the user
   - Do NOT mark the current issue as resolved

### 6. Update ISSUES.md

If fix was successfully applied and verified:
- Change status to `resolved`
- Set resolved date to today
- Write resolution description explaining what was changed

If fix could not be applied:
- Add a note with today's date explaining the blocker

## Post-Fix Summary

Update REFLECTIONS.md — prepend fix entry using the format from `knowledge/lifecycle-formats.md`.

## Output

Display summary:

```
Fix results for {plugin-name} v{version}

{For each issue attempted:}
ISSUE-{NNN} ({severity}): {title}
  Status: {resolved | blocked | skipped}
  {Resolution description or reason for skip}

Non-regression: {N} resolved issues verified — {all intact | M regressions detected}

{Updated ISSUES.md and REFLECTIONS.md | Dry run — no files modified}
```

## Handling Complex Fixes

If an issue requires changes across multiple files or significant refactoring:
1. Break the fix into steps
2. Verify non-regression after EACH step
3. If any step causes regression, revert that step and report partial progress
4. Update issue status to `in-progress` with notes on what was completed
