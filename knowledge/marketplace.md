# Marketplace

A marketplace is a git repository containing a `marketplace.json` file that catalogs available Claude Code plugins. Users point Claude Code at a marketplace repo to discover and install plugins.

## marketplace.json Schema

```json
{
  "name": "my-plugin-store",
  "metadata": {
    "description": "Description of this marketplace",
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "plugin-name",
      "source": {
        "type": "git",
        "url": "https://github.com/user/plugin-name.git"
      },
      "description": "What the plugin does",
      "version": "1.2.0"
    }
  ]
}
```

The `marketplace.json` lives at `.claude-plugin/marketplace.json` inside the marketplace repo.

## Multi-Marketplace Support

A plugin can be published to multiple marketplaces. The user configures their marketplaces in `.claude/plugin-ops.local.md` (see `knowledge/configuration.md`).

## Provider Support

### GitHub
- Create repos: `gh repo create <name> --public`
- Clone: `git clone https://github.com/<owner>/<repo>.git`
- Push: standard git push
- Requires: `gh` CLI authenticated

### GitLab (including on-prem)
- Create repos: `glab project create <name>` or GitLab API
- Clone: `git clone https://gitlab.example.com/<group>/<repo>.git`
- Push: standard git push
- Requires: `glab` CLI authenticated, or `GITLAB_TOKEN` + API URL
- On-prem: use `--hostname` with glab, or configure via `GITLAB_HOST`

### Generic Git
- Any git remote that supports push (Gitea, Bitbucket, self-hosted)
- No marketplace management CLI — manual or API-based

## Version Sync Rule

The `version` in `marketplace.json` MUST match the `version` in the plugin's `plugin.json`. The `release` skill enforces this.

## Versioning Guidelines

| Change Type | Version Bump | Example |
|-------------|-------------|---------|
| New skill or major feature | Minor | 0.1.0 → 0.2.0 |
| Bug fix, knowledge update | Patch | 0.1.0 → 0.1.1 |
| Breaking changes (rename, remove skill) | Major | 0.x.y → 1.0.0 |

For pre-1.0 plugins, minor bumps can include breaking changes.
