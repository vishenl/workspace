#!/bin/bash

# Google Drive MCP Setup Script

echo "=== Google Drive MCP Setup ==="
echo ""

# Check if credentials file exists
CREDS_PATH="$HOME/.config/google-drive-mcp/gcp-oauth.keys.json"

if [ ! -f "$CREDS_PATH" ]; then
    echo "❌ OAuth credentials file not found at: $CREDS_PATH"
    echo ""
    echo "Please follow these steps:"
    echo "1. Go to https://console.cloud.google.com/"
    echo "2. Create/select a project"
    echo "3. Enable Google Drive, Docs, Sheets, and Slides APIs"
    echo "4. Create OAuth 2.0 credentials (Desktop app)"
    echo "5. Download the JSON file"
    echo "6. Save it to: $CREDS_PATH"
    echo ""
    exit 1
fi

echo "✅ Found credentials file"
echo ""

# Run authentication
echo "Starting authentication process..."
echo "This will open a browser window for you to authorize the app."
echo ""

export GOOGLE_DRIVE_OAUTH_CREDENTIALS="$CREDS_PATH"
npx @piotr-agier/google-drive-mcp auth

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Authentication successful!"
    echo ""
    echo "Now updating your Claude Desktop configuration..."

    # Backup existing config
    CONFIG_PATH="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
    cp "$CONFIG_PATH" "$CONFIG_PATH.backup.$(date +%Y%m%d_%H%M%S)"

    # Update config with Google Drive MCP
    cat > "/tmp/claude_config_update.json" << 'EOF'
{
  "mcpServers": {
    "airtable": {
      "command": "npx",
      "args": ["@rashidazarang/airtable-mcp"],
      "env": {
        "AIRTABLE_TOKEN": "patCH6J42EFYDP5lo.d78f2da717586f98aa2ebb50749ff82c149866dcd1acb06dc76f58b3fd48466c"
      }
    },
    "google-drive": {
      "command": "npx",
      "args": ["@piotr-agier/google-drive-mcp"],
      "env": {
        "GOOGLE_DRIVE_OAUTH_CREDENTIALS": "$HOME/.config/google-drive-mcp/gcp-oauth.keys.json"
      }
    }
  }
}
EOF

    mv "/tmp/claude_config_update.json" "$CONFIG_PATH"

    echo "✅ Claude Desktop configuration updated!"
    echo ""
    echo "Next steps:"
    echo "1. Restart Claude Desktop app"
    echo "2. The Google Drive MCP tools will be available"
    echo ""
    echo "You can now:"
    echo "  - Create and edit Google Docs"
    echo "  - Create and edit Google Sheets"
    echo "  - Create and edit Google Slides"
    echo "  - Search and manage Drive files"
    echo ""
else
    echo ""
    echo "❌ Authentication failed. Please check your credentials and try again."
    exit 1
fi
