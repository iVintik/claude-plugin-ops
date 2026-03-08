# Plugin-Ops Size Analysis and Reduction Plan

## Current Size Breakdown

**Total plugin size: 2,344 KB** (excluding `.git/` and `skill-workspaces/`)

| Component | Size | Files | % of Total |
|-----------|------|-------|------------|
| `_bmad/` | 2,008 KB | 232 | **85.7%** |
| `.claude/commands/` | 172 KB | 43 | 7.3% |
| `knowledge/` | 24 KB | 4 | 1.0% |
| `skills/` | 20 KB | 5 | 0.9% |
| `agents/` | 12 KB | 3 | 0.5% |
| `scripts/` | 12 KB | 1 | 0.5% |
| `hooks/` | 8 KB | 2 | 0.3% |
| Root files (CLAUDE.md, README.md, etc.) | ~88 KB | - | 3.8% |

### `_bmad/` Internal Breakdown (2,008 KB total)

| Subdirectory | Size |
|--------------|------|
| `_bmad/bmm/` | 1,600 KB (185 files) |
| `_bmad/core/` | 236 KB |
| `_bmad/_config/` | 140 KB |
| `_bmad/_memory/` | 12 KB |

### `_bmad/bmm/workflows/` Breakdown (largest subtree)

| Workflow | Size |
|----------|------|
| `2-plan-workflows/` (PRD, UX design) | 536 KB |
| `1-analysis/` (research) | 296 KB |
| `4-implementation/` (stories, reviews) | 228 KB |
| `3-solutioning/` (architecture, epics) | 208 KB |
| `document-project/` | 128 KB |
| `bmad-quick-flow/` | 68 KB |
| `generate-project-context/` | 36 KB |
| `qa-generate-e2e-tests/` | 12 KB |

---

## Key Finding: `_bmad/` Is Not Part of the Plugin

The `_bmad/` directory (and the 41 `.claude/commands/bmad-*.md` files that reference it) is the **BMAD methodology framework** -- a project management / development methodology tool. It is:

- **Not referenced by any plugin skill, agent, hook, or knowledge file.** The plugin's own functionality (diagnose, reflect, optimize, marketplace, release) does not use `_bmad/` at all.
- **Not declared in `plugin.json`** -- no agents, skills, or MCP entries point to `_bmad/`.
- **A separate concern** -- it provides project planning workflows (PRDs, architecture, brainstorming, sprint planning) that are orthogonal to the plugin-ops purpose of "plugin lifecycle management."

The 41 `.claude/commands/bmad-*.md` files are slash commands that load BMAD workflows. They only exist to serve the `_bmad/` framework.

**`_bmad/` + its commands account for 2,180 KB out of 2,344 KB -- 93% of the entire plugin.**

---

## Concrete Reduction Recommendations

### 1. Remove `_bmad/` and its commands (saves ~2,180 KB, 93% reduction)

**Impact: Eliminates 93% of plugin size.**

The `_bmad/` directory and the 41 `.claude/commands/bmad-*.md` files are a development methodology framework unrelated to plugin-ops functionality. They should be:

- Moved to a separate plugin (e.g., `claude-plugin-bmad`) if still needed
- Or simply removed from this repo if BMAD is installed separately

**Files to remove:**
- Entire `_bmad/` directory (232 files, 2,008 KB)
- All `bmad-*.md` files in `.claude/commands/` (41 files, ~164 KB)
- `_bmad-output/` directory (empty, but still present)

**After removal, plugin size drops from 2,344 KB to ~164 KB.**

### 2. Trim `knowledge/marketplace.md` (saves ~5-6 KB)

This file is 303 lines / 11 KB -- the largest knowledge file and over the plugin's own 10 KB per-file guideline. It contains:

- Full CI workflow YAML for both GitHub Actions and GitLab CI (~180 lines of YAML code blocks)
- Token renewal instructions
- Setup checklists

**Suggested approach:**
- Keep the schema, versioning guidelines, and core concepts (~100 lines)
- Move the full CI workflow templates to a separate reference (e.g., a `templates/` directory or external docs)
- Or condense by removing duplicated explanations between GitHub and GitLab sections

**Target: Under 5 KB** (currently 11 KB)

### 3. Consider merging `knowledge/env-vars.md` into `knowledge/configuration.md` (saves ~2 KB)

Both files cover plugin developer configuration patterns. `env-vars.md` (63 lines, 2.2 KB) covers environment variable usage which is fairly generic knowledge that any LLM already knows. It could be:

- Condensed to a short section in `configuration.md`
- Or removed entirely since it documents standard env var behavior, not plugin-ops-specific logic

### 4. Consolidate agents (minor, saves ~3-4 KB)

Three agent files exist:
- `plugin-diagnostician.md` (98 lines, 3 KB) -- overlaps heavily with the `diagnose` skill
- `plugin-auditor.md` (96 lines, 2.7 KB) -- overlaps heavily with the `reflect` skill
- `plugin-optimizer.md` (72 lines, 2 KB) -- overlaps heavily with the `optimize` skill

These agents largely duplicate the instructions already in their corresponding skills. Consider whether agents are needed at all, or if they can be collapsed into a single `plugin-ops-agent.md` that dispatches to the appropriate skill.

### 5. AGENTS.md and CLAUDE.md review (minor)

- `AGENTS.md` (127 lines) is entirely about the `bd` (beads) issue tracker integration and session-end workflow. This is development process tooling, not plugin functionality. If BMAD is removed, this likely goes too (or gets trimmed to essentials).

---

## Summary

| Reduction | Savings | Effort |
|-----------|---------|--------|
| Remove `_bmad/` + bmad commands | ~2,180 KB (93%) | Low -- just delete, no code dependencies |
| Trim `marketplace.md` | ~5-6 KB | Low -- extract CI templates |
| Remove/merge `env-vars.md` | ~2 KB | Low |
| Consolidate agents | ~3-4 KB | Medium -- need to verify agent dispatch behavior |
| **Total potential** | **~2,190 KB (93.4%)** | |

### Before vs After

| Metric | Before | After |
|--------|--------|-------|
| Total size | 2,344 KB | ~154 KB |
| Total files | 280+ | ~20 |
| Knowledge | 24 KB (4 files) | ~14 KB (2-3 files) |
| Skills | 20 KB (5 files) | 20 KB (5 files, unchanged) |

The plugin's core functionality (5 skills, 1 script, 1 hook, 3 knowledge files) is already well-sized at ~76 KB. The bloat is entirely from the bundled BMAD framework which is a separate concern.
