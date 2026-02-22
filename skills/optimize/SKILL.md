---
name: optimize
description: Optimize a Claude Code plugin — reduce knowledge size, improve skill clarity, remove dead references. Use when the user asks to slim down a plugin, clean up a plugin, optimize plugin size, or improve plugin quality.
argument-hint: "[plugin-path] [--dry-run] [--target knowledge|skills|all]"
---

# Plugin Optimization

Optimize a plugin with non-regression guarantees. Reads ISSUES.md to protect resolved fixes.

## Parse Arguments

Parse `$ARGUMENTS`:
- **First positional argument** (optional): Path to plugin directory. If omitted, use current working directory.
- `--dry-run`: Report what would change without modifying files
- `--target`: Focus area — `knowledge` (default), `skills`, or `all`

## Locate Plugin

1. Verify `.claude-plugin/plugin.json` exists
2. Read plugin name and version

## Non-Regression Protocol

**This step is MANDATORY before making any changes.**

Read `knowledge/lifecycle-formats.md` for the non-regression protocol.

1. **Read ISSUES.md** — collect ALL resolved issues
2. For each resolved issue, record:
   - Issue ID and title
   - Resolution description
   - Files/logic mentioned in the resolution
3. Store this as a "protected set" — changes to these files/sections require extra care

## Knowledge Optimization

If `--target` is `knowledge` or `all`:

### Size Analysis
- Measure each knowledge file
- Identify files > 10 KB
- Calculate total knowledge size

### Content Analysis
- Find duplicate content across files
- Identify generic content that could be removed
- Find outdated references (to non-existent files, old versions)
- Detect overly verbose sections that can be condensed

### Proposed Changes
For each change:
1. **Check against protected set** — if the change touches a file/section involved in a resolved issue, SKIP it and explain why
2. Describe what would change and why
3. Estimate size reduction

### Apply Changes (unless --dry-run)
- Use Edit tool for modifications
- Remove duplicate sections (keep the more detailed version)
- Condense verbose explanations
- Remove outdated references
- Split oversized files if > 10 KB

## Skills Optimization

If `--target` is `skills` or `all`:

### Clarity Analysis
- Check description trigger coverage
- Identify unclear or missing steps
- Find references to non-existent knowledge files or tools
- Detect overly complex skills that could be simplified

### Proposed Changes
For each change:
1. **Check against protected set** — same non-regression check
2. Describe what would change and why

### Apply Changes (unless --dry-run)
- Fix broken knowledge references
- Improve description trigger phrases
- Clarify ambiguous steps

## Post-Optimization Verification

After all changes are applied:

1. **Re-check resolved issues** — verify each resolved issue's fix is still intact
2. **Update ISSUES.md** — add notes to any issues affected by optimization:
   ```
   - {today's date}: Verified during optimization — fix intact
   ```
3. **Update REFLECTIONS.md** — prepend optimization entry using format from `knowledge/lifecycle-formats.md`

## Output

Display summary:

```
Optimization {applied|dry-run} for {plugin-name} v{version}

Knowledge: {before} KB → {after} KB ({reduction}% reduction)
  - {file}: {change description}

Skills: {N} modified
  - {skill}: {change description}

Non-regression: {N} resolved issues checked, {all intact | M conflicts skipped}

{Written to REFLECTIONS.md | Dry run — no files modified}
```
