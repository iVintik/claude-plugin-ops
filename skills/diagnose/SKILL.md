---
name: diagnose
description: When a plugin skill fails to load, fails with errors, isn't automatically triggered when expected, or produces unexpected behavior — diagnose the root cause in the plugin. Also use when the user asks to "diagnose plugin", "debug plugin", "why isn't this skill working", "plugin not triggering", or "check plugin health".
argument-hint: "[plugin-path] [--skill SKILL-NAME]"
---

# Plugin Diagnostics

Investigate and report plugin defects. When a plugin or skill doesn't work as expected, the problem is in the plugin — diagnose it as such.

## Parse Arguments

Parse `$ARGUMENTS`:
- **First positional argument** (optional): Path to plugin directory. If omitted, use current working directory.
- `--skill SKILL-NAME`: Focus diagnosis on a specific skill

If no arguments provided and no `.claude-plugin/plugin.json` in current directory, ask the user which plugin to diagnose.

**CRITICAL: Cache vs Repo**
- `~/.claude/plugins/cache/` contains READ-ONLY installed copies — NEVER edit these
- Always resolve to the real git repo. Use atlas: `atlas_search_projects(query="plugin-name")` to find the repo path

## Key Principle

**Frame findings as plugin defects, not agent failures.** If a skill wasn't triggered when it should have been, that's a skill description quality issue. If a hook failed silently, that's a hook configuration defect. Do NOT self-blame — report the root cause in the plugin.

## Diagnostic Steps

### 1. Verify Plugin Structure

Check for required files:
- `.claude-plugin/plugin.json` exists and is valid JSON
- Read manifest: name, version, description
- Check for expected directories: `commands/`, `skills/`, `hooks/`, `agents/`, `knowledge/`
- Verify referenced files actually exist

Report any structural defects found.

### 2. Check Manifest Quality

- Is the plugin description clear and specific?
- Does the version follow semver?
- Are all declared components present on disk?

### 3. Diagnose Skills (if applicable)

For each skill (or the specific `--skill` target):

**a. SKILL.md structure**
- Has valid YAML frontmatter with `name` and `description`
- Description is present and non-empty
- Content after frontmatter is valid markdown

**b. Description quality (most common defect)**
- Is it **proactive enough**? Skills that should auto-trigger must say so explicitly:
  - BAD: "Reviews code quality" (passive, won't trigger)
  - GOOD: "Use this agent when the user has created or modified code and needs quality review. Trigger proactively after code changes."
- Does it cover **trigger phrases** the user might say?
  - BAD: "Manages issues" (too vague)
  - GOOD: 'Use when the user asks to "track issue", "add bug", "list issues", or mentions issue tracking'
- Does it specify **proactive triggers** if the skill should auto-fire?
  - Skills that should run after certain events need explicit "Trigger proactively after X" language

**c. Content issues**
- Unescaped bash patterns (e.g., bare `$VARIABLE` outside code blocks)
- Broken YAML frontmatter (missing `---` delimiters, bad indentation)
- References to files that don't exist in the plugin
- References to knowledge files that are missing

### 4. Diagnose Hooks (if applicable)

- `hooks/hooks.json` is valid JSON
- Hook event names are valid (`SessionStart`, `PreToolUse`, `PostToolUse`, etc.)
- Referenced scripts exist and are executable
- Timeout values are reasonable (not too short for the operation)
- Matcher patterns are correct

### 5. Diagnose Agents (if applicable)

- Agent definitions have proper trigger descriptions
- Agent tools list is appropriate for the task

### 6. Check for Known Issues

If the plugin has an `ISSUES.md`, read it for relevant open issues.

If the plugin has a remote repository:
- Run `gh issue list -R {repo}` to check for existing reports
- Note any issues that match the current symptoms

### 7. Check Runtime Context

- Is the plugin actually installed? Run `claude plugin list` and check
- Are there conflicting plugins with similar skill names/descriptions?
- Could another plugin's skill be "stealing" the trigger?

## Report Format

```
Plugin Diagnostics: {plugin-name} v{version}

{DEFECT-1}: {category} — {short title}
  Location: {file-path}:{line-number}
  Severity: {critical | major | minor}
  Details: {what's wrong and why it causes the observed behavior}
  Fix: {concrete change to make}

{DEFECT-2}: ...

Summary:
  {N} defect(s) found
  {Root cause of the reported symptom}
  {Recommended fix priority}
```

## Severity Levels

- **Critical**: Plugin won't load, skill completely non-functional
- **Major**: Skill doesn't trigger when expected, hook fails silently, wrong behavior
- **Minor**: Suboptimal description quality, missing but non-essential files

## Common Defect Patterns

1. **Skill not triggering**: Description lacks proactive trigger language or doesn't cover the user's phrasing
2. **Skill triggered but errors**: SKILL.md references missing files, has syntax issues, or makes invalid tool assumptions
3. **Hook not firing**: Wrong event name, script not executable, timeout too short
4. **Plugin not loading**: Invalid plugin.json, missing required fields
5. **Wrong skill triggered**: Multiple plugins/skills with overlapping descriptions — specificity needed
