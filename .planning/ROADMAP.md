# Roadmap: AI Brain

## Overview

AI Brain transforms scattered team documents into a centralized AI-powered workspace. The journey starts with secure multi-tenant document management, progresses through conversational AI with transparency (our first differentiator), adds HTML output generation with permanent URLs (our second differentiator), and culminates with document editing and intelligence versioning for enterprise readiness.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

- [ ] **Phase 1: Foundation & Document Ingestion** - Multi-tenant workspaces with secure document upload and vector search
- [ ] **Phase 2: Conversational AI with Transparency** - Streaming chat with RAG and AI transparency markers
- [ ] **Phase 3: HTML Output Generation & Access Control** - Permanent shareable URLs with granular permissions
- [ ] **Phase 4: Document Editing & Polish** - AI-assisted and manual editing, intelligence versioning

## Phase Details

### Phase 1: Foundation & Document Ingestion
**Goal**: Establish secure multi-tenant infrastructure with document upload, text extraction, semantic chunking, and vector search foundation
**Depends on**: Nothing (first phase)
**Requirements**: FOUN-01, FOUN-02, FOUN-03, FOUN-04, FOUN-05, DOCS-01, DOCS-02, DOCS-03, DOCS-04, DOCS-05, DOCS-06, DOCS-07, DOCS-08
**Success Criteria** (what must be TRUE):
  1. User can create personal and network workspaces
  2. User can upload documents (PDF, DOCX, TXT, MD, CSV) via drag-drop
  3. Documents are processed async with visible progress indicators
  4. Document chunks are embedded and stored in pgvector
  5. Cross-tenant isolation tests pass (User A cannot see User B's documents)
  6. UI is mobile-responsive
**Plans**: TBD

Plans:
- [ ] 01-01: Database schema and RLS policies
- [ ] 01-02: Workspace CRUD and document upload UI
- [ ] 01-03: Document processing pipeline (extraction, chunking, embedding)

### Phase 2: Conversational AI with Transparency
**Goal**: Deliver streaming chat with RAG-based document retrieval and AI transparency markers showing which documents are accessed
**Depends on**: Phase 1
**Requirements**: CHAT-01, CHAT-02, CHAT-03, CHAT-04, CHAT-05, CHAT-06, CHAT-07, CHAT-08, INTL-01, INTL-02, INTL-03, INTL-04, INTL-05, INTL-06
**Success Criteria** (what must be TRUE):
  1. User can chat naturally with AI about their documents
  2. AI responses stream in real-time (not waiting for full response)
  3. AI shows transparency markers ("Accessing [Document X]... relevance: 0.89")
  4. AI asks clarifying questions when request is ambiguous
  5. Conversation history persists and user can continue past conversations
  6. Default intelligences (LinkedIn, Email, Report, Summary) are available
  7. AI auto-detects and references which intelligence it's using
**Plans**: TBD

Plans:
- [ ] 02-01: Chat UI with streaming (Vercel AI SDK)
- [ ] 02-02: RAG integration and transparency markers
- [ ] 02-03: Intelligence system (CRUD, auto-detection, versioning)
- [ ] 02-04: Conversation persistence and history

### Phase 3: HTML Output Generation & Access Control
**Goal**: Transform AI responses into styled HTML documents with permanent shareable URLs and granular access control
**Depends on**: Phase 2
**Requirements**: OUTP-01, OUTP-02, OUTP-03, OUTP-04, OUTP-05, OUTP-06, OUTP-07, ACCS-01, ACCS-02, ACCS-03, ACCS-04, ACCS-05, ACCS-06
**Success Criteria** (what must be TRUE):
  1. AI responses appear as rich text in chat
  2. User can click "Render as HTML" to generate styled document
  3. User can click "Render as MD" to generate Markdown
  4. Generated output gets permanent URL (/o/[slug])
  5. User can set access: private, specific emails, network members, or public
  6. Unauthorized users cannot access private/restricted outputs
  7. User can copy/export outputs
**Plans**: TBD

Plans:
- [ ] 03-01: Output rendering (markdown to HTML, templates)
- [ ] 03-02: Permanent URLs and output storage
- [ ] 03-03: Access control system

### Phase 4: Document Editing & Polish
**Goal**: Enable editing of generated outputs via AI panel or direct text editing, plus intelligence versioning for enterprise readiness
**Depends on**: Phase 3
**Requirements**: EDIT-01, EDIT-02, EDIT-03
**Success Criteria** (what must be TRUE):
  1. User can open AI panel sidebar on any output to request changes via chat
  2. User can switch to direct text editing mode
  3. Edits are saved to the same URL (no new URL created)
  4. Intelligence changes are tracked with version history
**Plans**: TBD

Plans:
- [ ] 04-01: AI panel sidebar for chat-based editing
- [ ] 04-02: Direct text editor mode
- [ ] 04-03: Intelligence versioning history

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Foundation & Document Ingestion | 0/3 | Not started | - |
| 2. Conversational AI with Transparency | 0/4 | Not started | - |
| 3. HTML Output Generation & Access Control | 0/3 | Not started | - |
| 4. Document Editing & Polish | 0/3 | Not started | - |

---
*Roadmap created: 2026-01-24*
*Last updated: 2026-01-24 after research synthesis*
