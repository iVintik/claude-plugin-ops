#!/usr/bin/env bash
# Guard against editing plugin cache files directly.
# Reads hook input from stdin, checks if file_path is under ~/.claude/plugins/cache/
set -euo pipefail

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path',''))" 2>/dev/null || echo "")

CACHE_DIR="$HOME/.claude/plugins/cache"

if [[ "$FILE_PATH" == "$CACHE_DIR"* ]]; then
  cat <<EOF
STOP: You are editing a plugin cache file.

  Path: $FILE_PATH

Plugin cache (~/.claude/plugins/cache/) is a READ-ONLY installed copy.
Edits here are lost on reinstall and invisible to git.

Instead:
1. Use atlas to find the plugin's source repo: atlas_search_projects(query="<plugin-name>")
2. Edit the source repo
3. After fixing, use /plugin-ops:release to publish
4. Only THEN patch the cache copy if you need immediate effect
EOF
  exit 2
fi
