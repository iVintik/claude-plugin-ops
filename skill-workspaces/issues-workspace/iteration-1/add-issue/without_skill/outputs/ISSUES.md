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

## ISSUE-002: optimize skill crashes with KeyError on plugins with no skills directory
- **Status**: open
- **Severity**: major
- **Found**: 2026-03-08
- **Resolved**:
- **Context**: Discovered during audit
- **Description**: The optimize skill crashes with a KeyError when run against a plugin that has no skills/ directory. The skill attempts to access skills-related data without first checking whether the directory exists, causing an unhandled exception.
- **Resolution**:
- **Notes**:
