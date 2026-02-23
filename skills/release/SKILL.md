---
name: release
description: Bump plugin version and publish to marketplace(s). Use when the user asks to release a plugin, bump version, publish a new version, deploy a plugin update, tag a release, ship it, commit and release, push a release, or says "release this". IMPORTANT — this is the ONLY correct way to release any repo containing .claude-plugin/. Never use manual git tags or gh release for plugins.
argument-hint: "[plugin-path] [version] [--dry-run] [--no-tag]"
---

# Plugin Release

Version bump a plugin, commit, push, and create a git tag. If the plugin repo has CI configured, the tag triggers automated marketplace updates.

## Parse Arguments

Parse `$ARGUMENTS`:
- **First positional**: Path to plugin directory (default: current directory)
- **Version**: semver string like `1.2.0` (optional — will prompt if missing)
- `--dry-run`: Show what would happen without making changes
- `--no-tag`: Skip git tag creation

Set `PLUGIN_PATH` and `RELEASE_ARGS` from the parsed values.

## Get Version (if not provided)

If no version was given in arguments, run the suggest command to get options:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/release.py <PLUGIN_PATH> --suggest
```

This prints JSON like `{"current": "1.1.0", "patch": "1.1.1", "minor": "1.2.0", "major": "2.0.0"}`.

Present the three options to the user via `AskUserQuestion` and let them pick one.

## Execute Release

Run the release script via the Bash tool:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/release.py <PLUGIN_PATH> <VERSION> [--dry-run] [--no-tag]
```

## Handle Result

The script prints a JSON result to stdout.

**On success (exit 0):** Display a human-friendly summary:
```
Released {plugin} v{new_version} (was v{old_version})

Plugin pushed: yes/no
Tag pushed: yes/no
```

If `tag_pushed` is true and the plugin has CI configured, mention that the marketplace will be updated automatically by the CI pipeline.

**On error (exit 1 or 2):** Display the error message from JSON `error` field and suggest fixes.

## Marketplace Updates

This script does NOT update marketplaces directly. Marketplace updates are handled by CI:

- **GitHub**: Tag triggers GitHub Actions → dispatches to marketplace repo
- **GitLab**: Tag triggers multi-project pipeline → marketplace repo updates itself

If CI is not configured, the marketplace must be updated manually or via `/plugin-ops:marketplace`.
