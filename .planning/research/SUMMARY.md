# Project Research Summary

**Project:** AI Brain - Conversational AI Workspace
**Domain:** Multi-tenant AI workspace with document-grounded conversational AI
**Researched:** 2026-01-24
**Confidence:** HIGH

## Executive Summary

AI Brain is a multi-tenant conversational AI workspace that extends an existing React/Supabase application with document upload, RAG-based chat, and HTML output generation. The market has matured significantly since 2024 - what was experimental is now table stakes (document upload, semantic search, multi-turn context). The opportunity lies in three genuinely novel differentiators: **AI transparency** (showing document access patterns, not just citations), **permanent HTML outputs** with auto-generated URLs (competitors require manual publishing), and **network-level intelligence customization** with versioning (org-wide AI behavior tuning that no competitor offers).

The recommended approach leverages existing Supabase infrastructure (Auth, RLS, PostgreSQL) and adds pgvector for semantic search, Vercel AI SDK for streaming chat, and a RAG pipeline using OpenAI embeddings. This brownfield strategy minimizes new infrastructure while enabling sophisticated AI capabilities. The architecture follows a four-layer pattern: document ingestion (chunking, embedding, storage), conversation orchestration (RAG retrieval, context management), intelligence routing (auto-detection, prompt assembly), and output generation (HTML rendering, access control).

The critical risks center on multi-tenant security: RLS misconfiguration can cause data leakage across tenants, vector searches must be tenant-scoped (often forgotten), and LLM output requires XSS sanitization. Additionally, prompt versioning chaos and context window mismanagement can break production. Mitigations include tenant isolation from day 1 with automated tests, DOMPurify wrapper for all AI output, prompts as versioned code artifacts, and RAG-based retrieval instead of stuffing documents into context.

## Key Findings

### Recommended Stack

The existing React 18/Vite/Tailwind/Supabase stack is solid. Research recommends adding six focused libraries rather than large frameworks: **Vercel AI SDK** (streaming chat hooks), **unpdf** (serverless PDF extraction), **react-markdown + remark-gfm + rehype-highlight** (safe markdown rendering), **nanoid** (URL-friendly IDs), and optionally **isomorphic-dompurify** if rendering raw HTML from AI. The pgvector extension (already in Supabase) handles vector search without needing a separate database.

**Core technologies:**
- **Vercel AI SDK (ai + @ai-sdk/react + @ai-sdk/anthropic) ^6.0.49**: Streaming chat interface with useChat hook — de facto standard for AI chat in React, handles message state, streaming, retries, provider abstraction
- **unpdf ^0.12.x**: PDF text extraction — modern TypeScript-first library built on PDF.js, serverless-ready, specifically designed for AI/summarization use cases (avoids unmaintained pdf-parse)
- **react-markdown ^10.x + remark-gfm ^4.x + rehype-highlight ^7.x**: Markdown rendering with GitHub Flavored Markdown and syntax highlighting — safe by default (no dangerouslySetInnerHTML), lighter than Shiki for real-time chat
- **pgvector (Supabase extension)**: Vector similarity search in PostgreSQL — single database for all data, simpler than separate vector DB, supports HNSW indexing for fast retrieval
- **nanoid ^5.1.6**: Unique ID generation — 60% faster than UUID, URL-safe, 21 chars vs 36, same collision probability
- **OpenAI text-embedding-3-small (API)**: Embedding generation — 1536 dimensions, industry standard, cost-effective for RAG

**Critical version note:** Supabase JS 2.79+ requires Node 20+. Pin to 2.78.0 if deploying to Node 18 environments.

**What to avoid:** pdf-parse (unmaintained since 2019), direct @anthropic-ai/sdk in frontend (exposes API keys), Shiki (250KB+ WASM overkill), Slate.js (steep learning curve), sanitize-html (server-only, doesn't work in browser).

### Expected Features

The AI workspace market has established clear user expectations. Missing table stakes features will cause users to immediately compare unfavorably to Notion AI, Claude Projects, ChatGPT Projects, Mem.ai, and Guru.

**Must have (table stakes):**
- Document upload and ingestion (PDF, DOCX, TXT, MD, CSV minimum; 512MB per file is ChatGPT standard) — core premise of "chat with documents"
- Conversational chat interface with multi-turn context retention (200K context like Claude Projects) — users expect natural language interaction
- Semantic search / RAG (meaning-based, not keyword) — finding relevant content across documents
- Basic workspace organization (folders/projects/collections) — multiple conversations, all competitors have this
- User authentication and accounts with SSO for enterprise — multi-tenant requires identity
- Mobile responsiveness (40%+ of users on mobile) — Notion added mobile AI parity in Jan 2026
- Chat history persistence and basic export — users expect to resume conversations and get content out
- Basic permissions (private vs shared minimum) — who can see what

**Should have (competitive differentiators):**
- **AI transparency with source attribution** (MEDIUM complexity) — shows what documents AI accessed for each response, not just citations. Claude shows citations but not access patterns. Guru has verification but not real-time transparency. This is genuinely differentiating and builds enterprise trust.
- **HTML output rendering with permanent URLs** (HIGH complexity) — generates shareable web pages from conversations. Claude Artifacts requires manual publish, no competitor auto-generates permanent URLs. Significant differentiator that solves workflow friction.
- **Network-level intelligence customization with versioning** (HIGH complexity) — organization-wide AI behavior tuning. Guru has "Knowledge Agents" per team but no versioning. Claude has memory but no org-level customization. Novel combination for enterprise.
- **Granular access control on outputs** (MEDIUM complexity) — different permissions for generated content vs source docs. Standard permissions exist but output-specific ACLs are rare. Valuable for enterprise.
- Verification workflows (MEDIUM) — SME review and approval of AI outputs, critical for enterprise trust (Guru's strongest feature)
- Temporal context awareness (MEDIUM) — AI knows when information was added/updated, surfaces time-relevant content (Mem.ai pioneered this)

**Defer (v2+):**
- Real-time collaboration (multiple users in same chat/output) — HIGH complexity, ChatGPT Projects added Sep 2025, growing expectation but not critical for MVP
- API/MCP access for programmatic workspace intelligence — HIGH complexity, power users expect but can wait
- Smart Write with user knowledge (AI drafts using uploaded context) — MEDIUM complexity, Mem.ai's signature feature but not table stakes
- Advanced integrations (Slack, browser extensions) — consider for post-MVP to reduce context switching

**Anti-features to explicitly avoid:**
- "Now with AI!" badge features (generic assistants trying to do everything — novelty wears off, focus on document-centric workflows)
- Constant prompting requirements (users don't want to babysit AI — build automation and defaults)
- Unlimited context claims (technically impossible, be honest about context limits — aligns with transparency differentiator)
- Copy-paste workflow (forcing users to copy between tools — direct output generation reduces context switching)
- Complex folder hierarchies (users don't want to manually organize — AI-assisted organization, collections over hierarchies)
- Training on user data without consent (immediate trust killer, regulatory risk — clear data policy, never train without explicit opt-in)

### Architecture Approach

The architecture integrates conversational AI into the existing React/Supabase multi-tenant system using a four-layer pattern that maximizes reuse while adding pgvector for semantic search and streaming API routes for real-time chat. This RAG-enhanced conversational pattern avoids the "stuff everything in context" anti-pattern that causes poor quality, high costs, and slow responses.

**Major components:**
1. **Document ingestion layer** — chunks documents semantically (500-1000 tokens with 10% overlap), generates embeddings via OpenAI text-embedding-3-small, stores raw content + chunks in PostgreSQL with pgvector HNSW indexing. Uses async job queue (not synchronous on upload) to prevent timeouts and memory exhaustion.

2. **Conversation orchestration layer** — manages chat sessions with context retrieval (RAG), maintains conversation history with sliding window (max 10-20 messages to avoid unbounded growth), persists to PostgreSQL with full RLS tenant isolation. Includes transparency markers injected before RAG retrieval ("Accessing [Document X]... relevance: 0.89").

3. **Intelligence routing layer** — auto-detects user intent from message content (keyword matching or LLM-based classification with Haiku), selects appropriate intelligence template, assembles final prompt with system prompt + retrieved chunks + conversation history + user message. Stores intelligence versions in PostgreSQL for audit trail and rollback.

4. **Output generation layer** — converts markdown/rich text AI responses to styled HTML using templates (Mindvalley stylesheet or AI-generated layout), generates unique slug via nanoid for permanent public URLs (/o/abc123), implements granular access control (private, email, network, public) with middleware checking at URL access time.

**Critical patterns:**
- **Streaming chat with SSE** (Server-Sent Events) for real-time token streaming from Claude — improves perceived responsiveness, users see AI "thinking" in real-time
- **RAG with pgvector** using HNSW indexing and tenant-scoped queries — single database for all data, simpler architecture than separate vector DB, but requires explicit tenant_id in every vector search
- **Context budget management** with max 8K-10K tokens for retrieved chunks (not entire documents) — avoids "Lost in the Middle" problem where LLMs struggle with info buried in context
- **Prompt versioning** with semantic versioning (MAJOR for output format changes, MINOR for new capability, PATCH for wording) — prevents production failures from untracked prompt edits
- **Defense in depth for tenant isolation** — RLS policies + explicit workspace_id filtering in all queries + tenant-scoped vector namespaces

**Build order dependencies:**
1. Phase 1 (Foundation): Workspace CRUD, document upload/storage, text extraction, semantic chunking, embedding generation, pgvector setup
2. Phase 2 (Conversational AI): Chat UI with streaming, SSE API route, RAG integration, conversation persistence, intelligence CRUD, auto-detection, transparency markers
3. Phase 3 (Output Generation): Markdown to HTML conversion, template application, output storage, public URL rendering, access control, email-based sharing
4. Phase 4 (Polish & Advanced): AI panel for editing, manual text mode, intelligence versioning history, cross-network workspaces, enhanced search

### Critical Pitfalls

Research identified 11 domain-specific pitfalls across critical, moderate, and minor severity. The top 5 have the highest impact and must be addressed in corresponding phases.

1. **Multi-tenant data leakage via RLS misconfiguration** (CRITICAL) — User A sees documents/chat history belonging to User B's organization. Caused by RLS policies with USING (true), confusing auth.uid() with tenant_id, views bypassing RLS, or service role key exposed client-side. **Prevention:** Derive tenant_id from JWT (cannot be spoofed), add tenant_id to EVERY table including vector embeddings, use RLS policy template with auth.jwt() extraction, views must use security_invoker = true, never expose service_role key, namespace vector queries by tenant, automated RLS tests in CI/CD. **Address in Phase 1 (Foundation) before any document upload.**

2. **LLM output XSS/injection via unsanitized HTML rendering** (CRITICAL) — Claude generates HTML/Markdown containing malicious JavaScript that executes in browser, enabling session hijacking, data theft, CSRF attacks. Caused by dangerouslySetInnerHTML without sanitization, markdown renderers without config, prompt injection causing script tags. **Prevention:** Always use DOMPurify for any LLM output rendered as HTML with strict allowlist (ALLOWED_TAGS, FORBIDDEN_ATTR), create single SafeHTML component all devs must use, ESLint rule flagging direct dangerouslySetInnerHTML, strict CSP headers, server-side sanitization before DB storage (defense in depth). **Address in Phase 2 (AI Integration) before any LLM output is displayed.**

3. **Prompt version chaos causing production failures** (CRITICAL) — Minor prompt change breaks JSON parsing, changes output format, causes hallucinations, and nobody knows which version worked or how to rollback. Real case: 40% JSON parsing failure from 3-word change, $340K losses from 21 days of misclassification, 6-hour rollback. **Prevention:** Prompts as versioned code artifacts with semantic versioning (MAJOR/MINOR/PATCH), Zod schema validation, changelog, prompt testing in CI/CD with golden test cases, feature flags for rollout (5% of users first), centralized prompt registry with audit log, never edit prompts in production. **Address in Phase 2 (AI Integration) from day 1 — retrofitting is painful.**

4. **Context window mismanagement with large document sets** (CRITICAL) — System becomes slow, expensive, produces poor answers when users upload many documents because naive "stuff everything in context" approach fails. Caused by not understanding "Lost in the Middle" problem (LLMs struggle with info buried in middle), linear cost increase with context size (2x pricing over 200K tokens), no retrieval strategy. **Prevention:** Implement RAG with chunking (500-1000 tokens), embed chunks consistently, retrieve top-K relevant chunks only (not entire documents), smart chunking with sentence-window retrieval (embed sentence, inject surrounding context), context budget management (max 8K tokens for chunks), hierarchical retrieval for many documents (find relevant docs first, then chunks), use Claude prompt caching for repeated content (90% cost reduction), set max_tokens response limit. **Address in Phase 2-3 (AI Integration / Document Processing) before document upload goes live.**

5. **Document processing pipeline that doesn't scale** (MODERATE) — System works fine with 10 documents but falls over at 1000. Processing times go from seconds to hours, workers crash, users abandon. Caused by synchronous processing in request/response cycle, no queue/job system, single-threaded embedding generation, large files processed in memory. **Prevention:** Async processing with job queue (enqueue on upload, background worker does work), stream large files instead of loading into memory, progress webhooks or polling for user feedback, batch embedding generation (100 chunks at once), retry with exponential backoff, dead letter queue for failed documents. **Address in Phase 3 (Document Processing) — design for async from day 1.**

**Other notable pitfalls:**
- Conversation history growing unboundedly (Phase 4) — sliding window approach, summarization for long conversations
- Vector store tenant leakage (Phase 3) — tenant-scoped vector namespaces, tenant_id in every query, integration tests for isolation
- Embedding model inconsistency (Phase 3) — lock embedding model version, validate dimensions on insert, re-embed all documents on model change
- AI response latency without streaming (Phase 2) — always use streaming for user-facing responses
- Rate limit thundering herd (Phase 2) — exponential backoff on 429 errors, server-side queue with concurrency limit
- Ignoring AI output validation (Phase 2) — always validate with Zod, handle refusals explicitly, graceful degradation

## Implications for Roadmap

Based on combined research, the architecture dependencies and pitfall timing suggest a four-phase approach with clear build order and risk mitigation checkpoints.

### Phase 1: Foundation & Tenant Isolation
**Rationale:** Multi-tenant security is non-negotiable infrastructure that must precede any document upload. RLS misconfiguration causes catastrophic data breaches. This phase establishes the bedrock without AI complexity, enabling thorough testing of tenant isolation before sensitive data flows through the system.

**Delivers:**
- Multi-tenant workspace management (personal, network, cross-network types)
- Document upload UI with drag-drop (react-dropzone)
- Document storage in Supabase Storage with RLS
- Document text extraction (Claude vision for PDFs, direct for txt/md)
- Semantic chunking implementation (500-1000 tokens, 10% overlap)
- Embedding generation pipeline (OpenAI text-embedding-3-small, async job queue)
- pgvector setup with HNSW indexing and tenant-scoped retrieval functions
- Document browser UI (workspace-scoped, processing status indicators)

**Addresses (from FEATURES.md):**
- Document upload and ingestion (table stakes)
- Basic workspace organization (table stakes)
- User authentication and accounts (table stakes)
- Mobile-responsive UI (table stakes)

**Avoids (from PITFALLS.md):**
- Pitfall 1: Multi-tenant data leakage via RLS misconfiguration (CRITICAL) — tenant_id in every table, RLS policy template, automated tests
- Pitfall 5: Document processing pipeline that doesn't scale (MODERATE) — async job queue from day 1, not synchronous upload
- Pitfall 7: Vector store tenant leakage (MODERATE) — tenant-scoped pgvector queries, namespace enforcement
- Pitfall 8: Embedding model inconsistency (MODERATE) — lock embedding model version in config, store model metadata

**Uses (from STACK.md):**
- react-dropzone for file upload UI
- unpdf for PDF text extraction
- Supabase Storage for file storage
- Supabase PostgreSQL + pgvector for vector search
- OpenAI Embeddings API (text-embedding-3-small)
- nanoid for document/chunk IDs

**Acceptance criteria:**
- RLS enabled on all tables with tenant data
- No USING (true) in any RLS policy
- Service role key not in client code
- Vector queries include tenant filter in every call
- Automated cross-tenant isolation tests pass
- Document processing is async with queue and progress indicators
- Embedding model version locked and validated

### Phase 2: Conversational AI with Transparency
**Rationale:** With secure document foundation in place, add the core differentiator (AI transparency) before output generation. This phase delivers immediate value (chat with documents) while showcasing the unique transparency feature that builds trust. Streaming and prompt versioning from day 1 prevent accumulation of technical debt.

**Delivers:**
- Chat UI with streaming message display (Vercel AI SDK useChat hook)
- SSE streaming API route (/api/chat/stream)
- RAG integration (semantic search over workspace documents)
- Conversation persistence (conversations and messages tables with RLS)
- Intelligence CRUD (create, edit, list intelligences with triggers)
- Intelligence auto-detection (keyword matching or Haiku classification)
- Transparency markers in responses ("Accessing [Document X]... relevance: 0.89")
- Chat history persistence and basic export
- Context budget management (max 8K tokens for retrieved chunks, sliding window for history)

**Addresses (from FEATURES.md):**
- Conversational chat interface (table stakes)
- Multi-turn context retention (table stakes)
- Semantic search / RAG (table stakes)
- Chat history persistence and export (table stakes)
- AI transparency with source attribution (DIFFERENTIATOR - shows document access patterns, not just citations)

**Avoids (from PITFALLS.md):**
- Pitfall 2: LLM output XSS/injection (CRITICAL) — DOMPurify wrapper for all AI output, SafeHTML component, ESLint rule
- Pitfall 3: Prompt version chaos (CRITICAL) — prompts as versioned code artifacts with semantic versioning, Zod validation, testing in CI/CD
- Pitfall 4: Context window mismanagement (CRITICAL) — RAG with top-K retrieval, context budget management, no "stuff everything" approach
- Pitfall 9: AI response latency without streaming (MINOR) — always use streaming for user-facing responses
- Pitfall 10: Rate limit thundering herd (MINOR) — exponential backoff on 429 errors, server-side queue
- Pitfall 11: Ignoring AI output validation (MINOR) — Zod validation, handle refusals, graceful degradation

**Uses (from STACK.md):**
- Vercel AI SDK (ai + @ai-sdk/react + @ai-sdk/anthropic)
- react-markdown + remark-gfm + rehype-highlight for safe markdown rendering
- Anthropic Claude API (streaming)
- OpenAI Embeddings API (query embeddings)
- Supabase PostgreSQL + pgvector (vector search)

**Implements (from ARCHITECTURE.md):**
- Conversation orchestration layer (chat session manager, context retrieval)
- Intelligence routing layer (auto-detection, prompt assembly)
- LLM gateway (streaming response handler)
- Document retriever (semantic search with pgvector)

**Acceptance criteria:**
- All LLM output rendered through sanitized component (no direct dangerouslySetInnerHTML)
- Prompts versioned in code with tests and changelog
- Vector queries include tenant filter
- Streaming enabled for user-facing AI
- Rate limit handling with exponential backoff
- Output validation with Zod schemas
- Transparency markers show document sources accessed
- Context budget enforced (max tokens for chunks + history)

### Phase 3: HTML Output Generation & Access Control
**Rationale:** With high-quality AI responses proven in Phase 2, add the second major differentiator (permanent HTML outputs with auto-generated URLs). This phase transforms AI Brain from "yet another chat tool" into a content generation platform. Granular access control enables enterprise use cases (internal knowledge bases, client-facing outputs).

**Delivers:**
- Markdown to HTML conversion (react-markdown on server side)
- Template application (Mindvalley stylesheet or AI-generated layout)
- Output storage with unique slugs (nanoid-generated)
- Public URL rendering (/o/[slug])
- Access control implementation (private, email, network, public)
- Email-based sharing (output_access table with email allowlist)
- Access control middleware (checks permissions at URL access time)
- Output viewer UI (display, edit, download)
- Copy/export functionality

**Addresses (from FEATURES.md):**
- Basic export capabilities (table stakes)
- HTML output rendering with permanent URLs (DIFFERENTIATOR - auto-generated, no manual publish required)
- Granular access control on outputs (DIFFERENTIATOR - output-specific ACLs, not just document-level)

**Avoids (from PITFALLS.md):**
- Pitfall 1: Multi-tenant data leakage (CRITICAL) — RLS on outputs table, access middleware checks tenant/email
- Pitfall 2: LLM output XSS/injection (CRITICAL) — sanitize before storing HTML, CSP headers on public URLs

**Uses (from STACK.md):**
- react-markdown (server-side rendering for HTML generation)
- isomorphic-dompurify (sanitization for HTML storage and display)
- nanoid (unique slug generation for URLs)
- Supabase PostgreSQL (outputs and output_access tables with RLS)

**Implements (from ARCHITECTURE.md):**
- Output generation layer (HTML rendering, template application, slug generation)
- Access control layer (permissions middleware, email allowlist)

**Acceptance criteria:**
- Outputs table has RLS enabled with tenant isolation
- All HTML content sanitized before storage
- Unique slugs generated for all outputs
- Access control middleware checks permissions at URL access
- Email-based sharing works with allowlist
- Public URLs render with proper CSP headers
- Copy/export functionality works

### Phase 4: Advanced Features & Polish
**Rationale:** With core differentiators delivered (transparency, HTML outputs, access control), add features that improve usability and enable enterprise adoption. Intelligence versioning provides audit trails and rollback. Cross-network workspaces enable collaboration across organizational boundaries.

**Delivers:**
- AI panel for document editing (side-by-side chat and output)
- Manual text editing mode (rich text editor for outputs)
- Intelligence versioning history (intelligence_versions table, rollback UI)
- Cross-network workspaces (workspace type = cross_network, RLS policies)
- Enhanced search/filtering (full-text search over documents, date filters)
- Conversation history length limits (sliding window, summarization)
- Verification workflows (SME review and approval of outputs)

**Addresses (from FEATURES.md):**
- Network-level intelligence customization with versioning (DIFFERENTIATOR - org-wide AI behavior tuning)
- Verification workflows (competitive differentiator from Guru)

**Avoids (from PITFALLS.md):**
- Pitfall 6: Conversation history growing unboundedly (MODERATE) — sliding window approach (max 10-20 messages), summarization for long conversations

**Uses (from STACK.md):**
- Existing stack (no new major dependencies)

**Implements (from ARCHITECTURE.md):**
- Intelligence versioning system (audit trail, rollback capability)
- Cross-network workspace logic (extended RLS policies)

**Acceptance criteria:**
- Intelligence versioning with changelog and rollback
- Cross-network workspaces with proper RLS isolation
- Conversation history has length limit with summarization
- Verification workflow (if implemented) integrates with outputs

### Phase Ordering Rationale

- **Security first:** Phase 1 establishes multi-tenant isolation before any AI features. Data breaches from RLS misconfiguration are catastrophic and non-recoverable. Testing tenant isolation on static documents is easier than testing with live AI responses.

- **Value increments:** Phase 2 delivers immediate user value (chat with documents) while showcasing primary differentiator (transparency). Phase 3 adds second differentiator (HTML outputs) once AI quality is proven. Phase 4 polishes for enterprise adoption.

- **Dependency chain:** Document ingestion (Phase 1) → RAG retrieval (Phase 2) → HTML generation (Phase 3) → Intelligence versioning (Phase 4). Each phase builds on proven infrastructure from previous phases.

- **Risk mitigation timing:** Critical pitfalls (RLS, XSS, prompts, context) are addressed in phases where they emerge naturally. Moderate pitfalls (scaling, history growth) are handled in later phases when usage patterns are understood.

- **Async infrastructure early:** Phase 1 establishes job queue for document processing, preventing the need to refactor synchronous upload handling later. This architectural decision avoids "works fine with 10 docs, fails at 1000" scenarios.

- **Prompt versioning from day 1:** Phase 2 implements prompt versioning infrastructure before prompt proliferation occurs. Retrofitting versioning after 47 variants of prompts exist is painful and error-prone.

### Research Flags

Phases likely needing deeper research during planning:
- **Phase 3 (HTML Output Generation):** Complex template system requires research into layout generation strategies (AI-generated vs fixed templates), CSS injection risks, responsive design patterns for unknown content shapes
- **Phase 4 (Cross-Network Workspaces):** Niche multi-tenant pattern (workspace spanning multiple networks) has sparse documentation, may need custom RLS policy design and access control logic research

Phases with standard patterns (skip research-phase):
- **Phase 1 (Foundation):** Well-documented patterns for file upload, chunking, embedding, pgvector setup. Supabase docs are comprehensive, RAG architecture is established.
- **Phase 2 (Conversational AI):** Vercel AI SDK has excellent docs, streaming SSE is standard pattern, RAG retrieval is well-understood. Main work is integration, not research.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Recommendations verified with official documentation (Vercel AI SDK, Supabase, pgvector, OpenAI). Version compatibility matrix complete. All recommended libraries are actively maintained with recent releases. |
| Features | HIGH | Competitive analysis based on official product docs (Notion, Claude, ChatGPT, Mem.ai, Guru). Feature categorization (table stakes vs differentiators) validated across multiple authoritative sources. User expectation patterns confirmed via industry analysis. |
| Architecture | MEDIUM-HIGH | Patterns verified across multiple sources (Supabase docs, AI SDK docs, AWS/Azure multi-tenant guides). Specific implementation details (exact chunk sizes, token thresholds) are general guidance requiring validation. Database schema and RLS patterns are well-established. |
| Pitfalls | HIGH | Critical pitfalls verified with official security guides (OWASP LLM Top 10, Supabase RLS docs). Real-world failure cases documented with specific metrics ($340K losses, 40% parsing failures, 6-hour rollback). Prevention strategies validated across multiple sources. |

**Overall confidence:** HIGH

The research synthesis draws primarily from official documentation (Anthropic, OpenAI, Supabase, Vercel) and authoritative sources (OWASP, AWS, Azure). The brownfield context (existing React/Supabase stack) reduces uncertainty compared to greenfield architecture decisions. The main areas of medium confidence are specific tuning parameters (chunk sizes, token limits, similarity thresholds) that require validation during implementation but have well-documented starting points.

### Gaps to Address

**Chunk size optimization:** Research recommends 500-1000 tokens with 10% overlap based on general RAG best practices, but optimal size varies by document type (meeting notes vs technical docs vs transcripts). **Mitigation:** Start with 750 tokens and 10% overlap, implement A/B testing in Phase 2 to measure retrieval quality vs chunk size, add metrics for "answer quality" (user feedback) and "relevance scores" (cosine similarity distribution).

**Intelligence auto-detection accuracy:** Two approaches proposed (keyword matching vs LLM-based classification) with different tradeoffs (speed vs accuracy). Research doesn't provide accuracy benchmarks. **Mitigation:** Implement keyword matching first (simple, fast, deterministic), add LLM classification as fallback in Phase 2, track detection accuracy via user corrections (when user manually selects different intelligence), iterate based on usage patterns.

**Template system for HTML outputs:** Research identifies the need but doesn't specify whether to use fixed templates (Mindvalley stylesheet) or AI-generated layouts. **Mitigation:** Conduct focused research in Phase 3 planning to evaluate tradeoffs (control vs flexibility, security implications of AI-generated CSS, responsive design challenges). Consider hybrid approach (fixed base template with AI-customized content blocks).

**Context window allocation:** Research recommends max 8K tokens for retrieved chunks, but doesn't specify allocation between chunks vs conversation history vs system prompt. **Mitigation:** Implement configurable budget in Phase 2 (e.g., 60% chunks, 30% history, 10% system prompt), add monitoring for token distribution, adjust based on answer quality metrics and cost analysis.

**Cross-network workspace access control:** Phase 4 feature has sparse documentation for RLS policy design spanning multiple networks. **Mitigation:** Design RLS policies with explicit cross-network permissions table (network_cross_access with allowed_network_ids), conduct security review before implementation, add integration tests for all permission scenarios (creator, network member, cross-network member, unauthorized).

**Embedding model evolution:** OpenAI may release new embedding models (text-embedding-3-large, future versions) with different dimensions or quality. **Mitigation:** Lock model version in Phase 1 config, store embedding_model and embedding_dimensions in document_chunks metadata, design migration script template for re-embedding (can be run as background job), monitor OpenAI announcements for deprecation notices.

## Sources

### Primary (HIGH confidence)
- [Vercel AI SDK Documentation](https://ai-sdk.dev/docs/introduction) — AI SDK 6.0, useChat, streaming (STACK.md)
- [Supabase AI & Vectors Documentation](https://supabase.com/docs/guides/ai) — pgvector, RLS, embeddings (STACK.md, ARCHITECTURE.md)
- [Anthropic Claude Documentation](https://platform.claude.com/docs/) — context windows, streaming, API (STACK.md, PITFALLS.md)
- [pgvector GitHub](https://github.com/pgvector/pgvector) — HNSW indexing, vector operations (STACK.md, ARCHITECTURE.md)
- [Notion Releases](https://www.notion.com/releases/2026-01-20) — mobile AI parity, Notion 3.2 (FEATURES.md)
- [Claude Projects](https://www.anthropic.com/news/projects) — 200K context, document upload (FEATURES.md)
- [OpenAI File Uploads FAQ](https://help.openai.com/en/articles/8555545-file-uploads-faq) — 512MB limit (FEATURES.md)
- [ChatGPT Projects](https://academy.openai.com/public/clubs/work-users-ynjqu/resources/projects) — collaborative workspaces (FEATURES.md)
- [Supabase RLS Documentation](https://supabase.com/docs/guides/database/postgres/row-level-security) — tenant isolation (PITFALLS.md)
- [OWASP LLM Top 10 2025](https://genai.owasp.org/llmrisk/) — LLM05 Improper Output Handling (PITFALLS.md)

### Secondary (MEDIUM confidence)
- [Chunking Strategies for RAG - Weaviate](https://weaviate.io/blog/chunking-strategies-for-rag) — semantic chunking (ARCHITECTURE.md)
- [Multi-LLM Routing Strategies - AWS](https://aws.amazon.com/blogs/machine-learning/multi-llm-routing-strategies-for-generative-ai-applications-on-aws/) — intent detection (ARCHITECTURE.md)
- [RAG Architecture Best Practices](https://medium.com/@shekhar.manna83/rag-architecture-best-practice-vector-database-ingestion-6a7aecaa5ae4) — ingestion patterns (ARCHITECTURE.md)
- [Prompt Versioning Best Practices](https://www.getmaxim.ai/articles/prompt-versioning-best-practices-for-ai-engineering-teams/) — semantic versioning (PITFALLS.md)
- [Long Context RAG Performance](https://www.databricks.com/blog/long-context-rag-performance-llms) — context window management (PITFALLS.md)
- [Tenant Isolation Checklist](https://fixmymess.ai/blog/tenant-isolation-checklist-saas-prototypes) — multi-tenant security (PITFALLS.md)
- [RAG Tools 2026 - Meilisearch](https://www.meilisearch.com/blog/rag-tools) — framework comparison (FEATURES.md)
- [Seekr - Citation-Based AI Agents](https://www.seekr.com/blog/how-citation-based-agents-build-trust/) — enterprise trust (FEATURES.md)

### Tertiary (LOW confidence - needs validation)
- react-dropzone version (v14.x assumed based on React 16.8+ requirement in STACK.md)
- rehype-highlight version (v7.x based on ecosystem patterns in STACK.md)
- Optimal chunk size (500-1000 tokens is general guidance in ARCHITECTURE.md)
- Intelligence auto-detection trigger accuracy (pattern is sound but needs user testing in ARCHITECTURE.md)

---
*Research completed: 2026-01-24*
*Ready for roadmap: yes*
