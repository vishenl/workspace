---
allowed-tools:
  - Bash
  - Glob
  - Read
  - Grep
  - mcp__airtable__list_records
  - mcp__airtable__create_record
  - mcp__airtable__update_records
  - mcp__airtable__search_records
description: "Add all web pages (localhost/GitHub) to Airtable Claude Pages table"
tags: [airtable, pages, documentation, urls, tracking]
version: "1.0.0"
---

# Sync Web Pages to Airtable

## Your Mission

Discover all web pages created in this workspace (HTML files) and sync them to the **Innovation Task Force** Airtable base in the **Claude Pages** table.

## Airtable Configuration

- **Base ID**: `appoX9UV0ewM07Mi1`
- **Table**: `Claude Pages` (ID: `tblqm3DEjztJg0qRl`)

## Table Fields Reference

| Field | Type | Description |
|-------|------|-------------|
| Name | Single Line Text | Page name/title |
| LOCALHOST URL | URL | Local development URL (e.g., file:// path) |
| Github URL | URL | Live GitHub Pages URL |
| Password | Single Line Text | Password if page is protected |
| Status | Single Select | Todo, In progress, Done |
| Type | Single Select | Class Notes, Class Report, Sales Page, Presentation Slides, Strategy Doc, Training Guide |
| Notes | Multiline Text | Description of the page |
| Rating | Rating (1-5 stars) | Quality rating |
| Projects | Linked Records | Link to Projects table |

## Execution Steps

**STEP 1: Discover All HTML Pages**

1. Use Glob to find all HTML files in the repository:
   - Pattern: `**/*.html`
   - Exclude: `node_modules`, `dist`, `build`, `.git`

2. For each HTML file found:
   - Extract the filename as the page name
   - Read the file to find `<title>` tag for better name
   - Check for password protection (look for `checkPassword`, `password-overlay`, or similar patterns)

**STEP 2: Generate URLs**

1. **Localhost URL**: Create file path URL
   - Format: `file:///Users/vishen/Documents/Github/workspace/[filename]`

2. **GitHub Pages URL**: Construct from git remote
   - Get repository info from `git remote get-url origin`
   - Format: `https://vishenl.github.io/workspace/[filename]`

**STEP 3: Determine Page Type**

Analyze filename and content to categorize:
- Contains "curriculum", "course", "lesson" → Class Notes
- Contains "report", "analysis" → Class Report
- Contains "sales", "offer", "pricing", "black-friday" → Sales Page
- Contains "slides", "presentation", "deck" → Presentation Slides
- Contains "strategy", "optimization", "guide" → Strategy Doc
- Contains "training", "tutorial", "how-to" → Training Guide

**STEP 4: Check Existing Records**

1. Fetch all existing records from Claude Pages table
2. Compare by GitHub URL or Name to avoid duplicates
3. Identify records that need updating vs. creating

**STEP 5: Sync to Airtable**

For each discovered page:

1. **If page exists in Airtable** (match by GitHub URL):
   - Update the record with any new information
   - Preserve existing fields like Rating and Projects

2. **If page is new**:
   - Create new record with all discovered fields
   - Set Status to "Done" (since page exists)

**STEP 6: Report Results**

Display a summary table:

```
## Pages Synced to Airtable

| Page Name | GitHub URL | Password | Type | Action |
|-----------|------------|----------|------|--------|
| Example Page | https://... | (none) | Strategy Doc | Created |
| Another Page | https://... | black | Sales Page | Updated |

Total: X pages synced (Y created, Z updated)
```

## Password Detection Patterns

Look for these patterns in HTML files to detect password protection:
- `const correctPassword = '...'`
- `password-overlay`
- `checkPassword()`
- `type="password"`
- Comments containing "password:"

Extract the actual password value if found in the code.

## Error Handling

- **No HTML files found**: Report and suggest creating pages
- **Airtable API error**: Display error message and suggest checking permissions
- **Duplicate detection**: Show which records were skipped and why

## Output Format

Present results in clean markdown with:
- Summary of actions taken
- Table of all pages with their status
- Any errors or warnings
- Link to the Airtable view: https://airtable.com/appoX9UV0ewM07Mi1/tblqm3DEjztJg0qRl

## Success Criteria

This command succeeds when:
- All HTML pages in the workspace are discovered
- Each page is either created or updated in Airtable
- Passwords are correctly extracted and recorded
- No duplicate records are created
- User receives clear summary of actions taken
