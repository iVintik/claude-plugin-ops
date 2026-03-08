# Creating a "my-plugins" GitHub Repo as a Claude Code Plugin Marketplace

## Overview

The goal is to create a GitHub repository that serves as a centralized marketplace for discovering, sharing, and installing Claude Code plugins (also known as skills or slash commands). Below is a complete breakdown of the steps required.

---

## Step 1: Create the GitHub Repository

```bash
gh repo create my-plugins --public --description "A marketplace for Claude Code plugins" --clone
cd my-plugins
```

Key decisions:
- **Public** visibility so the community can discover and contribute plugins.
- Choose a license (MIT or Apache 2.0 are common for plugin ecosystems).

---

## Step 2: Define the Repository Structure

A marketplace repo needs a clear, scalable directory layout:

```
my-plugins/
├── README.md                  # Marketplace overview, how to browse/install/contribute
├── LICENSE
├── CONTRIBUTING.md            # Guidelines for submitting plugins
├── plugins/                   # One subdirectory per plugin
│   ├── example-plugin/
│   │   ├── plugin.json        # Metadata: name, version, description, author, tags
│   │   ├── README.md          # Plugin-specific docs and usage
│   │   └── src/               # Plugin source files (skill definitions, etc.)
│   └── another-plugin/
│       ├── plugin.json
│       ├── README.md
│       └── src/
├── schema/
│   └── plugin-schema.json     # JSON Schema for validating plugin.json files
├── scripts/
│   ├── validate.sh            # CI script to validate all plugin.json files
│   └── generate-index.sh      # Generates a searchable index/catalog
├── index.json                 # Auto-generated catalog of all plugins
└── .github/
    ├── ISSUE_TEMPLATE/
    │   └── new-plugin.md      # Template for plugin submission issues
    ├── PULL_REQUEST_TEMPLATE.md
    └── workflows/
        ├── validate.yml       # CI: validate plugin metadata on PRs
        └── publish-index.yml  # CI: regenerate index.json on merge to main
```

---

## Step 3: Define the Plugin Metadata Schema

Create `schema/plugin-schema.json` to enforce a consistent format for every plugin's `plugin.json`:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["name", "version", "description", "author", "entrypoint"],
  "properties": {
    "name": { "type": "string", "pattern": "^[a-z0-9-]+$" },
    "version": { "type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$" },
    "description": { "type": "string", "maxLength": 200 },
    "author": { "type": "string" },
    "license": { "type": "string" },
    "tags": { "type": "array", "items": { "type": "string" } },
    "entrypoint": { "type": "string" },
    "dependencies": { "type": "array", "items": { "type": "string" } },
    "claude_code_version": { "type": "string" },
    "homepage": { "type": "string", "format": "uri" },
    "repository": { "type": "string", "format": "uri" }
  }
}
```

Each plugin would then have a `plugin.json` like:

```json
{
  "name": "commit-helper",
  "version": "1.0.0",
  "description": "Smart commit message generator with conventional commits support",
  "author": "username",
  "license": "MIT",
  "tags": ["git", "commit", "productivity"],
  "entrypoint": "src/skill.md",
  "claude_code_version": ">=1.0.0"
}
```

---

## Step 4: Write the README

The top-level `README.md` should include:

1. **What this is** -- a curated marketplace of Claude Code plugins.
2. **Browsing plugins** -- link to `index.json` or a rendered catalog.
3. **Installing a plugin** -- instructions for how users install a plugin into their Claude Code environment (e.g., cloning, copying skill files, or referencing via a plugin manager).
4. **Contributing a plugin** -- link to `CONTRIBUTING.md`.
5. **Plugin quality standards** -- what is expected (docs, tests, schema compliance).

---

## Step 5: Write Contribution Guidelines

`CONTRIBUTING.md` should cover:

1. Fork the repo and create a branch.
2. Add a new directory under `plugins/` with the plugin name.
3. Include a valid `plugin.json` matching the schema.
4. Include a `README.md` with usage instructions.
5. Submit a pull request using the provided PR template.
6. CI will validate the metadata; a maintainer will review.

---

## Step 6: Set Up CI/CD with GitHub Actions

### Validation Workflow (`.github/workflows/validate.yml`)

Triggered on pull requests. It should:
- Find all `plugin.json` files in `plugins/`.
- Validate each against `schema/plugin-schema.json` (using a tool like `ajv-cli` or `check-jsonschema`).
- Ensure each plugin directory has a `README.md`.
- Ensure no duplicate plugin names exist.

### Index Generation Workflow (`.github/workflows/publish-index.yml`)

Triggered on push to `main`. It should:
- Aggregate all `plugin.json` files into a single `index.json`.
- Commit and push the updated `index.json` (or publish it as a GitHub Pages artifact).

---

## Step 7: Set Up GitHub Pages (Optional)

For a browsable web catalog:
- Enable GitHub Pages on the repo (from `main` branch or a `docs/` folder).
- Create a simple static site (even a single HTML page) that reads `index.json` and renders a searchable list of plugins.
- This gives users a web UI to discover plugins without cloning the repo.

---

## Step 8: Seed with Example Plugins

Include 1-2 example plugins to demonstrate the expected structure:
- A simple "hello-world" skill that shows the minimal viable plugin.
- A more complete example that demonstrates tags, dependencies, and advanced features.

---

## Step 9: Configure Repository Settings

Via `gh` CLI or the GitHub web UI:
- **Branch protection** on `main`: require PR reviews, require CI to pass.
- **Issue templates**: for bug reports, feature requests, and new plugin submissions.
- **Topics/tags**: add `claude-code`, `plugins`, `marketplace`, `ai-tools` to the repo for discoverability.
- **About section**: set the repo description and website URL (if using Pages).

```bash
gh repo edit my-plugins --description "A marketplace for Claude Code plugins" \
  --add-topic claude-code --add-topic plugins --add-topic marketplace
```

---

## Step 10: Announce and Iterate

- Share the repo URL with potential contributors.
- Consider adding a plugin installation CLI tool or script that automates downloading and placing plugin files into the user's Claude Code configuration directory.
- Over time, add features like plugin ratings, download counts (via GitHub API), and versioned releases.

---

## Summary of Commands (Not Executed)

| Step | Command / Action |
|------|-----------------|
| Create repo | `gh repo create my-plugins --public --clone` |
| Init structure | `mkdir -p plugins schema scripts .github/workflows .github/ISSUE_TEMPLATE` |
| Add schema | Write `schema/plugin-schema.json` |
| Add CI | Write `.github/workflows/validate.yml` and `publish-index.yml` |
| Add docs | Write `README.md`, `CONTRIBUTING.md`, `LICENSE` |
| Add examples | Create example plugin directories under `plugins/` |
| Configure repo | `gh repo edit` to add topics, enable branch protection |
| Enable Pages | Configure GitHub Pages for a web-based catalog |

None of these steps were actually executed -- this document describes the complete process for reference.
