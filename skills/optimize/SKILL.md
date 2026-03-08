---
name: optimize
description: "Optimize a Claude Code plugin — reduce knowledge size, improve skill descriptions, remove dead references, condense verbose content. Use when the user asks to \"slim down\", \"clean up\", \"optimize\", \"reduce size\", \"make plugin smaller\", \"trim plugin\", \"reduce footprint\", or \"improve plugin quality\". Runs in dry-run mode by default and respects non-regression protocol for resolved issues."
argument-hint: "[plugin-path] [--dry-run] [--target knowledge|skills|all]"
---

# Plugin Optimization

Optimize a plugin with non-regression guarantees.

## Parse Arguments

Parse `$ARGUMENTS`:
- **First positional** (optional): Path to plugin directory. Default: current working directory.
- `--dry-run`: Report changes without applying (default behavior).
- `--target`: Focus area — `knowledge` (default), `skills`, or `all`.

**Cache guard**: `~/.claude/plugins/cache/` is READ-ONLY. Resolve to the real git repo via atlas: `atlas_search_projects(query="plugin-name")`.

## Non-Regression Protocol (mandatory)

Read `knowledge/lifecycle-formats.md` for the full protocol.

1. Read ISSUES.md — collect all resolved issues
2. Record: ID, title, resolution, files/logic involved
3. This "protected set" must remain intact after changes
4. Skip changes that would touch protected files/sections — explain why

## Knowledge Optimization (target: knowledge | all)

- Measure each file, flag > 10 KB or total > 50 KB
- Find duplicates, generic content, outdated refs, verbose sections
- For each proposed change: check against protected set first
- Apply: remove duplicates (keep detailed version), condense, remove dead refs, split oversized files

## Skills Optimization (target: skills | all)

- Check description trigger coverage and proactiveness
- Find unclear steps, broken knowledge refs, overly complex flows
- For each proposed change: check against protected set first
- Apply: fix broken refs, sharpen descriptions, clarify steps

## Post-Optimization

1. Re-verify all resolved issues — fixes still intact
2. Update ISSUES.md: add verification notes
3. Prepend optimization entry to REFLECTIONS.md (format from `knowledge/lifecycle-formats.md`)

## Output

```
Optimization {applied|dry-run} for {plugin-name} v{version}

Knowledge: {before} KB → {after} KB ({reduction}%)
  - {file}: {change}

Skills: {N} modified
  - {skill}: {change}

Non-regression: {N} resolved issues checked, {all intact | M conflicts skipped}
```
