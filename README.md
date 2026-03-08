# plugin-ops

Plugin lifecycle management for Claude Code. Audit health, optimize, diagnose, release, and manage marketplaces.

## Installation

```bash
git clone https://github.com/iVintik/claude-plugin-ops.git
```

Then add to your Claude Code plugins.

## Skills

| Skill | Usage | Purpose |
|-------|-------|---------|
| `/plugin-ops:reflect` | `/plugin-ops:reflect [path] [--brief]` | Analyze plugin health |
| `/plugin-ops:diagnose` | `/plugin-ops:diagnose [path] [--skill SKILL-NAME]` | Diagnose plugin defects |
| `/plugin-ops:optimize` | `/plugin-ops:optimize [path] [--dry-run] [--target ...]` | Optimize plugin size/quality |
| `/plugin-ops:marketplace` | `/plugin-ops:marketplace init\|list\|add\|remove` | Manage plugin marketplaces |
| `/plugin-ops:release` | `/plugin-ops:release [path] <version> [--store name]` | Version bump + publish |

## Workflow

Typical plugin lifecycle:

1. **Create** — Use Anthropic's `/plugin-dev:create-plugin` to scaffold
2. **Develop** — Add skills, knowledge, hooks as needed
3. **Reflect** — `/plugin-ops:reflect` to assess quality
4. **Diagnose** — `/plugin-ops:diagnose` to investigate specific issues
5. **Optimize** — `/plugin-ops:optimize` to slim down
6. **Release** — `/plugin-ops:release . 1.0.0` to bump and publish

## Marketplace Support

Manage plugin marketplaces backed by git repositories. Supports:
- **GitHub** — via `gh` CLI
- **GitLab** (cloud and on-prem) — via `glab` CLI or API
- **Any git remote** — manual workflow

Configure marketplaces in `.claude/plugin-ops.local.md` with YAML frontmatter. See `knowledge/configuration.md` for details.

## Complementary to plugin-dev

This plugin handles **operational lifecycle** (audits, optimization, releases, marketplaces). For **plugin creation and development** (scaffolding, skills, hooks, MCP servers), use Anthropic's [`plugin-dev`](https://github.com/anthropics/claude-code/tree/main/plugins/plugin-dev) plugin.

## License

MIT
