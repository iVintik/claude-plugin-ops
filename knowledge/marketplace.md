# Marketplace

A marketplace is a git repository containing `.claude-plugin/marketplace.json` that catalogs available Claude Code plugins.

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

The file lives at `.claude-plugin/marketplace.json` inside the marketplace repo.

## Multi-Marketplace Support

A plugin can be published to multiple marketplaces. Configure in `.claude/plugin-ops.local.md` (see `knowledge/configuration.md`).

## Provider Support

### GitHub
- Create repos: `gh repo create <name> --public`
- Requires: `gh` CLI authenticated

### GitLab (including on-prem)
- Create repos: `glab project create <name>` or GitLab API
- Requires: `glab` CLI authenticated, or `GITLAB_TOKEN` + API URL
- On-prem: use `--hostname` with glab, or `GITLAB_HOST`

### Generic Git
- Any git remote (Gitea, Bitbucket, self-hosted)
- No marketplace management CLI — manual or API-based

## Automated Releases via CI

### GitHub Actions — Repository Dispatch Pattern

```
Plugin repo (on GitHub release)
  └── marketplace job: fires repository_dispatch with {plugin, version}
        → Marketplace repo (update-plugin.yml) updates marketplace.json
```

**Plugin repo** (`.github/workflows/publish.yml`): On release, read plugin name/version from `plugin.json`, then `gh api repos/<owner>/<marketplace-repo>/dispatches` with `event_type=plugin-release` and `client_payload` containing plugin + version. Requires `MARKETPLACE_TOKEN` secret (fine-grained PAT with Contents: Read+Write on marketplace repo).

**Marketplace repo** (`.github/workflows/update-plugin.yml`): On `repository_dispatch`, use `jq` to update version in `.claude-plugin/marketplace.json`, commit, push.

### GitLab CI — Multi-Project Pipelines

```
Plugin repo (on tag push v*)
  └── trigger keyword fires downstream pipeline on marketplace repo
        → passes PLUGIN_NAME + PLUGIN_VERSION via dotenv
```

Uses `CI_JOB_TOKEN` — no tokens to configure. Marketplace project must grant job token access to plugin repos (Settings → CI/CD → Job token permissions).

**Plugin repo**: `read-metadata` stage extracts name/version to `build.env`, `update-marketplace` stage uses `trigger: project: <group>/<marketplace-repo>`.

**Marketplace repo**: Receives `PLUGIN_NAME`/`PLUGIN_VERSION` variables, updates `.claude-plugin/marketplace.json` with `jq`, commits, pushes.

### Setup Checklist (both providers)

1. Ensure plugin is listed in marketplace (`/plugin-ops:marketplace add`)
2. Copy the appropriate CI workflow template to your plugin repo
3. Set required secrets/permissions (GitHub: `MARKETPLACE_TOKEN`; GitLab: job token access)
4. Ensure marketplace repo has the receiver workflow
5. Test by creating a release/tag

### CI vs Local Release

| Method | When to use |
|--------|------------|
| CI (GitHub/GitLab) | Standard releases — tag triggers auto-update |
| Local (`/plugin-ops:release`) | Quick iteration, or no CI yet. If CI exists, the tag push triggers it automatically |

## Version Sync Rule

The `version` in `marketplace.json` MUST match the plugin's `plugin.json` version. The `release` skill enforces this.

## Versioning Guidelines

| Change Type | Version Bump | Example |
|-------------|-------------|---------|
| New skill or major feature | Minor | 0.1.0 → 0.2.0 |
| Bug fix, knowledge update | Patch | 0.1.0 → 0.1.1 |
| Breaking changes (rename, remove) | Major | 0.x.y → 1.0.0 |
