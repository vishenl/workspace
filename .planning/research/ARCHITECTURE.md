# Architecture Patterns: AI Brain Conversational Workspace

**Domain:** Multi-tenant conversational AI workspace with document-grounded generation
**Researched:** 2026-01-24
**Overall Confidence:** MEDIUM-HIGH (patterns verified across multiple sources; specific implementation details require validation)

## Executive Summary

The AI Brain architecture integrates conversational AI capabilities into an existing React/Supabase multi-tenant system. The recommended architecture follows a **RAG-enhanced conversational pattern** with:

1. **Document ingestion layer** that chunks, embeds, and stores workspace documents in pgvector
2. **Conversation orchestration layer** that manages chat sessions with context retrieval
3. **Intelligence routing layer** that auto-detects and applies appropriate AI intelligences
4. **Output generation layer** that converts AI responses to styled HTML documents

This brownfield approach leverages existing Supabase infrastructure (Auth, RLS, PostgreSQL) while adding pgvector for semantic search and streaming API routes for real-time chat.

---

## Recommended Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND (React 18)                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Workspace   │  │    Chat      │  │  Document    │  │   Output     │     │
│  │   Picker     │  │  Interface   │  │   Browser    │  │   Viewer     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                 │                 │                 │              │
│         └─────────────────┴─────────────────┴─────────────────┘              │
│                                     │                                        │
│                          TanStack Query / State                              │
└─────────────────────────────────────│────────────────────────────────────────┘
                                      │ SSE / REST
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           API LAYER (Next.js App Router)                     │
├─────────────────────────────────────────────────────────────────────────────┤
│  /api/chat/stream ─────────► Streaming Chat Handler (SSE)                    │
│  /api/documents/upload ────► Document Ingestion Pipeline                     │
│  /api/documents/render ────► HTML Output Generator                           │
│  /api/intelligences ───────► Intelligence CRUD + Version Management          │
│  /api/outputs ─────────────► Generated Document Storage + Access Control     │
└─────────────────────────────────────│────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          ORCHESTRATION LAYER (lib/)                          │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌───────────────────┐  ┌───────────────────┐  ┌───────────────────┐        │
│  │   Chat Session    │  │   Intelligence    │  │   Document        │        │
│  │   Manager         │  │   Router          │  │   Retriever       │        │
│  │                   │  │                   │  │                   │        │
│  │ - Context window  │  │ - Intent detect   │  │ - Semantic search │        │
│  │ - Message history │  │ - Prompt assembly │  │ - Chunk ranking   │        │
│  │ - Memory persist  │  │ - Version select  │  │ - Citation track  │        │
│  └─────────┬─────────┘  └─────────┬─────────┘  └─────────┬─────────┘        │
│            │                      │                      │                   │
│            └──────────────────────┼──────────────────────┘                   │
│                                   │                                          │
│                    ┌──────────────▼──────────────┐                           │
│                    │     LLM Gateway             │                           │
│                    │ - Claude API (primary)      │                           │
│                    │ - Streaming response        │                           │
│                    │ - Token counting            │                           │
│                    └─────────────────────────────┘                           │
└─────────────────────────────────────│────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        DATA LAYER (Supabase + pgvector)                      │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │
│  │   workspaces    │  │   documents     │  │  document_      │              │
│  │                 │  │                 │  │  chunks         │              │
│  │ - network_id    │  │ - workspace_id  │  │                 │              │
│  │ - name, type    │  │ - name, type    │  │ - document_id   │              │
│  │ - settings      │  │ - raw_content   │  │ - content       │              │
│  └─────────────────┘  └─────────────────┘  │ - embedding     │              │
│                                            │   VECTOR(1536)  │              │
│  ┌─────────────────┐  ┌─────────────────┐  └─────────────────┘              │
│  │  conversations  │  │   messages      │                                   │
│  │                 │  │                 │  ┌─────────────────┐              │
│  │ - workspace_id  │  │ - convo_id      │  │  intelligences  │              │
│  │ - title         │  │ - role          │  │                 │              │
│  │ - created_by    │  │ - content       │  │ - network_id    │              │
│  └─────────────────┘  │ - citations[]   │  │ - name, prompt  │              │
│                       └─────────────────┘  │ - version       │              │
│  ┌─────────────────┐                       └─────────────────┘              │
│  │  outputs        │  ┌─────────────────┐                                   │
│  │                 │  │  output_access  │  Row Level Security (RLS)         │
│  │ - workspace_id  │  │                 │  enforced on all tables via       │
│  │ - html_content  │  │ - output_id     │  network_id + user_id policies    │
│  │ - public_url    │  │ - access_type   │                                   │
│  │ - access_level  │  │ - email/network │                                   │
│  └─────────────────┘  └─────────────────┘                                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Component Boundaries

| Component | Responsibility | Communicates With | Build Order |
|-----------|---------------|-------------------|-------------|
| **Workspace Picker** | Switch between personal/network/cross-network workspaces | Chat Interface, Document Browser | Phase 1 |
| **Document Browser** | Display uploaded docs, allow selection for AI context | API /documents, Chat Interface | Phase 1 |
| **Chat Interface** | Real-time conversation UI with streaming responses | API /chat/stream, Output Viewer | Phase 2 |
| **Output Viewer** | Display/edit generated HTML documents | API /outputs, Chat Interface | Phase 3 |
| **Chat Session Manager** | Maintain conversation state, history, context window | Intelligence Router, Document Retriever, LLM Gateway | Phase 2 |
| **Document Retriever** | Semantic search over workspace documents using pgvector | Supabase (document_chunks), Chat Session Manager | Phase 1 |
| **Intelligence Router** | Detect user intent, select appropriate intelligence, assemble prompt | Chat Session Manager, Supabase (intelligences) | Phase 2 |
| **LLM Gateway** | Unified interface to Claude API with streaming | Chat Session Manager, Anthropic SDK | Phase 2 |
| **Document Ingestion** | Chunk documents, generate embeddings, store in pgvector | API /documents, Supabase, OpenAI Embeddings API | Phase 1 |
| **HTML Renderer** | Convert markdown/rich text to styled HTML with template | API /outputs, Output Viewer | Phase 3 |
| **Access Control** | Manage document visibility (private/email/network/public) | Supabase RLS, API /outputs | Phase 3 |

---

## Data Flow

### 1. Document Upload Flow

```
User selects file → FileUploader Component
        │
        ▼
POST /api/documents/upload (multipart/form-data)
        │
        ├── Extract text (Claude vision for PDFs/images, direct for .txt/.md)
        │
        ├── Chunk content (semantic chunking: 500-1000 tokens, 10% overlap)
        │
        ├── Generate embeddings (OpenAI text-embedding-3-small → 1536 dimensions)
        │
        └── Store in Supabase:
            ├── documents table (raw content, metadata)
            └── document_chunks table (chunks + embeddings)
```

**Key Decision:** Use semantic chunking over fixed-size to preserve document meaning. This adds complexity but significantly improves retrieval quality for multi-topic documents like meeting transcripts.

### 2. Chat Message Flow

```
User sends message → Chat Interface
        │
        ▼
POST /api/chat/stream (Server-Sent Events)
        │
        ├── 1. Load conversation history (last N messages from `messages` table)
        │
        ├── 2. Retrieve relevant documents (semantic search on workspace's chunks)
        │       └── Top 5-10 chunks by cosine similarity
        │
        ├── 3. Detect intent + select intelligence
        │       ├── Parse user request for output type hints
        │       ├── Match against available intelligences
        │       └── Default: "General Assistant" if no match
        │
        ├── 4. Assemble prompt:
        │       ├── System prompt (intelligence template)
        │       ├── Retrieved document context (with citations)
        │       ├── Conversation history
        │       └── User message
        │
        ├── 5. Call Claude API with streaming
        │
        ├── 6. Stream tokens back to client via SSE
        │       └── Include transparency markers: "Accessing [Document X]..."
        │
        └── 7. Persist message + response to `messages` table
```

**Transparency Pattern:** Before RAG retrieval results, inject a system message like:
```
[Transparency] Accessing documents:
- Meeting Notes 2026-01-15.md (relevance: 0.89)
- Customer Interview - Sarah.txt (relevance: 0.76)
Using intelligence: LinkedIn Post Writer v2
```

### 3. Output Generation Flow

```
User clicks "Render as HTML" on AI response
        │
        ▼
POST /api/outputs/render
        │
        ├── Take markdown/rich text content
        │
        ├── Apply HTML template (Mindvalley stylesheet or AI-generated layout)
        │
        ├── Generate unique slug for public URL
        │
        ├── Store in `outputs` table:
        │       ├── html_content (rendered HTML)
        │       ├── raw_content (original markdown)
        │       ├── public_url (e.g., /o/abc123)
        │       └── access_level (private, email, network, public)
        │
        └── Return public URL to user
```

### 4. Document Access Flow

```
External user visits /o/[slug]
        │
        ▼
Middleware checks access:
        │
        ├── access_level = 'public' → Render HTML
        │
        ├── access_level = 'network' → Check if user is network member
        │       └── If yes → Render; If no → 403
        │
        ├── access_level = 'email' → Check if user email in output_access
        │       └── If yes → Render; If no → 403 (with email login prompt)
        │
        └── access_level = 'private' → Check if user is creator
                └── If yes → Render; If no → 404
```

---

## Patterns to Follow

### Pattern 1: Streaming Chat with SSE

**What:** Use Server-Sent Events for real-time token streaming from LLM
**When:** All chat interactions where user benefits from seeing response as it generates
**Why:** Improves perceived responsiveness; users see AI "thinking" in real-time

**Implementation:**

```typescript
// app/api/chat/stream/route.ts
export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

export async function POST(request: NextRequest) {
  const encoder = new TextEncoder();

  const stream = new ReadableStream({
    async start(controller) {
      // ... retrieve context, assemble prompt ...

      const response = await anthropic.messages.stream({
        model: 'claude-sonnet-4-20250514',
        max_tokens: 4096,
        system: systemPrompt,
        messages: conversationMessages,
      });

      for await (const event of response) {
        if (event.type === 'content_block_delta') {
          const text = event.delta.text;
          controller.enqueue(encoder.encode(`data: ${JSON.stringify({ text })}\n\n`));
        }
      }

      controller.enqueue(encoder.encode('data: [DONE]\n\n'));
      controller.close();
    },
  });

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
      'X-Accel-Buffering': 'no', // Prevent NGINX buffering
    },
  });
}
```

**Confidence:** HIGH (verified in Vercel AI SDK docs and multiple implementations)

### Pattern 2: RAG with pgvector

**What:** Store document embeddings in PostgreSQL using pgvector extension
**When:** Document-grounded AI conversations
**Why:** Single database for all data; simpler architecture than separate vector DB

**Implementation:**

```sql
-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Document chunks with embeddings
CREATE TABLE document_chunks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
  workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  chunk_index INTEGER NOT NULL,
  content TEXT NOT NULL,
  embedding VECTOR(1536), -- OpenAI text-embedding-3-small
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- HNSW index for fast similarity search
CREATE INDEX ON document_chunks
  USING hnsw (embedding vector_cosine_ops)
  WITH (m = 16, ef_construction = 64);

-- RLS policy: users can only query chunks in their workspace
CREATE POLICY "Workspace members can read chunks" ON document_chunks
  FOR SELECT USING (
    workspace_id IN (
      SELECT id FROM workspaces
      WHERE network_id IN (
        SELECT network_id FROM network_members WHERE user_id = auth.uid()
      )
      OR created_by = auth.uid()
    )
  );
```

**Retrieval query:**

```typescript
// lib/document-retriever.ts
async function retrieveRelevantChunks(
  workspaceId: string,
  query: string,
  limit: number = 5
): Promise<DocumentChunk[]> {
  // Generate embedding for query
  const queryEmbedding = await openai.embeddings.create({
    model: 'text-embedding-3-small',
    input: query,
  });

  const { data, error } = await supabase.rpc('match_document_chunks', {
    query_embedding: queryEmbedding.data[0].embedding,
    match_workspace_id: workspaceId,
    match_count: limit,
    match_threshold: 0.5, // Minimum similarity score
  });

  return data;
}
```

**Confidence:** HIGH (Supabase official docs, pgvector documentation)

### Pattern 3: Intelligence Auto-Detection

**What:** Analyze user request to automatically select appropriate intelligence
**When:** User doesn't explicitly specify output type
**Why:** Reduces friction; AI feels more natural

**Implementation:**

```typescript
// lib/intelligence-router.ts
interface Intelligence {
  id: string;
  name: string;
  triggers: string[];  // Keywords/phrases that trigger this intelligence
  systemPrompt: string;
}

async function detectIntelligence(
  message: string,
  availableIntelligences: Intelligence[]
): Promise<Intelligence> {
  // Option 1: Simple keyword matching (fast, no LLM call)
  for (const intel of availableIntelligences) {
    if (intel.triggers.some(t => message.toLowerCase().includes(t.toLowerCase()))) {
      return intel;
    }
  }

  // Option 2: LLM-based classification (more accurate, adds latency)
  const classification = await anthropic.messages.create({
    model: 'claude-haiku-3-20240307', // Fast, cheap model for classification
    max_tokens: 50,
    messages: [{
      role: 'user',
      content: `Classify this request into one of: ${availableIntelligences.map(i => i.name).join(', ')}

      Request: "${message}"

      Respond with just the intelligence name.`
    }],
  });

  const matchedName = classification.content[0].text.trim();
  return availableIntelligences.find(i => i.name === matchedName)
    || availableIntelligences.find(i => i.name === 'General Assistant')!;
}
```

**Confidence:** MEDIUM (pattern is sound; exact trigger mechanism needs user testing)

### Pattern 4: Conversation Memory with Context Window Management

**What:** Persist conversation history; trim when approaching context limits
**When:** Multi-turn conversations
**Why:** Maintains context while avoiding token limit errors

**Implementation:**

```typescript
// lib/chat-session-manager.ts
const MAX_CONTEXT_TOKENS = 100000; // Claude's context window

async function buildConversationContext(
  conversationId: string,
  newMessage: string,
  retrievedChunks: DocumentChunk[]
): Promise<MessageParam[]> {
  // Fetch all messages for conversation
  const { data: messages } = await supabase
    .from('messages')
    .select('role, content')
    .eq('conversation_id', conversationId)
    .order('created_at', { ascending: true });

  // Count tokens (rough estimate: 4 chars = 1 token)
  let tokenCount = estimateTokens(newMessage);
  tokenCount += retrievedChunks.reduce((acc, c) => acc + estimateTokens(c.content), 0);

  // Add messages from most recent, stopping when we hit limit
  const contextMessages: MessageParam[] = [];
  for (const msg of messages.reverse()) {
    const msgTokens = estimateTokens(msg.content);
    if (tokenCount + msgTokens > MAX_CONTEXT_TOKENS * 0.8) break; // Leave 20% buffer
    contextMessages.unshift({ role: msg.role, content: msg.content });
    tokenCount += msgTokens;
  }

  return contextMessages;
}
```

**Confidence:** HIGH (standard pattern; verified in LangChain/LangGraph docs)

---

## Anti-Patterns to Avoid

### Anti-Pattern 1: Blocking Chat Responses

**What:** Waiting for complete LLM response before showing anything
**Why bad:** Users see loading spinner for 5-30 seconds; feels broken
**Instead:** Stream tokens in real-time via SSE

### Anti-Pattern 2: Storing Full Documents as Single Chunks

**What:** Inserting entire document content as one embedding
**Why bad:** Embeddings lose semantic meaning for long texts; retrieval returns irrelevant content
**Instead:** Chunk documents semantically (500-1000 tokens) with overlap

### Anti-Pattern 3: Hardcoded Intelligence Selection

**What:** Forcing users to pick intelligence from dropdown before chatting
**Why bad:** Adds friction; interrupts natural conversation flow
**Instead:** Auto-detect from message content; show which intelligence was used

### Anti-Pattern 4: Embedding on Upload Synchronously

**What:** Generating embeddings during the upload request
**Why bad:** Long documents cause request timeouts; poor UX
**Instead:** Queue embedding jobs; show "processing" status; notify when ready

### Anti-Pattern 5: No Access Control at Query Time

**What:** Relying only on RLS; not filtering workspace context in RAG queries
**Why bad:** Cross-workspace data leakage if RLS policy has bugs
**Instead:** Always pass workspace_id to retrieval functions; defense in depth

---

## Database Schema

```sql
-- =====================================================
-- AI BRAIN WORKSPACE SCHEMA (extends existing multi-tenant)
-- =====================================================

-- Workspaces: Containers for documents and conversations
CREATE TABLE workspaces (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  network_id UUID REFERENCES networks(id) ON DELETE CASCADE,
  created_by UUID REFERENCES profiles(id) ON DELETE SET NULL,
  name TEXT NOT NULL,
  type workspace_type NOT NULL DEFAULT 'personal', -- personal, network, cross_network
  settings JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TYPE workspace_type AS ENUM ('personal', 'network', 'cross_network');

-- Documents: Raw uploaded files
CREATE TABLE documents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  uploaded_by UUID NOT NULL REFERENCES profiles(id),
  name TEXT NOT NULL,
  type TEXT NOT NULL, -- pdf, txt, md, docx
  raw_content TEXT, -- Extracted text content
  file_path TEXT, -- Supabase Storage path (optional)
  metadata JSONB DEFAULT '{}', -- size, pages, etc.
  processing_status TEXT DEFAULT 'pending', -- pending, processing, ready, failed
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Document Chunks: Semantic chunks with embeddings
CREATE TABLE document_chunks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
  workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  chunk_index INTEGER NOT NULL,
  content TEXT NOT NULL,
  embedding VECTOR(1536),
  token_count INTEGER,
  metadata JSONB DEFAULT '{}', -- heading, section, page
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Conversations: Chat sessions within workspaces
CREATE TABLE conversations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  created_by UUID NOT NULL REFERENCES profiles(id),
  title TEXT, -- Auto-generated from first message
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Messages: Individual chat messages with citations
CREATE TABLE messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
  role TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
  content TEXT NOT NULL,
  intelligence_id UUID REFERENCES intelligences(id),
  citations JSONB DEFAULT '[]', -- [{document_id, chunk_id, relevance}]
  metadata JSONB DEFAULT '{}', -- tokens, model, latency
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Intelligences: AI personality/behavior templates
CREATE TABLE intelligences (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  network_id UUID REFERENCES networks(id) ON DELETE CASCADE, -- NULL = platform default
  name TEXT NOT NULL,
  description TEXT,
  system_prompt TEXT NOT NULL,
  triggers TEXT[] DEFAULT '{}', -- Keywords for auto-detection
  is_default BOOLEAN DEFAULT FALSE,
  version INTEGER DEFAULT 1,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Intelligence Versions: Track prompt history
CREATE TABLE intelligence_versions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  intelligence_id UUID NOT NULL REFERENCES intelligences(id) ON DELETE CASCADE,
  version INTEGER NOT NULL,
  system_prompt TEXT NOT NULL,
  created_by UUID REFERENCES profiles(id),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Outputs: Generated HTML documents
CREATE TABLE outputs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  conversation_id UUID REFERENCES conversations(id),
  message_id UUID REFERENCES messages(id),
  created_by UUID NOT NULL REFERENCES profiles(id),
  title TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL, -- URL-safe identifier
  raw_content TEXT NOT NULL, -- Markdown/rich text source
  html_content TEXT NOT NULL, -- Rendered HTML
  access_level access_level_type NOT NULL DEFAULT 'private',
  stylesheet_url TEXT, -- Custom stylesheet (optional)
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TYPE access_level_type AS ENUM ('private', 'email', 'network', 'public');

-- Output Access: Email-based sharing
CREATE TABLE output_access (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  output_id UUID NOT NULL REFERENCES outputs(id) ON DELETE CASCADE,
  email TEXT NOT NULL,
  accessed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(output_id, email)
);

-- =====================================================
-- INDEXES
-- =====================================================

CREATE INDEX idx_documents_workspace ON documents(workspace_id);
CREATE INDEX idx_documents_status ON documents(processing_status);
CREATE INDEX idx_chunks_workspace ON document_chunks(workspace_id);
CREATE INDEX idx_chunks_document ON document_chunks(document_id);
CREATE INDEX idx_conversations_workspace ON conversations(workspace_id);
CREATE INDEX idx_messages_conversation ON messages(conversation_id);
CREATE INDEX idx_intelligences_network ON intelligences(network_id);
CREATE INDEX idx_outputs_slug ON outputs(slug);
CREATE INDEX idx_outputs_workspace ON outputs(workspace_id);
CREATE INDEX idx_output_access_email ON output_access(email);

-- HNSW index for vector similarity search
CREATE INDEX idx_chunks_embedding ON document_chunks
  USING hnsw (embedding vector_cosine_ops)
  WITH (m = 16, ef_construction = 64);

-- =====================================================
-- RLS POLICIES
-- =====================================================

ALTER TABLE workspaces ENABLE ROW LEVEL SECURITY;
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE document_chunks ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE intelligences ENABLE ROW LEVEL SECURITY;
ALTER TABLE outputs ENABLE ROW LEVEL SECURITY;

-- Workspace access: creator or network member
CREATE POLICY "Users can access own workspaces" ON workspaces
  FOR ALL USING (
    created_by = auth.uid() OR
    network_id IN (SELECT network_id FROM network_members WHERE user_id = auth.uid())
  );

-- Document access: follows workspace
CREATE POLICY "Users can access workspace documents" ON documents
  FOR ALL USING (
    workspace_id IN (SELECT id FROM workspaces WHERE
      created_by = auth.uid() OR
      network_id IN (SELECT network_id FROM network_members WHERE user_id = auth.uid())
    )
  );

-- Similar policies for chunks, conversations, messages...

-- =====================================================
-- FUNCTIONS
-- =====================================================

-- Semantic search function
CREATE OR REPLACE FUNCTION match_document_chunks(
  query_embedding VECTOR(1536),
  match_workspace_id UUID,
  match_count INT DEFAULT 5,
  match_threshold FLOAT DEFAULT 0.5
)
RETURNS TABLE (
  id UUID,
  document_id UUID,
  content TEXT,
  similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    dc.id,
    dc.document_id,
    dc.content,
    1 - (dc.embedding <=> query_embedding) AS similarity
  FROM document_chunks dc
  WHERE dc.workspace_id = match_workspace_id
    AND 1 - (dc.embedding <=> query_embedding) > match_threshold
  ORDER BY dc.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;
```

---

## Scalability Considerations

| Concern | At 100 users | At 10K users | At 1M users |
|---------|--------------|--------------|-------------|
| **Vector Search** | pgvector HNSW sufficient | Add read replicas; partition by network_id | Consider dedicated vector DB (Pinecone/Weaviate) |
| **LLM Latency** | Direct Anthropic calls | Add request queuing; batch similar requests | Multi-region LLM gateways; caching for common queries |
| **Document Storage** | Supabase Storage | Supabase Storage with CDN | S3 with CloudFront; tiered storage |
| **Embedding Generation** | Synchronous on upload | Background job queue (pg_cron or external) | Dedicated embedding service; batch processing |
| **Chat Sessions** | In-memory state OK | Persist to Redis for session affinity | Stateless design; all state in DB |
| **Output CDN** | Vercel Edge | Vercel Edge with caching | Multi-CDN with edge rendering |

---

## Build Order Dependencies

```
Phase 1: Document Foundation (No AI yet)
├── Workspace CRUD + multi-tenant scoping
├── Document upload + storage (Supabase Storage)
├── Document text extraction (Claude vision)
├── Semantic chunking implementation
├── Embedding generation (OpenAI)
└── pgvector setup + retrieval queries

    ⬇️ Depends on Phase 1

Phase 2: Conversational AI
├── Chat UI with streaming display
├── SSE streaming API route
├── Document retrieval integration (RAG)
├── Conversation persistence
├── Intelligence CRUD
├── Intelligence auto-detection
└── Transparency markers in responses

    ⬇️ Depends on Phase 2

Phase 3: Output Generation
├── Markdown → HTML conversion
├── Template application (stylesheet)
├── Output storage + slug generation
├── Public URL rendering
├── Access control implementation
└── Email-based sharing

    ⬇️ Depends on Phase 3

Phase 4: Polish & Advanced
├── AI panel for document editing
├── Manual text editing mode
├── Intelligence versioning history
├── Cross-network workspaces
└── Enhanced search/filtering
```

---

## Integration Points with Existing Codebase

### Reusable from Vibrantly/Learning-Accelerator

| Component | Source | Adaptation Needed |
|-----------|--------|-------------------|
| Supabase Auth | `vibrantly/lib/supabase/` | None - direct reuse |
| Multi-tenant RLS patterns | `vibrantly/supabase-schema.sql` | Extend for workspace/document tables |
| LLM API calling | `vibrantly/lib/llm-council.ts` | Simplify to single-model streaming |
| Chat UI patterns | `learning-accelerator/src/components/EveChat.tsx` | Adapt for SSE streaming |
| System prompt templating | `learning-accelerator/src/lib/eve-system-prompt.ts` | Generalize for intelligences |

### New Components Required

| Component | Why New |
|-----------|---------|
| Document ingestion pipeline | Domain-specific chunking + embedding |
| pgvector integration | New capability, not in existing codebase |
| Streaming chat API | Existing chat is non-streaming |
| HTML output renderer | Domain-specific template system |
| Access control middleware | Document-level sharing is new |

---

## Sources

**HIGH Confidence (Official Documentation):**
- [Supabase AI & Vectors Documentation](https://supabase.com/docs/guides/ai)
- [pgvector Key Features Guide 2026](https://www.instaclustr.com/education/vector-database/pgvector-key-features-tutorial-and-pros-and-cons-2026-guide/)
- [Vercel AI SDK Stream Protocols](https://ai-sdk.dev/docs/ai-sdk-ui/stream-protocol)
- [LangChain Conversation Memory Migration](https://python.langchain.com/docs/versions/migrating_memory/conversation_buffer_memory/)

**MEDIUM Confidence (Multiple Sources Agree):**
- [Multi-LLM Routing Strategies on AWS](https://aws.amazon.com/blogs/machine-learning/multi-llm-routing-strategies-for-generative-ai-applications-on-aws/)
- [Chunking Strategies for RAG - Weaviate](https://weaviate.io/blog/chunking-strategies-for-rag)
- [SSE Streaming in Next.js - Upstash](https://upstash.com/blog/sse-streaming-llm-responses)
- [RAG Models 2026 Enterprise Guide](https://www.techment.com/blogs/rag-models-2026-enterprise-ai/)

**LOW Confidence (Needs Validation):**
- Exact token thresholds for context window management
- Optimal chunk size (500-1000 tokens is general guidance)
- Intelligence auto-detection trigger accuracy

---

*Architecture research: 2026-01-24*
