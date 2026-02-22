---
name: release
description: Bump plugin version and publish to marketplace(s). Use when the user asks to release a plugin, bump version, publish a new version, deploy a plugin update, or tag a release.
argument-hint: "<plugin-path> <version> [--store name|--all-stores]"
---

# Plugin Release

Version bump a plugin and update its entry in one or more marketplaces.

## Parse Arguments

Parse `$ARGUMENTS`:
- **First positional argument**: Path to plugin directory (or current directory if omitted)
- **Second positional argument**: New version (semver format, e.g., `1.2.0`)
- `--store name`: Target a specific marketplace (from config)
- `--all-stores`: Update all configured marketplaces that contain this plugin
- `--dry-run`: Show what would happen without making changes

If version is not provided, ask the user. Suggest next patch/minor/major based on current version.

## Read Configuration

Read `.claude/plugin-ops.local.md` for marketplace configurations (see `knowledge/configuration.md`).

If no config exists and `--store` is not provided, ask where to publish or skip marketplace update.

## Validate

1. Verify the plugin directory has `.claude-plugin/plugin.json`
2. Read current version from `plugin.json`
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

## Update Marketplace(s)

For each target marketplace:

### Determine targets:
- `--store name`: use that specific marketplace
- `--all-stores`: find all marketplaces from config, check which ones contain this plugin
- No flag: use `default_marketplace` from config

### For each marketplace:

1. **Fetch marketplace.json**:
   - For GitHub: use `gh api` to read, then update and push via a temp clone
   - For GitLab: use API or temp clone
   - If locally cloned: update directly

2. **Find plugin entry** in `marketplace.json` by plugin name
   - If not found: ask user if they want to add it (delegate to marketplace add logic)

3. **Update version** in the plugin entry

4. **Commit**: `"release: {plugin-name} v{version}"`

5. **Push** to marketplace remote

## Output

Display summary:

```
Released {plugin-name} v{version}

Plugin repo:
  Updated: .claude-plugin/plugin.json
  Commit:  release: v{version}
  Pushed:  {remote-url}

Marketplaces updated:
  - {marketplace-name} ({provider}): v{old} → v{new}

{Or: No marketplaces configured — plugin version updated locally only}
```

## Error Handling

- If git push fails (auth, permissions), report and suggest fixes
- If marketplace update fails, the plugin version is still bumped — report partial success
- Never force-push
- If `--dry-run`, show all steps without executing
