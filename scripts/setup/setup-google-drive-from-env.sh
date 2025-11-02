#!/bin/bash

# Google Drive MCP Setup Script (using .env file)

echo "=== Google Drive MCP Setup (from .env) ==="
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found"
    echo ""
    echo "Please create a .env file with your Google OAuth credentials"
    exit 1
fi

# Load .env
source .env

# Check if credentials are set
if [ -z "$GOOGLE_OAUTH_CREDENTIALS_JSON" ]; then
    echo "❌ GOOGLE_OAUTH_CREDENTIALS_JSON not set in .env file"
    echo ""
    echo "Please edit .env and paste your OAuth JSON credentials"
    echo ""
    echo "Example:"
    echo 'GOOGLE_OAUTH_CREDENTIALS_JSON={"installed":{...}}'
    exit 1
fi

echo "✅ Found OAuth credentials in .env"
echo ""

# Create config directory
mkdir -p "$HOME/.config/google-drive-mcp"

# Save credentials to file
CREDS_PATH="$HOME/.config/google-drive-mcp/gcp-oauth.keys.json"
echo "$GOOGLE_OAUTH_CREDENTIALS_JSON" > "$CREDS_PATH"

echo "✅ Saved credentials to: $CREDS_PATH"
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
    cat > "/tmp/claude_config_update.json" << EOF
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
        "GOOGLE_DRIVE_OAUTH_CREDENTIALS": "$CREDS_PATH"
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
