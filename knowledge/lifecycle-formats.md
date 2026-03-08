# Lifecycle Formats

Formats for tracking plugin reflections.

## REFLECTIONS.md Format

Lives at plugin root. Newest entries prepended.

```markdown
# Plugin Reflections

## YYYY-MM-DD — [full-analysis | session | optimization]

### Observations
- [What was noticed during analysis]

### What Worked Well
- [Patterns that performed well]

### Improvement Opportunities
- [Actionable suggestions]
```

**Entry types:**
- `full-analysis` — Complete audit via `/plugin-ops:reflect`
- `session` — Notes from a working session
- `optimization` — Results of `/plugin-ops:optimize`

## File Size Guidelines

| Component | Budget | Rationale |
|-----------|--------|-----------|
| Single knowledge file | < 10 KB | Loaded into context; large files waste tokens |
| All knowledge combined | < 50 KB | Total context budget for knowledge |
| SKILL.md | < 5 KB | Instructions should be concise |
| plugin.json | < 1 KB | Metadata only |
| REFLECTIONS.md | No limit | Grows over time, read selectively |
