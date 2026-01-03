#!/bin/bash

set -e

echo "=================================="
echo "  Claude Code Configuration Setup"
echo "=================================="
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Create directories if they don't exist
mkdir -p ~/.claude/skills
mkdir -p ~/.claude/commands
mkdir -p ~/.claude/plugins

echo "[1/5] Installing settings..."
if [ -f ~/.claude/settings.json ]; then
    echo "  → Backing up existing settings to ~/.claude/settings.json.backup"
    cp ~/.claude/settings.json ~/.claude/settings.json.backup
fi
cp "$SCRIPT_DIR/claude/settings.json" ~/.claude/settings.json
echo "  ✓ Settings installed"

echo ""
echo "[2/5] Installing skills..."
for skill in "$SCRIPT_DIR/claude/skills"/*; do
    if [ -d "$skill" ]; then
        skill_name=$(basename "$skill")
        cp -r "$skill" ~/.claude/skills/
        echo "  ✓ $skill_name"
    fi
done

echo ""
echo "[3/5] Installing commands..."
cp -r "$SCRIPT_DIR/claude/commands"/* ~/.claude/commands/ 2>/dev/null || echo "  → No commands to install"
echo "  ✓ Commands installed"

echo ""
echo "[4/5] Installing plugins registry..."
cp "$SCRIPT_DIR/claude/plugins/installed_plugins.json" ~/.claude/plugins/ 2>/dev/null || echo "  → No plugins registry"
echo "  ✓ Plugins registry installed"

echo ""
echo "[5/5] Docker MCP configuration..."
if command -v docker &> /dev/null; then
    mkdir -p ~/.docker/mcp
    cp "$SCRIPT_DIR/docker-mcp/catalog.json" ~/.docker/mcp/ 2>/dev/null || true
    cp "$SCRIPT_DIR/docker-mcp/config.yaml" ~/.docker/mcp/ 2>/dev/null || true
    cp "$SCRIPT_DIR/docker-mcp/registry.yaml" ~/.docker/mcp/ 2>/dev/null || true
    cp "$SCRIPT_DIR/docker-mcp/tools.yaml" ~/.docker/mcp/ 2>/dev/null || true
    echo "  ✓ Docker MCP configured"
else
    echo "  → Docker not found, skipping MCP configuration"
fi

echo ""
echo "=================================="
echo "  Installation Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "  1. Run 'claude login' if not already authenticated"
echo "  2. Restart Claude Code to load new configuration"
echo ""
echo "Plugins requiring API keys:"
echo "  • greptile - Set GREPTILE_API_KEY"
echo "  • sentry - Configure in Claude settings"
echo "  • stripe - Set STRIPE_API_KEY"
echo "  • chrome-devtools-mcp - Install Chrome extension"
echo ""
echo "Enjoy your configured Claude Code!"
