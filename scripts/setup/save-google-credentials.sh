#!/bin/bash

# Script to help save Google OAuth credentials

echo "=== Save Google OAuth Credentials ==="
echo ""
echo "Please paste the FULL path to your downloaded credentials file"
echo "(Usually in ~/Downloads/ and named something like client_secret_*.json)"
echo ""
read -p "Path to downloaded file: " DOWNLOAD_PATH

# Expand ~ if present
DOWNLOAD_PATH="${DOWNLOAD_PATH/#\~/$HOME}"

if [ ! -f "$DOWNLOAD_PATH" ]; then
    echo "❌ File not found at: $DOWNLOAD_PATH"
    echo ""
    echo "Please check the path and try again."
    echo "Hint: Drag and drop the file into this terminal to get the full path"
    exit 1
fi

# Create config directory if it doesn't exist
mkdir -p "$HOME/.config/google-drive-mcp"

# Copy the file
cp "$DOWNLOAD_PATH" "$HOME/.config/google-drive-mcp/gcp-oauth.keys.json"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Credentials saved successfully to:"
    echo "   $HOME/.config/google-drive-mcp/gcp-oauth.keys.json"
    echo ""
    echo "You can now proceed with authentication!"
else
    echo "❌ Failed to save credentials"
    exit 1
fi
