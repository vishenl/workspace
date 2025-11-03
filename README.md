# Mindvalley Workspace

A comprehensive workspace for Mindvalley curriculum development, conversion analysis, data management, and automation tools. Built with Claude Code and powered by AI-assisted workflows.

## 📋 Overview

This repository contains tools, scripts, documentation, and strategic analysis for:
- **Conversion Analysis**: Homepage optimization, sales page analysis, webinar strategies
- **Airtable Data Management**: Outcome consolidation, migration, and analysis
- **Curriculum Development**: Spiritual Mastery program evaluation and optimization
- **AI-Powered Workflows**: Custom Claude Code agents and automation scripts
- **Integration Tools**: Google Drive MCP setup and Airtable API utilities

## 🗂️ Project Structure

```
workspace/
├── reports/                    # 📊 Published analysis & conversion reports (GitHub Pages)
│   ├── index.html             # Landing page for all reports
│   ├── mindvalley/            # Mindvalley-specific analyses
│   │   ├── homepage-conversion-analysis.html
│   │   └── black-friday-analysis.html
│   └── webinar/               # Webinar optimization guides
│       ├── masterclass-optimization.html
│       ├── masterclass-optimization-formatted.html
│       └── masterclass-optimization-detailed.html
│
├── tools/                      # 🛠️ Interactive tools and utilities
│   └── areas-of-growth-viewer.html
│
├── docs/                       # 📚 Documentation and research
│   ├── airtable/              # Airtable outcomes project documentation
│   ├── curriculum/            # Curriculum analysis and evaluation reports
│   ├── setup/                 # Setup guides and migration notes
│   └── guides/                # Strategic guides and best practices
│       ├── webinar-email-best-practices.md
│       ├── webinar-optimization-masterclass.md
│       ├── webinar-optimization-masterclass-detailed.md
│       └── mindvalley-webinar-research.md
│
├── scripts/                    # 🤖 Automation scripts
│   └── airtable/              # Airtable data processing scripts
│       ├── migrate-outcomes.py
│       ├── add-merge-links.py
│       ├── analyze-outcomes.py
│       └── analyze-outcomes.js
│
└── .claude/                    # ⚙️ Claude Code configuration
    ├── agents/                # Custom AI agents
    │   ├── mindvalley-sales-page-analyzer.md
    │   ├── mindvalley-copywriting-strategist.md
    │   ├── mindvalley-webinar-architect.md
    │   ├── mindvalley-visual-architect.md
    │   └── webinar-master.md
    └── commands/              # Slash commands
        ├── agent.md
        ├── commit.md
        ├── organize-and-git-push.md
        └── reprompt.md
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
   - Custom agents include 5 specialized Mindvalley agents
   - Slash commands: `/agent`, `/commit`, `/organize-and-git-push`, `/reprompt`

## 📊 Published Reports (GitHub Pages)

View all analysis reports and optimization guides:

**🌐 [Reports Landing Page](https://vishenl.github.io/workspace/reports/)**

### Mindvalley Conversion Analysis

**[Homepage Conversion Analysis](https://vishenl.github.io/workspace/reports/mindvalley/homepage-conversion-analysis.html)**
- Comprehensive conversion optimization using proven frameworks
- Score: 72/100 with 35-55% lift potential
- Revenue impact: $38-69M annually
- 10 prioritized recommendations with 3-phase implementation roadmap

**[Black Friday Sales Page Analysis](https://vishenl.github.io/workspace/reports/mindvalley/black-friday-analysis.html)**
- Strategic Black Friday campaign optimization
- Urgency mechanisms, pricing psychology, offer stacking
- Critical recommendations for peak shopping season

### Webinar Optimization Guides

**[Masterclass Optimization (Standard)](https://vishenl.github.io/workspace/reports/webinar/masterclass-optimization.html)**
- Core webinar optimization strategies for transformational education
- Essential framework for high-converting masterclasses

**[Masterclass Optimization (Formatted)](https://vishenl.github.io/workspace/reports/webinar/masterclass-optimization-formatted.html)**
- Beautifully formatted version with enhanced visuals and examples
- Interactive elements for easier implementation

**[Masterclass Optimization (Detailed)](https://vishenl.github.io/workspace/reports/webinar/masterclass-optimization-detailed.html)**
- Comprehensive deep-dive with psychological frameworks
- Advanced conversion tactics and A/B testing strategies

### Interactive Tools

**[Areas of Growth Viewer](https://vishenl.github.io/workspace/tools/areas-of-growth-viewer.html)**
- Interactive data visualization for personal development tracking
- Growth metrics across Mindvalley's transformation framework

## 📚 Documentation

### Strategic Guides

**[Webinar Email Best Practices](docs/guides/webinar-email-best-practices.md)**
- 2025 best practices for webinar email sequences
- Show-up sequences, post-webinar follow-ups, conversion tactics

**[Mindvalley Webinar Research](docs/guides/mindvalley-webinar-research.md)**
- Comprehensive research on Mindvalley's webinar strategies
- Analysis of successful masterclass patterns

### Airtable Projects

**[Outcomes Consolidation Analysis](docs/airtable/outcomes-consolidation-analysis.md)**
- Comprehensive analysis of 413 outcomes in Mindvalley Brain
- Consolidation strategy achieving 39.7% reduction (exceeds 20% target by 2x)
- Semantic duplicate identification and merge recommendations

**[Implementation Summary](docs/airtable/outcomes-implementation-summary.md)**
- Complete Outcomes2 table implementation details
- Migration results and distribution analysis
- Phased rollout recommendations

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

**[Google Drive MCP Setup](docs/setup/google-drive-mcp-setup.md)**
- Complete Google Drive MCP server configuration
- OAuth setup and troubleshooting guide

## 🔧 Scripts & Tools

### Airtable Scripts

Located in `scripts/airtable/`:

- **`migrate-outcomes.py`** - Migrate outcomes from source to Outcomes2 table
- **`add-merge-links.py`** - Create merge relationships between duplicate outcomes
- **`analyze-outcomes.py`** - Python-based outcome consolidation analysis
- **`analyze-outcomes.js`** - JavaScript alternative for outcome analysis

**Usage Example:**
```bash
# Set your Airtable API key
export AIRTABLE_API_KEY="your_key_here"

# Run migration
python scripts/airtable/migrate-outcomes.py

# Add merge relationships
python scripts/airtable/add-merge-links.py
```

## 🤖 Claude Code Integration

### Custom Agents

**Mindvalley Sales Page Analyzer** (`.claude/agents/mindvalley-sales-page-analyzer.md`)
- Expert in Hormozi's offer model, Sugarman's slippery slope, Schwartz's frameworks
- Analyzes sales pages, landing pages, membership offers
- Provides conversion optimization with brand essence preservation

**Mindvalley Copywriting Strategist** (`.claude/agents/mindvalley-copywriting-strategist.md`)
- Elite conversion copywriting for transformational education
- Masters Eugene Schwartz, Robert Cialdini, and Joe Sugarman frameworks
- Specialized for Mindvalley's highly educated audience

**Mindvalley Webinar Architect** (`.claude/agents/mindvalley-webinar-architect.md`)
- Designs, structures, and optimizes webinars and masterclasses
- Expert in Mindvalley's science-meets-spirituality positioning
- Balances sophistication with transformation promise

**Mindvalley Visual Architect** (`.claude/agents/mindvalley-visual-architect.md`)
- Creates gorgeous, visually stunning websites with Apple-level aesthetics
- Premium brand design with Mindvalley guidelines
- Crisp typography, stunning photography, elegant animations

**Webinar Master** (`.claude/agents/webinar-master.md`)
- Optimizes webinars for personal growth and transformation industry
- Acts as webinar director, scriptwriter, conversion strategist
- Email sequence specialist for show-up and post-webinar campaigns

### Slash Commands

- **`/agent`** - Elite AI Agent Generator with parallel research and advanced prompt engineering
- **`/commit`** - Create atomic git commits following conventional commit standards
- **`/organize-and-git-push`** - Intelligently organize project and push to GitHub with Pages links
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

## 📈 Key Achievements

### Conversion Analysis
- ✅ Mindvalley homepage analysis: 72/100 score with $38-69M revenue potential
- ✅ Black Friday sales page strategic recommendations
- ✅ 3 comprehensive webinar optimization guides published
- ✅ Framework synthesis: Hormozi, Schwartz, Sugarman, Cialdini

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
- **Frameworks**: Hormozi Value Equation, Schwartz Market Sophistication, Sugarman Psychological Triggers

## 📊 Revenue Impact Summary

| Analysis | Potential Impact | Implementation Time |
|----------|-----------------|-------------------|
| Homepage Conversion | $38-69M annually | 6 weeks (3 phases) |
| Black Friday Campaign | TBD | 1-2 weeks |
| Webinar Optimization | Varies by deployment | Ongoing |
| **Total Identified Opportunity** | **$107M+ combined** | **Phased rollout** |

## 🌐 GitHub Pages Deployment

All HTML reports are automatically published via GitHub Pages:

- **Reports Landing Page**: [vishenl.github.io/workspace/reports/](https://vishenl.github.io/workspace/reports/)
- **Base URL**: `https://vishenl.github.io/workspace/`
- **Deployment**: Automatic on push to main branch
- **Latency**: 1-2 minutes after push

## 📈 Future Enhancements

- [ ] Automated outcome merge workflow with program reassignment
- [ ] Real-time curriculum completion rate tracking dashboard
- [ ] AI-powered curriculum gap analysis
- [ ] Bulk operations UI for Airtable management
- [ ] Integration with Mindvalley LMS for direct data sync
- [ ] A/B testing implementation for homepage recommendations
- [ ] Webinar email sequence automation tools

## 🤝 Contributing

This is a personal workspace repository for Mindvalley curriculum development and strategic analysis. While it's public for transparency, it's primarily maintained by @vishenl with Claude Code assistance.

## 📝 License

This project is maintained for internal Mindvalley use. Please contact the repository owner for usage permissions.

## 🙏 Acknowledgments

- Built with [Claude Code](https://claude.com/claude-code) by Anthropic
- Powered by the Model Context Protocol (MCP)
- Airtable for flexible data management
- GitHub for version control and GitHub Pages hosting
- Conversion frameworks: Alex Hormozi, Eugene Schwartz, Joe Sugarman, Robert Cialdini

---

**Last Updated:** November 3, 2025
**Maintained by:** [@vishenl](https://github.com/vishenl)
**Powered by:** Claude Code + AI-assisted workflows
**View Reports:** [vishenl.github.io/workspace/reports/](https://vishenl.github.io/workspace/reports/)
