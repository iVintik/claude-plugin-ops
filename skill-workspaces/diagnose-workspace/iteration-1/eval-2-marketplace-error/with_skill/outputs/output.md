# Plugin Diagnostics: plugin-ops v1.8.5

## DEFECT-1: Skill — Ambiguous marketplace.json path reference

  Location: `skills/marketplace/SKILL.md:44`
  Severity: **major**
  Details: The `list` subcommand instructs the agent to "Read `marketplace.json` from local clone" but does not specify the full path `.claude-plugin/marketplace.json`. The knowledge file (`knowledge/marketplace.md:27`) clearly states the file lives at `.claude-plugin/marketplace.json` inside the marketplace repo. When the agent follows the skill literally, it may attempt to read `marketplace.json` at the repo root, which does not exist, causing a file-not-found error. The same ambiguity affects `add` and `remove` subcommands which also reference `marketplace.json` without the `.claude-plugin/` prefix.
  Fix: Change all references to `marketplace.json` in the skill body to explicitly say `.claude-plugin/marketplace.json`. For example, line 44 should read: "Read `.claude-plugin/marketplace.json` from local clone, display:"

## DEFECT-2: Skill — Inconsistent config file search order

  Location: `skills/marketplace/SKILL.md:23`
  Severity: **minor**
  Details: The skill says "Look for `.claude/plugin-ops.local.md` in cwd then home dir" but the knowledge file `knowledge/configuration.md:7-8` says the config lives "in the user's home directory or project root." The search order is reversed -- knowledge says home-first, skill says cwd-first. This inconsistency can lead to unpredictable behavior when a user has config files in both locations.
  Fix: Align the search order. Recommended: "Look for `.claude/plugin-ops.local.md` in home dir (`~/.claude/plugin-ops.local.md`) then project root." Update either the skill or the knowledge file to match.

## DEFECT-3: Skill — Missing knowledge file path context

  Location: `skills/marketplace/SKILL.md:23`
  Severity: **minor**
  Details: The skill instructs the agent to "Read `knowledge/configuration.md` for config format" using a relative path. When the skill is loaded by Claude Code, the agent needs to resolve this relative to the plugin root (`${CLAUDE_PLUGIN_ROOT}`). However, the skill provides no anchor for path resolution. If the agent's working directory differs from the plugin root (which it almost always does -- the user is in their own project), the read will fail silently or error out. The same issue applies to the `init` subcommand's reference to `knowledge/marketplace.md`.
  Fix: Use an explicit path anchor: "Read `${CLAUDE_PLUGIN_ROOT}/knowledge/configuration.md` for config format" or "Read the plugin-ops knowledge file `knowledge/configuration.md`" with a note that paths are relative to the plugin root.

## DEFECT-4: Skill — No error guidance for missing git remote

  Location: `skills/marketplace/SKILL.md:54-55`
  Severity: **minor**
  Details: The `add` subcommand step 2 says "Get plugin's git remote URL" but provides no guidance for the case where the plugin directory has no git remote configured (e.g., a newly created plugin not yet pushed). The agent would encounter a git error with no recovery path specified in the skill.
  Fix: Add error handling guidance: "Get plugin's git remote URL. If no remote is configured, prompt the user to set one up first (`git remote add origin <url>`)."

## Summary

4 defects found. **Root cause: the marketplace skill's instructions are ambiguous about file paths**, both for the `marketplace.json` location within marketplace repos (DEFECT-1, most likely to cause the "errors out" behavior) and for knowledge file references (DEFECT-3). The agent executing the skill will attempt to read files at incorrect paths, producing file-not-found errors.

**Fix priority:**
1. DEFECT-1 (major) -- Specify `.claude-plugin/marketplace.json` explicitly in all subcommands
2. DEFECT-3 (minor) -- Anchor knowledge file paths to `${CLAUDE_PLUGIN_ROOT}`
3. DEFECT-2 (minor) -- Align config search order between skill and knowledge
4. DEFECT-4 (minor) -- Add missing git remote error handling
