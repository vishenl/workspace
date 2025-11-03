---
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Glob
  - Grep
  - TodoWrite
  - WebSearch
  - SlashCommand
description: "Intelligently analyze, reorganize, and document project structure using best practices, optimized for GitHub Pages"
tags: ["project-management", "organization", "documentation", "git", "github-pages"]
---

# Project Organization & Documentation Command

## Context

You are an expert software architect and technical documentation specialist with deep knowledge of repository best practices, file organization patterns, and project documentation standards. Your expertise includes analyzing codebases, identifying logical groupings, and creating maintainable folder structures that scale.

## Your Mission

Transform a messy project folder into a professionally organized repository with:
- Logical folder hierarchy following industry best practices
- Consistent file naming conventions (kebab-case, descriptive names)
- Comprehensive README documentation
- Clean git history with atomic commits

## PHASE 1: INTELLIGENT PROJECT ANALYSIS

**Step 1.1: Initialize Progress Tracking**

Use TodoWrite to create a task list for this organization workflow:
- Analyze current project structure and file purposes
- Identify HTML pages for GitHub Pages deployment
- Design optimal folder hierarchy
- Move and rename files with git tracking
- Generate comprehensive README documentation
- Commit changes using /commit command
- Generate GitHub Pages links

**Step 1.2: Deep Project Discovery**

Think step-by-step about the current project state:

1. **Discover all project files** using intelligent pattern matching:
   - Use Glob to find all documentation files (*.md)
   - Use Glob to find all scripts (*.py, *.js, *.sh)
   - Use Glob to find all HTML pages (*.html) - these are candidates for GitHub Pages
   - Use Glob to find all tools and utilities (*.json, other files)
   - List all directories and their purposes

2. **Identify GitHub Pages candidates**:
   - Find all HTML files that should be publicly accessible
   - Note their current locations and purposes
   - Plan their organization for optimal GitHub Pages URLs
   - Consider index.html for directories vs named pages

3. **Analyze file contents and relationships**:
   - Read key documentation files to understand their purpose
   - Identify file relationships and dependencies
   - Detect existing organizational patterns or conventions
   - Note any configuration files (.env, .gitignore, package.json)

4. **Assess project type and domain**:
   - Is this primarily a data analysis project?
   - Is it a web application, CLI tool, or library?
   - What languages and frameworks are used?
   - What integrations exist (APIs, databases, services)?

**Think harder about categorization patterns:**
- Group files by functional domain (e.g., data processing, documentation, setup)
- Identify files that serve similar purposes
- Find files that could be renamed for clarity
- Spot files that might be obsolete or redundant

## PHASE 2: ARCHITECTURAL DESIGN

**Step 2.1: Design Optimal Folder Structure**

Based on your analysis, think step-by-step about the ideal organization:

**Common Best Practice Patterns:**

For **Data/Analysis Projects:**
```
project/
├── docs/           # All documentation
│   ├── analysis/   # Analysis reports
│   ├── guides/     # Setup and usage guides
│   └── research/   # Research notes
├── scripts/        # Automation scripts
│   ├── data/       # Data processing
│   └── utils/      # Utility scripts
├── tools/          # Interactive tools
└── tests/          # Test files
```

For **Application Projects:**
```
project/
├── src/            # Source code
├── docs/           # Documentation
├── tests/          # Tests
├── scripts/        # Build/deploy scripts
├── config/         # Configuration files
└── assets/         # Static assets
```

For **Multi-Domain Projects:**
```
project/
├── docs/           # Documentation by category
│   ├── domain-a/
│   └── domain-b/
├── scripts/        # Scripts by category
│   ├── domain-a/
│   └── domain-b/
├── tools/          # Shared tools
└── config/         # Configuration
```

**Apply extended thinking to determine:**
- Which pattern best fits this project's needs?
- What custom folders are needed for unique requirements?
- How deep should the hierarchy go? (balance: not too flat, not too nested)
- What naming conventions will be most intuitive?

**Step 2.2: Design File Renaming Strategy**

Think about how to rename files for consistency:
- Use kebab-case for all files (better-than-snake_case.md)
- Remove ambiguous abbreviations
- Make names descriptive but concise
- Preserve file extensions
- Keep related files grouped by prefix when helpful

## PHASE 3: INTELLIGENT REORGANIZATION

**Step 3.1: Execute Folder Structure Creation**

Use intelligent tool orchestration to create the designed folder hierarchy:
- Create parent folders first
- Create nested subfolders
- Ensure consistent naming and organization

**Step 3.2: Smart File Movement and Renaming**

Think step-by-step about moving each file:

For each file identified in Phase 1:
1. **Determine its new location** based on the folder design
2. **Decide if renaming is beneficial** for clarity
3. **Use git-aware operations** to preserve history
4. **Update any internal references** if files are moved

Use the Bash tool with git commands to:
- Move files with `git mv` to preserve history
- Rename files for consistency
- Organize into the designed folder structure

**Important git considerations:**
- Always use `git mv` instead of regular `mv` to preserve history
- Group related moves into logical commits
- Validate each move before proceeding to the next

**Step 3.3: Validation Checkpoint**

After reorganization, intelligently verify:
- All files successfully moved to intended locations
- No files were lost or duplicated
- Git status shows clean rename/move operations
- Folder structure matches the design

Update TodoWrite with completed steps.

## PHASE 4: COMPREHENSIVE DOCUMENTATION GENERATION

**Step 4.1: README Architecture**

Design a comprehensive README structure following best practices:

**Essential Sections:**
1. **Title & Overview**: Clear project description
2. **Table of Contents**: For easy navigation (if lengthy)
3. **Features/Capabilities**: What the project does
4. **Project Structure**: Explain the folder organization
5. **Getting Started**: Prerequisites, installation
6. **Usage**: How to use scripts, tools, commands
7. **Documentation Index**: Links to docs with descriptions
8. **Technology Stack**: Languages, frameworks, tools used
9. **Contributing**: Guidelines if applicable
10. **License/Acknowledgments**: Credits and legal info

**Step 4.2: Content Generation**

Use extended thinking to craft compelling, accurate documentation:

For **Overview section:**
- Clearly articulate the project's purpose and value
- Highlight key capabilities and use cases
- Set appropriate context for the audience

For **Project Structure section:**
- Use a tree diagram showing folder hierarchy
- Explain the purpose of each major folder
- Describe file naming conventions used

For **Documentation Index:**
- List each documentation file with brief description
- Organize by category matching folder structure
- Include relative links for easy navigation

For **Usage Examples:**
- Provide concrete examples for common tasks
- Show command syntax and expected output
- Include troubleshooting tips

**Step 4.3: Write README.md**

Use the Write tool to create the comprehensive README file with:
- Well-structured markdown with proper headers
- Code blocks for commands and examples
- Links to relevant documentation
- Badges or status indicators if appropriate
- Clear, professional tone

## PHASE 5: GIT COMMIT AND GITHUB PAGES

**Step 5.1: Commit Changes Using /commit Command**

Use the SlashCommand tool to execute the /commit command:
- This will intelligently stage and commit all changes
- Follow conventional commit format
- Handle git operations with proper error handling
- Push changes to GitHub

Example:
```
SlashCommand with command: "/commit"
```

The /commit command will:
- Review all staged and unstaged changes
- Create atomic commits with proper messages
- Include Co-Authored-By attribution
- Push to GitHub remote

**Step 5.2: Push Changes to GitHub**

After the /commit command completes, push the changes to GitHub:

1. Use the Bash tool to push changes:
   ```bash
   git push origin main
   ```

2. Handle potential errors:
   - If branch is named 'master' instead of 'main', retry with correct branch
   - If push fails due to diverged history, inform user
   - If push succeeds, proceed to next step

**Step 5.3: Detect and Open New/Modified HTML Pages**

After successful push, detect HTML files that were created or modified in the commit and open them in the browser:

1. **Detect files from the last commit:**
   ```bash
   git diff-tree --no-commit-id --name-only -r HEAD
   ```

2. **Filter for HTML files:**
   - Look for files ending in `.html`
   - These are the files that should be opened in browser

3. **Generate GitHub Pages URLs:**
   - Extract username and repository from git remote URL
   - For each HTML file, create URL: `https://[username].github.io/[repository]/[path-to-file.html]`

4. **Open pages in default browser:**
   - Use `open` command on macOS to open each URL
   - Example: `open https://vishenl.github.io/workspace/tools/areas-of-growth-viewer.html`
   - Wait 2-3 seconds between opening multiple pages to prevent browser overwhelm

**Step 5.4: Generate GitHub Pages Links Summary**

After opening pages in browser, generate a summary of GitHub Pages URLs for all HTML files:

**GitHub Pages URL Format:**
```
https://[username].github.io/[repository]/[path-to-file.html]
```

**Process:**
1. Get GitHub repository information:
   - Extract username from remote URL
   - Extract repository name from remote URL

2. For each HTML file in the repository:
   - Calculate its relative path from repository root
   - Generate the GitHub Pages URL
   - Include a description of what the page contains

3. Organize links by category:
   - Analysis reports
   - Tools and utilities
   - Documentation pages
   - Other HTML content

**Important GitHub Pages Considerations:**
- Files must be in the main/master branch (or gh-pages branch)
- GitHub Pages must be enabled in repository settings
- URLs are case-sensitive
- Use index.html for directory root pages
- HTML files should be self-contained or reference relative paths
- ⏱️ **Deployment Time**: GitHub Pages may take 1-2 minutes to deploy after push

## PHASE 6: COMPLETION AND VALIDATION

**Step 6.1: Final Verification**

Confirm all success criteria met:
- ✅ Project files organized in logical folder structure
- ✅ Files renamed following consistent conventions
- ✅ Comprehensive README created with all sections
- ✅ Changes committed with meaningful message
- ✅ Changes pushed to GitHub successfully

**Step 6.2: Provide Summary Report**

Generate a clear summary showing:
- Folder structure created (tree diagram)
- Number of files moved and renamed
- Key documentation created
- Git commit hash and message
- Link to GitHub repository
- **GitHub Pages Links**: Complete list of all HTML pages with their public URLs

**Step 6.3: Clean Up TodoWrite**

Mark all tasks as completed in TodoWrite.

## GitHub Pages Link Generation

### Format and Organization

When generating GitHub Pages links, present them in a clear, organized format:

**Example Output:**
```markdown
## 🌐 GitHub Pages Links

Your HTML pages are now publicly accessible:

### 📊 Analysis Reports
- [Mindvalley Black Friday Analysis](https://vishenl.github.io/workspace/mindvalley-black-friday-analysis.html)
  Comprehensive sales page conversion analysis with recommendations

### 🛠️ Tools & Utilities
- [Areas of Growth Viewer](https://vishenl.github.io/workspace/tools/areas-of-growth-viewer.html)
  Interactive tool for tracking personal development areas

### 📚 Documentation
- [Project Documentation](https://vishenl.github.io/workspace/docs/index.html)
  Main documentation index page
```

### Link Verification Notes

Include helpful information:
- ⚠️ **Note**: GitHub Pages may take 1-2 minutes to deploy after push
- 📝 **Tip**: GitHub Pages must be enabled in repository settings
- 🔒 **Privacy**: These pages are publicly accessible if repository is public

## Advanced Patterns & Considerations

### Handling Edge Cases

**If git is not initialized:**
- Detect this condition early
- Guide user through git initialization
- Set up .gitignore appropriately

**If README already exists:**
- Read the existing README
- Preserve valuable content
- Enhance rather than replace
- Create backup if substantial changes

**If files have complex interdependencies:**
- Identify dependencies through content analysis
- Update import paths or references
- Validate functionality after moves

### Intelligent Adaptation

**For different project types:**
- Adjust folder structure based on project domain
- Use domain-specific naming conventions
- Include relevant documentation sections

**For different scales:**
- Smaller projects: Flatter structure
- Larger projects: More nested organization
- Consider future growth in design

### Quality Standards

**Folder Organization:**
- Clear purpose for each folder
- Balanced depth (typically 2-3 levels)
- Consistent naming conventions
- Logical grouping of related files

**File Naming:**
- Descriptive yet concise
- Consistent case convention (kebab-case recommended)
- Appropriate file extensions
- Avoid special characters and spaces

**Documentation:**
- Clear and comprehensive
- Well-structured with headers
- Includes examples and usage
- Links to additional resources
- Professional tone and formatting

**Git Hygiene:**
- Meaningful commit messages
- Atomic commits when possible
- Clean git history
- No sensitive data committed

## Execution Notes

Throughout this workflow:
- **Use chain-of-thought reasoning** at each decision point
- **Apply extended thinking** for complex organizational decisions
- **Validate assumptions** before making changes
- **Provide clear status updates** at each phase
- **Handle errors gracefully** with helpful recovery suggestions
- **Maintain professional communication** throughout

The goal is not just to organize files, but to create a maintainable, professional repository structure that will scale as the project grows.
