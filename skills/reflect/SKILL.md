---
name: reflect
description: "Run a comprehensive health audit on a Claude Code plugin — checks structure, skills quality, knowledge size, hooks, MCP config, and cross-references. Use when the user asks to \"analyze plugin health\", \"audit plugin\", \"assess plugin quality\", \"review plugin structure\", \"run self-assessment\", or \"how healthy is this plugin\". Also trigger proactively after significant plugin changes to catch regressions."
argument-hint: "[plugin-path] [--brief]"
---

# Plugin Self-Reflection

Perform a comprehensive health analysis. Write findings to REFLECTIONS.md.

## Parse Arguments

Parse `$ARGUMENTS`:
- **First positional** (optional): Path to plugin directory. Default: current working directory.
- `--brief`: Summary only, skip writing REFLECTIONS.md.

**Cache guard**: `~/.claude/plugins/cache/` is READ-ONLY. Resolve to the real git repo via atlas: `atlas_search_projects(query="plugin-name")`.

## Analysis Areas

### 1. Structure
- `.claude-plugin/plugin.json` valid with name, description, version (semver)
- `skills/` has at least one skill
- `CLAUDE.md` and `README.md` exist

### 2. Skills
For each `skills/*/SKILL.md`:
- Valid YAML frontmatter with name, description
- Name matches directory name
- Description includes trigger phrases and is proactive
- Body has clear step-by-step instructions
- All referenced knowledge files exist
- No references to non-existent tools

### 3. Knowledge
For each file in `knowledge/**/*.md`:
- Individual file < 10 KB, total < 50 KB
- Content is project-specific (not generic filler)
- No broken cross-references or duplicate content

### 4. Hooks (if present)
- `hooks/hooks.json` valid JSON
- Scripts exist and are executable
- Exit codes and stdin handling documented

### 5. MCP (if present)
- `.mcp.json` valid JSON
- Servers have `command` and `args`
- Uses `${CLAUDE_PLUGIN_ROOT}` for local paths

### 6. Cross-References
- Skills don't reference missing knowledge files
- CLAUDE.md consistent with actual structure
- README.md lists all available skills

### 7. Issues Integration
If ISSUES.md exists: count open vs resolved, check for regressions.

## Write REFLECTIONS.md

Read `knowledge/lifecycle-formats.md` for format. Prepend entry:

```markdown
## {today's date} — full-analysis

### Observations
- {findings per area}

### What Worked Well
- {positive patterns}

### Improvement Opportunities
- {actionable suggestions, ordered by impact}

### Issues Discovered
- {new ISSUE-NNN entries if created, or "None"}
```

For critical/major findings, auto-create entries in ISSUES.md.

## Output

```
Reflection complete for {plugin-name} v{version}

Structure:  pass/warn/fail
Skills:     N total, M with issues
Knowledge:  size KB across N files
Hooks:      present/absent (status)
MCP:        present/absent (status)
Issues:     N open, M resolved

Top 3 improvement opportunities

Full analysis written to REFLECTIONS.md
```
