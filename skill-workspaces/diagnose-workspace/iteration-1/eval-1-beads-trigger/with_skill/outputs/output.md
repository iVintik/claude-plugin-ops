Plugin Diagnostics: beads v0.56.1

DEFECT-1: skill-description — Skill description lacks trigger phrases for common user intents
  Location: skills/beads/SKILL.md:3-6
  Severity: critical
  Details: The skill description reads: "Git-backed issue tracker for multi-session work with
    dependencies and persistent memory across conversation compaction. Use when work spans
    sessions, has blockers, or needs context recovery after compaction."
    This description is entirely abstract and conceptual. It describes WHAT beads IS, not
    WHEN to trigger it. A user saying "list issues", "show my tasks", "what's on my plate",
    "list bugs", or "show open issues" would not match this description because:
    1. No trigger phrases — the description contains zero examples of user utterances
    2. No action verbs — missing words like "list", "show", "create", "track", "manage"
    3. No proactive triggers — doesn't say when the skill should auto-fire
    4. Focuses on architecture ("git-backed", "compaction survival") rather than user intent
  Fix: Rewrite the description to include trigger phrases and action verbs. Example:
    ```
    description: >
      Issue tracker for managing tasks, bugs, and features. Use when the user says
      "list issues", "show tasks", "create a bug", "what needs to be done",
      "show open issues", "track this work", or any task/issue management request.
      Also trigger proactively when work spans multiple sessions, has blockers,
      or needs context recovery after compaction.
    ```

DEFECT-2: plugin-manifest — No skills or commands declared in plugin.json
  Location: .claude-plugin/plugin.json
  Severity: major
  Details: The plugin.json manifest declares only hooks (SessionStart, PreCompact).
    It does not declare a `skills` or `commands` key. The plugin relies on directory
    convention (`skills/` and `commands/` directories) for discovery. This is valid
    but means Claude's skill matching depends entirely on the SKILL.md frontmatter
    description quality, which is deficient (see DEFECT-1). The `commands/` directory
    contains 29 command files (including `list.md` with description "List issues with
    optional filters"), but these are slash-commands (`/beads:list`), not natural
    language triggers. A user saying "list issues" in natural language would need
    to match via the skill description, not the command description.

DEFECT-3: skill-description — Description excludes core use cases
  Location: skills/beads/SKILL.md:3-6
  Severity: major
  Details: The description's trigger conditions are narrowly scoped to multi-session and
    compaction scenarios: "Use when work spans sessions, has blockers, or needs context
    recovery after compaction." This excludes the most common use case: a user simply
    wanting to list, view, or manage their issues within a single session. A user saying
    "list issues" is not asking about multi-session work or compaction recovery — they
    just want to see their issues.
  Fix: Broaden the description to cover everyday issue management, not just
    multi-session/compaction scenarios.

DEFECT-4: version-mismatch — SKILL.md frontmatter version doesn't match plugin.json
  Location: skills/beads/SKILL.md:8
  Severity: minor
  Details: SKILL.md frontmatter declares `version: "0.47.1"` but plugin.json declares
    `version: "0.56.1"`. This is cosmetic but indicates the skill file hasn't been
    updated with recent releases.
  Fix: Update SKILL.md frontmatter to `version: "0.56.1"`.

Summary: 4 defects found (1 critical, 2 major, 1 minor).

Root cause: The skill description (DEFECT-1) is the primary reason "list issues" does
not trigger the beads skill. The description is written as an architectural overview
rather than a trigger specification. It contains no action verbs matching common user
intents (list, show, create, track) and no example trigger phrases. Claude's skill
matching system uses the description to decide when to invoke the skill, so a
description focused on "git-backed persistent memory" will never match "list issues".

Fix priority:
1. DEFECT-1 (critical): Rewrite skill description with trigger phrases and action verbs
2. DEFECT-3 (major): Broaden description to cover everyday issue management
3. DEFECT-2 (major): Consider adding explicit skill/command declarations to plugin.json
4. DEFECT-4 (minor): Update version in SKILL.md frontmatter

Recommendation: Run `/skill-creator` to iterate on the description with test prompts
like "list issues", "show my tasks", "create a bug", "what work is blocked" to verify
the updated description triggers correctly.

Note: This is a READ-ONLY diagnosis of the installed cache copy at
~/.claude/plugins/cache/beads-marketplace/beads/0.56.1/. To apply fixes, locate and
edit the source repository (https://github.com/steveyegge/beads).
