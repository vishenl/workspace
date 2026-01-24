# Requirements: AI Brain

**Defined:** 2026-01-24
**Core Value:** Team uploads docs → chats naturally with AI → gets shareable HTML output with a URL

## v1 Requirements

Requirements for initial release. Each maps to roadmap phases.

### Foundation (FOUN)

- [ ] **FOUN-01**: User can create personal workspaces (private to user)
- [ ] **FOUN-02**: User can create network workspaces (shared with network members)
- [ ] **FOUN-03**: Admin can manage network membership and roles
- [ ] **FOUN-04**: All workspace data is tenant-isolated via RLS
- [ ] **FOUN-05**: Mobile-responsive UI for all workspace views

### Document Upload (DOCS)

- [ ] **DOCS-01**: User can upload documents via drag-drop (PDF, DOCX, TXT, MD, CSV)
- [ ] **DOCS-02**: System extracts text from uploaded documents
- [ ] **DOCS-03**: System chunks documents semantically (500-1000 tokens)
- [ ] **DOCS-04**: System generates embeddings for document chunks
- [ ] **DOCS-05**: User can view uploaded documents with metadata (name, type, date, status)
- [ ] **DOCS-06**: User can select/deselect documents for AI context
- [ ] **DOCS-07**: Document processing runs async with progress indicators
- [ ] **DOCS-08**: Documents are stored with tenant-scoped RLS

### Conversational AI (CHAT)

- [ ] **CHAT-01**: User can chat naturally with AI in workspace
- [ ] **CHAT-02**: AI responses stream in real-time (SSE)
- [ ] **CHAT-03**: AI retrieves relevant document chunks via RAG
- [ ] **CHAT-04**: AI shows transparency markers ("Accessing [Document X]...")
- [ ] **CHAT-05**: AI asks clarifying questions when request is ambiguous
- [ ] **CHAT-06**: Conversation history persists per workspace
- [ ] **CHAT-07**: User can view and continue past conversations
- [ ] **CHAT-08**: Context budget managed (max tokens for chunks + history)

### Intelligence System (INTL)

- [ ] **INTL-01**: Default intelligences ship with new networks (LinkedIn, Email, Report, Summary)
- [ ] **INTL-02**: AI auto-detects appropriate intelligence from user request
- [ ] **INTL-03**: AI references which intelligence it's using in responses
- [ ] **INTL-04**: Network admins can create custom intelligences
- [ ] **INTL-05**: Network admins can edit intelligence prompts
- [ ] **INTL-06**: Prompts stored as versioned artifacts with changelog

### Output Generation (OUTP)

- [ ] **OUTP-01**: AI responses appear as rich text in chat
- [ ] **OUTP-02**: "Render as HTML" button converts response to styled HTML
- [ ] **OUTP-03**: "Render as MD" button converts response to Markdown
- [ ] **OUTP-04**: HTML uses Mindvalley stylesheet (or AI-generated layout)
- [ ] **OUTP-05**: Generated outputs stored with unique slugs (nanoid)
- [ ] **OUTP-06**: Outputs get permanent shareable URLs (/o/[slug])
- [ ] **OUTP-07**: All HTML output sanitized before storage (XSS prevention)

### Access Control (ACCS)

- [ ] **ACCS-01**: Output access: private (creator only)
- [ ] **ACCS-02**: Output access: specific email addresses
- [ ] **ACCS-03**: Output access: all network members
- [ ] **ACCS-04**: Output access: public (anyone with URL)
- [ ] **ACCS-05**: Access control middleware checks permissions at URL access time
- [ ] **ACCS-06**: User can copy/export outputs

### Document Editing (EDIT)

- [ ] **EDIT-01**: AI panel sidebar on document view for chat-based editing
- [ ] **EDIT-02**: Direct text editor mode for manual editing
- [ ] **EDIT-03**: Edits saved to document, URL stays the same

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

### Advanced Features

- **ADV-01**: Cross-network workspaces (shared across all user's networks)
- **ADV-02**: Intelligence versioning history with rollback UI
- **ADV-03**: Verification workflows (SME review and approval)
- **ADV-04**: Enhanced search/filtering (full-text, date filters)
- **ADV-05**: Conversation summarization for long histories
- **ADV-06**: Real-time collaboration (multiple users in same output)
- **ADV-07**: API/MCP access for programmatic workspace intelligence
- **ADV-08**: Smart Write with user knowledge (AI drafts using context)
- **ADV-09**: Advanced integrations (Slack, browser extensions)
- **ADV-10**: SSO/SAML authentication

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
|---------|--------|
| Real-time collaborative editing | High complexity, defer to v2 |
| Mobile native app | Web-first approach |
| Video/audio file processing | Text documents only for v1 |
| Billing/subscriptions | Manual network creation for now |
| SSO/SAML | Email/password auth sufficient for v1 |
| Custom domains per network | Single domain for v1 |
| API access for external integrations | Internal use only for v1 |
| "Now with AI!" generic features | Focus on document-centric workflows |
| Unlimited context claims | Be honest about context limits |
| Training on user data | Never train without explicit opt-in |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| FOUN-01 | Phase 1 | Pending |
| FOUN-02 | Phase 1 | Pending |
| FOUN-03 | Phase 1 | Pending |
| FOUN-04 | Phase 1 | Pending |
| FOUN-05 | Phase 1 | Pending |
| DOCS-01 | Phase 1 | Pending |
| DOCS-02 | Phase 1 | Pending |
| DOCS-03 | Phase 1 | Pending |
| DOCS-04 | Phase 1 | Pending |
| DOCS-05 | Phase 1 | Pending |
| DOCS-06 | Phase 1 | Pending |
| DOCS-07 | Phase 1 | Pending |
| DOCS-08 | Phase 1 | Pending |
| CHAT-01 | Phase 2 | Pending |
| CHAT-02 | Phase 2 | Pending |
| CHAT-03 | Phase 2 | Pending |
| CHAT-04 | Phase 2 | Pending |
| CHAT-05 | Phase 2 | Pending |
| CHAT-06 | Phase 2 | Pending |
| CHAT-07 | Phase 2 | Pending |
| CHAT-08 | Phase 2 | Pending |
| INTL-01 | Phase 2 | Pending |
| INTL-02 | Phase 2 | Pending |
| INTL-03 | Phase 2 | Pending |
| INTL-04 | Phase 2 | Pending |
| INTL-05 | Phase 2 | Pending |
| INTL-06 | Phase 2 | Pending |
| OUTP-01 | Phase 3 | Pending |
| OUTP-02 | Phase 3 | Pending |
| OUTP-03 | Phase 3 | Pending |
| OUTP-04 | Phase 3 | Pending |
| OUTP-05 | Phase 3 | Pending |
| OUTP-06 | Phase 3 | Pending |
| OUTP-07 | Phase 3 | Pending |
| ACCS-01 | Phase 3 | Pending |
| ACCS-02 | Phase 3 | Pending |
| ACCS-03 | Phase 3 | Pending |
| ACCS-04 | Phase 3 | Pending |
| ACCS-05 | Phase 3 | Pending |
| ACCS-06 | Phase 3 | Pending |
| EDIT-01 | Phase 4 | Pending |
| EDIT-02 | Phase 4 | Pending |
| EDIT-03 | Phase 4 | Pending |

**Coverage:**
- v1 requirements: 40 total
- Mapped to phases: 40
- Unmapped: 0 ✓

---
*Requirements defined: 2026-01-24*
*Last updated: 2026-01-24 after research synthesis*
