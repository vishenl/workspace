# AI Brain

## What This Is

AI Brain is a multi-tenant, conversational AI workspace where teams centralize documents (transcripts, meeting logs, interviews, customer data) and generate polished, shareable outputs through natural language chat. Instead of scattered files across laptops and manual content creation, teams talk to AI that transparently accesses their workspace content and produces LinkedIn posts, email campaigns, reports, and more — rendered as beautiful HTML documents with permanent shareable URLs.

Built for serial entrepreneurs managing multiple companies, each "network" (company) has its own team members, workspaces, and customizable AI intelligences.

## Core Value

**Team uploads docs → chats naturally with AI → gets shareable HTML output with a URL.**

If everything else fails, this must work. A user should be able to drop documents into a workspace, ask the AI to create something, and share the result with a link.

## Requirements

### Validated

<!-- Existing boilerplate provides foundation -->

- ✓ React/Vite frontend with Tailwind CSS — existing
- ✓ Supabase Auth integration — existing
- ✓ Multi-tenant network architecture (networks, members, roles) — existing
- ✓ Basic workspace CRUD — existing
- ✓ Platform-level intelligences with network copies — existing
- ✓ Basic "Ask AI" interface — existing

### Active

<!-- Building toward these for v1 -->

**Workspace & Content:**
- [ ] Upload documents to workspace (transcripts, PDFs, meeting logs, text files)
- [ ] Display uploaded documents with metadata (name, type, upload date)
- [ ] Select/deselect specific documents for AI context

**Conversational AI:**
- [ ] Natural language chat interface in workspace
- [ ] AI shows transparency: "Accessing Document X...", "Using LinkedIn intelligence..."
- [ ] AI asks clarifying questions when ambiguous (e.g., "Which of these 3 meeting transcripts?")
- [ ] AI auto-detects appropriate intelligence based on user request
- [ ] Conversation history persisted per workspace

**Intelligence System:**
- [ ] Default intelligences ship with new networks (LinkedIn, Email, Report, Summary, etc.)
- [ ] Network admins can customize intelligence prompts
- [ ] Intelligence versioning — save versions when updating
- [ ] AI references which intelligence it's using in responses

**Output Generation:**
- [ ] AI responses appear as rich text in chat
- [ ] "Render as HTML" button converts response to styled HTML document
- [ ] "Render as MD" button converts response to Markdown
- [ ] HTML uses provided stylesheet (fallback: AI generates layout)
- [ ] Generated documents stored with permanent URLs

**Document Sharing & Access:**
- [ ] Documents get permanent shareable URLs
- [ ] Access control: private (creator only)
- [ ] Access control: specific email addresses
- [ ] Access control: all network members
- [ ] Access control: public (anyone with URL)

**Document Editing:**
- [ ] AI panel sidebar on document view — chat to edit ("Update the third paragraph...")
- [ ] Direct text editor mode — click to edit document text manually
- [ ] Edits saved to document, URL stays the same

**Multi-Tenant:**
- [ ] Personal workspaces (private to user)
- [ ] Network workspaces (shared with network members)
- [ ] Cross-network workspaces (shared across all user's networks)

### Out of Scope

- Real-time collaborative editing (Google Docs style) — complexity, defer to v2
- Mobile native app — web-first approach
- Video/audio file processing — text documents only for v1
- Billing/subscriptions — manual network creation for now
- SSO/SAML — email/password auth sufficient for v1
- Custom domains per network — single domain for v1
- API access for external integrations — internal use only for v1

## Context

**Team pain point:** Currently using separate Claude Code instances on individual laptops, manually sharing documents via Slack/email. No central repository, no shared AI context, no easy way to share polished outputs.

**Target users:**
- Mindvalley teams (marketing, events, content)
- Vibrantly team (health/wellness)
- Other portfolio companies

**Existing codebase:** Boilerplate React/Vite app with Supabase integration. Multi-tenant architecture exists. Basic workspace and intelligence CRUD implemented. Core conversational AI experience needs to be built.

**Related apps in ecosystem:**
- Vibrantly (health analytics) — similar tech stack, can share patterns
- Learning Accelerator — similar AI chat patterns

## Constraints

- **Tech stack**: React 18, Vite, Tailwind CSS, Supabase (Auth + PostgreSQL) — must use existing stack
- **AI provider**: Anthropic Claude — primary LLM, already integrated
- **Hosting**: Vercel-compatible deployment
- **Styling**: Mindvalley Design System for HTML outputs when stylesheet provided

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| HTML output over plain text | Polished, shareable reports need visual formatting | — Pending |
| Conversational AI over form-based | Natural language is faster than dropdown selection | — Pending |
| Network-level intelligence customization | Each company has different brand voice | — Pending |
| Document-level access control | Granular sharing needed for sensitive content | — Pending |

---
*Last updated: 2026-01-24 after initialization*
