---
name: marketplace
description: Manage plugin marketplaces — create, list, add, or remove plugins from marketplace repositories. Use when the user asks to create a marketplace, publish a plugin, list marketplace plugins, add a plugin to a marketplace, manage a plugin store, or set up a plugin registry.
argument-hint: "<subcommand> [options]"
---

# Marketplace Management

Manage Claude Code plugin marketplaces. A marketplace is a git repository with a `marketplace.json` that catalogs available plugins.

## Parse Arguments

Parse `$ARGUMENTS` for a subcommand:
- `init <local-path>` — Create a new marketplace repository
- `list [--store name]` — List plugins in a marketplace
- `add <plugin-path> [--store name]` — Add a plugin to a marketplace
- `remove <plugin-name> [--store name]` — Remove a plugin from a marketplace

If no subcommand given, show usage help.

## Read Configuration

Read `knowledge/configuration.md` for the config file format.

Look for `.claude/plugin-ops.local.md` in:
1. Current working directory
2. User's home directory

Parse the YAML frontmatter to get marketplace `local_path` entries.

If `--store name` is provided, use that marketplace. Otherwise use the first configured marketplace.

If no config exists and no `--store` flag, prompt the user to set up a marketplace.

## init — Create New Marketplace

Ask the user for:
1. **Provider**: `github` or `gitlab` (detect from context if possible)
2. **Repository name**: e.g., `my-claude-plugins`
3. **Visibility**: public or private (default: private)
4. **Local path**: where to clone it

### For GitHub:
```bash
gh repo create <name> --<visibility> --clone
```

### For GitLab:
- If `glab` CLI is available: `glab project create <name> --visibility <vis>`
- If not: guide the user to create via GitLab UI or API, provide the API curl command:
  ```bash
  curl --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
    -X POST "https://<gitlab-url>/api/v4/projects" \
    -d "name=<name>&visibility=<vis>"
  ```

### Initialize marketplace:

Create `.claude-plugin/marketplace.json` using schema from `knowledge/marketplace.md`:

```json
{
  "name": "<repo-name>",
  "metadata": {
    "description": "Claude Code plugin marketplace",
    "version": "1.0.0"
  },
  "plugins": []
}
```

Commit and push.

### Update config:

Add the new marketplace to `.claude/plugin-ops.local.md`. Create the config file if it doesn't exist.

## list — List Marketplace Plugins

For the target marketplace(s):

1. Get `local_path` from config
2. Read `.claude-plugin/marketplace.json` directly from the local clone
3. Display plugins table:

```
Marketplace: {name} ({local_path})
Remote: {git remote get-url origin}

| Plugin | Version | Description |
|--------|---------|-------------|
| plugin-a | 1.2.0 | Does X |
| plugin-b | 0.3.1 | Does Y |

{N} plugins total
```

If `--store` is not specified and multiple marketplaces are configured, list all of them.

## add — Add Plugin to Marketplace

1. Read the plugin's `.claude-plugin/plugin.json` from `<plugin-path>`
2. Extract: name, description, version
3. Determine the plugin's git remote URL (`git remote get-url origin`)
4. Read `marketplace.json` from the target marketplace's `local_path`
5. Check if plugin already exists:
   - If yes: ask to update version/description instead
   - If no: append new entry
6. Write updated `marketplace.json`
7. Commit: `"add: <plugin-name> v<version>"`
8. Push to remote
9. Display confirmation

## remove — Remove Plugin from Marketplace

1. Read `marketplace.json` from the target marketplace's `local_path`
2. Find the plugin by name
3. If not found, show available plugins
4. Confirm removal with the user
5. Remove the entry from `plugins` array
6. Write updated `marketplace.json`
7. Commit: `"remove: <plugin-name>"`
8. Push to remote
9. Display confirmation

## Error Handling

- If `local_path` doesn't exist or has no `marketplace.json`, report clearly
- If git push fails, report and suggest `git pull` first
- Never expose tokens or credentials in output
