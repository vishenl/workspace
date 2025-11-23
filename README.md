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
├── campaigns/                  # 🎯 Marketing campaigns (GitHub Pages)
│   ├── sailspain/             # Windstar cruise collaboration with Vishen
│   │   ├── southern-spain-cruise-landing-page.html
│   │   ├── southern-spain-winter-escapes-mindvalley.html
│   │   ├── southern-spain-cruise-webinar-beautiful.html
│   │   ├── southern-spain-cruise-email-templates.html
│   │   └── southern-spain-cruise-complete-marketing-proposal.md
│   ├── self-reset/            # Self Reset campaign materials
│   │   ├── self-reset-copy-strategy-guide.html
│   │   ├── self-reset-version-a-pattern-interrupt.html
│   │   └── self-reset-version-b-empathy-bridge.html
│   ├── black-friday/          # Black Friday campaign materials
│   │   ├── black-friday-exact-replica.html
│   │   └── black-friday-improved.html
│   └── spiritual-mastery/     # Spiritual Mastery program materials
│       └── spiritual-mastery-complete-curriculum.html
│
├── social-media/               # 📱 Social media strategy guides (GitHub Pages)
│   └── youtube-strategy-guide.html  # Comprehensive YouTube strategy (password: blackpanther)
│
├── reports/                    # 📊 Published analysis & conversion reports (GitHub Pages)
│   ├── index.html             # Landing page for all reports
│   ├── social-media-mastery-2025-feedback-report.html
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
│       ├── mindvalley-webinar-research.md
│       ├── southern-spain-cruise-webinar-masterclass.md
│       ├── southern-spain-cruise-email-sequences.md
│       └── duality-masterclass-email-sequences.md
│
├── scripts/                    # 🤖 Automation scripts
│   └── airtable/              # Airtable data processing scripts
│       ├── migrate-outcomes.py
│       ├── add-merge-links.py
│       ├── analyze-outcomes.py
│       └── analyze-outcomes.js
│
├── index.html                  # 🔐 Password-protected campaign hub
│
└── .claude/                    # ⚙️ Claude Code configuration
    ├── agents/                # Custom AI agents
    │   ├── mindvalley-sales-page-analyzer.md
    │   ├── mindvalley-copywriting-strategist.md
    │   ├── mindvalley-webinar-architect.md
    │   ├── mindvalley-visual-architect.md
    │   ├── mindvalley-curriculum-architect.md
    │   ├── viral-social-media-expert.md
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

## 🎯 Marketing Campaigns (GitHub Pages)

**🔐 [Campaign Hub](https://vishenl.github.io/workspace/)** (Password: `sailspain`)

### Southern Spain Cruise Campaign

**Windstar Cruise Collaboration with Vishen Lakhiani** - December 13-20, 2025

**[Landing Page](https://vishenl.github.io/workspace/campaigns/sailspain/southern-spain-cruise-landing-page.html)**
- 7-day private yacht experience: Málaga to Barcelona
- Maximum 312 guests on Star Legend
- Mediterranean Reset Protocol™ with Vishen
- 3-tier pricing: Base $4,399 | Premium +$250 | VIP +$500

**[Alternative Landing Page](https://vishenl.github.io/workspace/campaigns/sailspain/southern-spain-winter-escapes-mindvalley.html)**
- Enhanced features and animations
- Apple-level visual design
- Full conversion optimization

**[Webinar Masterclass Guide](https://vishenl.github.io/workspace/campaigns/sailspain/southern-spain-cruise-webinar-beautiful.html)**
- 90-minute webinar framework
- Mediterranean Reset Protocol positioning
- Complete Q&A and objection handling
- "Casual luxury" private yacht messaging

**[Email Templates](https://vishenl.github.io/workspace/campaigns/sailspain/southern-spain-cruise-email-templates.html)**
- 13 complete email sequences across 4 campaigns
- Launch sequence (5 emails)
- Webinar sequence (3 emails)
- Post-webinar sequence (3 emails)
- Premium/VIP upgrade sequence (2 emails)

### Self Reset Campaign

**[Copy Strategy Guide](https://vishenl.github.io/workspace/campaigns/self-reset/self-reset-copy-strategy-guide.html)**
- Strategic copy framework and positioning

**[Version A - Pattern Interrupt](https://vishenl.github.io/workspace/campaigns/self-reset/self-reset-version-a-pattern-interrupt.html)**
- Pattern interrupt approach

**[Version B - Empathy Bridge](https://vishenl.github.io/workspace/campaigns/self-reset/self-reset-version-b-empathy-bridge.html)**
- Empathy-first positioning

### Black Friday Campaign

**[Exact Replica](https://vishenl.github.io/workspace/campaigns/black-friday/black-friday-exact-replica.html)**
- Precise reproduction of original design

**[Improved Version](https://vishenl.github.io/workspace/campaigns/black-friday/black-friday-improved.html)**
- Conversion-optimized enhancements

### Spiritual Mastery Program

**[Complete Curriculum](https://vishenl.github.io/workspace/campaigns/spiritual-mastery/spiritual-mastery-complete-curriculum.html)**
- Full program structure and curriculum design

**🎯 [Pitch Performance Diagnostic](https://vishenl.github.io/workspace/campaigns/spiritual-mastery/pitch-performance-diagnostic.html)** (Password: `ocean-thunder`)
- Comprehensive analysis of Vishen's first live sales pitch delivery
- 23-minute webinar analyzed against proven conversion frameworks
- Overall Score: 7.2/10 with 15-25% conversion improvement potential
- Identifies 3 critical issues: weak opening hook (5.5/10), premature price reveal (4.0/10), weak closing CTA (5.0/10)
- Provides before/after scripts, timestamped feedback, and action items
- Projected impact: +15-35% conversion with structural changes

**📊 [Student Needs Analysis](https://vishenl.github.io/workspace/campaigns/spiritual-mastery/student-needs-analysis-mindvalley.html)** (Password: `crystal-horizon`)
- Data-driven insights from 3,484 survey responses
- Reveals top challenges: 38% struggle with consistency, losing momentum repeatedly
- Key interests: Neuroscience-backed practices (67%), advanced manifestation (64%), somatic healing (57%)
- Breakthrough desires: Quiet mind, emotional blocks cleared, clear intuition, life purpose clarity
- Validates 7-Gate System curriculum design with survey data

## 📱 Social Media Strategy

### YouTube Strategy Guide

**🎬 [YouTube Strategy & Implementation Guide](https://vishenl.github.io/workspace/social-media/youtube-strategy-guide.html)** (Password: `blackpanther`)

**Comprehensive YouTube strategy modeled after Daniel Priestley's approach:**
- Strategic positioning as consciousness entrepreneur
- 4 content pillars: Frameworks (40%), Behind-the-Scenes (25%), Experiments (20%), Guest Conversations (15%)
- Sample thumbnail mockups with Mindvalley branding
- Complete production workflow: batch recording, 2x/week publishing
- Growth roadmap: 10K subs (Month 3) → 100K (Year 1) → 250K+ (Year 2)
- Monetization funnel: YouTube → Free Masterclass → Quest Purchase → Membership
- Revenue projections: $0 (Months 1-6) → $50K/mo (Year 1) → $200K+/mo (Year 2)
- First 20 video topics ready to film
- 90-day action plan with team roles and equipment list
- Interactive charts, timelines, and visual strategy elements

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

## 🔑 Password-Protected Content

Several HTML pages are password-protected to secure sensitive strategic analysis and data:

| Page | Password | Description |
|------|----------|-------------|
| YouTube Strategy Guide | `blackpanther` | Comprehensive YouTube growth strategy |
| Campaign Hub (index.html) | `sailspain` | Main campaign hub and overview |
| Pitch Performance Diagnostic | `ocean-thunder` | Vishen's sales pitch analysis |
| Student Needs Analysis | `crystal-horizon` | 3,484 survey responses analysis |

**Note:** Passwords are stored in `.passwords.txt` (gitignored for security). Share with authorized team members only.

---

**Last Updated:** November 23, 2025
**Maintained by:** [@vishenl](https://github.com/vishenl)
**Powered by:** Claude Code + AI-assisted workflows
**Campaign Hub:** [vishenl.github.io/workspace/](https://vishenl.github.io/workspace/) (Password: sailspain)
**View Reports:** [vishenl.github.io/workspace/reports/](https://vishenl.github.io/workspace/reports/)
