# Lifecycle Formats

Formats for tracking issues and reflections across any Claude Code plugin.

## ISSUES.md Format

Lives at plugin root. Tracks known issues per plugin.

```markdown
# Plugin Issues

## ISSUE-001: [Title]
- **Status**: open | in-progress | resolved | wont-fix
- **Severity**: critical | major | minor | enhancement
- **Found**: YYYY-MM-DD
- **Resolved**: — (or date)
- **Context**: How the issue was discovered
- **Description**: What is wrong or needs improvement
- **Resolution**: — (or how it was fixed)
- **Notes**:
  - YYYY-MM-DD: Additional observations
```

**Status flow:** `open` → `in-progress` → `resolved` or `wont-fix`

**Severity guide:**
- `critical` — Plugin unusable, skill fails entirely
- `major` — Feature broken but workaround exists
- `minor` — Cosmetic, edge case, or minor inconvenience
- `enhancement` — Not a bug, but an improvement opportunity

**ID assignment:** Sequential per plugin. Never reuse IDs.

## REFLECTIONS.md Format

Lives at plugin root. Newest entries prepended.

```markdown
# Plugin Reflections

## YYYY-MM-DD — [full-analysis | session | optimization | fix]

### Observations
- [What was noticed during analysis]

### What Worked Well
- [Patterns that performed well]

### Improvement Opportunities
- [Actionable suggestions]

### Issues Discovered
- [References to ISSUES.md entries if created]
```

**Entry types:**
- `full-analysis` — Complete audit via `/plugin-ops:reflect`
- `session` — Notes from a working session
- `optimization` — Results of `/plugin-ops:optimize`
- `fix` — Results of `/plugin-ops:fix`

## Non-Regression Protocol

Used by `optimize` and `fix` skills before making changes:

1. Read ISSUES.md — collect ALL resolved issues
2. For each resolved issue, record: ID, title, resolution, files/logic mentioned
3. This is the "protected set" — changes to these files/sections require extra care
4. After changes: re-verify each resolved fix is still intact
5. If any regression detected: revert the specific change, report conflict

## File Size Guidelines

| Component | Budget | Rationale |
|-----------|--------|-----------|
| Single knowledge file | < 10 KB | Loaded into context; large files waste tokens |
| All knowledge combined | < 50 KB | Total context budget for knowledge |
| SKILL.md | < 5 KB | Instructions should be concise |
| plugin.json | < 1 KB | Metadata only |
| ISSUES.md | No limit | Grows over time, read selectively |
| REFLECTIONS.md | No limit | Grows over time, read selectively |
