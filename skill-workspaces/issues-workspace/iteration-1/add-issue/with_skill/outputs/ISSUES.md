# Plugin Issues

<!-- Managed by /plugin-ops:issues — see knowledge/lifecycle-formats.md for format -->

## ISSUE-001: optimize skill crashes with KeyError when plugin has no skills directory
- **Status**: open
- **Severity**: major
- **Found**: 2026-03-08
- **Resolved**: —
- **Context**: Found during audit of plugin-ops plugin
- **Description**: The optimize skill does not handle the case where a plugin has no `skills/` directory. When run against such a plugin, it crashes with a `KeyError` instead of gracefully handling the missing directory and proceeding with the rest of the audit.
- **Resolution**: —
- **Notes**:
