# /htmlpush - Publish HTML Page to GitHub + Airtable

This command prepares an HTML page for publishing by adding a favicon emoji and social media share image, pushes to GitHub, and logs the page to Airtable.

## Instructions

When the user runs `/htmlpush`, follow these steps:

### Step 1: Identify the HTML file
- If the user has been working on an HTML file in the current conversation, use that file
- If multiple HTML files or no clear file, ask the user which file to publish

### Step 2: Add Favicon Emoji
- Check if the HTML file already has a favicon link in the `<head>`
- If not, add an emoji favicon using this pattern:
```html
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🚀</text></svg>">
```
- Ask the user what emoji they want to use for the favicon (suggest one based on page content)
- **Save the emoji** for Airtable later

### Step 3: Add Social Media Share Image (Open Graph)
- Check if the HTML file already has Open Graph meta tags
- If not, add the following meta tags in the `<head>`:
```html
<!-- Open Graph / Social Media -->
<meta property="og:type" content="website">
<meta property="og:title" content="[PAGE TITLE]">
<meta property="og:description" content="[PAGE DESCRIPTION]">
<meta property="og:image" content="[IMAGE URL]">
<meta property="og:url" content="[PAGE URL]">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="[PAGE TITLE]">
<meta name="twitter:description" content="[PAGE DESCRIPTION]">
<meta name="twitter:image" content="[IMAGE URL]">
```
- Extract the title from the existing `<title>` tag
- Extract the description from the existing `<meta name="description">` tag
- Ask the user for a social share image URL, or suggest using a relevant image from the page

### Step 4: Determine GitHub Folder (Project Name)
- Check if the HTML file is already in a subfolder of the workspace
- If it's in a subfolder (e.g., `ai-accelerator/`), use that as the target folder AND project name
- If the file is in the root or location is unclear, ask the user:
  "What folder name should this page be published under? (e.g., 'ai-accelerator', 'states')"
- **The folder name = Project name** for Airtable linking

### Step 5: Git Operations
- Run `git status` to check current state
- Add the relevant files (HTML, CSS, and any assets in the folder)
- Create a commit with message: "feat: publish [folder-name] page with social sharing"
- Push to GitHub

### Step 6: Provide GitHub Pages URL
- After successful push, provide the GitHub Pages URL:
  `https://vishen.github.io/workspace/[folder-name]/`
- Note: User may need to enable GitHub Pages in repo settings if not already done

### Step 7: Add/Update Airtable Record
After the push succeeds, add or update the page in Airtable:

**Airtable Details:**
- Base ID: `appoX9UV0ewM07Mi1`
- Table: `Claude Pages` (ID: `tblqm3DEjztJg0qRl`)
- Projects Table: `tblm2DdUAe3rY55i9`

**First, check if a record already exists** by searching for the GitHub URL or page name.

**Fields to populate:**
| Field | Value |
|-------|-------|
| Name | Page title from `<title>` tag |
| LOCALHOST URL | `http://localhost:5500/[folder-name]/[filename].html` (or appropriate local path) |
| Github URL | `https://vishen.github.io/workspace/[folder-name]/[filename].html` |
| Desc | Page description from `<meta name="description">` or a brief summary |
| Favicon | The emoji used for the favicon (e.g., "🚀") |
| Projects | Link to matching project record (match folder name to project name) |
| Status | "Done" |

**Project Matching:**
- The folder name should match a project in the Projects table
- Search the Projects table for a matching name (case-insensitive)
- Known projects include: States, AI Mastery, Spiritual Mastery, Entrepreneurship Mastery, Black Friday, A-Fest, etc.
- If no matching project exists, ask user if they want to create a new project or skip linking

**If record exists:** Update the existing record
**If record doesn't exist:** Create a new record

## Example Usage

User: `/htmlpush`

Assistant will:
1. Identify the current HTML file being worked on
2. Ask for favicon emoji preference
3. Ask for social share image URL (or suggest one)
4. Confirm the folder name (which is also the project name)
5. Add favicon and OG tags to the HTML
6. Commit and push to GitHub
7. Provide the live URL
8. Add/update the Airtable record with:
   - Page name and description
   - Localhost URL
   - GitHub Pages URL
   - Favicon emoji
   - Link to the matching project
