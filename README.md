# Claude Code Configuration

Personal Claude Code configuration with custom skills, agents, plugins, and MCP integrations.

## Contents

```
claude-config/
├── claude/
│   ├── settings.json          # Main settings (permissions, plugins, MCP servers)
│   ├── skills/                # Custom skills
│   │   ├── agent-debug-system/
│   │   ├── cybersecurity-expert/
│   │   ├── debug-agent/
│   │   ├── frontend-design/
│   │   └── modern-dev-languages/
│   ├── commands/              # Custom commands
│   │   └── agent-cybersecurity-system.md
│   └── plugins/
│       └── installed_plugins.json
├── docker-mcp/                # Docker MCP Gateway configuration
│   ├── catalog.json
│   ├── catalogs/
│   ├── config.yaml
│   ├── registry.yaml
│   └── tools.yaml
├── install.sh                 # Installation script
└── README.md
```

## Custom Skills

| Skill | Description |
|-------|-------------|
| `modern-dev-languages` | Reference guide for Python, JavaScript, TypeScript, React, React Native, Rust |
| `debug-agent` | Autonomous debugging agent with ReAct reasoning |
| `cybersecurity-expert` | Security auditing, SAST, OWASP, vulnerability analysis |
| `frontend-design` | Production-grade frontend interfaces with high design quality |
| `agent-debug-system` | Professional debugging system with diagnostic tools |

## Enabled Plugins

### Official Plugins
- `code-review` - Code review automation
- `commit-commands` - Git commit helpers
- `context7` - Up-to-date library documentation
- `feature-dev` - Guided feature development
- `frontend-design` - Frontend UI development
- `github` - GitHub integration
- `greptile` - Code search and analysis
- `pr-review-toolkit` - PR review tools
- `sentry` - Error tracking integration
- `stripe` - Payment integration helpers
- `taskmaster` - Task management
- `typescript-lsp` - TypeScript language server
- `chrome-devtools-mcp` - Browser automation
- `claude-mem` - Memory/context management

### Workflow Plugins (claude-code-workflows)
- Backend: `backend-development`, `backend-api-security`, `database-design`, `database-migrations`
- Frontend: `frontend-mobile-development`, `frontend-mobile-security`
- Testing: `tdd-workflows`, `unit-testing`, `debugging-toolkit`
- Security: `security-compliance`, `security-scanning`
- Code Quality: `code-refactoring`, `codebase-cleanup`, `git-pr-workflows`
- And more...

## Installation

### Quick Install

```bash
git clone https://github.com/YOUR_USERNAME/claude-config.git
cd claude-config
chmod +x install.sh
./install.sh
```

### Manual Install

1. **Copy Claude settings:**
   ```bash
   cp claude/settings.json ~/.claude/settings.json
   ```

2. **Copy skills:**
   ```bash
   cp -r claude/skills/* ~/.claude/skills/
   ```

3. **Copy commands:**
   ```bash
   cp -r claude/commands/* ~/.claude/commands/
   ```

4. **Copy plugins registry:**
   ```bash
   cp claude/plugins/installed_plugins.json ~/.claude/plugins/installed_plugins.json
   ```

5. **(Optional) Docker MCP:**
   ```bash
   mkdir -p ~/.docker/mcp
   cp -r docker-mcp/* ~/.docker/mcp/
   ```

## Post-Installation

### Authentication
```bash
claude login
```

### Plugins Requiring API Keys
Some plugins need additional configuration:
- **greptile** - Requires Greptile API token
- **sentry** - Requires Sentry API token
- **stripe** - Requires Stripe API key
- **posthog** - Requires PostHog API key

### Chrome DevTools MCP
Install the Chrome extension from:
https://chromewebstore.google.com/detail/anthropic-claude-in-chrom

## Customization

### Adding a Skill
Create a new directory in `claude/skills/` with:
- `SKILL.md` - Skill description and instructions
- `REFERENCE.md` (optional) - Reference documentation

### Modifying Permissions
Edit `claude/settings.json` to add/remove auto-approved commands in the `permissions.allow` array.

### Enabling/Disabling Plugins
Toggle plugins in `claude/settings.json` under `enabledPlugins`.

## Syncing Changes

After modifying your local Claude configuration:

```bash
# Copy updated files to repo
cp ~/.claude/settings.json claude/settings.json
cp -r ~/.claude/skills/* claude/skills/
cp -r ~/.claude/commands/* claude/commands/

# Commit and push
git add .
git commit -m "Update configuration"
git push
```

## License

Personal configuration - use at your own discretion.
