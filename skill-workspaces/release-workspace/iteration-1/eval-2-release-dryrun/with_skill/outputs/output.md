# Release Skill Execution: plugin-ops 2.0.0 --dry-run

## Invocation

```
release plugin-ops 2.0.0 --dry-run
```

## Step 1: Parse Arguments

| Parameter    | Value                                                    |
|-------------|----------------------------------------------------------|
| Plugin path | `/Users/ivintik/dev/personal/tools/claude-plugin-ops/`   |
| Version     | `2.0.0`                                                  |
| Flags       | `--dry-run`                                              |

Version was provided explicitly, so no interactive prompt needed.

## Step 2: Version Suggestion (informational)

Command:
```bash
python3 /Users/ivintik/dev/personal/tools/claude-plugin-ops/scripts/release.py \
  /Users/ivintik/dev/personal/tools/claude-plugin-ops/ --suggest
```

Output:
```json
{"current": "1.8.5", "patch": "1.8.6", "minor": "1.9.0", "major": "2.0.0"}
```

The requested version `2.0.0` matches the suggested major bump.

## Step 3: Execute Release (dry-run)

Command:
```bash
python3 /Users/ivintik/dev/personal/tools/claude-plugin-ops/scripts/release.py \
  /Users/ivintik/dev/personal/tools/claude-plugin-ops/ 2.0.0 --dry-run
```

Exit code: **0** (success)

Output:
```json
{
  "plugin": "plugin-ops",
  "old_version": "1.8.5",
  "new_version": "2.0.0",
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

## Step 4: Handle Result

**Status:** Success (exit 0), dry-run mode.

**Summary:** Would release **plugin-ops** v2.0.0 (currently v1.8.5).

**What would happen without --dry-run:**
1. `plugin.json` version bumped from `1.8.5` to `2.0.0`
2. All changes committed with message `release: v2.0.0`
3. Changes pushed to remote
4. Git tag `v2.0.0` created and pushed (triggers CI)

**Warnings:**
- Working tree has uncommitted changes -- they would be included in the release commit.

**Post-release (if this were real):**
- Update command: `claude plugin update plugin-ops@ivintik`
- No stale MCP processes detected.
- After updating, start a new Claude Code session to load the new version.
