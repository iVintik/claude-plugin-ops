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

## Automated Releases via CI

Plugins can automate releases using GitHub Actions with a **repository dispatch** pattern. Instead of duplicating marketplace update logic in every plugin repo, the marketplace repo owns a single workflow that receives dispatch events.

### Architecture

```
Plugin repo (on GitHub release)
  ├── npm job: publishes to public npm registry (for OpenClaw)
  └── marketplace job: fires repository_dispatch with {plugin, version}
                            │
                            ▼
Marketplace repo (update-plugin.yml workflow)
  └── Receives dispatch → updates marketplace.json → commits → pushes
```

### Plugin Repo Workflow (`.github/workflows/publish.yml`)

```yaml
name: Publish
on:
  release:
    types: [published]

jobs:
  npm:
    name: Publish to npm
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          registry-url: https://registry.npmjs.org
      - run: npm publish --provenance --access public
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}

  marketplace:
    name: Update Claude marketplace
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Read plugin metadata
        id: meta
        run: |
          echo "name=$(jq -r .name .claude-plugin/plugin.json)" >> "$GITHUB_OUTPUT"
          echo "version=$(jq -r .version .claude-plugin/plugin.json)" >> "$GITHUB_OUTPUT"
      - name: Dispatch marketplace update
        run: |
          gh api repos/<owner>/<marketplace-repo>/dispatches \
            -f event_type=plugin-release \
            -f 'client_payload[plugin]=${{ steps.meta.outputs.name }}' \
            -f 'client_payload[version]=${{ steps.meta.outputs.version }}'
        env:
          GH_TOKEN: ${{ secrets.MARKETPLACE_TOKEN }}
```

### Marketplace Repo Workflow (`.github/workflows/update-plugin.yml`)

```yaml
name: Update plugin version
on:
  repository_dispatch:
    types: [plugin-release]

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Update marketplace.json
        run: |
          jq --arg name "${{ github.event.client_payload.plugin }}" \
             --arg ver "${{ github.event.client_payload.version }}" \
             '(.plugins[] | select(.name == $name)).version = $ver' \
             .claude-plugin/marketplace.json > tmp.json
          mv tmp.json .claude-plugin/marketplace.json
      - name: Commit and push
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add .claude-plugin/marketplace.json
          if git diff --cached --quiet; then
            echo "No changes"
          else
            git commit -m "release: ${{ github.event.client_payload.plugin }} v${{ github.event.client_payload.version }}"
            git push
          fi
```

### Setting Up a New Plugin for CI Release

1. **Ensure plugin is listed in marketplace** — use `/plugin-ops:marketplace add` first
2. **Add `package.json`** for npm publishing (with `license`, `repository`, `files` fields)
3. **Add `openclaw.plugin.json`** if the plugin also targets OpenClaw
4. **Copy the publish workflow** above to `.github/workflows/publish.yml`
5. **Set secrets** on the plugin repo:
   ```bash
   gh secret set NPM_TOKEN --repo <org>/<repo>
   gh secret set MARKETPLACE_TOKEN --repo <org>/<repo>
   ```
6. **Ensure marketplace has the dispatch workflow** — copy `update-plugin.yml` above
7. **Test**: create a GitHub release → both npm and marketplace should update

### Required Secrets

| Secret | Purpose | How to create |
|--------|---------|---------------|
| `NPM_TOKEN` | Publish to npm | https://www.npmjs.com/settings/tokens → **Automation** type |
| `MARKETPLACE_TOKEN` | Dispatch to marketplace repo | GitHub fine-grained PAT with **Contents: Read and write** on the marketplace repo |

### Token Renewal

**NPM_TOKEN** (npm Automation token):
- No expiration by default — regenerate only if compromised
- Create at https://www.npmjs.com/settings/tokens/create, type **Automation**
- Update secret: `gh secret set NPM_TOKEN --repo <org>/<repo>`

**MARKETPLACE_TOKEN** (GitHub fine-grained PAT):
- Expires after the duration you set (max 1 year) — **set a calendar reminder**
- Create at https://github.com/settings/tokens?type=beta
- Scope: **Only select repositories** → marketplace repo, **Contents: Read and write**
- The same PAT works across all plugin repos
- When expired, regenerate and update on all repos:
  ```bash
  gh secret set MARKETPLACE_TOKEN --repo <org>/<plugin-1>
  gh secret set MARKETPLACE_TOKEN --repo <org>/<plugin-2>
  ```

### GitLab CI

For GitLab-hosted plugins (including on-prem GitLab), use **multi-project pipelines** with the `trigger` keyword. The plugin repo triggers a downstream pipeline on the marketplace repo using GitLab's built-in `CI_JOB_TOKEN` — no tokens or CI/CD variables to configure.

#### Architecture

```
Plugin repo (on tag push v*)
  └── read-metadata job: extracts plugin name + version from tag
  └── update-marketplace job: triggers downstream pipeline via `trigger` keyword
                            │  (passes PLUGIN_NAME + PLUGIN_VERSION via dotenv)
                            ▼
Marketplace repo (triggered pipeline)
  └── Receives variables → updates marketplace.json → commits → pushes (CI_JOB_TOKEN)
```

#### Prerequisites

The marketplace project must allow job tokens from plugin repos:
- Marketplace project → Settings → CI/CD → **Job token permissions** → add plugin repos (or their parent group)

#### Plugin Repo Pipeline (`.gitlab-ci.yml`)

```yaml
stages:
  - prepare
  - release

read-metadata:
  stage: prepare
  image: alpine:latest
  rules:
    - if: '$CI_COMMIT_TAG =~ /^v\d+\.\d+\.\d+$/'
  before_script:
    - apk add --no-cache jq
  script:
    - echo "PLUGIN_NAME=$(jq -r .name .claude-plugin/plugin.json)" >> build.env
    - echo "PLUGIN_VERSION=${CI_COMMIT_TAG#v}" >> build.env
  artifacts:
    reports:
      dotenv: build.env

update-marketplace:
  stage: release
  needs: [read-metadata]
  rules:
    - if: '$CI_COMMIT_TAG =~ /^v\d+\.\d+\.\d+$/'
  trigger:
    project: <group>/<marketplace-repo>
    branch: <default-branch>
    forward:
      pipeline_variables: true
```

#### Marketplace Repo Pipeline (`.gitlab-ci.yml`)

```yaml
stages:
  - update

update-plugin-version:
  stage: update
  image: alpine:latest
  rules:
    - if: '$PLUGIN_NAME && $PLUGIN_VERSION'
  before_script:
    - apk add --no-cache git jq
  script:
    - |
      jq --arg name "$PLUGIN_NAME" \
         --arg ver "$PLUGIN_VERSION" \
         '(.plugins[] | select(.name == $name)).version = $ver' \
         .claude-plugin/marketplace.json > tmp.json
      mv tmp.json .claude-plugin/marketplace.json
      git config user.name "gitlab-ci[bot]"
      git config user.email "ci@your-gitlab-host.com"
      git add .claude-plugin/marketplace.json
      if git diff --cached --quiet; then
        echo "No changes needed"
      else
        git commit -m "release: ${PLUGIN_NAME} v${PLUGIN_VERSION}"
        git push "https://gitlab-ci-token:${CI_JOB_TOKEN}@your-gitlab-host.com/${CI_PROJECT_PATH}.git" HEAD:develop
      fi
```

#### Setting Up a New Plugin for GitLab CI Release

1. **Ensure plugin is listed in marketplace** — use `/plugin-ops:marketplace add` first
2. **Grant job token access** — marketplace project → Settings → CI/CD → Job token permissions → add the plugin repo (or its parent group for all repos at once)
3. **Copy `.gitlab-ci.yml`** template above to the plugin repo (update `project` and `branch` in the `trigger` block)
4. **Ensure marketplace repo has its `.gitlab-ci.yml`** with the `update-plugin-version` job
5. **Test**: push a semver tag (`git tag -a v1.0.0 -m "release: v1.0.0" && git push origin v1.0.0`) → marketplace should update

No CI/CD variables or tokens needed on any repo.

### CI vs Local Release

| Method | When to use |
|--------|------------|
| CI (GitHub Actions) | Standard releases for GitHub-hosted plugins — create a GitHub release, auto-publishes to npm + marketplace |
| CI (GitLab) | Standard releases for GitLab-hosted plugins — push a tag, auto-updates marketplace |
| Local (`/plugin-ops:release`) | Quick iteration, or when CI isn't set up yet. If CI is configured, the tag push triggers CI automatically — marketplace update is then redundant (but harmless) |

Both methods keep `plugin.json` version and `marketplace.json` version in sync.

## Version Sync Rule

The `version` in `marketplace.json` MUST match the `version` in the plugin's `plugin.json`. The `release` skill enforces this.

## Versioning Guidelines

| Change Type | Version Bump | Example |
|-------------|-------------|---------|
| New skill or major feature | Minor | 0.1.0 → 0.2.0 |
| Bug fix, knowledge update | Patch | 0.1.0 → 0.1.1 |
| Breaking changes (rename, remove skill) | Major | 0.x.y → 1.0.0 |

For pre-1.0 plugins, minor bumps can include breaking changes.
