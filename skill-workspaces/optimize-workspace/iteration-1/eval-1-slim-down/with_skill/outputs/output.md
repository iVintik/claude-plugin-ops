# Optimization dry-run for plugin-ops v1.8.5

## Knowledge: 16.3 KB total (target: < 50 KB -- PASS, but 1 file exceeds 10 KB)

| File | Current | Proposed | Change |
|------|---------|----------|--------|
| `knowledge/marketplace.md` | 10.8 KB | 4.5 KB | -58% |
| `knowledge/configuration.md` | 2.3 KB | 2.3 KB | 0% |
| `knowledge/env-vars.md` | 2.2 KB | 2.2 KB | 0% |
| `knowledge/lifecycle-formats.md` | 1.0 KB | 1.0 KB | 0% |

**Total**: 16.3 KB -> 10.0 KB (-39%)

### Proposed Changes

1. **`knowledge/marketplace.md`**: Exceeds 10 KB limit (10.8 KB). The file contains full CI workflow YAML templates for both GitHub Actions and GitLab CI (lines 69-278), including complete `.yml` files that could be referenced externally or condensed into skeleton examples. Proposed changes:
   - **Remove full GitHub Actions workflow YAML** (lines 71-112, ~1.5 KB). Replace with a 5-line skeleton showing the dispatch pattern and a note: "See `.github/workflows/publish.yml` in the plugin repo for the full template."
   - **Remove full marketplace repo workflow YAML** (lines 114-145, ~1.2 KB). Same treatment -- skeleton + reference note.
   - **Remove full GitLab CI pipeline YAML** (lines 207-278, ~2.5 KB). Replace with a skeleton showing the `trigger` keyword pattern and dotenv forwarding.
   - **Condense the "Setting Up" checklists** (lines 147-159 and 271-278, ~0.6 KB). Both are near-identical numbered lists. Merge into a single "Setup Checklist" section with a provider column.
   - **Remove the Token Renewal section** (lines 168-184, ~0.5 KB). This is generic GitHub/npm documentation, not plugin-specific. A one-line note linking to the GitHub PAT docs suffices.
   - Estimated reduction: ~6.3 KB, bringing the file to ~4.5 KB.

2. **`knowledge/env-vars.md`**: Within budget, content is useful and project-specific. No changes needed.

3. **`knowledge/configuration.md`**: Within budget, well-structured. The "CI Pipeline Setup" section (lines 59-65) duplicates a pointer already in marketplace.md, but it is only 6 lines and serves as a helpful cross-reference. No action required.

4. **`knowledge/lifecycle-formats.md`**: Compact and well-scoped. No changes needed.

---

## Skills: 5 total, 0 with structural issues, 3 with optimization opportunities

| Skill | Issue | Proposed Change |
|-------|-------|-----------------|
| `diagnose` | None | -- |
| `reflect` | None | -- |
| `optimize` | None | -- |
| `marketplace` | None | -- |
| `release` | None | -- |

### Skill Observations

All 5 skills have proper YAML frontmatter, proactive trigger descriptions, and correct knowledge references. No broken references detected.

---

## Duplicate Content: Cache Guard Warning (6 occurrences)

The "Cache vs Repo" / "Cache guard" warning appears in **6 different files**:

| File | Lines |
|------|-------|
| `CLAUDE.md` | Lines 30-40 (detailed, 11 lines) |
| `skills/diagnose/SKILL.md` | Line 19 (1-liner) |
| `skills/reflect/SKILL.md` | Line 17 (1-liner) |
| `skills/optimize/SKILL.md` | Line 18 (1-liner) |
| `agents/plugin-diagnostician.md` | Lines 14-17 (4 lines) |
| `agents/plugin-auditor.md` | Lines 14-17 (4 lines) |
| `agents/plugin-optimizer.md` | Lines 14-17 (4 lines) |

**Assessment**: The skill-level 1-liners are acceptable -- they serve as inline reminders during skill execution and cost ~100 bytes each. The agent-level 4-line sections (3 agents x 4 lines = ~0.4 KB total) duplicate what CLAUDE.md already covers and what the PreToolUse hook enforces. However, since agents run in sub-conversations without CLAUDE.md, these duplications are **justified** and should be kept.

**Recommendation**: No changes. The hook enforces the rule mechanically; the text reminders are cheap insurance for agent sub-conversations. If token budget becomes a concern later, the agent sections could reference CLAUDE.md instead.

---

## Duplicate Content: Diagnostic Steps (skill vs agent)

The `skills/diagnose/SKILL.md` and `agents/plugin-diagnostician.md` contain substantially overlapping diagnostic checklists:

| Content | Skill (SKILL.md) | Agent (.md) |
|---------|-------------------|-------------|
| Structure check | 4 bullet points | 7 checklist items |
| Skills check | 3 sub-sections | 3 sub-sections (more detailed) |
| Hooks check | 3 bullet points | 4 checklist items |
| Agents check | 2 bullet points | 3 checklist items |
| Report format | 8 lines | 12 lines |

Similarly, `skills/reflect/SKILL.md` and `agents/plugin-auditor.md` have overlapping audit checklists, and `skills/optimize/SKILL.md` and `agents/plugin-optimizer.md` overlap on optimization analysis.

**Assessment**: This is the largest duplication area (~3.5 KB across all three pairs). The skill files drive interactive skill execution; the agent files drive sub-agent execution. Both paths are used. However, the agent files are strict supersets of the skill instructions in all three cases.

**Recommendation**: Consider having each skill SKILL.md reference "delegate to the corresponding agent for detailed steps" rather than duplicating the checklist inline. This would save ~1.5 KB across the three skills while keeping the agent files as the single source of truth for detailed steps. However, this changes the execution model (skills would need to spawn agents), so this is flagged as an **opportunity**, not a hard recommendation.

---

## AGENTS.md (3.7 KB) -- Outside Plugin Scope

`AGENTS.md` contains beads (bd) issue tracking integration instructions. This is project infrastructure, not plugin content. It is not loaded as plugin knowledge (not referenced from plugin.json or any skill). No optimization needed -- it does not contribute to plugin context window cost.

---

## Dead References Check

| Reference | Found In | Exists? |
|-----------|----------|---------|
| `knowledge/configuration.md` | marketplace SKILL, README | Yes |
| `knowledge/marketplace.md` | marketplace SKILL, configuration.md | Yes |
| `knowledge/lifecycle-formats.md` | optimize SKILL, reflect SKILL | Yes |
| `scripts/release.py` | release SKILL | Yes |
| `agents/plugin-diagnostician.md` | plugin.json | Yes |
| `agents/plugin-auditor.md` | plugin.json | Yes |
| `agents/plugin-optimizer.md` | plugin.json | Yes |

No dead references found.

---

## Summary

```
Optimization dry-run for plugin-ops v1.8.5

Knowledge: 16.3 KB -> 10.0 KB (-39%)
  - marketplace.md: 10.8 KB -> 4.5 KB (condense CI workflow templates, remove generic token docs)
  - configuration.md: no change
  - env-vars.md: no change
  - lifecycle-formats.md: no change

Skills: 0 modified (all 5 healthy)

Duplicates: Cache guard x6 (justified), diagnostic steps x3 pairs (opportunity for future refactor)
Dead references: 0
```

### Priority Actions

1. **Condense `knowledge/marketplace.md`** -- Replace full CI workflow YAML blocks with skeletons + reference notes. This is the single highest-impact change: -6.3 KB, brings the file under the 10 KB guideline.

2. **(Future)** Consider having skill SKILL.md files delegate detailed checklists to their paired agent files to eliminate ~1.5 KB of duplication. Only worthwhile if token budget becomes a constraint.

No other changes recommended. The plugin is well-structured, skills have good trigger descriptions, and cross-references are all valid.
