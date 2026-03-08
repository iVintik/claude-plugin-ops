# Plugin Reflections

## 2026-03-08 — full-analysis

### Observations
- Plugin uses `commands/` pattern (5 toolkit + 41 BMAD) rather than `skills/` pattern — no trigger phrases, no proactive activation
- No `CLAUDE.md` at root; `AGENTS.md` serves as the agent-facing instructions (focused on Beads workflow)
- No `knowledge/` directory — all documentation lives in README.md (38 KB)
- `_bmad/` directory contains 232 files totaling 1.9 MB (79% of the 2.4 MB plugin)
- SessionStart hook works correctly: starts servers, checks for missing tools with 7-day cooldown
- Hook script has CRLF line terminators and is not marked executable (mode 644)
- `scripts/__pycache__/lib.cpython-310.pyc` is included in the distribution
- `.beads/` directory (56 KB) is shipped with the plugin, including `interactions.jsonl` which may contain development-time issue data
- `plugin.json` is minimal and valid (name, version, description, author, repository)
- No `.mcp.json` — appropriate since the plugin manages external MCP-providing tools rather than providing MCP itself
- README.md is thorough (609 lines) covering all 9 managed tools, workflows, architecture diagrams, and file locations
- `lib.py` is well-structured: stdlib-only, color support, clean helper functions for all managed services

### What Worked Well
- Clear separation between toolkit commands (commands/) and BMAD commands (.claude/commands/)
- Hook architecture: single SessionStart hook delegates to well-factored Python script
- `lib.py` shared helpers keep all scripts DRY with zero external dependencies
- README serves as both user documentation and comprehensive reference
- BMAD workflow files are loaded on-demand by commands (not eagerly loaded into context)
- Plugin properly uses `${CLAUDE_PLUGIN_ROOT}` for script paths in commands
- Auto-setup with cooldown (7-day marker) prevents repeated slow checks
- Server lifecycle management (start if installed but not running) is robust with timeout-based health checks

### Improvement Opportunities
1. **Externalize _bmad/ (high impact)** — At 1.9 MB / 232 files, BMAD dominates the plugin. Consider making it a separate plugin dependency or using lazy installation (download on first `/toolkit-init --bmad`). Most sessions never touch BMAD files directly.
2. **Add __pycache__ and .beads/ to .gitignore (medium impact)** — Python bytecode and development-time Beads data should not be distributed. Add `__pycache__/`, `*.pyc`, and `.beads/interactions.jsonl` to `.gitignore`.
3. **Fix hook script line endings and permissions (low impact)** — Convert `auto-setup.py` from CRLF to LF and mark executable. While `python3 script.py` invocation works regardless, this is a hygiene issue.
4. **Consider migrating to skills/ pattern (medium impact)** — The 5 toolkit commands would benefit from skill frontmatter features (trigger phrases, proactive descriptions). This would let Claude suggest `/toolkit-status` when users ask about tool health without knowing the exact command name.
5. **Add CLAUDE.md at plugin root (low impact)** — Currently `AGENTS.md` focuses only on Beads integration. A `CLAUDE.md` could provide Claude with a concise overview of what the toolkit does and when to suggest its commands, without needing to parse the full 38 KB README.
6. **README size (low impact)** — At 38 KB, the README is loaded into context when the plugin activates. Consider splitting into README.md (quick start + command reference) and a separate USAGE.md or docs/ for workflows and architecture details.
