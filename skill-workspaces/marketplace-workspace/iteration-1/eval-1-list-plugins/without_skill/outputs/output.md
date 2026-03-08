# Claude Code Plugin Marketplace - Complete Plugin Listing

## What is the Claude Code Plugin Marketplace?

The Claude Code plugin marketplace is a distribution system for Claude Code extensions. It works similarly to package registries: **marketplaces** are repositories (Git/GitHub) that contain a `marketplace.json` manifest listing available plugins, and users can install plugins from any marketplace they have configured.

Key CLI commands:
- `claude plugin marketplace list` -- list configured marketplaces
- `claude plugin marketplace add <source>` -- add a marketplace
- `claude plugin install <plugin>@<marketplace>` -- install a plugin
- `claude plugin list` -- list installed plugins

Configuration is stored under `~/.claude/plugins/`:
- `known_marketplaces.json` -- registry of configured marketplaces
- `installed_plugins.json` -- record of installed plugins
- `marketplaces/<name>/` -- cloned marketplace repos with manifests
- `cache/<marketplace>/<plugin>/<version>/` -- installed plugin files
- `blocklist.json` -- centrally blocked plugins

---

## Configured Marketplaces (4)

| # | Marketplace | Source | Last Updated |
|---|-------------|--------|--------------|
| 1 | **claude-plugins-official** | github: `anthropics/claude-plugins-official` | 2026-03-08 |
| 2 | **datasapience-internal** | git: `https://git.angara.cloud/mm-product/ai/tools/internal-claude-plugins.git` | 2026-03-08 |
| 3 | **ivintik** | github: `iVintik/private-claude-marketplace` | 2026-03-08 |
| 4 | **beads-marketplace** | github: `steveyegge/beads` | 2026-02-23 |

---

## All Available Plugins by Marketplace

### 1. claude-plugins-official (Anthropic) -- 42 plugins

#### First-Party Plugins (Anthropic)

| # | Plugin | Category | Description |
|---|--------|----------|-------------|
| 1 | typescript-lsp | development | TypeScript/JavaScript language server for enhanced code intelligence |
| 2 | pyright-lsp | development | Python language server (Pyright) for type checking and code intelligence |
| 3 | gopls-lsp | development | Go language server for code intelligence and refactoring |
| 4 | rust-analyzer-lsp | development | Rust language server for code intelligence and analysis |
| 5 | clangd-lsp | development | C/C++ language server (clangd) for code intelligence |
| 6 | php-lsp | development | PHP language server (Intelephense) for code intelligence |
| 7 | swift-lsp | development | Swift language server (SourceKit-LSP) for code intelligence |
| 8 | kotlin-lsp | development | Kotlin language server for code intelligence |
| 9 | csharp-lsp | development | C# language server for code intelligence |
| 10 | jdtls-lsp | development | Java language server (Eclipse JDT.LS) for code intelligence |
| 11 | lua-lsp | development | Lua language server for code intelligence |
| 12 | agent-sdk-dev | development | Development kit for working with the Claude Agent SDK |
| 13 | pr-review-toolkit | productivity | Comprehensive PR review agents specializing in comments, tests, error handling, type design, code quality, and code simplification |
| 14 | commit-commands | productivity | Commands for git commit workflows including commit, push, and PR creation |
| 15 | feature-dev | development | Comprehensive feature development workflow with specialized agents |
| 16 | security-guidance | security | Security reminder hook that warns about potential security issues when editing files |
| 17 | code-review | productivity | Automated code review for pull requests using multiple specialized agents with confidence-based scoring |
| 18 | code-simplifier | productivity | Agent that simplifies and refines code for clarity, consistency, and maintainability |
| 19 | explanatory-output-style | learning | Adds educational insights about implementation choices and codebase patterns |
| 20 | learning-output-style | learning | Interactive learning mode that requests meaningful code contributions at decision points |
| 21 | frontend-design | development | Create distinctive, production-grade frontend interfaces with high design quality |
| 22 | playground | development | Creates interactive HTML playgrounds -- self-contained single-file explorers with visual controls |
| 23 | ralph-loop | development | Interactive self-referential AI loops for iterative development (Ralph Wiggum technique) |
| 24 | hookify | productivity | Easily create custom hooks to prevent unwanted behaviors by analyzing conversation patterns |
| 25 | plugin-dev | development | Comprehensive toolkit for developing Claude Code plugins (hooks, MCP, commands, agents) |
| 26 | claude-code-setup | productivity | Analyze codebases and recommend tailored Claude Code automations |
| 27 | claude-md-management | productivity | Tools to maintain and improve CLAUDE.md files -- audit quality, capture session learnings |
| 28 | skill-creator | development | Create new skills, improve existing skills, and measure skill performance with evals |

#### Third-Party / External Plugins (in official marketplace)

| # | Plugin | Category | Description |
|---|--------|----------|-------------|
| 29 | greptile | development | AI-powered codebase search and understanding |
| 30 | serena | development | Semantic code analysis MCP server (community-managed) |
| 31 | playwright | testing | Browser automation and end-to-end testing MCP server by Microsoft |
| 32 | github | productivity | Official GitHub MCP server for repository management |
| 33 | supabase | database | Supabase MCP integration for database operations |
| 34 | atlassian | productivity | Connect to Jira and Confluence |
| 35 | laravel-boost | development | Laravel development toolkit MCP server |
| 36 | figma | design | Figma design platform integration |
| 37 | asana | productivity | Asana project management integration |
| 38 | linear | productivity | Linear issue tracking integration |
| 39 | Notion | productivity | Notion workspace integration |
| 40 | gitlab | productivity | GitLab DevOps platform integration |
| 41 | sentry | monitoring | Sentry error monitoring integration |
| 42 | slack | productivity | Slack workspace integration |
| 43 | vercel | deployment | Vercel deployment platform integration |
| 44 | stripe | development | Stripe development plugin |
| 45 | firebase | database | Google Firebase MCP integration |
| 46 | context7 | development | Up-to-date documentation lookup (community-managed) |
| 47 | pinecone | database | Pinecone vector database integration |
| 48 | huggingface-skills | development | Build, train, evaluate, and use open source AI models |
| 49 | circleback | productivity | Meeting, email, and calendar context integration |
| 50 | superpowers | development | Brainstorming, subagent-driven development, debugging, and TDD |
| 51 | posthog | monitoring | PostHog analytics platform integration |
| 52 | coderabbit | productivity | External code review with 40+ static analyzers |
| 53 | sonatype-guide | security | Software supply chain intelligence and dependency security |
| 54 | firecrawl | development | Web scraping and crawling, turn websites into LLM-ready markdown |
| 55 | qodo-skills | development | Reusable AI agent capabilities for code quality, testing, security |
| 56 | semgrep | security | Real-time security vulnerability detection |

### 2. datasapience-internal (DataSapience) -- 2 plugins

| # | Plugin | Version | Description |
|---|--------|---------|-------------|
| 1 | kolmo | 1.31.1 | Kolmogorov LLM platform agent management -- pull, push, test, and debug agents |
| 2 | ds | 2.8.2 | DataSapience engineering: GitLab pipelines/MRs/issues, Jira, Confluence, Helm charts, CI/CD |

### 3. ivintik (iVintik) -- 6 plugins

| # | Plugin | Version | Category | Description |
|---|--------|---------|----------|-------------|
| 1 | game-test | 0.1.0 | testing | AI-driven game testing with TITAN-inspired agent architecture (Unity) |
| 2 | plugin-ops | 1.4.0 | development | Plugin lifecycle management -- issue tracking, health audits, optimization, releasing |
| 3 | famdeck-toolkit | 2.6.1 | development | Setup and project init for Claude Code tools (Context7, Serena, Beads, etc.) |
| 4 | famdeck-atlas | 0.5.2 | development | Project registry and awareness across all Claude sessions via MCP tools |
| 5 | famdeck | 0.12.1 | development | Autonomous development toolkit -- autopilot, quality gates, story validation |
| 6 | famdeck-relay | 0.6.0 | development | Cross-project issue routing and work handoff (GitHub/GitLab/Jira) |

### 4. beads-marketplace (Steve Yegge) -- 1 plugin

| # | Plugin | Version | Description |
|---|--------|---------|-------------|
| 1 | beads | 0.56.1 | AI-supervised issue tracker for coding workflows |

---

## Installed Plugins (16)

| # | Plugin | Marketplace | Installed Version | Scope | Last Updated |
|---|--------|-------------|-------------------|-------|--------------|
| 1 | ralph-loop | claude-plugins-official | 205b6e0b3036 | user | 2026-03-04 |
| 2 | claude-plugin-ds | datasapience-internal | 2.6.0 | user | 2026-02-19 |
| 3 | kolmo-llm | datasapience-internal | 1.11.0 | user | 2026-02-20 |
| 4 | plugin-dev | claude-plugins-official | 205b6e0b3036 | user | 2026-03-04 |
| 5 | kolmo | datasapience-internal | 1.31.1 | user | 2026-03-08 |
| 6 | ds | datasapience-internal | 2.8.2 | user | 2026-03-08 |
| 7 | plugin-ops | ivintik | 1.8.5 | user | 2026-03-08 |
| 8 | beads | beads-marketplace | 0.56.1 | user | 2026-02-23 |
| 9 | context7 | claude-plugins-official | 205b6e0b3036 | user | 2026-03-04 |
| 10 | serena | claude-plugins-official | 205b6e0b3036 | user | 2026-03-04 |
| 11 | famdeck-toolkit | ivintik | 2.8.0 | user | 2026-03-02 |
| 12 | famdeck-atlas | ivintik | 0.7.2 | user | 2026-03-08 |
| 13 | famdeck | ivintik | 0.12.1 | user | 2026-03-08 |
| 14 | famdeck-relay | ivintik | 0.8.2 | user | 2026-03-08 |
| 15 | pyright-lsp | claude-plugins-official | 1.0.0 | user | 2026-03-01 |
| 16 | skill-creator | claude-plugins-official | 205b6e0b3036 | user | 2026-03-08 |

## Blocked Plugins (2)

| Plugin | Reason |
|--------|--------|
| code-review@claude-plugins-official | just-a-test |
| fizz@testmkt-marketplace | security |

---

## Summary

- **4 marketplaces** configured (1 official Anthropic, 1 internal corporate, 1 personal, 1 community)
- **65 plugins** available across all marketplaces
- **16 plugins** currently installed (all at user scope)
- **2 plugins** on the blocklist
