# Famdeck Toolkit Plugin Audit (v2.8.0)

**Audit date:** 2026-03-08
**Plugin path:** `~/.claude/plugins/cache/ivintik/famdeck-toolkit/2.8.0/`
**Total size on disk:** 2.4 MB
**License:** MIT (Copyright 2026 Alexander Budkov)
**Repository:** https://github.com/iVintik/claude-plugin-toolkit

---

## 1. Plugin Identity and Metadata

| Field | Value |
|-------|-------|
| Name | famdeck-toolkit |
| Version | 2.8.0 |
| Author | iVintik |
| Description | "Setup and project init for Claude Code tools -- Context7, Serena, Beads, Agent Mail, Atlas, Relay, Codeman" |
| Manifest file | `.claude-plugin/plugin.json` |

**Version history in cache:** 2.4.2, 2.5.0, 2.6.1, 2.8.0 (four versions present; no 2.7.x -- jump from 2.6.1 to 2.8.0).

**Assessment:** Metadata is clean and minimal. The description accurately reflects the plugin's scope.

---

## 2. Structure Overview

```
2.8.0/
  .claude-plugin/plugin.json          # Plugin manifest
  .claude/
    atlas.yaml                         # Self-registration in Atlas
    relay.yaml                         # Self-registration in Relay
    commands/                          # 41 slash commands (5 toolkit + 36 BMAD)
  commands/                            # 5 toolkit command definitions
  hooks/
    hooks.json                         # SessionStart hook definition
    scripts/auto-setup.py              # Hook implementation
  scripts/
    lib.py                             # Shared library (stdlib-only)
    setup.py                           # Interactive tool installer
    init.py                            # Batch project initializer
    status.py                          # Status reporter
    uninstall.py                       # Tool uninstaller
    bmad-patches/                      # 5 BMAD agent customize patches
  _bmad/                               # BMAD-METHOD v6.0.3 (bundled)
  .beads/                              # Beads issue DB for the toolkit itself
  .github/workflows/publish.yml        # CI/CD
  AGENTS.md                            # Agent instructions (Beads workflow)
  README.md                            # Comprehensive documentation (609 lines)
  LICENSE                              # MIT
  .gitignore                           # .serena/, .DS_Store, node_modules/
```

---

## 3. Commands / Skills

### 3.1 Toolkit Commands (5)

Located in `commands/` (top-level, referenced by the plugin system):

| Command | Purpose | Invocation |
|---------|---------|------------|
| `toolkit-setup` | Interactive tool installer | Delegates to terminal `python3 scripts/setup.py` |
| `toolkit-init` | Batch project initializer (scan + init) | Runs `python3 scripts/init.py` directly |
| `toolkit-status` | Shows installed tools + per-project state | Runs `python3 scripts/status.py` |
| `toolkit-mode` | Set project init mode (normal/readonly/ignore) | Inline logic in command markdown |
| `toolkit-uninstall` | Remove installed tools | Runs `python3 scripts/uninstall.py` |

**Notable:** `toolkit-setup` explicitly tells Claude NOT to run the script itself but to instruct the user to run it in a terminal, because `claude plugin install` hangs when invoked from within a running Claude Code session. This is a practical workaround for a real limitation.

### 3.2 BMAD Commands (36)

Located in `.claude/commands/`. These are slash commands forwarded from the bundled BMAD-METHOD module:

- **10 agent personas:** bmad-master, analyst, architect, dev, pm, qa, quick-flow-solo-dev, sm, tech-writer, ux-designer
- **26 workflow commands:** covering the full SDLC lifecycle (PRD creation, architecture, epics/stories, dev-story implementation, code review, sprint planning, retrospective, domain/market/technical research, etc.)

All BMAD commands follow a uniform pattern: load `_bmad/core/tasks/workflow.xml`, then process the specific workflow YAML. This is consistent and maintainable.

**Total command file lines:** 432 lines across 41 files (average ~10.5 lines per command -- commands are concise delegates).

---

## 4. Hooks

### SessionStart Hook

**File:** `hooks/hooks.json` + `hooks/scripts/auto-setup.py`
**Matcher:** `*` (runs in every project)
**Timeout:** 120 seconds

**What it does:**
1. Starts Agent Mail server (port 8765) if installed but not running
2. Starts Dolt sql-server (port 3307) if installed but not running
3. Starts Codeman server (port 3000) if installed but not running
4. Checks which tools are missing (read-only, no installs)
5. Logs missing tools with a user-actionable setup command
6. Uses a 7-day TTL marker to avoid redundant checks

**Assessment:**
- Good: Read-only checks, no in-session installs (avoids the hanging bug)
- Good: Server auto-start is pragmatic for services that need to be always-on
- Good: 7-day cooldown prevents startup noise
- Risk: Starting 3 background services on every new session could be surprising to users who don't use all tools. No opt-out mechanism per service.
- Minor: File handle leak in `start_mail_server()` and `start_codeman()` -- `open(log_file, "a")` is passed to `Popen` but never closed by the parent process. This is harmless in practice (OS cleans up) but not clean.

---

## 5. Scripts / Core Logic

### 5.1 lib.py (Shared Library)

- **385 lines**, stdlib-only (no pip dependencies)
- Provides: color constants, logging, command runners, Claude config readers, server health checks, server starters, git helpers, marker file management
- Clean separation of concerns
- Handles both `~/.claude.json` and `~/.claude/settings.json` for MCP detection (robustness)

**Issues found:**
1. **File handle leaks:** `open(path).read()` pattern used without context managers in several places (lines 105, 126, 161, 185). Not critical but not best practice.
2. **Shell injection potential:** `run()` uses `shell=True` with string commands. Most callers pass hardcoded strings, but `init_beads()` in init.py interpolates `project_dir` into a shell command without escaping (line 323 of init.py: `f'cd "{project_dir}" && bd init --quiet {slug}'`). The slug is sanitized to `[a-z0-9-]` but `project_dir` relies on double-quoting only, which could break on paths containing `"` or `$`.
3. **Type hints:** Uses `str | None` union syntax (Python 3.10+), consistent with the stated requirement.

### 5.2 setup.py (Tool Installer)

- **451 lines**, defines 10 tools with install/uninstall/check functions
- Tools: Atlas, Relay, Famdeck, Context7, Serena, Dolt, Beads, beads-ui, Agent Mail, Codeman
- Supports interactive mode, `--non-interactive`, and `--install <tool>` targeting
- Handles legacy MCP-to-plugin migration for Context7 and Serena
- Auto-installs dependencies (uv, npm, tmux) per platform

**Issues found:**
1. **Inconsistency in uninstall.py:** The uninstall script still checks `check_mcp()` for Context7 and Serena (lines 32, 38), but setup.py migrates them to plugins. If a user installed them post-migration, uninstall would fail to find them via MCP check. The setup.py `_uninstall_*` functions handle both paths, but uninstall.py does not.
2. **Agent Mail install uses `uv sync`** which depends on a `pyproject.toml` in the cloned repo. If the upstream repo changes its dependency format, install breaks.
3. **Codeman install via curl pipe to bash** is a common pattern but carries the usual supply-chain risk.

### 5.3 init.py (Batch Project Initializer)

- **663 lines**, the most substantial script
- Scans for git repos up to configurable depth
- Initializes: Atlas, Relay, Beads, Agent Mail guard, Serena, BMAD
- Supports project modes: normal, readonly, ignore
- BMAD customize patches: applies toolkit-specific overrides to BMAD agent configs

**Quality highlights:**
- Idempotent: checks for existing config before writing
- Readonly mode uses `.git/info/exclude` (local-only gitignore) -- clever approach
- Legacy marker migration (toolkit-ignore -> toolkit-mode)
- BMAD patch system detects user customizations and skips to avoid clobbering

**Issues found:**
1. **Agent Mail guard install:** Passes `project_dir` twice to the CLI command (line 404: `guard install "{project_dir}" "{project_dir}"`). This looks like a potential bug or unusual API.
2. **Atlas registry format is fragile YAML:** Registry entries are appended with string concatenation rather than YAML library parsing. If the registry file is malformed, appending could produce invalid YAML.
3. **Slug collision handling is minimal:** If `slug` already exists, it appends `-2`. But if `slug-2` also exists, there's no further uniqueness guarantee.

### 5.4 status.py (Status Reporter)

- **125 lines**, clean and focused
- Shows user-level tool status + per-project state
- Includes marker timestamp

**No significant issues found.** This is well-written diagnostic code.

### 5.5 uninstall.py

- **134 lines**, interactive uninstaller
- Supports individual tool removal or "all"

**Issue:** Context7 and Serena check functions use `check_mcp()` instead of `check_plugin()`, which is stale after migration (see 5.2 above).

---

## 6. Knowledge Files and Documentation

### README.md (609 lines)
- Comprehensive: covers all 9 tools, installation, usage workflows, architecture diagrams
- Includes practical workflow examples (daily work, handoffs, overnight autonomous work, multi-agent coordination, BMAD lifecycle)
- Architecture diagrams are ASCII-based and clear
- File locations reference table is helpful

**Quality:** Excellent. This is production-grade documentation.

### AGENTS.md (127 lines)
- Instructions for AI agents using the project
- Beads integration guide with workflow steps
- "Landing the Plane" section enforces session completion protocol (commit, push, clean up)

**Quality:** Good. The "NEVER stop before pushing" and "YOU must push" directives are strongly worded and appropriate for autonomous agent contexts.

### BMAD Knowledge Files
- `_bmad/` contains the full BMAD-METHOD v6.0.3 installation
- Includes agent definitions, workflow configs, data templates, team configurations
- `_bmad/_memory/` contains persistent memory (documentation standards)
- `scripts/bmad-patches/` contains 5 customize patches for: architect, dev, pm, qa, sm

The BMAD patches are notable -- they inject toolkit-specific critical actions like mandatory E2E testing and retrospective entry verification. This is a sophisticated integration layer.

---

## 7. Beads Issue Tracking

The plugin tracks its own development via Beads (`.beads/` directory with `config.yaml`, `metadata.json`, `interactions.jsonl`).

- Database backend: Dolt (server mode, port 3307)
- Database name: `beads_famdeck-toolkit`

This is "eating your own dog food" -- using the issue tracker the plugin installs for others.

---

## 8. Health Assessment

### Strengths

1. **Comprehensive scope:** Manages 9 tools through a single entry point with consistent patterns
2. **Zero external Python dependencies:** All scripts are stdlib-only, eliminating version conflicts
3. **Idempotent operations:** Init functions check before writing, making re-runs safe
4. **Practical workarounds:** Correctly handles the Claude CLI in-session hanging limitation
5. **Server lifecycle management:** Auto-starts services and does health checks
6. **Excellent documentation:** README covers installation, daily workflows, architecture, and edge cases
7. **BMAD integration is deep:** Custom patches, per-project install, patch conflict detection
8. **Project mode system:** readonly and ignore modes handle third-party repos gracefully
9. **Legacy migration paths:** MCP-to-plugin migration for Context7 and Serena
10. **Self-dogfooding:** Uses Beads for its own issue tracking

### Weaknesses

1. **Uninstall script inconsistency:** Context7 and Serena check functions are stale (MCP vs plugin)
2. **File handle leaks:** Multiple `open().read()` without context managers
3. **Shell injection surface:** `shell=True` with interpolated paths in `run()` calls
4. **YAML registry fragility:** String concatenation for YAML writes instead of a YAML library
5. **No per-service opt-out for auto-start:** All three services start if installed, no configuration
6. **Slug collision handling is weak:** Only one `-2` suffix attempt
7. **Agent Mail guard CLI receives project_dir twice** -- appears to be a copy-paste issue or unusual API convention
8. **Four cached versions on disk:** 2.4.2, 2.5.0, 2.6.1, 2.8.0 occupy ~10 MB total. No automatic cleanup of old versions.

### Risks

1. **Service auto-start on every session** could conflict with user workflows (port conflicts, resource usage)
2. **Codeman install via remote bash script** is a supply-chain risk
3. **Agent Mail clones a third-party repo** (`Dicklesworthstone/mcp_agent_mail`) -- upstream changes could break the install
4. **BMAD v6.0.3 is bundled directly** -- no update mechanism if the upstream BMAD-METHOD publishes fixes

### Missing Elements

1. **No automated tests** for the Python scripts
2. **No changelog** between versions (version jump from 2.6.1 to 2.8.0 is unexplained)
3. **No health check for Dolt** in the status command (it checks install but not running state)
4. **No error recovery** if a service fails to start (logs a message but no retry or user notification beyond initial log)

---

## 9. Overall Health Score

| Category | Score | Notes |
|----------|-------|-------|
| Functionality | 9/10 | Comprehensive tool management with practical workflows |
| Code Quality | 7/10 | Clean but has file handle leaks, shell injection surface, and one stale module |
| Documentation | 9/10 | Excellent README, clear AGENTS.md, good inline comments |
| Reliability | 7/10 | Idempotent ops are good; fragile YAML writes and no tests are concerning |
| Security | 6/10 | Shell=True usage, curl-pipe-bash installs, third-party repo cloning |
| Maintainability | 7/10 | Clear structure but bundled BMAD has no update path; no tests |
| User Experience | 8/10 | Good interactive setup, clear status output, practical session hook |

**Overall: 7.6/10 -- Healthy with known technical debt.**

The plugin is functional, well-documented, and solves a real orchestration problem. The primary areas for improvement are: adding tests, fixing the uninstall inconsistency, replacing shell=True string interpolation with proper argument lists, and adding per-service auto-start configuration.
