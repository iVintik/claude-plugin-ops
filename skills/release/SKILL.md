---
name: release
description: "Release a Claude Code plugin — bump its version, commit, push, and tag. Use whenever the user wants to release, version-bump, ship, or publish a plugin (any project with a .claude-plugin/ directory). Covers phrases like \"release my plugin\", \"bump plugin version\", \"ship it\", \"publish a new version\", \"deploy update\", \"push a release\", \"tag and push\". This is the canonical plugin release workflow — do NOT use manual git tags, gh release, or npm publish for Claude Code plugins. Not for: npm registry publishing, GitHub Releases with release notes, marketplace listing, or editing package.json versions directly."
argument-hint: "[plugin-path] [version] [--dry-run] [--no-tag]"
---

# Plugin Release

Version bump, commit, push, and create a git tag. If CI is configured, the tag triggers automated marketplace updates.

## Parse Arguments

Parse `$ARGUMENTS`:
- **First positional**: Path to plugin directory (default: current directory).
- **Version**: semver string like `1.2.0` (optional — prompts if missing).
- `--dry-run`: Show what would happen without changes.
- `--no-tag`: Skip git tag creation.

## Get Version (if not provided)

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/release.py <PLUGIN_PATH> --suggest
```

Returns JSON: `{"current": "1.1.0", "patch": "1.1.1", "minor": "1.2.0", "major": "2.0.0"}`.
Present options to the user via `AskUserQuestion`.

## Execute Release

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/release.py <PLUGIN_PATH> <VERSION> [--dry-run] [--no-tag]
```

## Handle Result

**Success (exit 0):**
1. Show: `Released {plugin} v{new_version} (was v{old_version})`
2. If `update_command` present: show the command for user to run manually
3. If `update_command` null: show `claude plugin update <name>@<marketplace>`
4. If `mcp_pids` non-empty: warn about stale MCP processes to kill
5. Tell user: "After updating, start a new Claude Code session to load the new version."

**Error (exit 1/2):** Display error from JSON `error` field, suggest fixes.

**IMPORTANT:** Never run `claude plugin install/update` from within a session — these hang. Show commands for the user to run manually.
