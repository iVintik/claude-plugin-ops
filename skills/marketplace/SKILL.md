---
name: marketplace
description: "ALWAYS invoke this skill when the user mentions \"marketplace\" in connection with creating, managing, populating, or querying a plugin marketplace they own. Trigger phrases include: \"init marketplace\", \"create marketplace\", \"add to marketplace\", \"publish to marketplace\", \"list marketplace\", \"remove from marketplace\", \"marketplace repo\", \"plugin store\", \"plugin catalog\", \"plugin registry\". Also trigger when the user wants to set up a git repository for distributing or cataloging Claude Code plugins. Do NOT trigger for: installing/browsing plugins as a consumer, releasing plugin versions, plugin development, code pushes, or plugin audits."
argument-hint: "<subcommand> [options]"
---

# Marketplace Management

Manage Claude Code plugin marketplaces. A marketplace is a git repository with a `.claude-plugin/marketplace.json` that catalogs available plugins.

## Parse Arguments

Parse `$ARGUMENTS` for subcommand:
- `init <local-path>` — Create a new marketplace repository
- `list [--store name]` — List plugins in a marketplace
- `add <plugin-path> [--store name]` — Add a plugin to a marketplace
- `remove <plugin-name> [--store name]` — Remove a plugin

No subcommand → show usage help.

## Configuration

Read `knowledge/configuration.md` for config format. Look for `.claude/plugin-ops.local.md` in cwd then home dir. Use `--store name` to select marketplace, otherwise first configured.

## init — Create New Marketplace

Gather: provider (github/gitlab), repo name, visibility (default: private), local path.

GitHub: `gh repo create <name> --<visibility> --clone`
GitLab: `glab project create` or guide API curl.

Initialize `.claude-plugin/marketplace.json` (schema from `knowledge/marketplace.md`):
```json
{
  "name": "<repo-name>",
  "metadata": { "description": "Claude Code plugin marketplace", "version": "1.0.0" },
  "plugins": []
}
```
Commit, push, update config.

## list — List Marketplace Plugins

Read `.claude-plugin/marketplace.json` from local clone, display:
```
Marketplace: {name} ({path})
| Plugin | Version | Description |
{N} plugins total
```
If no `--store` and multiple configured, list all.

## add — Add Plugin to Marketplace

1. Read plugin's `plugin.json` for name, description, version
2. Get plugin's git remote URL
3. Check for existing entry (offer update if exists)
4. Append to `.claude-plugin/marketplace.json`, commit, push

## remove — Remove Plugin from Marketplace

1. Find plugin by name (show available if not found)
2. Confirm with user
3. Remove entry, commit, push

## Error Handling
- Missing `local_path` or `.claude-plugin/marketplace.json`: report clearly
- Git push fails: suggest `git pull` first
- Never expose tokens in output
