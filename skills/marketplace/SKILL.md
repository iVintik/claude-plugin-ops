---
name: marketplace
description: Manage plugin marketplaces — create, list, add, or remove plugins from marketplace repositories. Use when the user asks to create a marketplace, publish a plugin, list marketplace plugins, add a plugin to a marketplace, manage a plugin store, or set up a plugin registry.
argument-hint: "<subcommand> [options]"
---

# Marketplace Management

Manage Claude Code plugin marketplaces. A marketplace is a git repository with a `marketplace.json` that catalogs available plugins.

## Parse Arguments

Parse `$ARGUMENTS` for a subcommand:
- `init` — Create a new marketplace repository
- `list [--store name]` — List plugins in a marketplace
- `add <plugin-path> [--store name]` — Add a plugin to a marketplace
- `remove <plugin-name> [--store name]` — Remove a plugin from a marketplace

If no subcommand given, show usage help.

## Read Configuration

Read `knowledge/configuration.md` for the config file format.

Look for `.claude/plugin-ops.local.md` in:
1. Current working directory
2. User's home directory

Parse the YAML frontmatter to get marketplace configurations.

If `--store name` is provided, use that marketplace. Otherwise use `default_marketplace` from config.

If no config exists and no `--store` flag, prompt the user to set up a marketplace or provide `--store-url` directly.

## init — Create New Marketplace

Ask the user for:
1. **Provider**: `github` or `gitlab` (detect from context if possible)
2. **Repository name**: e.g., `my-claude-plugins`
3. **Visibility**: public or private (default: private)

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

Offer to add the new marketplace to `.claude/plugin-ops.local.md`. Create the config file if it doesn't exist.

## list — List Marketplace Plugins

For the target marketplace(s):

1. Determine the marketplace repo URL from config
2. Fetch `marketplace.json`:
   - For GitHub: `gh api repos/<owner>/<repo>/contents/.claude-plugin/marketplace.json` and decode
   - For GitLab: `curl "https://<url>/api/v4/projects/<id>/repository/files/.claude-plugin%2Fmarketplace.json/raw?ref=<branch>"`
   - Or if the repo is cloned locally, read directly
3. Display plugins table:

```
Marketplace: {name} ({provider})

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
4. Clone or fetch the target marketplace repo to a temp directory
5. Read `marketplace.json`
6. Check if plugin already exists:
   - If yes: ask to update version/description instead
   - If no: append new entry
7. Write updated `marketplace.json`
8. Commit: `"add: <plugin-name> v<version>"`
9. Push to remote
10. Display confirmation

## remove — Remove Plugin from Marketplace

1. Clone or fetch the target marketplace repo
2. Read `marketplace.json`
3. Find the plugin by name
4. If not found, show available plugins
5. Confirm removal with the user
6. Remove the entry from `plugins` array
7. Write updated `marketplace.json`
8. Commit: `"remove: <plugin-name>"`
9. Push to remote
10. Display confirmation

## Error Handling

- If `gh` or `glab` is not installed, provide manual instructions
- If auth fails, guide the user to authenticate (`gh auth login`, `glab auth login`)
- If marketplace repo is not accessible, report the error clearly
- Never expose tokens or credentials in output
