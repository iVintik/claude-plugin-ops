---
name: issues
description: "View, add, update, or resolve issues in a plugin's ISSUES.md. Use when the user asks to \"log an issue\", \"track a bug\", \"note this problem\", \"report a plugin issue\", \"list plugin issues\", \"resolve an issue\", \"update issue status\", \"what issues are open\", or any form of plugin issue management. Also trigger proactively when you discover a defect during plugin work — file it immediately."
argument-hint: "[plugin-path] [--add] [--resolve ISSUE-NNN] [--update ISSUE-NNN] [--list] [--init]"
---

# Plugin Issues Management

Manage the structured ISSUES.md file for any Claude Code plugin.

## Parse Arguments

Parse `$ARGUMENTS`:
- **First positional** (optional): Path to plugin directory. Default: current working directory.
- `--init`: Create a new ISSUES.md
- `--add`: Add a new issue (prompts for details)
- `--resolve ISSUE-NNN`: Mark as resolved
- `--update ISSUE-NNN`: Update an existing issue
- `--list`: List all issues (default if no flag)

**Cache guard**: `~/.claude/plugins/cache/` is READ-ONLY. Resolve to the real git repo via atlas: `atlas_search_projects(query="plugin-name")`.

## --init: Initialize ISSUES.md

Skip if exists. Create at plugin root:

```markdown
# Plugin Issues

<!-- Managed by /plugin-ops:issues — see knowledge/lifecycle-formats.md for format -->

No issues tracked yet.
```

## --list: List Issues

Read ISSUES.md, display summary:

```
Plugin: {name} — {count} issues ({open} open, {resolved} resolved)

| ID | Status | Severity | Title |
|----|--------|----------|-------|
```

## --add: Add New Issue

**Extract from context first — only prompt for missing fields.** The user often provides details inline (e.g. "log issue: X should not require Y"). Check conversation context for:
1. **Title**: Short problem description. Default if inferable.
2. **Severity**: critical/major/minor/enhancement. Default: minor.
3. **Context**: How discovered. Default: "Reported during development".
4. **Description**: What's wrong. Default if inferable.

If all 4 are clear from context, write directly — no prompts needed. Auto-create ISSUES.md if missing.

Format from `knowledge/lifecycle-formats.md`:

```markdown
## ISSUE-{NNN}: {Title}
- **Status**: open
- **Severity**: {severity}
- **Found**: {today YYYY-MM-DD}
- **Resolved**: —
- **Context**: {context}
- **Description**: {description}
- **Resolution**: —
- **Notes**:
```

## --resolve ISSUE-NNN

Find issue, update: status → `resolved`, set resolved date, set resolution description (ask user).

## --update ISSUE-NNN

Find issue, ask what to update: status, notes, severity, or description. Apply with Edit tool.

## Error Handling

- No ISSUES.md + not `--init`/`--add`: suggest `--init`
- Issue ID not found: list available IDs
- Malformed ISSUES.md: warn and parse what's available
