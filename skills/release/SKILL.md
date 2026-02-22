---
name: release
description: Bump plugin version and publish to marketplace(s). Use when the user asks to release a plugin, bump version, publish a new version, deploy a plugin update, or tag a release.
argument-hint: "[plugin-path] <version> [--store name] [--dry-run]"
---

# Plugin Release

Version bump a plugin and update its entry in the marketplace(s) that contain it.

## Parse Arguments

Parse `$ARGUMENTS`:
- **First positional argument**: Path to plugin directory (or current directory if omitted)
- **Version argument**: New version (semver format, e.g., `1.2.0`)
- `--store name`: Target a specific marketplace only (skip auto-detection)
- `--dry-run`: Show what would happen without making changes

If version is not provided, ask the user. Suggest next patch/minor/major based on current version.

## Validate

1. Verify the plugin directory has `.claude-plugin/plugin.json`
2. Read current version and plugin name from `plugin.json`
3. Validate the new version:
   - Must be valid semver
   - Must be greater than current version
   - Warn if jumping multiple major versions
4. Check for uncommitted changes in the plugin repo — warn if dirty

## Update Plugin Version

1. Update `version` in `.claude-plugin/plugin.json`
2. Stage the change: `git add .claude-plugin/plugin.json`
3. Commit: `"release: v{version}"`
4. Push to the plugin's remote

## Find and Update Marketplace(s)

Read `.claude/plugin-ops.local.md` for marketplace configurations (see `knowledge/configuration.md`).

### Auto-detect which marketplaces contain this plugin:

1. Read config → get list of marketplace `local_path` entries
2. For each marketplace path:
   - Read `.claude-plugin/marketplace.json`
   - Search `plugins` array for an entry matching this plugin's name
3. Collect all matching marketplaces

If `--store name` is specified, only use that marketplace (skip scan).

If no config exists, prompt the user to create one or provide `--marketplace-path` directly.

### For each matching marketplace:

1. Read `.claude-plugin/marketplace.json` from the local clone
2. Update the plugin's `version` field in the `plugins` array
3. Stage: `git add .claude-plugin/marketplace.json`
4. Commit: `"release: {plugin-name} v{version}"`
5. Push to remote

## Output

Display summary:

```
Released {plugin-name} v{version}

Plugin repo:
  Updated: .claude-plugin/plugin.json
  Commit:  release: v{version}
  Pushed:  {remote-url}

Marketplaces updated:
  - {marketplace-name} ({local_path}): v{old} → v{new}

{Or: No marketplaces configured — plugin version updated locally only}
{Or: Plugin not found in any configured marketplace — version bumped in plugin only}
```

## Error Handling

- If git push fails (auth, permissions), report and suggest fixes
- If marketplace update fails, the plugin version is still bumped — report partial success
- Never force-push
- If `--dry-run`, show all steps without executing
