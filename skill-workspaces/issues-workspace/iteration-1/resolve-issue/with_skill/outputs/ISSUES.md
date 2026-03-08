# Plugin Issues

## ISSUE-001: reflect skill skips hooks directory check
- **Status**: resolved
- **Severity**: major
- **Found**: 2026-03-01
- **Resolved**: 2026-03-08
- **Context**: Discovered during testing
- **Description**: The reflect skill doesn't check if hooks/ dir exists before scanning, causing errors on plugins without hooks.
- **Resolution**: Added a guard in the reflect skill to check whether the hooks/ directory exists before attempting to scan it. The skill now skips the hooks scan gracefully when the directory is absent.
- **Notes**:
