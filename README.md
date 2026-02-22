# plugin-ops

Plugin lifecycle management for Claude Code. Track issues, audit health, optimize, fix, release, and manage marketplaces.

## Installation

```bash
git clone https://github.com/iVintik/claude-plugin-ops.git
```

Then add to your Claude Code plugins.

## Skills

| Skill | Usage | Purpose |
|-------|-------|---------|
| `/plugin-ops:issues` | `/plugin-ops:issues [path] [--add\|--resolve\|--list\|--init]` | Manage plugin issue tracking |
| `/plugin-ops:reflect` | `/plugin-ops:reflect [path] [--brief]` | Analyze plugin health |
| `/plugin-ops:optimize` | `/plugin-ops:optimize [path] [--dry-run] [--target ...]` | Optimize with non-regression |
| `/plugin-ops:fix` | `/plugin-ops:fix [path] [--issue ISSUE-NNN\|--all-open]` | Fix issues with non-regression |
| `/plugin-ops:marketplace` | `/plugin-ops:marketplace init\|list\|add\|remove` | Manage plugin marketplaces |
| `/plugin-ops:release` | `/plugin-ops:release [path] <version> [--store name]` | Version bump + publish |

## Workflow

Typical plugin lifecycle:

1. **Create** — Use Anthropic's `/plugin-dev:create-plugin` to scaffold
2. **Develop** — Add skills, knowledge, hooks as needed
3. **Reflect** — `/plugin-ops:reflect` to assess quality
4. **Track** — `/plugin-ops:issues --add` to log issues found
5. **Fix** — `/plugin-ops:fix --issue ISSUE-001` to resolve with safety checks
6. **Optimize** — `/plugin-ops:optimize` to slim down
7. **Release** — `/plugin-ops:release . 1.0.0` to bump and publish

## Non-Regression Guarantees

The optimize and fix skills automatically:
- Read all resolved issues from ISSUES.md before making changes
- Check each proposed change against resolved issue resolutions
- Skip changes that would affect previously fixed code
- Verify all resolved fixes remain intact after changes

## Marketplace Support

Manage plugin marketplaces backed by git repositories. Supports:
- **GitHub** — via `gh` CLI
- **GitLab** (cloud and on-prem) — via `glab` CLI or API
- **Any git remote** — manual workflow

Configure marketplaces in `.claude/plugin-ops.local.md` with YAML frontmatter. See `knowledge/configuration.md` for details.

## Complementary to plugin-dev

This plugin handles **operational lifecycle** (issues, audits, releases, marketplaces). For **plugin creation and development** (scaffolding, skills, hooks, MCP servers), use Anthropic's [`plugin-dev`](https://github.com/anthropics/claude-code/tree/main/plugins/plugin-dev) plugin.

## License

MIT
