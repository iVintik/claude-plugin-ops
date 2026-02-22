---
name: reflect
description: Run self-reflection analysis on a Claude Code plugin. Use when the user asks to analyze plugin health, audit a plugin, assess plugin quality, review plugin structure, or run a plugin self-assessment.
argument-hint: "[plugin-path] [--brief]"
---

# Plugin Self-Reflection

Perform a comprehensive analysis of a Claude Code plugin's health and quality. Write findings to REFLECTIONS.md.

## Parse Arguments

Parse `$ARGUMENTS`:
- **First positional argument** (optional): Path to plugin directory. If omitted, use current working directory.
- `--brief`: Output summary only, skip detailed analysis

## Locate Plugin

1. Check if the target directory has `.claude-plugin/plugin.json`
2. If not found, search parent directories for `.claude-plugin/plugin.json`
3. Read plugin.json for name and version

## Analysis Checklist

Perform each check and record findings.

### 1. Structure Audit

- [ ] `.claude-plugin/plugin.json` exists and is valid JSON
- [ ] `plugin.json` has required fields: name, description, version
- [ ] Description is non-empty and not a TODO placeholder
- [ ] Version follows semver format
- [ ] `skills/` directory exists with at least one skill
- [ ] `CLAUDE.md` exists
- [ ] `README.md` exists

### 2. Skills Audit

For each skill in `skills/*/SKILL.md`:
- [ ] SKILL.md has valid YAML frontmatter (name, description, argument-hint)
- [ ] `name` matches directory name
- [ ] `description` includes trigger phrases
- [ ] Body has clear step-by-step instructions
- [ ] References to knowledge files exist (files actually present)
- [ ] No references to non-existent tools or skills

Count: total skills, skills with issues.

### 3. Knowledge Audit

For each file in `knowledge/**/*.md`:
- [ ] File size < 10 KB
- [ ] Total knowledge size < 50 KB
- [ ] Content is not generic (contains project-specific information)
- [ ] No broken internal cross-references
- [ ] No duplicate content across files

Report: file count, total size, largest file, any oversized files.

### 4. Hooks Audit (if hooks/ exists)

- [ ] `hooks/hooks.json` is valid JSON
- [ ] Referenced scripts exist
- [ ] Scripts are executable
- [ ] Scripts handle stdin correctly
- [ ] Exit codes are documented

### 5. MCP Audit (if .mcp.json exists)

- [ ] `.mcp.json` is valid JSON
- [ ] Each server has `command` and `args`
- [ ] `${CLAUDE_PLUGIN_ROOT}` used for local paths

### 6. Cross-Reference Check

- [ ] Skills don't reference non-existent knowledge files
- [ ] Knowledge files don't reference non-existent skills
- [ ] CLAUDE.md is consistent with actual structure
- [ ] README.md lists all available skills

### 7. Issues Integration

If ISSUES.md exists:
- [ ] Count open vs resolved issues
- [ ] Check if any resolved issues might have regressed (files changed since resolution date)
- [ ] Identify patterns in open issues

## Write REFLECTIONS.md

Read `knowledge/lifecycle-formats.md` for the REFLECTIONS.md format.

Create or prepend to REFLECTIONS.md at the plugin root:

```markdown
## {today's date} — full-analysis

### Observations
- {Structure findings}
- {Skills findings}
- {Knowledge findings}

### What Worked Well
- {Positive patterns found}

### Improvement Opportunities
- {Actionable suggestions, ordered by impact}

### Issues Discovered
- {New ISSUE-NNN entries if created, or "None"}
```

## Create Issues

For any critical or major findings, automatically create entries in ISSUES.md using the format from `knowledge/lifecycle-formats.md`. Link from REFLECTIONS.md to ISSUE-NNN IDs.

## Output

Display a summary to the user:

```
Reflection complete for {plugin-name} v{version}

Structure:  {pass/warn/fail}
Skills:     {N} total, {M} with issues
Knowledge:  {size} KB across {N} files
Hooks:      {present/absent} {status if present}
MCP:        {present/absent} {status if present}
Issues:     {N} open, {M} resolved

{Top 3 improvement opportunities}

Full analysis written to REFLECTIONS.md
```

If `--brief` flag is set, only show the summary table without writing to REFLECTIONS.md.
