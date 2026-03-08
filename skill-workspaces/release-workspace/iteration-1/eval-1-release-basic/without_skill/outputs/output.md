# Release Process for the plugin-ops Plugin

This document describes the complete process for releasing the `plugin-ops` Claude Code plugin, based on analysis of the repository at `/Users/ivintik/dev/personal/tools/claude-plugin-ops/`.

## Current State

- **Plugin name:** `plugin-ops`
- **Current version:** `1.8.5` (from `.claude-plugin/plugin.json`)
- **Repository:** `https://github.com/iVintik/claude-plugin-ops`

## Release Steps

### 1. Determine the New Version

Run the suggest command to see version options:

```bash
python3 /Users/ivintik/dev/personal/tools/claude-plugin-ops/scripts/release.py /Users/ivintik/dev/personal/tools/claude-plugin-ops/ --suggest
```

This returns JSON with three options based on the current version (`1.8.5`):

| Bump type | New version |
|-----------|-------------|
| Patch     | `1.8.6`     |
| Minor     | `1.9.0`     |
| Major     | `2.0.0`     |

Choose the appropriate bump level based on the versioning guidelines:

- **Patch** -- bug fixes, knowledge updates, minor tweaks
- **Minor** -- new skill or major feature
- **Major** -- breaking changes (renamed/removed skills, changed interfaces)

### 2. Execute the Release

Run the release script with the chosen version (e.g., `1.9.0`):

```bash
python3 /Users/ivintik/dev/personal/tools/claude-plugin-ops/scripts/release.py /Users/ivintik/dev/personal/tools/claude-plugin-ops/ 1.9.0
```

The script performs the following operations in sequence:

1. **Reads** `.claude-plugin/plugin.json` and validates the current version is valid semver.
2. **Validates** the new version is valid semver and strictly greater than the current version.
3. **Checks the working tree** -- if there are uncommitted changes, it warns that they will be included in the release commit (this is intentional; the project convention is to always stage everything).
4. **Updates** the `version` field in `.claude-plugin/plugin.json` to the new version.
5. **Stages all changes** via `git add -A` (ensures nothing is left behind).
6. **Commits** with message `release: v1.9.0`.
7. **Pushes** the commit to the remote (`git push`).
8. **Creates an annotated git tag** `v1.9.0` with message `release: v1.9.0`.
9. **Pushes the tag** to the remote (`git push origin v1.9.0`).

### 3. Post-Release Output

The script outputs a JSON result containing:

- `plugin` -- plugin name (`plugin-ops`)
- `old_version` / `new_version` -- version transition
- `plugin_pushed` -- whether the commit was pushed (true unless `--dry-run`)
- `tag_pushed` -- whether the tag was pushed (true unless `--dry-run` or `--no-tag`)
- `warnings` -- any warnings (e.g., uncommitted changes included)
- `update_command` -- if the plugin is installed via a marketplace, shows the update command (e.g., `claude plugin update plugin-ops@personal`)
- `mcp_pids` -- PIDs of any stale MCP server processes still running from the old version's cache path

### 4. Post-Release Actions (Manual)

After the release completes:

1. **Update locally** -- run the update command shown in the output:
   ```bash
   claude plugin update plugin-ops@<marketplace-name>
   ```
2. **Kill stale MCP processes** -- if `mcp_pids` is non-empty, kill those processes.
3. **Start a new Claude Code session** -- required to load the new plugin version.
4. **CI triggers** -- if the repository has GitHub Actions configured (`.github/workflows/publish.yml`), the tag push automatically triggers:
   - npm publish (if `package.json` exists with npm config)
   - Repository dispatch to the marketplace repo, which updates `marketplace.json` with the new version

## Optional Flags

| Flag | Effect |
|------|--------|
| `--dry-run` | Shows what would happen without making any changes (no file edits, no git operations) |
| `--no-tag` | Skips git tag creation and push (still commits and pushes the version bump) |

## Using the Skill Instead of the Script Directly

The recommended way to release is via the `/plugin-ops:release` skill, which wraps the script:

```
/plugin-ops:release /Users/ivintik/dev/personal/tools/claude-plugin-ops/ 1.9.0
```

The skill handles argument parsing, version suggestion prompts (if version is omitted), and formats the output with actionable guidance.

## Summary

The release process for a Claude Code plugin is:

1. Bump `version` in `.claude-plugin/plugin.json`
2. `git add -A && git commit -m "release: vX.Y.Z"`
3. `git push`
4. `git tag -a vX.Y.Z -m "release: vX.Y.Z"`
5. `git push origin vX.Y.Z`

All of this is automated by `scripts/release.py`. The tag push optionally triggers CI pipelines that propagate the version to marketplace repositories.
