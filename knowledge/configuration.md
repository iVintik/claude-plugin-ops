# Configuration

Plugin-ops uses a local configuration file to know which marketplaces are available and how to reach them.

## Config File Location

`.claude/plugin-ops.local.md` in the user's home directory or project root.

This follows the pattern of `.local.md` files that Claude Code loads as project-specific context.

## Format

YAML frontmatter in a markdown file:

```yaml
---
marketplaces:
  - name: personal
    provider: github
    repo: user/my-claude-plugins
    branch: main
  - name: work
    provider: gitlab
    url: https://gitlab.company.com
    project: team/claude-plugins
    branch: develop
  - name: oss
    provider: github
    repo: org/public-plugins
    branch: main
default_marketplace: personal
---
```

## Fields

### Marketplace Entry

| Field | Required | Description |
|-------|----------|-------------|
| `name` | yes | Short identifier for this marketplace |
| `provider` | yes | `github`, `gitlab`, or `git` |
| `repo` | github | `owner/repo-name` format |
| `project` | gitlab | `group/project` or numeric project ID |
| `url` | gitlab | GitLab instance URL (for on-prem) |
| `branch` | no | Default branch (defaults to `main`) |

### Top-Level

| Field | Required | Description |
|-------|----------|-------------|
| `marketplaces` | yes | List of marketplace configurations |
| `default_marketplace` | no | Which marketplace to use when `--store` is omitted |

## Provider Detection

If `provider` is not specified, skills infer it from the URL or repo format:
- Contains `github.com` or `repo` field → `github`
- Contains `gitlab` in URL → `gitlab`
- Otherwise → `git` (generic)

## No Config Behavior

If the config file doesn't exist, marketplace and release skills will:
1. Prompt the user to set up a marketplace
2. Offer to create the config file
3. Work with explicit `--store-url` arguments as a fallback
