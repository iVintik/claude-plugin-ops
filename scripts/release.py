#!/usr/bin/env python3
"""Release script for Claude Code plugins.

Bumps plugin version, commits, pushes, and updates marketplace entries.

Usage:
    python3 release.py <plugin-path> <version> [--dry-run] [--store NAME] [--config PATH]
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
# Config: read ~/.claude/plugin-ops.local.md YAML frontmatter
# ---------------------------------------------------------------------------

def read_config(config_path=None):
    """Read marketplace list from YAML frontmatter in config file.

    Returns list of dicts with 'name' and 'local_path', or empty list.
    """
    if config_path:
        path = expand_path(config_path)
    else:
        path = expand_path("~/.claude/plugin-ops.local.md")

    if not path.is_file():
        return []

    text = path.read_text()
    # Extract YAML frontmatter between --- markers
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return []

    # Minimal YAML parsing for the specific structure we expect
    # (stdlib only — no pyyaml dependency)
    yaml_text = m.group(1)
    return _parse_marketplaces_yaml(yaml_text)


def _parse_marketplaces_yaml(text):
    """Parse the marketplaces list from simple YAML. Handles:
        marketplaces:
          - name: foo
            local_path: ~/some/path
    """
    entries = []
    in_list = False
    current = {}

    for line in text.splitlines():
        stripped = line.strip()

        if stripped == "marketplaces:":
            in_list = True
            continue

        if not in_list:
            continue

        # New list item
        if stripped.startswith("- "):
            if current:
                entries.append(current)
            current = {}
            # The first key-value may be on the same line as the dash
            kv = stripped[2:].strip()
            if ":" in kv:
                k, v = kv.split(":", 1)
                current[k.strip()] = v.strip().strip('"').strip("'")
        elif ":" in stripped and current is not None:
            k, v = stripped.split(":", 1)
            current[k.strip()] = v.strip().strip('"').strip("'")
        elif stripped and not stripped.startswith("#"):
            # End of marketplaces block
            break

    if current:
        entries.append(current)

    return entries

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
# Marketplace operations
# ---------------------------------------------------------------------------

def read_marketplace_json(mp_path):
    mj = mp_path / ".claude-plugin" / "marketplace.json"
    if not mj.is_file():
        return None, mj
    return json.loads(mj.read_text()), mj


def find_plugin_in_marketplace(mp_data, plugin_name):
    """Return (index, entry) or (None, None)."""
    for i, p in enumerate(mp_data.get("plugins", [])):
        if p.get("name") == plugin_name:
            return i, p
    return None, None

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

def release(plugin_path, new_version, dry_run=False, store=None, config_path=None):
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

    # 4. Update plugin.json
    data["version"] = new_version
    if not dry_run:
        write_plugin_json(pj_path, data)
        run(f"git add .claude-plugin/plugin.json", cwd=plugin_path)
        run(f'git commit -m "release: v{new_version}"', cwd=plugin_path)
        run("git push", cwd=plugin_path)
    plugin_pushed = True

    # 5. Find and update marketplaces
    marketplaces_config = read_config(config_path)
    marketplace_results = []

    if not marketplaces_config:
        marketplace_results.append({
            "note": "No marketplaces configured",
        })
    else:
        targets = marketplaces_config
        if store:
            targets = [m for m in targets if m.get("name") == store]
            if not targets:
                die(f"Marketplace '{store}' not found in config")

        for mp_conf in targets:
            mp_name = mp_conf.get("name", "unknown")
            mp_path = expand_path(mp_conf.get("local_path", ""))

            if not mp_path.is_dir():
                marketplace_results.append({
                    "marketplace": mp_name,
                    "error": f"Path not found: {mp_path}",
                })
                continue

            mp_data, mj_path = read_marketplace_json(mp_path)
            if mp_data is None:
                marketplace_results.append({
                    "marketplace": mp_name,
                    "error": "No marketplace.json found",
                })
                continue

            idx, entry = find_plugin_in_marketplace(mp_data, plugin_name)
            if idx is None:
                marketplace_results.append({
                    "marketplace": mp_name,
                    "note": f"Plugin '{plugin_name}' not listed in this marketplace",
                })
                continue

            old_mp_version = entry.get("version", "?")
            if old_mp_version == new_version:
                marketplace_results.append({
                    "marketplace": mp_name,
                    "note": "Already up to date",
                    "version": new_version,
                })
                continue

            # Update marketplace entry
            mp_data["plugins"][idx]["version"] = new_version

            if not dry_run:
                # Pull first to ensure up to date
                pull_result = run("git pull", cwd=mp_path, check=False)

                mj_path.write_text(json.dumps(mp_data, indent=2) + "\n")
                run("git add .claude-plugin/marketplace.json", cwd=mp_path)
                run(
                    f'git commit -m "release: {plugin_name} v{new_version}"',
                    cwd=mp_path,
                )
                run("git push", cwd=mp_path)

            marketplace_results.append({
                "marketplace": mp_name,
                "old_version": old_mp_version,
                "new_version": new_version,
                "updated": True,
            })

    # 6. Output result (before install, which may produce noisy output)
    result = {
        "plugin": plugin_name,
        "old_version": current_version,
        "new_version": new_version,
        "dry_run": dry_run,
        "plugin_pushed": plugin_pushed and not dry_run,
        "marketplaces": marketplace_results,
        "warnings": warnings,
    }

    # 7. Reinstall plugin locally (after printing result)
    if not dry_run:
        # Flush JSON result first so caller always gets it
        print(json.dumps(result, indent=2), flush=True)

        # Install may produce interactive/noisy output — redirect to stderr
        install = subprocess.run(
            f"claude plugin install {plugin_name}",
            shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        # Report install status to stderr only
        if install.returncode == 0:
            print(f"Reinstalled {plugin_name} locally", file=sys.stderr)
        else:
            print(f"Warning: claude plugin install failed (exit {install.returncode})", file=sys.stderr)
    else:
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
    parser.add_argument("--store", help="Target a specific marketplace only")
    parser.add_argument("--config", help="Path to config file")

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
        store=args.store,
        config_path=args.config,
    )


if __name__ == "__main__":
    main()
