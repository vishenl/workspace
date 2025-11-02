# Mindvalley Workspace

A comprehensive workspace for Mindvalley curriculum development, data analysis, and automation tools. Built with Claude Code and powered by AI-assisted workflows.

## 📋 Overview

This repository contains tools, scripts, and documentation for:
- **Airtable Data Management**: Outcome consolidation, migration, and analysis
- **Curriculum Development**: Spiritual Mastery program evaluation and optimization
- **AI-Powered Workflows**: Custom Claude Code agents and automation scripts
- **Integration Tools**: Google Drive MCP setup and Airtable API utilities

## 🗂️ Project Structure

```
workspace/
├── docs/                   # Documentation and analysis
│   ├── airtable/          # Airtable outcomes project documentation
│   ├── curriculum/        # Curriculum analysis and evaluation reports
│   └── setup/             # Setup guides and migration notes
│
├── scripts/               # Automation scripts
│   ├── airtable/         # Airtable data processing scripts
│   └── setup/            # Environment and tool setup scripts
│
├── tools/                 # Interactive tools and viewers
│
└── .claude/              # Claude Code configuration
    ├── agents/           # Custom AI agents
    └── commands/         # Slash commands
```

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ (for MCP servers)
- Python 3.9+ (for data analysis scripts)
- Claude Desktop App (for Claude Code)
- Airtable account with API access
- GitHub CLI (optional, for repository management)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/vishenl/workspace.git
   cd workspace
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your credentials
   ```

3. **Configure Claude Code**
   - The `.claude/` directory contains pre-configured agents and commands
   - Custom agents include the Mindvalley Copywriting Strategist
   - Slash commands: `/agent`, `/commit`, `/reprompt`

## 📚 Documentation

### Airtable Projects

**[Outcomes Consolidation Analysis](docs/airtable/outcomes-consolidation-analysis.md)**
- Comprehensive analysis of 413 outcomes in Mindvalley Brain
- Consolidation strategy achieving 39.7% reduction (exceeds 20% target by 2x)
- Semantic duplicate identification and merge recommendations

**[Implementation Summary](docs/airtable/outcomes-implementation-summary.md)**
- Complete Outcomes2 table implementation details
- Migration results and distribution analysis
- Phased rollout recommendations

**[Rejected Outcomes List](docs/airtable/outcomes-rejected-list.txt)**
- List of outcomes marked for deletion
- Zero or minimal program usage validation

### Curriculum Development

**[Spiritual Mastery Evaluation](docs/curriculum/spiritual-mastery-evaluation.md)**
- Comprehensive analysis of 22-week Spiritual Mastery program
- 45 lessons reviewed with completion rate predictions
- Pedagogical assessment using AQAL and 7 Gates frameworks

**[Restructuring Options](docs/curriculum/spiritual-mastery-restructuring.md)**
- Strategic restructuring approaches for improved completion rates
- Multiple program formats analyzed (6-week, 12-week, hybrid)
- Recommendations balancing depth and engagement

### Setup Guides

**[Airtable Migration Notes](docs/setup/airtable-migration-notes.md)**
- MCP-based data migration strategies
- API key configuration and batch processing approaches

## 🔧 Scripts & Tools

### Airtable Scripts

Located in `scripts/airtable/`:

- **`migrate-outcomes.py`** - Migrate outcomes from source to Outcomes2 table
- **`add-merge-links.py`** - Create merge relationships between duplicate outcomes
- **`analyze-outcomes.py`** - Python-based outcome consolidation analysis
- **`analyze-outcomes.js`** - JavaScript alternative for outcome analysis
- **`fetch-outcomes.sh`** - Shell script for fetching outcomes via Airtable API

**Usage Example:**
```bash
# Set your Airtable API key
export AIRTABLE_API_KEY="your_key_here"

# Run migration
python scripts/airtable/migrate-outcomes.py

# Add merge relationships
python scripts/airtable/add-merge-links.py
```

### Setup Scripts

Located in `scripts/setup/`:

- **`setup-google-drive-mcp.sh`** - Complete Google Drive MCP server setup
- **`setup-google-drive-from-env.sh`** - Setup using .env credentials
- **`save-google-credentials.sh`** - Helper to save OAuth credentials

**Google Drive MCP Setup:**
```bash
# Interactive setup with browser authentication
./scripts/setup/setup-google-drive-mcp.sh

# Or use .env file
./scripts/setup/setup-google-drive-from-env.sh
```

### Interactive Tools

- **`tools/areas-of-growth-viewer.html`** - Interactive viewer for growth areas data

## 🤖 Claude Code Integration

### Custom Agents

**Mindvalley Copywriting Strategist** (`.claude/agents/mindvalley-copywriting-strategist.md`)
- Elite conversion copywriting for transformational education
- Masters Eugene Schwartz, Robert Cialdini, and Joe Sugarman frameworks
- Specialized for Mindvalley's highly educated audience (65% women, 3x graduate degree holders)
- Analyzes awareness stages, market sophistication, and psychological triggers

**Trigger Examples:**
- "Help me improve this headline for my manifestation course"
- "Create a 5-email launch sequence for our longevity program"
- "Analyze this sales page for conversion optimization"

### Slash Commands

- **`/agent`** - Elite AI Agent Generator with parallel research and advanced prompt engineering
- **`/commit`** - Create atomic git commits following conventional commit standards
- **`/reprompt`** - Veteran prompt engineer for optimizing prompts with latest techniques

## 🔐 Environment Configuration

Create a `.env` file based on `.env.example`:

```bash
# Google Drive MCP OAuth Credentials
GOOGLE_OAUTH_CREDENTIALS_JSON={"installed":{...}}

# Airtable API (if using scripts directly)
AIRTABLE_API_KEY=your_airtable_key
```

**Important:** The `.env` file is gitignored to protect your credentials.

## 📊 Key Achievements

### Outcomes Consolidation Project
- ✅ Analyzed 413 outcomes across Mindvalley Brain taxonomy
- ✅ Identified 39.7% reduction potential (exceeds 20% target by 2x)
- ✅ Created Outcomes2 table with consolidation recommendations
- ✅ 144 immediate deletion candidates identified
- ✅ 130 low-usage outcomes flagged for stakeholder review
- ✅ 3 semantic merge relationships created (with potential for 20+ more)

### Curriculum Analysis
- ✅ Comprehensive 22-week Spiritual Mastery program evaluation
- ✅ Completion rate risk assessment and optimization recommendations
- ✅ Multiple restructuring options provided (6-week, 12-week, hybrid formats)
- ✅ Pedagogical analysis using Integral Theory (AQAL) framework

## 🛠️ Technology Stack

- **AI & Automation**: Claude Code, MCP (Model Context Protocol)
- **Data Processing**: Python 3.9+, JavaScript/Node.js
- **Data Sources**: Airtable API, Google Drive API
- **Version Control**: Git, GitHub
- **Documentation**: Markdown, Interactive HTML

## 📈 Future Enhancements

- [ ] Automated outcome merge workflow with program reassignment
- [ ] Real-time curriculum completion rate tracking dashboard
- [ ] AI-powered curriculum gap analysis
- [ ] Bulk operations UI for Airtable management
- [ ] Integration with Mindvalley LMS for direct data sync

## 🤝 Contributing

This is a personal workspace repository for Mindvalley curriculum development. While it's public for transparency, it's primarily maintained by @vishenl with Claude Code assistance.

## 📝 License

This project is maintained for internal Mindvalley use. Please contact the repository owner for usage permissions.

## 🙏 Acknowledgments

- Built with [Claude Code](https://claude.com/claude-code) by Anthropic
- Powered by the Model Context Protocol (MCP)
- Airtable for flexible data management
- GitHub for version control and collaboration

---

**Last Updated:** November 2, 2025
**Maintained by:** @vishenl
**Powered by:** Claude Code + AI-assisted workflows
