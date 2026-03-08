# Release Skill Execution — plugin-ops

## Step 1: Parse Arguments

- **Input**: `release plugin-ops`
- **Plugin path resolved**: `/Users/ivintik/dev/personal/tools/claude-plugin-ops/`
- **Version**: not provided — must prompt user
- **Flags**: none (`--dry-run` and `--no-tag` not specified)

## Step 2: Get Version (suggest mode)

**Command executed**:
```bash
python3 /Users/ivintik/dev/personal/tools/claude-plugin-ops/scripts/release.py \
  /Users/ivintik/dev/personal/tools/claude-plugin-ops/ --suggest
```

**Output**:
```json
{"current": "1.8.5", "patch": "1.8.6", "minor": "1.9.0", "major": "2.0.0"}
```

**Prompt presented to user (via AskUserQuestion)**:

> Current version is **1.8.5**. Which version bump?
>
> 1. **Patch** — 1.8.6 (bug fixes)
> 2. **Minor** — 1.9.0 (new features, backward compatible)
> 3. **Major** — 2.0.0 (breaking changes)
> 4. Custom version (enter semver)

**Assumed user selection**: `1.8.6` (patch)

## Step 3: Pre-release State

**Git status** (uncommitted changes detected):
```
 M .claude-plugin/plugin.json
 M CLAUDE.md
 M README.md
 M agents/plugin-auditor.md
 M agents/plugin-optimizer.md
 M knowledge/lifecycle-formats.md
 M skills/diagnose/SKILL.md
 D skills/fix/SKILL.md
 D skills/issues/SKILL.md
 M skills/optimize/SKILL.md
 M skills/reflect/SKILL.md
```

**Recent commits**:
```
ea009ba fix: add mcpServers to agent frontmatter to prevent MCP process explosion
d99f793 release: v1.8.4
cc8f726 release: v1.8.3
9fbffdf release: v1.8.2
21f46c5 feat: add post-release update command and stale MCP detection
```

## Step 4: Execute Release (what WOULD happen)

**Command that would run**:
```bash
python3 /Users/ivintik/dev/personal/tools/claude-plugin-ops/scripts/release.py \
  /Users/ivintik/dev/personal/tools/claude-plugin-ops/ 1.8.6
```

**Dry-run output** (actual dry-run was executed to preview):
```json
{
  "plugin": "plugin-ops",
  "old_version": "1.8.5",
  "new_version": "1.8.6",
  "dry_run": true,
  "plugin_pushed": false,
  "tag_pushed": false,
  "warnings": [
    "Working tree has uncommitted changes — they will be included in the release commit"
  ],
  "update_command": "claude plugin update plugin-ops@ivintik",
  "mcp_pids": []
}
```

**What the release script would do (non-dry-run)**:
1. Update `version` in `.claude-plugin/plugin.json` from `1.8.5` to `1.8.6`
2. `git add -A` — stage all changes (including the 11 modified/deleted files above)
3. `git commit -m "release: v1.8.6"`
4. `git push`
5. `git tag -a v1.8.6 -m "release: v1.8.6"`
6. `git push origin v1.8.6`

## Step 5: Handle Result (what WOULD be presented)

**Success message**:
> Released **plugin-ops** v1.8.6 (was v1.8.5)

**Warning about uncommitted changes**:
> Working tree has uncommitted changes — they will be included in the release commit.

**Update instructions** (shown to user, NOT executed):
> To update your installed copy, run in a terminal:
> ```
> claude plugin update plugin-ops@ivintik
> ```

**Stale MCP processes**: None detected.

**Post-release note**:
> After updating, start a new Claude Code session to load the new version.

## Summary

| Field | Value |
|-------|-------|
| Plugin | plugin-ops |
| Old version | 1.8.5 |
| New version | 1.8.6 |
| Uncommitted changes | 11 files (would be included) |
| Tag | v1.8.6 |
| Update command | `claude plugin update plugin-ops@ivintik` |
| Stale MCP PIDs | none |
| Dry-run only | Yes (no actual changes made) |
