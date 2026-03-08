# Plugin Health Audit: plugin-ops v1.8.5

**Date**: 2026-03-08
**Method**: Manual analysis without using the reflect skill

---

## 1. Structure — PASS

| Check | Status | Notes |
|-------|--------|-------|
| `.claude-plugin/plugin.json` | Pass | Valid JSON, all required fields present |
| `name` field | Pass | "plugin-ops" |
| `description` field | Pass | Clear, specific purpose statement |
| `version` field | Pass | 1.8.5, valid semver |
| `skills/` directory | Pass | 5 skills present |
| `CLAUDE.md` | Pass | Exists, well-structured development guide |
| `README.md` | Pass | Exists, clear installation and usage docs |
| `agents` declared in plugin.json | Pass | 3 agents declared, all files exist on disk |

The `docs/` directory exists but is empty. This is a minor cosmetic issue — it should either contain content or be removed.

---

## 2. Skills — 5 total, 0 with critical issues, 2 with minor observations

### diagnose (skills/diagnose/SKILL.md) — 2,969 bytes

- **Frontmatter**: Valid. Name and description present.
- **Description quality**: Excellent. Rich trigger phrases ("why isn't this working", "plugin not triggering", "skill broken", "debug plugin"). Includes proactive trigger language.
- **Content**: Clear diagnostic steps organized by category. Report format well-defined.
- **References**: References `atlas_search_projects` (external tool, valid). References `/skill-creator` at the end — this is a skill from a different plugin (plugin-dev), which is fine as a recommendation but could confuse users if plugin-dev is not installed.
- **Verdict**: Pass

### reflect (skills/reflect/SKILL.md) — 2,874 bytes

- **Frontmatter**: Valid.
- **Description quality**: Strong. Covers "analyze plugin health", "audit plugin", "assess plugin quality", "review plugin structure", "run self-assessment", "how healthy is this plugin". Includes proactive trigger.
- **Content**: Well-organized 6-area analysis framework. References `knowledge/lifecycle-formats.md` (exists). Output format clearly defined.
- **References**: References `/skill-creator` at end — same observation as diagnose.
- **Verdict**: Pass

### optimize (skills/optimize/SKILL.md) — 1,962 bytes

- **Frontmatter**: Valid.
- **Description quality**: Good trigger phrases ("slim down", "clean up", "optimize", "reduce size", "make plugin smaller").
- **Content**: Clear two-phase approach (knowledge + skills). References `knowledge/lifecycle-formats.md` (exists).
- **Minor observation**: References `/skill-creator` for deeper refinement. Consistent cross-plugin reference pattern.
- **Verdict**: Pass

### marketplace (skills/marketplace/SKILL.md) — 2,493 bytes

- **Frontmatter**: Valid.
- **Description quality**: Good. Covers create, list, add, remove, and abstract phrases like "plugin distribution and discovery".
- **Content**: Well-structured subcommand documentation. References `knowledge/configuration.md` and `knowledge/marketplace.md` (both exist).
- **Verdict**: Pass

### release (skills/release/SKILL.md) — 1,950 bytes

- **Frontmatter**: Valid.
- **Description quality**: Good trigger phrases. Importantly includes "This is the ONLY correct way to release any repo containing .claude-plugin/" — strong claim that prevents competing approaches.
- **Content**: Clean wrapper around `scripts/release.py`. Uses `${CLAUDE_PLUGIN_ROOT}` correctly. Includes important caveat about never running `claude plugin install/update` from within a session.
- **Verdict**: Pass

### Cross-skill observation

All 5 skills consistently implement:
- Cache guard pattern (atlas resolution)
- Argument parsing section
- Clear output format

Three skills (diagnose, reflect, optimize) reference `/skill-creator` from the external `plugin-dev` plugin. This is a soft dependency — not broken, but the user gets a dead-end recommendation if plugin-dev is not installed. Could add a note like "if plugin-dev is installed".

---

## 3. Knowledge — 16.7 KB across 4 files

| File | Size | Assessment |
|------|------|------------|
| `configuration.md` | 2,341 B | Good. Concise config format docs with fallback behavior. |
| `env-vars.md` | 2,230 B | Good. Practical guidance for MCP/hooks/skills env var access. |
| `lifecycle-formats.md` | 1,037 B | Good. Minimal, defines REFLECTIONS.md format and size budgets. |
| `marketplace.md` | 11,109 B | **Warning**: Exceeds 10 KB budget (11.1 KB). |
| **Total** | **16,717 B** | Within 50 KB budget |

### marketplace.md deep-dive

At 11.1 KB, this file exceeds the plugin's own stated budget of 10 KB per knowledge file (defined in `lifecycle-formats.md`). The file contains:

- marketplace.json schema (essential, ~1 KB)
- Multi-marketplace support (essential, ~0.5 KB)
- Provider support (GitHub, GitLab, Generic) (essential, ~1 KB)
- GitHub Actions CI workflow templates (~3 KB)
- GitLab CI workflow templates (~3 KB)
- Token renewal docs (~1 KB)
- Setup instructions (~1 KB)

The CI workflow templates are the bulk. They contain full YAML code blocks that are useful but verbose. These could be split into a separate `knowledge/ci-templates.md` file or condensed by removing the full YAML blocks in favor of key configuration points with a reference to the `.github/workflows/publish.yml` that already exists in the repo.

---

## 4. Hooks — PASS

| Check | Status | Notes |
|-------|--------|-------|
| `hooks/hooks.json` valid JSON | Pass | Well-structured |
| Event names valid | Pass | Uses `PreToolUse` — correct event name |
| Matchers | Pass | `Edit` and `Write` — the two tools that modify files |
| Script exists | Pass | `hooks/scripts/guard-plugin-cache.sh` present |
| Script executable | Pass | `-rwxr-xr-x` permissions set |
| Timeout | Pass | 5 seconds — reasonable for a stdin-reading script |

### Hook script quality

The `guard-plugin-cache.sh` script is well-written:
- Uses `set -euo pipefail` for safety
- Parses JSON input via python3 (dependency assumption — reasonable for macOS/Linux)
- Fails gracefully if python3 parsing fails (falls through to empty string)
- Uses exit code 2 correctly to block the tool call
- Provides actionable guidance in the error message (use atlas, edit source repo)

**One minor concern**: The script uses `python3 -c` with inline JSON parsing. If `python3` is not available (unlikely but possible), the script silently allows the edit through because the `|| echo ""` fallback results in an empty `FILE_PATH`, which won't match the cache pattern. This is actually the safe-fail direction — better to allow than to block unexpectedly.

---

## 5. Agents — 3 total, well-structured

| Agent | Model | Max Turns | Assessment |
|-------|-------|-----------|------------|
| plugin-auditor | haiku | 15 | Read-only audit agent. Good model choice for cost-effective analysis. |
| plugin-diagnostician | sonnet | 12 | Root-cause investigation. Sonnet appropriate for deeper reasoning. |
| plugin-optimizer | sonnet | 15 | Analysis-only by default (dry-run). Good safety pattern. |

All three agents:
- Have valid YAML frontmatter with name, description, tools, model, maxTurns
- Correctly specify `mcpServers: []` (added in commit ea009ba to prevent MCP process explosion — good fix)
- Are declared in plugin.json's `agents` array
- Have clear scope boundaries (read-only analysis, report format)
- Reference the cache vs repo pattern consistently
- Use `ToolSearch` to find atlas — correct approach for discovering deferred tools

**Observation**: The agents mirror the skills (auditor ~ reflect, diagnostician ~ diagnose, optimizer ~ optimize). This creates two invocation paths for the same functionality: skill-based (user-driven) and agent-based (delegatable). This is intentional and well-designed — agents can be spawned as subagents while skills run in the main conversation.

---

## 6. MCP — Not present (by design)

The CLAUDE.md explicitly states "No MCP server — All functionality through skills (markdown workflows)." This is a deliberate design choice. For a plugin that primarily orchestrates file reads, git operations, and text analysis, MCP would add unnecessary complexity.

---

## 7. Cross-References

| Check | Status | Notes |
|-------|--------|-------|
| Skills reference existing knowledge | Pass | All 4 knowledge files are referenced by at least one skill |
| CLAUDE.md matches actual structure | Pass | Directory tree accurate, relationship table correct |
| README.md lists all skills | Pass | All 5 skills documented with usage |
| Agents reference valid tools | Pass | Read, Grep, Glob, Bash, ToolSearch — all standard tools |
| plugin.json agents list matches files | Pass | 3 agents declared, 3 files exist |

**Minor**: CLAUDE.md directory tree does not mention `agents/` directory, though agents are referenced in plugin.json. The tree shows `knowledge/` having only 3 files but there are actually 4 (missing `env-vars.md`).

---

## 8. Release Infrastructure

### release.py (scripts/release.py) — 8,880 bytes

Well-structured Python script with:
- Clean argument parsing with `--suggest`, `--dry-run`, `--no-tag` modes
- Semver validation (strict X.Y.Z format)
- Version comparison (prevents downgrade)
- Working tree check with warnings (does not block dirty releases — deliberate)
- `git add -A` in release commit (aligns with the project's CLAUDE.md rule about always staging everything)
- Post-release helpers: marketplace detection from cache, stale MCP PID detection
- JSON output for machine consumption
- Clear exit codes (0=success, 1=validation, 2=git)

**No issues found.** The script is deterministic and well-tested based on commit history.

### CI (`.github/workflows/publish.yml`)

- Triggers on GitHub release publish
- Dispatches to `iVintik/private-claude-marketplace` — note this is a hardcoded reference to a specific private marketplace repo, which is appropriate for this specific plugin's CI but means the workflow template in `knowledge/marketplace.md` differs from the actual workflow (uses `<owner>/<marketplace-repo>` placeholder).

---

## 9. Auxiliary Files

| File | Assessment |
|------|------------|
| `AGENTS.md` | Issue tracking instructions using `bd` (beads). Well-documented but is a project management file, not a plugin component. |
| `.claude/atlas.yaml` | Minimal — just initialized. Summary is "Initialized by toolkit" which is a TODO. |
| `.claude/relay.yaml` | Issue tracker config. Not plugin-relevant. |
| `.claude/commands/bmad-*` | 40+ BMAD framework commands. These are development tools, not part of the plugin's shipped functionality. |
| `_bmad/`, `_bmad-output/` | BMAD framework files. Development tooling. |
| `.beads/` | Issue tracking data. |
| `LICENSE` | MIT. Present and valid. |

The `.claude/atlas.yaml` summary being "Initialized by toolkit" is a minor cosmetic issue — it should describe the project.

---

## Summary Scorecard

| Category | Status | Score |
|----------|--------|-------|
| Structure | Pass | 9/10 |
| Skills (5) | Pass, minor observations | 9/10 |
| Knowledge (4 files, 16.7 KB) | Warn — marketplace.md exceeds 10 KB | 7/10 |
| Hooks | Pass | 10/10 |
| Agents (3) | Pass | 9/10 |
| MCP | N/A (by design) | -- |
| Cross-references | Pass, minor CLAUDE.md drift | 8/10 |
| Release infrastructure | Pass | 9/10 |
| **Overall** | **Healthy** | **8.7/10** |

---

## Top Improvement Opportunities (ordered by impact)

### 1. Split or condense `knowledge/marketplace.md` (7/10 impact)

At 11.1 KB, this file exceeds the plugin's own 10 KB budget. The CI workflow templates (GitHub Actions + GitLab CI) account for ~6 KB. Options:
- Split CI templates into `knowledge/ci-templates.md`
- Condense by removing full YAML blocks and referencing `.github/workflows/publish.yml` as the canonical example
- Either approach brings marketplace.md well under budget

### 2. Update CLAUDE.md directory tree (3/10 impact)

The directory tree in CLAUDE.md is missing:
- `agents/` directory (3 agent files)
- `knowledge/env-vars.md` (only shows 3 of 4 knowledge files)

This drift between documentation and reality is minor but could confuse contributors.

### 3. Remove empty `docs/` directory (1/10 impact)

The `docs/` directory exists but contains no files. Either add content or remove it.

### 4. Qualify `/skill-creator` references (2/10 impact)

Three skills recommend `/skill-creator` from plugin-dev without noting it requires a separate plugin. Adding "if plugin-dev is installed" would prevent confusion.

### 5. Update atlas.yaml summary (1/10 impact)

The summary "Initialized by toolkit" should be replaced with a real project description.

---

## Conclusion

**plugin-ops is a healthy, well-designed plugin.** It has a clear purpose (lifecycle management), clean separation from Anthropic's plugin-dev, consistent patterns across all skills and agents, and a working release pipeline. The cache guard hook is a smart safety measure. The agent/skill duality provides flexibility for different invocation patterns.

The only substantive issue is the oversized `marketplace.md` knowledge file. All other findings are cosmetic. The plugin practices what it preaches — its own structure would pass its own reflect/audit checks with only a warning on knowledge size.
