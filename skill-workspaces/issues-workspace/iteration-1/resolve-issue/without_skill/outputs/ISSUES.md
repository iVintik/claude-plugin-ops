# Plugin Issues

## ISSUE-001: reflect skill skips hooks directory check
- **Status**: resolved
- **Severity**: major
- **Found**: 2026-03-01
- **Resolved**: 2026-03-08
- **Context**: Discovered during testing
- **Description**: The reflect skill doesn't check if hooks/ dir exists before scanning, causing errors on plugins without hooks.
- **Resolution**: Added a guard to check if hooks/ dir exists before scanning it.
- **Notes**:
