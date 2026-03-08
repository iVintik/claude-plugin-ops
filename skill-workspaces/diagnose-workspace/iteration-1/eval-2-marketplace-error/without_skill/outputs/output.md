# Marketplace Skill Error Diagnosis

## Summary

The `/plugin-ops:marketplace` skill has **three root causes** that would produce errors during execution. Two are structural issues in the SKILL.md instructions, and one is an environmental dependency gap.

---

## Defect 1: Config file location mismatch — SKILL.md references wrong path

**Severity:** Critical — causes error on every subcommand except `init`

**Location:** `skills/marketplace/SKILL.md:23`

**Details:**

The SKILL.md says:

> Read `knowledge/configuration.md` for config format. Look for `.claude/plugin-ops.local.md` in cwd then home dir.

The actual config file exists at `~/.claude/plugin-ops.local.md` and uses YAML frontmatter format. However, the skill instructs the agent to look in the **current working directory first** (`.claude/plugin-ops.local.md` relative to cwd). When the user runs the marketplace command from an arbitrary project directory, there is no such file, and the agent must fall back to the home directory version.

This is a **minor ambiguity** rather than a hard error — the fallback to home dir should work. But it could cause confusion or incorrect behavior if a stale `.claude/plugin-ops.local.md` exists in a project directory.

**Fix:** Clarify the lookup order more explicitly, or just read from `~/.claude/plugin-ops.local.md` directly.

---

## Defect 2: marketplace.json path inconsistency

**Severity:** Critical — causes "file not found" errors for `list`, `add`, and `remove` subcommands

**Location:** `skills/marketplace/SKILL.md:33-39` vs `knowledge/marketplace.md:28` vs `knowledge/configuration.md:43-44`

**Details:**

The SKILL.md `init` subcommand creates `marketplace.json` at:

```
.claude-plugin/marketplace.json
```

This matches `knowledge/marketplace.md` line 28: "The `marketplace.json` lives at `.claude-plugin/marketplace.json` inside the marketplace repo."

However, the `list` subcommand (line 44) says:

> Read `marketplace.json` from local clone

This bare reference to `marketplace.json` (without the `.claude-plugin/` prefix) is ambiguous. An LLM executing this skill could look for `marketplace.json` at the repo root instead of `.claude-plugin/marketplace.json`, causing a "file not found" error.

The `add` and `remove` subcommands reference `marketplace.json` similarly without the full path (lines 57, 63).

**Fix:** Change all references to use the explicit path `.claude-plugin/marketplace.json` consistently in the `list`, `add`, and `remove` sections.

---

## Defect 3: No YAML frontmatter parser — config reading will fail

**Severity:** Critical — blocks all subcommands that need marketplace configuration

**Location:** `skills/marketplace/SKILL.md:23`

**Details:**

The skill instructs the agent to "Read `knowledge/configuration.md` for config format" and then read the config file. The config file (`~/.claude/plugin-ops.local.md`) uses **YAML frontmatter** delimited by `---`:

```yaml
---
marketplaces:
  - name: ivintik
    local_path: ~/dev/personal/tools/private-claude-marketplace
  - name: datasapience-internal
    local_path: ~/dev/ds/cmo/cmo-ai/tools/internal-claude-plugins
---
```

The skill gives no instructions on **how to parse YAML frontmatter from a markdown file**. The agent (Claude) can likely handle this since it understands YAML, but there is no explicit instruction to:

1. Strip the `---` delimiters
2. Parse the YAML between them
3. Extract the `marketplaces` array
4. Resolve `~` in `local_path` to the actual home directory

This is less of a hard error and more of an instruction gap — Claude will likely figure it out, but other skills (like `release`) delegate to a Python script (`release.py`) for deterministic operations. The marketplace skill has no such backing script, relying entirely on the LLM to interpret instructions correctly.

**Fix:** Either add explicit parsing instructions to the SKILL.md, or create a backing script similar to `release.py`.

---

## Defect 4: `--store` flag references "first configured" without defining selection logic

**Severity:** Minor — causes unpredictable behavior with multiple marketplaces

**Location:** `skills/marketplace/SKILL.md:23`

**Details:**

> Use `--store name` to select marketplace, otherwise first configured.

The user's config has two marketplaces (`ivintik` and `datasapience-internal`). Without `--store`, the skill says to use "first configured" — but YAML array ordering is preserved, so this should be deterministic. However, the `list` subcommand (line 50) says:

> If no `--store` and multiple configured, list all.

This contradicts the earlier "otherwise first configured" instruction. For `list` it lists all; for other subcommands it uses the first. This inconsistency could cause the agent to pick the wrong marketplace for `add` or `remove` operations.

**Fix:** Clarify the default selection behavior per-subcommand.

---

## Defect 5: `add` subcommand reads `plugin.json` at wrong path

**Severity:** Major — causes error when adding a plugin

**Location:** `skills/marketplace/SKILL.md:54`

**Details:**

The `add` subcommand says:

> 1. Read plugin's `plugin.json` for name, description, version

But the actual plugin metadata file lives at `.claude-plugin/plugin.json` (as seen in this repo and documented in the CLAUDE.md). The bare `plugin.json` reference is ambiguous and could cause the agent to look in the wrong location.

**Fix:** Change to "Read plugin's `.claude-plugin/plugin.json`".

---

## Defect 6: No `$ARGUMENTS` variable documentation or injection mechanism

**Severity:** Major — the skill may receive no arguments at all

**Location:** `skills/marketplace/SKILL.md:13`

**Details:**

The skill references `$ARGUMENTS` for parsing subcommands. This is a convention used by Claude Code's skill system where the user's arguments after the skill name are injected. However, unlike the `release` skill which passes arguments to a concrete script (`release.py`), the marketplace skill relies on the LLM to parse `$ARGUMENTS` from the skill invocation context.

If the skill is invoked without arguments (e.g., just `/plugin-ops:marketplace`), the skill says "No subcommand -> show usage help." This is fine. But if the user types something like `/plugin-ops:marketplace list --store ivintik`, the `$ARGUMENTS` string must contain `list --store ivintik`. Whether this works depends on how Claude Code injects arguments into skill context.

This is **not a bug in the skill itself** but rather a dependency on the skill runtime that may or may not work correctly.

---

## Defect 7: `init` subcommand — `glab` may not be installed

**Severity:** Minor — GitLab init path fails without clear error

**Location:** `skills/marketplace/SKILL.md:29-30`

**Details:**

The `init` section says:

> GitLab: `glab project create` or guide API curl.

If the user selects GitLab but `glab` is not installed, the skill says to "guide API curl" as a fallback, but provides no actual curl template. The agent would need to improvise the GitLab API call.

**Fix:** Add a concrete curl example for GitLab project creation as a fallback.

---

## Root Cause Summary

The most likely error when running the marketplace command is:

1. **Path ambiguity** — The skill references `marketplace.json` and `plugin.json` without their full `.claude-plugin/` prefix paths, causing file-not-found errors when the agent looks in the wrong directory.

2. **No backing script** — Unlike the `release` skill which delegates to `scripts/release.py` for deterministic execution, the marketplace skill is purely instruction-driven. Every operation (YAML parsing, JSON manipulation, git operations) relies on the LLM interpreting instructions correctly, making it fragile.

3. **Config parsing gap** — The YAML frontmatter parsing of the config file is not explicitly instructed, and tilde expansion in `local_path` values needs manual handling.

## Recommended Fixes (Priority Order)

1. **Fix all path references** — Use `.claude-plugin/marketplace.json` and `.claude-plugin/plugin.json` explicitly everywhere
2. **Create a `scripts/marketplace.py`** backing script for deterministic operations (init, list, add, remove), similar to `release.py`
3. **Add explicit config parsing instructions** with tilde expansion
4. **Resolve the `--store` default behavior contradiction** between general rule and `list` subcommand
