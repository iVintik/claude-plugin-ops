# Marketplace Init: `my-plugins` — Full Flow

## User Request

> "create a new marketplace repo on github called my-plugins"

## Step 1: Parse Arguments

Subcommand: `init`
Repo name: `my-plugins`
Provider: GitHub (explicit from user request)

## Step 2: Gather Parameters

The skill asks for any missing parameters. Since the user specified provider (GitHub) and name (`my-plugins`), two remain:

- **Visibility**: default to `private` (skill default)
- **Local path**: needs to be determined

**Prompt to user:**

> I'll create a new GitHub marketplace repository called `my-plugins`.
>
> A few details:
> - **Visibility**: private (default). Would you like it public instead?
> - **Local path**: Where should I clone it? Suggested: `~/dev/personal/tools/my-plugins`
>
> Shall I proceed with these defaults?

**Assumed answer**: User accepts defaults.

## Step 3: Create the GitHub Repository

### Command:

```bash
gh repo create my-plugins --private --clone --description "Claude Code plugin marketplace"
```

### Expected output:

```
✓ Created repository iVintik/my-plugins on GitHub
Cloning into 'my-plugins'...
```

### Working directory after clone:

```
~/dev/personal/tools/my-plugins/
```

## Step 4: Initialize marketplace.json

### Command:

```bash
mkdir -p .claude-plugin
```

### Create `.claude-plugin/marketplace.json`:

```json
{
  "name": "my-plugins",
  "metadata": {
    "description": "Claude Code plugin marketplace",
    "version": "1.0.0"
  },
  "plugins": []
}
```

## Step 5: Initial Commit and Push

### Commands:

```bash
cd ~/dev/personal/tools/my-plugins
git add -A
git commit -m "init: marketplace repository"
git push -u origin main
```

### Expected output:

```
[main (root-commit) abc1234] init: marketplace repository
 1 file changed, 8 insertions(+)
 create mode 100644 .claude-plugin/marketplace.json
Enumerating objects: 4, done.
...
To https://github.com/iVintik/my-plugins.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

## Step 6: Update Configuration

### Existing config found at `~/.claude/plugin-ops.local.md`:

```yaml
---
marketplaces:
  - name: ivintik
    local_path: ~/dev/personal/tools/private-claude-marketplace
  - name: datasapience-internal
    local_path: ~/dev/ds/cmo/cmo-ai/tools/internal-claude-plugins
---
```

### Updated config — append new marketplace entry:

```yaml
---
marketplaces:
  - name: ivintik
    local_path: ~/dev/personal/tools/private-claude-marketplace
  - name: datasapience-internal
    local_path: ~/dev/ds/cmo/cmo-ai/tools/internal-claude-plugins
  - name: my-plugins
    local_path: ~/dev/personal/tools/my-plugins
---
```

### Edit applied to `~/.claude/plugin-ops.local.md`.

## Step 7: Confirmation to User

> Marketplace `my-plugins` is ready.
>
> - **Repository**: https://github.com/iVintik/my-plugins (private)
> - **Local path**: `~/dev/personal/tools/my-plugins`
> - **Config**: Added to `~/.claude/plugin-ops.local.md` as marketplace `my-plugins`
>
> You can now add plugins with `/plugin-ops:marketplace add <plugin-path> --store my-plugins`.

---

## Summary of Commands (in order)

| # | Command | Purpose |
|---|---------|---------|
| 1 | `gh repo create my-plugins --private --clone --description "Claude Code plugin marketplace"` | Create repo and clone |
| 2 | `mkdir -p .claude-plugin` | Create plugin directory structure |
| 3 | Write `.claude-plugin/marketplace.json` | Initialize empty marketplace catalog |
| 4 | `git add -A` | Stage all files |
| 5 | `git commit -m "init: marketplace repository"` | Initial commit |
| 6 | `git push -u origin main` | Push to GitHub |
| 7 | Edit `~/.claude/plugin-ops.local.md` | Register marketplace in config |

## Files Created/Modified

| File | Action |
|------|--------|
| `~/dev/personal/tools/my-plugins/.claude-plugin/marketplace.json` | Created |
| `~/.claude/plugin-ops.local.md` | Modified (appended entry) |

## Error Handling Notes

- If `gh repo create` fails (e.g., name taken): report error, suggest alternative name
- If `git push` fails: check remote, suggest `git remote -v` to verify
- If config file missing: offer to create `~/.claude/plugin-ops.local.md` from scratch
- Never expose tokens in output
