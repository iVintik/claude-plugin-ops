---
name: marketplace
description: "Manage Claude Code plugin marketplaces — create, list, add, or remove plugins from marketplace repositories. Use when the user asks to \"create a marketplace\", \"publish a plugin\", \"list marketplace plugins\", \"add plugin to store\", \"manage plugin catalog\", \"set up a plugin registry\", \"remove from marketplace\", or anything about plugin distribution and discovery."
argument-hint: "<subcommand> [options]"
---

# Marketplace Management

Manage Claude Code plugin marketplaces. A marketplace is a git repository with a `marketplace.json` that catalogs available plugins.

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

Read `marketplace.json` from local clone, display:
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
4. Append to `marketplace.json`, commit, push

## remove — Remove Plugin from Marketplace

1. Find plugin by name (show available if not found)
2. Confirm with user
3. Remove entry, commit, push

## Error Handling
- Missing `local_path` or `marketplace.json`: report clearly
- Git push fails: suggest `git pull` first
- Never expose tokens in output
