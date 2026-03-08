---
name: issues
description: "Track bugs and problems in a local ISSUES.md file. Use when the user wants to log, note, or record a problem for later — not fix it now. Also use for: listing what's currently tracked, marking an ISSUE-NNN as resolved, or updating issue status. Key triggers: \"log it\", \"note it somewhere\", \"what issues are we tracking\", \"mark ISSUE-NNN as resolved\", reporting a problem with no immediate action requested. Do NOT trigger when the user wants to actively fix, debug, investigate, optimize, or audit something, or when they ask to create a relay handoff or open a GitHub/Jira ticket. This skill is for lightweight documentation of known problems — record now, fix later."
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
