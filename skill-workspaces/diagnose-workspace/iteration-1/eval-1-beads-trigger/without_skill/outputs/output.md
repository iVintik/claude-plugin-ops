# Diagnosis: Why "list issues" Does Not Trigger the Beads Skill

## Summary

The beads skill does not trigger on "list issues" because the skill's description in `SKILL.md` focuses on **multi-session persistence, compaction survival, and dependency management** -- none of which match the intent of "list issues." The word "issue" appears only incidentally in the description, and "list" does not appear at all. Claude's skill-matching system uses the `description` field in the SKILL.md frontmatter to decide when to activate a skill, and the current description is too narrow/abstract to match everyday task-management phrases.

## Root Cause Analysis

### 1. Skill Description Does Not Cover Operational Commands

The skill's frontmatter description (`SKILL.md` lines 3-6):

```yaml
description: >
  Git-backed issue tracker for multi-session work with dependencies and persistent
  memory across conversation compaction. Use when work spans sessions, has blockers,
  or needs context recovery after compaction.
```

This description emphasizes:
- "multi-session work"
- "dependencies"
- "persistent memory"
- "conversation compaction"
- "context recovery"

It does **not** mention:
- Listing, searching, or browsing issues
- Creating, updating, or closing issues
- Any day-to-day issue tracker operations
- The words "list," "show," "search," "tasks," "bugs," or "tickets"

### 2. The README Confirms the Narrow Trigger Set

From `README.md` (lines 28-31), the skill self-documents its activation triggers as:

> The skill activates when conversations involve:
> - "multi-session", "complex dependencies", "resume after weeks"
> - "project memory", "persistent context", "side quest tracking"
> - Work that spans multiple days or compaction cycles
> - Tasks too complex for simple TodoWrite lists

"List issues" matches **none** of these trigger patterns.

### 3. Commands Exist But Are Not Skills

The plugin has a rich `commands/` directory with 29 command files including `list.md`, `show.md`, `search.md`, `create.md`, etc. These are **slash commands** (invoked as `/beads:list`, `/beads:show`, etc.), not skills. They require explicit invocation -- they are not auto-triggered by natural language matching.

The distinction is:
- **Skills** (`skills/beads/SKILL.md`): Auto-triggered by Claude when the description matches user intent
- **Commands** (`commands/list.md`): Only triggered when user explicitly types the slash command

### 4. There Is Only One Skill, and It Is High-Level

The entire plugin has exactly **one skill** named "beads" with a single `SKILL.md`. There are no sub-skills for individual operations (list, create, show, etc.). The single skill acts as an entry point for the entire beads system, but its description is tuned for "should I use beads at all?" rather than "the user wants to do something with beads."

## Plugin Structure (for reference)

```
~/.claude/plugins/cache/beads-marketplace/beads/0.56.1/
  .claude-plugin/
    plugin.json          # Plugin manifest with hooks (SessionStart, PreCompact)
  commands/              # 29 slash commands (list.md, create.md, show.md, etc.)
  skills/
    beads/
      SKILL.md           # Single skill definition -- the only trigger surface
      CLAUDE.md          # Maintenance guide
      README.md          # Human documentation
      resources/         # 15 detailed resource files
      adr/               # Architecture Decision Records
  agents/
    task-agent.md        # Agent definition
```

## Why It Works for Some Phrases But Not Others

Phrases that WOULD likely trigger the skill:
- "I need to track work across sessions"
- "Resume my work after compaction"
- "What are my dependencies and blockers?"
- "I need persistent task memory"

Phrases that WOULD NOT trigger the skill:
- "list issues" -- too generic, sounds like any issue tracker
- "show my tasks" -- not specific enough to beads' differentiators
- "create a bug" -- generic issue-tracking language

## Recommendations to Fix

### Option A: Broaden the Skill Description (Recommended)

Update the `description` in `SKILL.md` frontmatter to include operational verbs:

```yaml
description: >
  Git-backed issue tracker. List, create, search, show, update, and close issues
  with dependencies. Persistent memory across conversation compaction. Use for
  listing issues, tracking tasks, managing bugs, or any work that spans sessions.
```

### Option B: Add Trigger Keywords

If the skill system supports a `keywords` or `triggers` field, add:
```yaml
keywords:
  - list issues
  - show issues
  - create issue
  - search issues
  - my tasks
  - open bugs
  - issue tracker
```

### Option C: Use the Slash Command Directly

As a workaround, use `/beads:list` instead of saying "list issues" in natural language. This bypasses skill matching entirely and invokes the command directly.

## Files Examined

| File | Path |
|------|------|
| Plugin manifest | `~/.claude/plugins/cache/beads-marketplace/beads/0.56.1/.claude-plugin/plugin.json` |
| Skill definition | `~/.claude/plugins/cache/beads-marketplace/beads/0.56.1/skills/beads/SKILL.md` |
| Skill README | `~/.claude/plugins/cache/beads-marketplace/beads/0.56.1/skills/beads/README.md` |
| Skill maintenance guide | `~/.claude/plugins/cache/beads-marketplace/beads/0.56.1/skills/beads/CLAUDE.md` |
| List command | `~/.claude/plugins/cache/beads-marketplace/beads/0.56.1/commands/list.md` |
| Plugin config | `~/.claude/plugins/config.json` |
