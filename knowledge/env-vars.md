# Environment Variables for Plugin Developers

How secrets and configuration flow through Claude Code plugins.

## Where to Define Secrets

Put secrets in your shell profile (`~/.zshrc` or `~/.bashrc`):

```bash
export MY_API_KEY="sk-..."
export MY_SERVICE_TOKEN="token-..."
```

This ensures they're available in all terminal sessions, including Claude Code.

**Never commit `.env` files.** If you use `.env`, load them via `direnv` or source from your profile.

## How Plugin Components Access Env Vars

### MCP Servers

MCP servers inherit the environment of the Claude Code process. No special wiring needed — `process.env.MY_API_KEY` (Node) or `os.environ["MY_API_KEY"]` (Python) just works.

To pass specific vars or override values, use the `env` field in plugin.json:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["server.js"],
      "env": {
        "MY_API_KEY": "${MY_API_KEY}",
        "CUSTOM_VAR": "hardcoded-value"
      }
    }
  }
}
```

The `${VAR}` syntax expands from the parent process environment at launch time.

### Hooks

Hooks run as shell commands and inherit the full Claude Code process environment. No extra configuration needed.

### Skills

Skills are markdown — they don't execute directly. When a skill instructs Claude to run a Bash command, that command inherits the session environment.

## Remote / Headless Sessions (Codeman)

For CI or remote sessions where there's no interactive shell profile:

1. **Launch environment** — set vars before starting: `MY_API_KEY=sk-... claude-code`
2. **direnv** — place `.envrc` in the project root with `export MY_API_KEY=...`
3. **CI secrets** — inject via your CI platform's secret management (GitHub Actions secrets, GitLab CI variables, etc.)

## Troubleshooting

- **Var not visible in MCP server?** — Restart Claude Code after adding to shell profile. MCP servers only see the env from when Claude Code launched.
- **Var works in terminal but not in Claude Code?** — Check that you exported it (not just `VAR=value` but `export VAR=value`).
- **Different value in MCP server?** — Check if plugin.json `env` field overrides it.
