---
name: diagnose
description: "Diagnose why a Claude Code plugin skill fails to load, doesn't trigger when expected, errors out, or behaves unexpectedly. Use proactively whenever you notice a plugin or skill misbehaving, or when the user reports something like: \"why isn't this working\", \"plugin not triggering\", \"skill broken\", \"debug plugin\", \"diagnose plugin\", \"this skill should have fired\", \"fix plugin\", \"skill overlap\", \"wrong skill triggered\". Also trigger when a hook fails silently, a plugin won't load, or tools from an MCP server aren't available. Does NOT cover: overall plugin health audits (use reflect), size optimization (use optimize), or version releases (use release)."
argument-hint: "[plugin-path] [--skill SKILL-NAME]"
---

# Plugin Diagnostics

Investigate and report plugin defects. Frame findings as plugin defects, not agent failure — if a skill wasn't triggered, that's a description quality issue; if a hook failed, that's a configuration defect.

## Parse Arguments

Parse `$ARGUMENTS`:
- **First positional** (optional): Path to plugin directory. Default: current working directory.
- `--skill SKILL-NAME`: Focus on a specific skill.

If no plugin found at path, ask the user which plugin to diagnose.

**Cache guard**: `~/.claude/plugins/cache/` is READ-ONLY. Resolve to the real git repo via atlas: `atlas_search_projects(query="plugin-name")`.

## Diagnostic Steps

### 1. Plugin Structure
- `.claude-plugin/plugin.json` exists, valid JSON, has name/version/description
- Declared directories (`skills/`, `hooks/`, `agents/`, `knowledge/`) exist
- Referenced files in manifest actually exist on disk

### 2. Skills (most common defect source)

For each skill (or `--skill` target):

**Structure**: Valid YAML frontmatter with `name` + `description`, valid markdown body.

**Description quality** (the #1 reason skills don't trigger):
- Must be proactive: BAD "Reviews code" → GOOD "Use when user has modified code and needs review. Trigger proactively after changes."
- Must include trigger phrases the user would say
- Must specify proactive triggers if the skill should auto-fire

**Content**: No bare `$VARIABLE` outside code blocks, no broken refs to missing knowledge/files.

### 3. Hooks
- `hooks/hooks.json` valid JSON with correct event names
- Referenced scripts exist and are executable
- Timeouts reasonable for the operation

### 4. Agents
- Trigger descriptions match intended use
- Tools list appropriate for the task

### 5. Runtime Context
- Check remote repo issues: `gh issue list -R {repo}`
- Verify plugin is installed: `claude plugin list`
- Check for conflicting plugins with overlapping skill descriptions

## Report Format

```
Plugin Diagnostics: {plugin-name} v{version}

{DEFECT-1}: {category} — {short title}
  Location: {file-path}:{line-number}
  Severity: critical | major | minor
  Details: {what's wrong and why}
  Fix: {concrete change}

Summary: {N} defects, root cause, fix priority
```

If skill description quality is the root cause, recommend running `/skill-creator (from the plugin-dev plugin)` to iterate with test prompts and description optimization.
