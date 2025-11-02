# Google Drive MCP Server Setup Guide

Complete guide to setting up the Google Drive Model Context Protocol (MCP) server for Claude Code integration.

## Overview

The Google Drive MCP server enables Claude Code to:
- Create and edit Google Docs, Sheets, and Slides
- Search and manage Drive files
- Read document contents
- Navigate folder structures

## Prerequisites

- Node.js 18+ installed
- Google Cloud Platform account
- Claude Desktop App
- Bash shell access

## Setup Steps

### 1. Google Cloud Console Configuration

1. **Go to Google Cloud Console**: https://console.cloud.google.com/
2. **Create or select a project**
3. **Enable Required APIs**:
   - Google Drive API
   - Google Docs API
   - Google Sheets API
   - Google Slides API

4. **Configure OAuth Consent Screen**:
   - Navigate to: APIs & Services > OAuth consent screen
   - Select "External" user type
   - Fill in:
     - App name (e.g., "Claude Code Google Drive")
     - User support email (your email)
     - Developer contact (your email)
   - Add OAuth Scopes:
     - `https://www.googleapis.com/auth/drive`
     - `https://www.googleapis.com/auth/drive.file`
     - `https://www.googleapis.com/auth/documents`
     - `https://www.googleapis.com/auth/spreadsheets`
     - `https://www.googleapis.com/auth/presentations`
   - Add yourself as a test user

5. **Create OAuth 2.0 Credentials**:
   - Navigate to: APIs & Services > Credentials
   - Click "Create Credentials" > "OAuth client ID"
   - Application type: **Desktop app**
   - Name: "Claude Code" (or any name)
   - Download the JSON file

### 2. Save OAuth Credentials

Option A: Manual
```bash
mv ~/Downloads/client_secret_*.json ~/.config/google-drive-mcp/gcp-oauth.keys.json
```

Option B: Using Helper Script
```bash
./scripts/setup/save-google-credentials.sh
```

Option C: Using .env File
```bash
# Edit .env file and paste full JSON content
GOOGLE_OAUTH_CREDENTIALS_JSON={"installed":{...}}
```

### 3. Run Setup Script

**Using direct credentials file:**
```bash
./scripts/setup/setup-google-drive-mcp.sh
```

**Using .env file:**
```bash
./scripts/setup/setup-google-drive-from-env.sh
```

This will:
- Verify credentials exist
- Authenticate with Google (opens browser)
- Update Claude Desktop configuration
- Create backup of existing config

### 4. Restart Claude Desktop

After successful setup, restart the Claude Desktop app to load the new MCP server.

## Manual Configuration

If you prefer to configure manually:

1. **Authenticate:**
   ```bash
   export GOOGLE_DRIVE_OAUTH_CREDENTIALS="$HOME/.config/google-drive-mcp/gcp-oauth.keys.json"
   npx @piotr-agier/google-drive-mcp auth
   ```

2. **Update Claude Config** at `~/Library/Application Support/Claude/claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "google-drive": {
         "command": "npx",
         "args": ["@piotr-agier/google-drive-mcp"],
         "env": {
           "GOOGLE_DRIVE_OAUTH_CREDENTIALS": "/Users/YOUR_USERNAME/.config/google-drive-mcp/gcp-oauth.keys.json"
         }
       }
     }
   }
   ```

3. **Restart Claude Desktop**

## Usage Examples

Once configured, you can ask Claude Code to:

### Google Docs
```
"Create a new Google Doc with my project plan"
"Read the contents of this Google Doc: [URL]"
"Update the introduction section of this document"
```

### Google Sheets
```
"Create a spreadsheet to track expenses"
"Read data from this Google Sheet: [URL]"
"Add a new row to this spreadsheet with [data]"
```

### Google Slides
```
"Create a presentation about our product launch"
"Read the slides from this presentation: [URL]"
"Add a new slide with [content]"
```

### Google Drive
```
"Search my Drive for files about 'marketing'"
"List files in this folder: [URL]"
"Create a new folder for this project"
```

## Troubleshooting

### Authentication Issues

**Error: "Device not configured"**
- Run: `gh auth setup-git` to configure git credentials
- Or use SSH: `git remote set-url origin git@github.com:username/repo.git`

**Error: "Host key verification failed"**
- SSH keys not configured
- Use HTTPS instead or set up SSH keys

### MCP Server Issues

**Server not loading:**
- Check Claude Desktop logs
- Verify credentials file exists at the configured path
- Ensure Node.js 18+ is installed
- Restart Claude Desktop

**Permission errors:**
- Verify OAuth scopes include all required APIs
- Re-authenticate: `npx @piotr-agier/google-drive-mcp auth`
- Check test users are added in OAuth consent screen

## Security Notes

- OAuth credentials are stored in `~/.config/google-drive-mcp/gcp-oauth.keys.json`
- Tokens are stored in `~/.config/google-drive-mcp/tokens.json`
- Both files are gitignored for security
- Never commit credentials to version control
- Use `.env` file for project-specific configuration (also gitignored)

## References

- [Google Drive MCP Server](https://github.com/piotr-agier/google-drive-mcp)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Google Cloud Console](https://console.cloud.google.com/)
- [Claude Code Documentation](https://docs.claude.com/claude-code)

## Support

For issues or questions:
- Check the [Google Drive MCP GitHub Issues](https://github.com/piotr-agier/google-drive-mcp/issues)
- Review Claude Code documentation
- Verify Google Cloud API quotas and limits
