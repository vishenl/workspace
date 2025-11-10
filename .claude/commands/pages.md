---
allowed-tools: [Bash, Glob, Read, Grep]
description: "Intelligently discover and display all GitHub Pages URLs from your workspace"
tags: [github, pages, documentation, urls, discovery]
version: "1.0.0"
---

# GitHub Pages Discovery & URL Mapper

## Your Mission

Intelligently analyze this repository and generate a comprehensive, organized map of all public-facing GitHub Pages URLs with their categories and purposes.

## Context Discovery Phase

Let me think step-by-step about discovering your GitHub Pages setup:

**STEP 1: Repository Intelligence Gathering**

Use intelligent prompting to discover:
- Extract GitHub repository owner and name from git remote configuration
- Identify the primary branch used for GitHub Pages deployment
- Detect GitHub Pages source configuration (docs folder, root, etc.)

**STEP 2: Content Discovery Through Smart Analysis**

Deploy adaptive file discovery to:
- Intelligently scan for all HTML files in the repository
- Use pattern recognition to identify documentation directories
- Apply smart filtering to exclude non-public files (node_modules, build artifacts, etc.)
- Discover markdown files that could represent additional content

**STEP 3: Intelligent Organization & Categorization**

Think step-by-step about organizing discovered pages:
- Analyze directory structure to understand content organization
- Group pages by logical categories (main pages, analyses, guides, curriculum, etc.)
- Identify the purpose of each page through intelligent file name and path analysis
- Detect index pages and navigation structure

**STEP 4: URL Generation with Smart Formatting**

Use chain-of-thought reasoning to:
- Construct proper GitHub Pages URLs based on repository structure
- Apply GitHub Pages URL conventions (username.github.io/repository/path)
- Generate relative paths for all discovered HTML files
- Create properly formatted URLs for markdown files viewable on GitHub

**STEP 5: Comprehensive Output Generation**

Synthesize findings into organized sections:

### Main GitHub Pages Base URL
Display the root URL for the GitHub Pages site

### Live HTML Pages
Organize by category with:
- **Main Pages**: Primary landing pages and key content
- **Analyses**: Data analysis and research pages
- **Guides**: Documentation and tutorial content
- **Curriculum**: Educational content and course materials
- **Other Categories**: Any additional organized content

### Documentation Files (Markdown)
List markdown files with:
- Organized by directory structure
- Include GitHub URLs for viewing
- Note which could be converted to HTML for public pages

### Summary Statistics
Provide intelligent insights:
- Total number of public HTML pages
- Total documentation files
- Coverage by category
- Suggestions for potential improvements

## Smart Validation & Quality Checks

Apply adaptive validation through intelligent analysis:
- Verify all discovered URLs follow proper GitHub Pages conventions
- Check for broken internal references or missing index files
- Identify orphaned pages or undiscovered content
- Suggest potential organizational improvements

## Output Format

Present results in clean, scannable markdown with:
- Clear section headers for easy navigation
- Clickable URLs for immediate access
- Category groupings for logical organization
- Visual hierarchy using markdown formatting
- Action items or suggestions for enhancement

## Success Criteria

This command succeeds when:
- All public-facing HTML pages are discovered and mapped
- URLs are correctly formatted and accessible
- Content is logically organized by purpose/category
- Clear, actionable output is provided
- User can immediately access any page from the output

## Intelligent Error Handling

If issues are encountered:
- **No git remote found**: Explain GitHub Pages requires GitHub repository and provide setup guidance
- **No docs directory**: Search alternate locations and suggest GitHub Pages configuration
- **No HTML files found**: Check for static site generators and suggest next steps
- **Ambiguous structure**: Provide best-effort organization with notes on uncertainty

## Enhancement Suggestions

After mapping, intelligently suggest:
- Pages that could benefit from better organization
- Markdown files worth converting to HTML for public access
- Missing index pages or navigation improvements
- GitHub Pages configuration optimizations

---

**Remember**: Your goal is to provide immediate, comprehensive visibility into all public-facing pages with zero manual effort. Make it scannable, actionable, and insightful.
