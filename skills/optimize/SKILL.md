---
name: optimize
description: "Optimize a Claude Code plugin — reduce knowledge size, improve skill descriptions, remove dead references, condense verbose content. Use when the user asks to \"slim down\", \"clean up\", \"optimize\", \"reduce size\", \"make plugin smaller\", \"trim plugin\", \"reduce footprint\", \"condense\", \"shrink\", or \"improve plugin quality\". Also triggers when a user mentions a plugin file being too large (in KB), a knowledge directory approaching size limits, wanting to remove or condense things from plugin files, or wanting to sharpen skill descriptions as part of a cleanup pass. Covers any request to make a plugin leaner, smaller, or higher-quality by trimming, condensing, or removing content. Does NOT cover: health audits/reports (use reflect), skill description testing with eval loops (use skill-creator), or plugin debugging (use diagnose)."
argument-hint: "[plugin-path] [--dry-run] [--target knowledge|skills|all]"
---

# Plugin Optimization

Analyze and optimize a plugin's knowledge and skills for size and clarity.

## Parse Arguments

Parse `$ARGUMENTS`:
- **First positional** (optional): Path to plugin directory. Default: current working directory.
- `--dry-run`: Report changes without applying. This is the default — changes are only applied when user explicitly omits this flag.
- `--target`: Focus area — `knowledge` (default), `skills`, or `all`.

**Cache guard**: `~/.claude/plugins/cache/` is READ-ONLY. Resolve to the real git repo via atlas: `atlas_search_projects(query="plugin-name")`.

## Knowledge Optimization (target: knowledge | all)

- Measure each file, flag > 10 KB or total > 50 KB
- Find duplicates, generic content, outdated refs, verbose sections
- Apply: remove duplicates (keep detailed version), condense, remove dead refs, split oversized files

## Skills Optimization (target: skills | all)

For each skill, evaluate:

**Description quality** (most impactful — poor descriptions mean skills never trigger):
- Does it include specific trigger phrases a user would say?
- Does it have proactive language ("Use when...", "Trigger after...") if appropriate?
- Could another plugin's skill "steal" the trigger due to overlapping descriptions?
- Is it too vague ("manages things") or too narrow (only one exact phrase)?

**Instruction clarity**:
- Are steps concrete enough for an agent to follow without guessing?
- Are knowledge file references valid (files exist)?
- Are there stale references to removed features or files?
- Is there content drift between paired skill/agent files?

**Cross-skill consistency**:
- Consistent argument parsing patterns across skills?
- Cache guard reminder present where editing happens?
- Output format defined clearly?

Apply: fix broken refs, sharpen descriptions, align skill/agent pairs, clarify steps.

For deeper skill refinement (test prompts, eval loops, description optimization), recommend `/skill-creator` (from the plugin-dev plugin).

## Post-Optimization

Prepend optimization entry to REFLECTIONS.md (format from `knowledge/lifecycle-formats.md`)

## Output

```
Optimization {applied|dry-run} for {plugin-name} v{version}

Knowledge: {before} KB → {after} KB ({reduction}%)
  - {file}: {change}

Skills: {N} modified
  - {skill}: {change}
```
