# Plugin Audit: famdeck-toolkit v2.8.0

```
Reflection complete for famdeck-toolkit v2.8.0

Structure:  WARN — no skills/ or knowledge/ dirs; uses commands/ pattern instead
Skills:     0 skills (plugin uses 5 commands in commands/ + 41 in .claude/commands/)
Knowledge:  0 KB (no knowledge/ directory)
Hooks:      present (SessionStart — auto-setup.py, valid JSON, script exists)
MCP:        absent (no .mcp.json)

Top 3 improvement opportunities:

1. _bmad/ is 1.9 MB (232 files) — dominates the 2.4 MB plugin. Consider
   externalizing BMAD as a separate dependency or lazy-loading it, since most
   sessions don't use all 232 workflow files.

2. Python __pycache__/lib.cpython-310.pyc is shipped in the plugin cache.
   Add __pycache__/ to .gitignore to avoid distributing bytecode.

3. Hook script (auto-setup.py) is not marked executable (mode 644) and has
   CRLF line terminators. While Python handles this, the shebang line won't
   work if invoked directly on Unix. Fix with chmod +x and convert to LF.

For skills needing deeper refinement, recommend running /skill-creator
to iterate with test prompts and eval loops.

Full analysis captured below (not written to REFLECTIONS.md — draft only).
```

---

## Detailed Analysis

### 1. Structure

| Check | Status | Notes |
|-------|--------|-------|
| `.claude-plugin/plugin.json` | PASS | Valid JSON with name, description, version (2.8.0 semver), author, repository |
| `skills/` directory | MISSING | Plugin uses `commands/` (5 files) and `.claude/commands/` (41 files) instead of the skills pattern |
| `knowledge/` directory | MISSING | No dedicated knowledge directory |
| `CLAUDE.md` | MISSING | Not present at plugin root. `AGENTS.md` exists instead (Beads integration instructions) |
| `README.md` | PASS | Comprehensive, 609 lines, covers all tools, workflows, architecture |

**Verdict: WARN** — The plugin predates or deliberately avoids the skills/knowledge pattern. It uses the older `commands/` convention with `.claude/commands/` for BMAD. This works but means the plugin doesn't benefit from skill frontmatter features like trigger phrases or proactive activation.

### 2. Skills (Commands)

**Toolkit commands (commands/):** 5 files — toolkit-setup, toolkit-init, toolkit-status, toolkit-mode, toolkit-uninstall. All have valid YAML frontmatter with name and description. Clear step-by-step instructions. Appropriate use of `$ARGUMENTS` and `${CLAUDE_PLUGIN_ROOT}`.

**BMAD commands (.claude/commands/):** 41 files. Spot-checked:
- `bmad-bmm-create-prd.md` references `@{project-root}/_bmad/bmm/workflows/2-plan-workflows/create-prd/workflow-create-prd.md` — file **exists** in `_bmad/`.
- All BMAD commands follow the same pattern: load a workflow file and follow its directions.

**Issues found:**
- No trigger phrases or proactive descriptions in frontmatter — commands are only invoked explicitly by name.
- `toolkit-setup.md` references `/toolkit:toolkit-status` which uses a colon-separated skill path syntax, but the plugin doesn't have skills — just commands. May cause confusion.

### 3. Knowledge

No `knowledge/` directory exists. The plugin relies on:
- `README.md` (38 KB) — comprehensive but large for context loading
- `AGENTS.md` (3 KB) — Beads integration guide
- `_bmad/` (1.9 MB) — BMAD workflow templates loaded on demand by commands

Total plugin size is 2.4 MB, dominated by `_bmad/`. The README alone is within budget, but the overall plugin footprint is very large for a Claude Code plugin.

### 4. Hooks

| Check | Status | Notes |
|-------|--------|-------|
| `hooks/hooks.json` | PASS | Valid JSON, single SessionStart hook |
| Script exists | PASS | `hooks/scripts/auto-setup.py` present |
| Script executable | WARN | File mode is 644 (not executable) |
| Script encoding | WARN | CRLF line terminators (Windows-style) |
| Exit codes documented | No | Script uses implicit exit 0 |
| Timeout | PASS | 120s configured in hooks.json |

The hook script:
- Starts Agent Mail, Dolt, and Codeman servers if installed but not running
- Checks for missing tools with a 7-day cooldown (marker file)
- Logs missing tools with install instructions
- Uses `lib.py` for all shared helpers (clean separation)

### 5. MCP

No `.mcp.json` present. The plugin does not provide MCP servers itself — it manages tools that provide their own MCP servers (Agent Mail, Context7, Serena). This is appropriate for a meta-toolkit.

### 6. Cross-References

| Check | Status | Notes |
|-------|--------|-------|
| BMAD commands reference existing workflow files | PASS | Spot-checked — `workflow-create-prd.md` exists at referenced path |
| README lists all commands | PASS | All 5 toolkit commands documented; BMAD commands documented by category |
| Hook script references valid lib imports | PASS | All imported functions exist in `scripts/lib.py` |
| `__pycache__` in distribution | FAIL | `scripts/__pycache__/lib.cpython-310.pyc` shipped — should be gitignored |
| `.beads/` in distribution | WARN | `.beads/` directory (56 KB) shipped with the plugin — includes `interactions.jsonl` which may contain development-time data |

### Size Breakdown

| Directory | Size | Files | Notes |
|-----------|------|-------|-------|
| `_bmad/` | 1.9 MB | 232 | BMAD workflow templates — 79% of plugin |
| `.claude/commands/` | 164 KB | 41 | BMAD slash commands |
| `scripts/` | 124 KB | 8 | Python setup/init/status scripts |
| `.beads/` | 56 KB | 8 | Beads issue tracker (development data) |
| `commands/` | 20 KB | 5 | Toolkit core commands |
| `hooks/` | 8 KB | 2 | SessionStart hook |
| Other | ~48 KB | 17 | README, AGENTS, LICENSE, .github, .claude configs |
| **Total** | **2.4 MB** | **313** | |
