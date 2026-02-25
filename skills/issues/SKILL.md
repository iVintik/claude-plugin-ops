---
name: issues
description: View, add, update, or resolve issues in a plugin's ISSUES.md. Use when the user asks to log an issue, log a bug, track a bug, track this problem, note this issue, report a plugin issue, list plugin issues, resolve an issue, update issue status, or manage plugin issue tracking.
argument-hint: "[plugin-path] [--add] [--resolve ISSUE-NNN] [--update ISSUE-NNN] [--list] [--init]"
---

# Plugin Issues Management

Manage the structured ISSUES.md file for any Claude Code plugin.

## Parse Arguments

Parse `$ARGUMENTS`:
- **First positional argument** (optional): Path to plugin directory. If omitted, use current working directory.
- `--init`: Create a new ISSUES.md file
- `--add`: Add a new issue (will prompt for details)
- `--resolve ISSUE-NNN`: Mark an issue as resolved
- `--update ISSUE-NNN`: Update an existing issue
- `--list`: List all issues with status summary (default if no flag given)

If no flags are provided, default to `--list`.

## Locate Plugin

**CRITICAL: Cache vs Repo**
- `~/.claude/plugins/cache/` contains READ-ONLY installed copies — NEVER edit these
- Always resolve to the real git repo. Use atlas: `atlas_search_projects(query="plugin-name")` to find the repo path

1. Check if the target directory has `.claude-plugin/plugin.json`
2. If not found, search parent directories for a directory containing `.claude-plugin/plugin.json`
3. If still not found, ask the user to specify the plugin path

Read the plugin name from `plugin.json` for display purposes.

## --init: Initialize ISSUES.md

Check if ISSUES.md already exists at the plugin root. If it does, inform the user and do nothing.

Create `ISSUES.md` with:

```markdown
# Plugin Issues

<!-- Managed by /plugin-ops:issues — see knowledge/lifecycle-formats.md for format -->

No issues tracked yet.
```

## --list: List Issues

Read ISSUES.md from the plugin root.

Display a summary table:

```
Plugin: {name} — {count} issues ({open} open, {resolved} resolved)

| ID | Status | Severity | Title |
|----|--------|----------|-------|
| ISSUE-001 | open | major | Title here |
| ISSUE-002 | resolved | minor | Another issue |
```

If no issues exist, say so.

## --add: Add New Issue

Determine the next issue ID by finding the highest existing ID and incrementing.

**Extract from context first — only prompt for what's missing.**

The user often provides issue details inline (e.g. "log issue: X should not require Y"). Before prompting, check the user's message and conversation context for:
1. **Title**: Short description of the problem. **If inferable from context, use it.**
2. **Severity**: critical / major / minor / enhancement. **Default to minor if not stated.**
3. **Context**: How was this discovered? **Default to "Reported by user during development" if not stated.**
4. **Description**: What is wrong or needs improvement? **If inferable from context, use it.**

**Only ask the user for fields that cannot be reasonably inferred.** If all 4 fields are clear from context, write the issue directly without any prompts.

If ISSUES.md does not exist yet, create it automatically (same as `--init`) before appending.

Generate the issue entry using the format from `knowledge/lifecycle-formats.md`:

```markdown
## ISSUE-{NNN}: {Title}
- **Status**: open
- **Severity**: {severity}
- **Found**: {today's date YYYY-MM-DD}
- **Resolved**: —
- **Context**: {context}
- **Description**: {description}
- **Resolution**: —
- **Notes**:
```

Append the new issue to ISSUES.md (before any trailing whitespace).

Display the created issue ID and summary.

## --resolve ISSUE-NNN: Resolve Issue

Read ISSUES.md and find the specified issue.

If issue not found, report error.

If issue is already resolved, inform the user.

Ask the user for a resolution description.

Update the issue:
- Change `**Status**: open` (or `in-progress`) to `**Status**: resolved`
- Set `**Resolved**: {today's date}`
- Set `**Resolution**: {user's description}`

Display confirmation.

## --update ISSUE-NNN: Update Issue

Read ISSUES.md and find the specified issue.

Ask the user what to update:
- Status change (open → in-progress, etc.)
- Add a note with today's date
- Update severity
- Update description

Apply the changes using the Edit tool.

Display the updated issue.

## Error Handling

- If ISSUES.md doesn't exist and action is not `--init` or `--add`, suggest running `--init` first
- If an issue ID doesn't exist, list available IDs
- If ISSUES.md is malformed, warn the user and attempt to parse what's available
