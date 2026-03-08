# Skill Review and Improvement Analysis — plugin-ops

## Executive Summary

The plugin-ops plugin (v1.8.5) has 5 skills: `release`, `marketplace`, `optimize`, `reflect`, and `diagnose`. Overall, the skills are well-structured and follow a consistent pattern. However, there are several opportunities to improve trigger descriptions, instruction clarity, cross-references, and eliminate redundancy across skills.

---

## Per-Skill Analysis

### 1. `release` — `/plugin-ops:release`

**File**: `skills/release/SKILL.md`

#### Trigger Description (frontmatter `description`)

**Current**: Long sentence listing trigger phrases: "release", "bump version", "publish", "deploy update", "tag a release", "ship it", "push a release", "release this". Also includes a negative constraint about never using manual git tags.

**Issues**:
- The negative instruction ("This is the ONLY correct way to release any repo containing .claude-plugin/ — never use manual git tags or gh release for plugins") is important but bloats the description. The description field is primarily for matching user intent, not for behavioral constraints.
- Missing trigger phrases: "cut a release", "new version", "version up", "prepare release".

**Suggested improvement**:
```yaml
description: "Bump plugin version, commit, push, and tag a release. Use when the user asks to \"release\", \"bump version\", \"publish\", \"cut a release\", \"new version\", \"tag a release\", \"ship it\", or \"push a release\". Trigger proactively when the user has completed changes and discusses shipping or versioning."
```
Move the negative constraint into the SKILL.md body under a `## Constraints` section.

#### Instruction Clarity

**Strengths**:
- Clear argument parsing section.
- Explicit handling of success vs error paths.
- Good warning about not running `claude plugin install/update` from within a session.

**Issues**:
- The `argument-hint` says `[plugin-path] [version] [--dry-run] [--no-tag]` but the README says `/plugin-ops:release [path] <version> [--store name]`. The `--store` flag appears in README but not in the SKILL.md. This is a discrepancy.
- No mention of the `--store` flag in the SKILL.md argument parsing section.
- Step "Get Version" references `AskUserQuestion` but this is not a standard Claude Code tool name. Should clarify this is just asking the user inline.

**Suggested fixes**:
1. Add `--store name` to argument-hint and Parse Arguments section, or remove from README.
2. Replace `AskUserQuestion` with plain language: "Present options to the user and ask which version to use."

#### Cross-References

- References `${CLAUDE_PLUGIN_ROOT}/scripts/release.py` — valid, file exists.
- No references to knowledge files — acceptable since `release.py` is self-contained.

---

### 2. `marketplace` — `/plugin-ops:marketplace`

**File**: `skills/marketplace/SKILL.md`

#### Trigger Description

**Current**: Lists trigger phrases well: "create a marketplace", "publish a plugin", "list marketplace plugins", "add plugin to store", etc.

**Issues**:
- "publish a plugin" overlaps with the `release` skill. A user saying "publish my plugin" could mean either releasing a version or adding it to a marketplace for the first time. This ambiguity could cause misfires.
- Missing trigger phrases: "browse plugins", "search marketplace", "plugin catalog", "plugin store".

**Suggested improvement**:
```yaml
description: "Manage Claude Code plugin marketplaces — create, list, add, or remove plugins from marketplace repositories. Use when the user asks to \"create a marketplace\", \"add plugin to marketplace\", \"list marketplace plugins\", \"manage plugin catalog\", \"set up a plugin registry\", \"remove from marketplace\", \"browse plugins\", or anything about plugin distribution and discovery. NOT for version bumps or releasing — use /release for that."
```

#### Instruction Clarity

**Strengths**:
- Clean subcommand structure (init, list, add, remove).
- Good error handling section.

**Issues**:
- The `init` section mentions "glab project create" for GitLab but adds "or guide API curl" — vague. Should reference `knowledge/marketplace.md` for provider-specific details.
- The `add` section says "Get plugin's git remote URL" but doesn't specify which remote or how to handle detached/no-remote cases.
- No reference to `knowledge/configuration.md` for the `--store` flag resolution, though the Configuration section says to read it.

**Suggested fixes**:
1. In `init`: Replace "or guide API curl" with "See `knowledge/marketplace.md` for GitLab setup details."
2. In `add`: Specify "Get plugin's git remote URL via `git remote get-url origin`; if no remote, ask the user."

#### Cross-References

- References `knowledge/configuration.md` — valid.
- References `knowledge/marketplace.md` — valid.
- Both exist and are relevant.

---

### 3. `optimize` — `/plugin-ops:optimize`

**File**: `skills/optimize/SKILL.md`

#### Trigger Description

**Current**: Lists trigger phrases: "slim down", "clean up", "optimize", "reduce size", etc.

**Issues**:
- "clean up" is very generic and could match non-plugin contexts (e.g., "clean up this code"). Should scope it: "clean up plugin", "clean up plugin knowledge".
- Missing: "deduplicate", "compress knowledge", "reduce token usage", "shrink plugin".

**Suggested improvement**:
```yaml
description: "Optimize a Claude Code plugin — reduce knowledge size, improve skill descriptions, remove dead references, condense verbose content. Use when the user asks to \"optimize plugin\", \"slim down plugin\", \"reduce plugin size\", \"trim plugin\", \"reduce footprint\", \"deduplicate knowledge\", \"shrink plugin\", or \"improve plugin quality\". Also trigger proactively if plugin knowledge exceeds 50 KB total or individual files exceed 10 KB."
```

Adding the proactive trigger condition (size thresholds) makes the skill auto-fire when it detects oversized plugins during other operations.

#### Instruction Clarity

**Strengths**:
- Clear size thresholds (10 KB per file, 50 KB total).
- Separation of knowledge vs skills optimization.

**Issues**:
- The `--dry-run` flag says it's the "default behavior", which contradicts the argument-hint where it's listed as an option. If dry-run is default, the flag should be `--apply` to actually make changes. This is confusing.
- "Find duplicates, generic content, outdated refs, verbose sections" — these are goals, not steps. Should include HOW to detect each.
- The Skills Optimization section recommends `/skill-creator` but doesn't say where this comes from (it's presumably from plugin-dev). Should clarify.
- "Apply: remove duplicates (keep detailed version)" — which version is "detailed"? The longer one? The one with more examples? Needs clarification.

**Suggested fixes**:
1. Clarify dry-run default: Either change the default to apply (with `--dry-run` as opt-in safety) or rename to `--apply` flag. Currently contradictory.
2. Add detection steps: "Compare file contents for >50% overlap to find duplicates", "Flag content that doesn't reference the specific plugin by name as potentially generic".
3. Clarify `/skill-creator` source: "recommend the user run `/plugin-dev:skill-creator`" (assuming it's from plugin-dev).

#### Cross-References

- References `knowledge/lifecycle-formats.md` for REFLECTIONS.md format — valid.
- References `/skill-creator` without qualifying which plugin — should be `/plugin-dev:skill-creator`.

---

### 4. `reflect` — `/plugin-ops:reflect`

**File**: `skills/reflect/SKILL.md`

#### Trigger Description

**Current**: Lists trigger phrases and includes a proactive trigger: "Also trigger proactively after significant plugin changes to catch regressions."

**Issues**:
- The proactive trigger is good but vague — what counts as "significant"? Should define: "after adding/removing skills, after knowledge file changes, after version bumps".
- "run self-assessment" is oddly phrased for a user. More natural: "check plugin", "is my plugin okay", "plugin status".

**Suggested improvement**:
```yaml
description: "Run a comprehensive health audit on a Claude Code plugin — checks structure, skills quality, knowledge size, hooks, MCP config, and cross-references. Use when the user asks to \"audit plugin\", \"analyze plugin health\", \"assess plugin quality\", \"review plugin structure\", \"check plugin\", or \"how healthy is this plugin\". Trigger proactively after adding/removing skills, modifying knowledge files, or changing plugin structure."
```

#### Instruction Clarity

**Strengths**:
- Comprehensive analysis areas (structure, skills, knowledge, hooks, MCP, cross-references).
- Clear output format with pass/warn/fail indicators.
- Good REFLECTIONS.md write-back.

**Issues**:
- Section "2. Skills" checks that "Name matches directory name" — this is a structural check that overlaps with `diagnose`. Should note this is a health check, not a diagnostic.
- The output template mentions "For skills needing deeper refinement, recommend running /skill-creator" — same issue as optimize, should qualify as `/plugin-dev:skill-creator`.
- Section "5. MCP" checks for `.mcp.json` but the plugin.json schema doesn't appear to reference MCP configs. Should clarify where `.mcp.json` is expected.
- "Content is project-specific (not generic filler)" under Knowledge — how should the agent determine this? Needs heuristic guidance: "Flag content that could apply to any plugin without modification."

**Suggested fixes**:
1. Qualify `/skill-creator` reference.
2. Add heuristic for "project-specific" detection.
3. Clarify `.mcp.json` location expectation (plugin root).

#### Cross-References

- References `knowledge/lifecycle-formats.md` — valid.
- References `/skill-creator` — needs qualification.

---

### 5. `diagnose` — `/plugin-ops:diagnose`

**File**: `skills/diagnose/SKILL.md`

#### Trigger Description

**Current**: Most detailed and proactive description of all skills. Includes proactive triggers and a wide range of user phrases.

**Issues**:
- Very long description (347 characters). While comprehensive, it may reduce matching precision due to noise.
- "Also trigger when a hook fails silently or a plugin won't load" — this is a proactive trigger that the agent may not detect automatically (how does it know a hook failed silently?).
- Some trigger phrases overlap with `reflect`: "check plugin health" appears in both `diagnose` and `reflect` descriptions.

**Suggested improvement**:
```yaml
description: "Diagnose why a plugin skill fails to load, doesn't trigger, errors out, or behaves unexpectedly. Use when the user says \"why isn't this working\", \"plugin not triggering\", \"skill broken\", \"debug plugin\", \"diagnose plugin\", \"fix plugin\", or \"this skill should have fired\". Trigger proactively when you observe a skill that should have matched but didn't, or when a hook exits with a non-zero code."
```
Remove "check plugin health" (belongs to `reflect`). Add "fix plugin" as a common phrase. Make proactive triggers observable rather than speculative.

#### Instruction Clarity

**Strengths**:
- Excellent framing: "Frame findings as plugin defects, not agent failure."
- Strong description quality analysis with BAD/GOOD examples.
- Concrete report format with severity levels.

**Issues**:
- Section "5. Runtime Context" suggests `gh issue list -R {repo}` — this could be noisy and may fail if not a GitHub repo. Should be conditional on GitHub provider.
- "Verify plugin is installed: `claude plugin list`" — from within a session, this might behave unexpectedly. Should note caveats.
- "Check for conflicting plugins with overlapping skill descriptions" — great idea but no guidance on HOW to detect overlap. Should suggest comparing description keywords.
- Section "4. Agents" mentions "Trigger descriptions match intended use" but agents don't have trigger descriptions in the same way skills do. Agents in plugin.json are just file paths.

**Suggested fixes**:
1. Make `gh issue list` conditional: "If the plugin is hosted on GitHub, check for known issues..."
2. Clarify agent diagnosis: Agents have their own instruction files; check that those files exist and contain clear purpose/tool definitions.
3. Add overlap detection guidance: "List all installed plugin skill descriptions, flag pairs with >3 shared trigger phrases."

#### Cross-References

- References `/skill-creator` — needs qualification as `/plugin-dev:skill-creator`.
- No references to knowledge files — acceptable for a diagnostic skill.

---

## Cross-Cutting Issues

### 1. Overlap Between `reflect` and `diagnose`

Both skills check plugin structure and skills quality. The distinction should be clearer:
- `reflect` = proactive health audit (everything is fine, let's check)
- `diagnose` = reactive troubleshooting (something is broken, let's find out why)

**Recommendation**: Add a brief disambiguation line to each description:
- `reflect`: "...For investigating specific failures, use /plugin-ops:diagnose instead."
- `diagnose`: "...For routine health checks without a specific problem, use /plugin-ops:reflect instead."

### 2. Inconsistent `/skill-creator` References

Three skills (`optimize`, `reflect`, `diagnose`) reference `/skill-creator` without specifying the plugin. This should consistently be `/plugin-dev:skill-creator` since it comes from Anthropic's plugin-dev plugin. Without the qualifier, the agent may fail to find the skill or confuse it with something in plugin-ops.

### 3. Cache Guard Duplication

Three skills (`optimize`, `reflect`, `diagnose`) contain identical cache guard paragraphs:
```
**Cache guard**: `~/.claude/plugins/cache/` is READ-ONLY. Resolve to the real git repo via atlas: `atlas_search_projects(query="plugin-name")`.
```
This is already enforced by the PreToolUse hook in `hooks/hooks.json`. Including it in each skill is defensive but adds ~40 words x 3 = 120 words of redundancy. Consider moving this to a knowledge file (`knowledge/common-guards.md`) and referencing it once, or trusting the hook and removing from skills entirely.

### 4. Missing `argument-hint` Consistency

- `release`: `[plugin-path] [version] [--dry-run] [--no-tag]` — missing `--store`
- `marketplace`: `<subcommand> [options]` — good
- `optimize`: `[plugin-path] [--dry-run] [--target knowledge|skills|all]` — good
- `reflect`: `[plugin-path] [--brief]` — good
- `diagnose`: `[plugin-path] [--skill SKILL-NAME]` — good

Only `release` has the `--store` discrepancy with README.

### 5. Proactive Trigger Specificity

Skills vary widely in proactive trigger quality:
- `diagnose`: Excellent — describes observable conditions ("when you notice a plugin or skill misbehaving")
- `reflect`: Good but vague ("after significant plugin changes")
- `optimize`: No proactive trigger at all
- `release`: No proactive trigger (appropriate — releasing should be explicit)
- `marketplace`: No proactive trigger (appropriate)

**Recommendation**: Add a proactive trigger to `optimize`: "Trigger proactively if you observe plugin knowledge files exceeding 10 KB individually or 50 KB total during other plugin operations."

---

## Summary of Recommended Changes

### High Priority (affects skill triggering)

| # | Skill | Issue | Recommendation |
|---|-------|-------|----------------|
| 1 | `diagnose` + `reflect` | Trigger phrase overlap ("check plugin health") | Disambiguate descriptions; assign phrase to one skill |
| 2 | `marketplace` | "publish a plugin" overlaps with `release` | Change to "add plugin to marketplace" |
| 3 | `optimize` | "clean up" too generic | Scope to "clean up plugin" |
| 4 | All 3 referencing | `/skill-creator` unqualified | Change to `/plugin-dev:skill-creator` |

### Medium Priority (affects instruction clarity)

| # | Skill | Issue | Recommendation |
|---|-------|-------|----------------|
| 5 | `release` | `--store` flag missing from SKILL.md | Add to argument-hint and Parse Arguments, or remove from README |
| 6 | `release` | `AskUserQuestion` not a real tool name | Replace with plain language |
| 7 | `optimize` | `--dry-run` described as default but listed as a flag | Clarify: either `--apply` is the opt-in, or remove "default behavior" |
| 8 | `diagnose` | Agent diagnosis section references "trigger descriptions" for agents | Clarify what to check for agents (file existence, purpose clarity) |
| 9 | `reflect` | "project-specific" content detection lacks heuristics | Add: "Flag content applicable to any plugin without modification" |

### Low Priority (nice-to-have improvements)

| # | Skill | Issue | Recommendation |
|---|-------|-------|----------------|
| 10 | 3 skills | Duplicated cache guard paragraph | Move to knowledge file or trust the hook |
| 11 | `reflect` | No guidance on `.mcp.json` location | Clarify: expected at plugin root |
| 12 | `diagnose` | `gh issue list` unconditional | Make conditional on GitHub provider |
| 13 | `optimize` | Add proactive trigger | "Trigger if knowledge exceeds size thresholds" |
| 14 | `release` | Missing trigger phrases | Add "cut a release", "new version" |
| 15 | `marketplace` | `init` GitLab guidance vague | Reference `knowledge/marketplace.md` |

---

## Conclusion

The plugin-ops skills are well-organized and follow a consistent structure. The most impactful improvements are:

1. **Disambiguating overlapping triggers** between `diagnose`/`reflect` and `marketplace`/`release` to prevent misfires.
2. **Qualifying `/skill-creator` references** as `/plugin-dev:skill-creator` across three skills.
3. **Clarifying the `--dry-run` default behavior** in `optimize` which currently contradicts itself.

These changes would improve both trigger reliability and instruction execution accuracy without requiring structural changes to the plugin.
