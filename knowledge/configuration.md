# Configuration

Plugin-ops uses a local configuration file to know which marketplaces are available.

## Config File Location

`.claude/plugin-ops.local.md` in the user's home directory or project root.

This follows the pattern of `.local.md` files that Claude Code loads as project-specific context.

## Format

YAML frontmatter in a markdown file:

```yaml
---
marketplaces:
  - name: personal
    local_path: ~/dev/my-claude-plugins
  - name: work
    local_path: ~/dev/work/claude-plugins
---
```

## Fields

### Marketplace Entry

| Field | Required | Description |
|-------|----------|-------------|
| `name` | yes | Short identifier for this marketplace |
| `local_path` | yes | Path to the locally cloned marketplace repository |

That's it. The `release` and `marketplace` skills read everything else from the repo itself:
- **Remote URL**: `git remote get-url origin` from the local clone
- **Provider** (github/gitlab/generic): inferred from the remote URL
- **Branch**: current branch of the local clone
- **Plugin list**: parsed from `.claude-plugin/marketplace.json` in the clone

## How Plugin-to-Marketplace Matching Works

When releasing a plugin, the skill:
1. Reads `plugin.json` from the current plugin directory → gets plugin name
2. Reads config → gets list of marketplace local paths
3. For each marketplace, reads `.claude-plugin/marketplace.json`
4. Finds which marketplace(s) contain an entry for this plugin name
5. Updates version in those marketplace(s)

This means no per-plugin configuration is needed. The mapping lives in the marketplace repos themselves.

## No Config Behavior

If the config file doesn't exist, marketplace and release skills will:
1. Prompt the user to set up a marketplace
2. Offer to create the config file
3. Work with explicit `--marketplace-path` argument as a fallback
