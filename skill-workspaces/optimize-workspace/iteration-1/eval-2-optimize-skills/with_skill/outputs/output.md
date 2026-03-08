# Optimization dry-run for plugin-ops v1.8.5

**Target:** skills
**Date:** 2026-03-08
**Mode:** dry-run (no files modified)

---

## Skills Analysis

### Size Summary

| Skill | Size | Status |
|-------|------|--------|
| diagnose/SKILL.md | 2,969 B | OK (< 5 KB) |
| marketplace/SKILL.md | 2,493 B | OK (< 5 KB) |
| optimize/SKILL.md | 1,962 B | OK (< 5 KB) |
| reflect/SKILL.md | 2,874 B | OK (< 5 KB) |
| release/SKILL.md | 1,950 B | OK (< 5 KB) |

**Total skills size:** 12,248 B (~12 KB) across 5 skills. All within budget.

---

## Findings

### SKILL-1: Description trigger coverage — generally strong

All five skills have rich, proactive descriptions with multiple trigger phrases. This is the most common defect in plugins and plugin-ops handles it well.

| Skill | Trigger Phrases | Proactive? | Assessment |
|-------|----------------|------------|------------|
| diagnose | "why isn't this working", "plugin not triggering", "skill broken", "debug plugin", "diagnose plugin", "check plugin health", "this skill should have fired" | Yes ("Use proactively whenever you notice a plugin or skill misbehaving") | Excellent |
| reflect | "analyze plugin health", "audit plugin", "assess plugin quality", "review plugin structure", "run self-assessment", "how healthy is this plugin" | Yes ("trigger proactively after significant plugin changes") | Excellent |
| marketplace | "create a marketplace", "publish a plugin", "list marketplace plugins", "add plugin to store", "manage plugin catalog", "set up a plugin registry", "remove from marketplace" | No | Good (appropriate for marketplace, which is inherently user-initiated) |
| optimize | "slim down", "clean up", "optimize", "reduce size", "make plugin smaller", "trim plugin", "reduce footprint", "improve plugin quality" | No | Good |
| release | "release", "bump version", "publish", "deploy update", "tag a release", "ship it", "push a release", "release this" | No | Good |

**No changes needed.** Descriptions are well-crafted with strong trigger coverage.

---

### SKILL-2: Broken/orphan knowledge references

| Skill | References | Status |
|-------|-----------|--------|
| optimize | `knowledge/lifecycle-formats.md` | Valid |
| reflect | `knowledge/lifecycle-formats.md` | Valid |
| marketplace | `knowledge/configuration.md`, `knowledge/marketplace.md` | Valid |
| diagnose | (no explicit knowledge refs) | OK |
| release | (uses `scripts/release.py` via `${CLAUDE_PLUGIN_ROOT}`) | Valid |

**No broken references found in skills.**

---

### SKILL-3: Unreferenced knowledge file

`knowledge/env-vars.md` (2,230 B) is not referenced by any skill, agent, or CLAUDE.md. It exists as standalone knowledge that gets loaded into context but is never pointed to by any workflow.

**Proposed change:** This is a knowledge optimization finding (not skills), but worth noting. The file provides value as ambient context for plugin developers but adds 2.2 KB to every session. Consider whether it earns its context budget.

---

### SKILL-4: External dependency — `/skill-creator`

Three skills reference `/skill-creator` as a recommendation for deeper skill refinement:
- `diagnose/SKILL.md` line 69
- `reflect/SKILL.md` line 86
- `optimize/SKILL.md` line 31

`/skill-creator` is a skill from Anthropic's `plugin-dev` plugin, not from plugin-ops. This is a valid external reference (it complements plugin-ops per CLAUDE.md), but it creates a dependency on having `plugin-dev` installed. If `plugin-dev` is not installed, the recommendation is a dead end for the user.

**Proposed change:** Add a brief qualifier, e.g., "recommend running `/skill-creator` (from the `plugin-dev` plugin)" so users know where to find it if the skill doesn't auto-trigger.

---

### SKILL-5: Agent `plugin-diagnostician.md` references `commands/` directory

The `plugin-diagnostician.md` agent (line 25) lists `commands/` as an expected directory to check during structural validation:
```
- Expected directories: `commands/`, `skills/`, `hooks/`, `agents/`, `knowledge/`
```

The `commands/` directory concept was removed from Claude Code plugins. This is a stale reference that could cause false-positive defect reports during diagnostics.

**Proposed change:** Remove `commands/` from the expected directories list in `plugin-diagnostician.md`.

---

### SKILL-6: Agent `plugin-diagnostician.md` references `ISSUES.md`

Line 69 of `plugin-diagnostician.md` says:
```
- Read ISSUES.md for relevant open issues
```

There is no `ISSUES.md` in plugin-ops or in a standard Claude Code plugin structure. This is a dead reference.

**Proposed change:** Remove the `ISSUES.md` reference, or change to "Check for ISSUES.md if present".

---

### SKILL-7: Overlap between `diagnose` skill and `plugin-diagnostician` agent

The `diagnose` skill and `plugin-diagnostician` agent perform essentially the same function with similar diagnostic steps. The skill provides the workflow; the agent provides a delegatable version. This is intentional (agent = delegatable, skill = inline), but there is content drift:

- Agent lists `commands/` as expected directory; skill does not
- Agent references `ISSUES.md`; skill does not
- Agent has severity level definitions; skill references them inline
- Skill mentions checking `gh issue list`; agent also does

**Proposed change:** Ensure agent instructions stay aligned with skill instructions. The agent should reference the skill's logic rather than duplicating it, or at minimum be kept in sync.

---

### SKILL-8: Overlap between `reflect` skill and `plugin-auditor` agent

Similar pattern: `reflect` skill and `plugin-auditor` agent cover the same ground. The agent is more checklist-oriented. Again intentional but susceptible to drift.

**Proposed change:** Same recommendation — keep in sync or have the agent defer to the skill's analysis areas.

---

### SKILL-9: `marketplace` skill — missing `--marketplace-path` argument docs

The `marketplace` skill's argument-hint says `<subcommand> [options]` and the configuration section mentions `--marketplace-path` as a fallback (from `knowledge/configuration.md` line 53-54), but this argument is not documented in the skill's Parse Arguments section.

**Proposed change:** Add `--marketplace-path <path>` as a documented option in the marketplace skill's argument parsing section.

---

### SKILL-10: `optimize` skill — sparse instructions

At 1,962 B, `optimize` is the smallest skill. Its "Skills Optimization" section is only 4 bullet points:
```
- Check description trigger coverage and proactiveness
- Find unclear steps, broken knowledge refs, overly complex flows
- Apply: fix broken refs, sharpen descriptions, clarify steps
- For deeper skill refinement, recommend /skill-creator
```

This is quite vague compared to how `diagnose` and `reflect` spell out their steps in detail. An agent executing this skill has limited guidance on *how* to evaluate description trigger coverage or what constitutes "unclear steps."

**Proposed change:** Expand the skills optimization section with concrete evaluation criteria, similar to how `diagnose` breaks down description quality assessment (proactive trigger language, trigger phrases coverage, specificity).

---

## Summary

```
Optimization dry-run for plugin-ops v1.8.5

Skills: 5 total, 0 with structural defects
  - SKILL-3: knowledge/env-vars.md unreferenced by any skill (knowledge concern)
  - SKILL-4: /skill-creator references lack source plugin qualifier (3 skills)
  - SKILL-5: Agent references stale `commands/` directory (plugin-diagnostician.md)
  - SKILL-6: Agent references non-existent ISSUES.md (plugin-diagnostician.md)
  - SKILL-7: diagnose skill / diagnostician agent content drift
  - SKILL-8: reflect skill / auditor agent content drift
  - SKILL-9: marketplace skill missing --marketplace-path docs
  - SKILL-10: optimize skill has sparse instructions for skills analysis

Severity breakdown:
  - Major: 2 (SKILL-5 stale commands/ ref, SKILL-6 dead ISSUES.md ref)
  - Minor: 6 (SKILL-3, SKILL-4, SKILL-7, SKILL-8, SKILL-9, SKILL-10)

No files were modified (dry-run mode).

For deeper skill refinement on individual skills, consider running
/skill-creator (from the plugin-dev plugin) to iterate with test
prompts and eval loops.
```
