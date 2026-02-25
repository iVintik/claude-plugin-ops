# plugin-ops — Development Guide

## Overview

Plugin lifecycle management for Claude Code plugins. Provides issue tracking, health audits, optimization with non-regression guarantees, fixing, releasing, and marketplace operations.

Complements Anthropic's `plugin-dev` plugin (which handles plugin creation, structure, skills, hooks, and MCP development) by adding operational lifecycle tooling on top.

## Directory Structure

```
plugin-ops/
├── .claude-plugin/plugin.json
├── scripts/
│   └── release.py             # Deterministic release workflow
├── skills/
│   ├── issues/SKILL.md        # Manage ISSUES.md
│   ├── reflect/SKILL.md       # Self-reflection analysis
│   ├── optimize/SKILL.md      # Optimize with non-regression
│   ├── fix/SKILL.md           # Fix issues with non-regression
│   ├── marketplace/SKILL.md   # Manage plugin marketplaces
│   └── release/SKILL.md       # Version bump + publish (thin wrapper for release.py)
├── knowledge/
│   ├── lifecycle-formats.md   # ISSUES.md + REFLECTIONS.md formats
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

- **No hooks** — Operates on other plugin directories. No safety hooks needed.
- **No MCP server** — All functionality through skills (markdown workflows).
- **Non-regression** — optimize and fix skills read ISSUES.md to protect resolved fixes.
- **ISSUES.md over database** — Lightweight, version-controlled, readable without tools.
- **Provider-agnostic** — Works with GitHub, GitLab (including on-prem), and any git remote.
- **Generic** — No hardcoded paths, repos, or organization-specific references.

## Relationship to plugin-dev

This plugin does NOT duplicate Anthropic's `plugin-dev`. Use each for its strength:

| Need | Use |
|------|-----|
| Create a new plugin | `/plugin-dev:create-plugin` |
| Learn skill/hook/MCP development | `/plugin-dev:*` skills |
| Validate plugin structure | `plugin-dev:plugin-validator` agent |
| Track issues across plugin lifetime | `/plugin-ops:issues` |
| Audit plugin health over time | `/plugin-ops:reflect` |
| Optimize with regression safety | `/plugin-ops:optimize` |
| Fix tracked issues safely | `/plugin-ops:fix` |
| Manage plugin marketplaces | `/plugin-ops:marketplace` |
| Release and publish versions | `/plugin-ops:release` |

## Adding Knowledge

Knowledge files are kept minimal. When adding:
1. Keep under 10 KB per file, 50 KB total
2. Use concrete examples, not generic docs
3. Don't duplicate what Anthropic's plugin-dev already covers
