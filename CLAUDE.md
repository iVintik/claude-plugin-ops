# plugin-ops — Development Guide

## Overview

Plugin lifecycle management for Claude Code plugins. Provides health audits, optimization, releasing, and marketplace operations.

Complements Anthropic's `plugin-dev` plugin (which handles plugin creation, structure, skills, hooks, and MCP development) by adding operational lifecycle tooling on top.

## Directory Structure

```
plugin-ops/
├── .claude-plugin/plugin.json
├── scripts/
│   └── release.py             # Deterministic release workflow
├── skills/
│   ├── diagnose/SKILL.md      # Diagnose plugin defects
│   ├── reflect/SKILL.md       # Self-reflection analysis
│   ├── optimize/SKILL.md      # Optimize plugin size and quality
│   ├── marketplace/SKILL.md   # Manage plugin marketplaces
│   └── release/SKILL.md       # Version bump + publish (thin wrapper for release.py)
├── knowledge/
│   ├── lifecycle-formats.md   # REFLECTIONS.md format
│   ├── marketplace.md         # marketplace.json schema, multi-provider
│   └── configuration.md       # .local.md config pattern
├── CLAUDE.md
└── README.md
```

## Critical: Cache vs Repo

All plugin-ops skills operate on plugin source repos, NEVER on installed cache copies.

- `~/.claude/plugins/cache/` is the installed READ-ONLY copy — edits here are lost on reinstall and invisible to git
- Always use atlas (`atlas_search_projects`) to resolve the real repo path before editing
- If a path resolves into `~/.claude/plugins/cache/`, STOP and find the real repo

## Design Principles

- **Cache guard hook** — PreToolUse hook blocks Edit/Write on `~/.claude/plugins/cache/` with guidance to find the source repo via atlas.
- **No MCP server** — All functionality through skills (markdown workflows).
- **Provider-agnostic** — Works with GitHub, GitLab (including on-prem), and any git remote.
- **Generic** — No hardcoded paths, repos, or organization-specific references.

## Relationship to plugin-dev

This plugin does NOT duplicate Anthropic's `plugin-dev`. Use each for its strength:

| Need | Use |
|------|-----|
| Create a new plugin | `/plugin-dev:create-plugin` |
| Learn skill/hook/MCP development | `/plugin-dev:*` skills |
| Validate plugin structure | `plugin-dev:plugin-validator` agent |
| Diagnose plugin defects | `/plugin-ops:diagnose` |
| Audit plugin health over time | `/plugin-ops:reflect` |
| Optimize plugin size/quality | `/plugin-ops:optimize` |
| Manage plugin marketplaces | `/plugin-ops:marketplace` |
| Release and publish versions | `/plugin-ops:release` |

## Known Limitation: skill-creator Description Optimization

The `/skill-creator` description optimization loop (`run_loop.py`) has a 120-second timeout for `claude -p` calls in its `improve_description.py`. This is too short for Opus — the loop crashes during the "Improving description..." step.

**Workaround:** Use `--model claude-sonnet-4-6` when running `run_loop.py`, or write descriptions manually using the baseline failure data the loop produces before crashing.

**Cleanup:** After any `run_loop.py` run, remove leaked temp directories: `rm -r ~/.claude/plugins/cache/temp_git_*` (can be 100MB+ each, hundreds accumulate).

## Adding Knowledge

Knowledge files are kept minimal. When adding:
1. Keep under 10 KB per file, 50 KB total
2. Use concrete examples, not generic docs
3. Don't duplicate what Anthropic's plugin-dev already covers
