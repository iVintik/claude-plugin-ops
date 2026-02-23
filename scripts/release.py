#!/usr/bin/env python3
"""Release script for Claude Code plugins.

Bumps plugin version, commits, pushes, and creates a git tag.
If the plugin repo has CI configured, the tag triggers automated
marketplace updates via downstream pipelines.

Usage:
    python3 release.py <plugin-path> <version> [--dry-run] [--no-tag]
    python3 release.py <plugin-path> --suggest

Exit codes:
    0 = success
    1 = validation error
    2 = git error
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def die(msg, code=1):
    print(json.dumps({"error": msg}))
    sys.exit(code)


def run(cmd, cwd=None, check=True):
    """Run a shell command, return stdout. On failure with check=True, exit 2."""
    result = subprocess.run(
        cmd, shell=True, cwd=cwd,
        capture_output=True, text=True,
    )
    if check and result.returncode != 0:
        stderr = result.stderr.strip() or result.stdout.strip()
        die(f"Command failed: {cmd}\n{stderr}", code=2)
    return result.stdout.strip()


def parse_semver(v):
    """Parse 'X.Y.Z' into (major, minor, patch). Returns None on failure."""
    m = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", v)
    if not m:
        return None
    return tuple(int(x) for x in m.groups())


def semver_gt(a, b):
    return a > b


def expand_path(p):
    return Path(os.path.expanduser(p)).resolve()

# ---------------------------------------------------------------------------
# Plugin operations
# ---------------------------------------------------------------------------

def read_plugin_json(plugin_path):
    pj = plugin_path / ".claude-plugin" / "plugin.json"
    if not pj.is_file():
        die(f"No .claude-plugin/plugin.json found at {plugin_path}")
    return json.loads(pj.read_text()), pj


def write_plugin_json(pj_path, data):
    pj_path.write_text(json.dumps(data, indent=2) + "\n")

# ---------------------------------------------------------------------------
# Suggest mode
# ---------------------------------------------------------------------------

def suggest(plugin_path):
    data, _ = read_plugin_json(plugin_path)
    current = data.get("version", "0.0.0")
    parsed = parse_semver(current)
    if not parsed:
        die(f"Current version '{current}' is not valid semver")

    major, minor, patch = parsed
    result = {
        "current": current,
        "patch": f"{major}.{minor}.{patch + 1}",
        "minor": f"{major}.{minor + 1}.0",
        "major": f"{major + 1}.0.0",
    }
    print(json.dumps(result))
    sys.exit(0)

# ---------------------------------------------------------------------------
# Main release workflow
# ---------------------------------------------------------------------------

def release(plugin_path, new_version, dry_run=False, no_tag=False):
    # 1. Read plugin.json
    data, pj_path = read_plugin_json(plugin_path)
    plugin_name = data.get("name", "unknown")
    current_version = data.get("version", "0.0.0")

    # 2. Validate new version
    new_parsed = parse_semver(new_version)
    if not new_parsed:
        die(f"Invalid semver: {new_version}")

    cur_parsed = parse_semver(current_version)
    if not cur_parsed:
        die(f"Current version '{current_version}' is not valid semver")

    if new_parsed == cur_parsed:
        die(f"Version already at {new_version}")

    if not semver_gt(new_parsed, cur_parsed):
        die(f"New version {new_version} is not greater than current {current_version}")

    # 3. Check working tree
    dirty = run("git status --porcelain", cwd=plugin_path, check=False)
    warnings = []
    if dirty:
        warnings.append("Working tree has uncommitted changes")

    # 4. Update plugin.json, commit, push
    data["version"] = new_version
    if not dry_run:
        write_plugin_json(pj_path, data)
        run(f"git add .claude-plugin/plugin.json", cwd=plugin_path)
        run(f'git commit -m "release: v{new_version}"', cwd=plugin_path)
        run("git push", cwd=plugin_path)

        # Create and push git tag (triggers CI marketplace update)
        if not no_tag:
            run(f'git tag -a v{new_version} -m "release: v{new_version}"', cwd=plugin_path)
            run(f"git push origin v{new_version}", cwd=plugin_path)
    tag_pushed = not dry_run and not no_tag

    # 5. Output result
    result = {
        "plugin": plugin_name,
        "old_version": current_version,
        "new_version": new_version,
        "dry_run": dry_run,
        "plugin_pushed": not dry_run,
        "tag_pushed": tag_pushed,
        "warnings": warnings,
    }

    print(json.dumps(result, indent=2))

    sys.exit(0)

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Release a Claude Code plugin")
    parser.add_argument("plugin_path", help="Path to plugin directory")
    parser.add_argument("version", nargs="?", help="New version (semver)")
    parser.add_argument("--suggest", action="store_true", help="Print version suggestions")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen")
    parser.add_argument("--no-tag", action="store_true", help="Skip git tag creation")

    args = parser.parse_args()
    plugin_path = expand_path(args.plugin_path)

    if not plugin_path.is_dir():
        die(f"Plugin path is not a directory: {plugin_path}")

    if args.suggest:
        suggest(plugin_path)

    if not args.version:
        die("Version argument is required (or use --suggest)")

    release(
        plugin_path=plugin_path,
        new_version=args.version,
        dry_run=args.dry_run,
        no_tag=args.no_tag,
    )


if __name__ == "__main__":
    main()
