# Domain Pitfalls: AI-Powered Conversational Workspace

**Domain:** Multi-tenant AI workspace with document upload and conversational AI
**Stack Context:** React, Supabase, Anthropic Claude
**Researched:** 2026-01-24
**Confidence:** HIGH (verified across multiple authoritative sources)

---

## Critical Pitfalls

Mistakes that cause data breaches, rewrites, or major production failures.

---

### Pitfall 1: Multi-Tenant Data Leakage via RLS Misconfiguration

**What goes wrong:** User A sees documents or chat history belonging to User B's organization. This is a catastrophic security failure in a multi-tenant system.

**Why it happens:**
- Supabase RLS policies written with `USING (true)` during prototyping, never tightened
- Confusing `auth.uid()` (user ID) with `tenant_id` (organization ID)
- Views bypass RLS by default in Postgres (they run as `security definer`)
- Queries filter by `user_id` but forget `tenant_id`, so users in same role see cross-tenant data
- Service role key accidentally exposed in client-side code, bypassing all RLS

**Consequences:**
- GDPR/HIPAA violations with massive fines
- Complete loss of customer trust
- Potential lawsuit from affected tenants
- Forced disclosure and incident response

**Warning signs:**
- RLS policies use `USING (true)` anywhere
- `service_role` key present in any client bundle or environment variable exposed to browser
- Queries don't include `tenant_id` in WHERE clauses
- No RLS tests in CI/CD pipeline
- Vector store queries (Pinecone, Qdrant, pgvector) lack tenant scoping

**Prevention:**
1. **Derive tenant_id from JWT**, not from request parameters (cannot be spoofed)
2. **Add tenant_id to EVERY table** that contains customer data, including:
   - Documents table
   - Chat messages table
   - Vector embeddings table (critical - often forgotten)
   - File storage metadata
3. **RLS policy template for all tables:**
   ```sql
   CREATE POLICY "tenant_isolation" ON documents
   FOR ALL
   USING (tenant_id = (auth.jwt() -> 'app_metadata' ->> 'tenant_id')::uuid);
   ```
4. **Views must use `security_invoker = true`** (Postgres 15+) to inherit RLS
5. **Never expose `service_role` key** - use Edge Functions for admin operations
6. **Vector store isolation:** Namespace or filter by tenant_id in every vector query
7. **Automated RLS tests:** Create test users in different tenants, verify cross-tenant access fails

**Detection (testing approach):**
```typescript
// In your test suite
test('cross-tenant isolation', async () => {
  const tenantA = await createTestTenant();
  const tenantB = await createTestTenant();
  const docA = await createDocument(tenantA, 'secret data');

  // Switch to tenant B context
  const result = await supabase
    .from('documents')
    .select()
    .eq('id', docA.id);

  expect(result.data).toHaveLength(0); // Must not see tenant A's doc
});
```

**Phase to address:** Phase 1 (Foundation) - Before any document upload feature. This is non-negotiable infrastructure.

**Sources:**
- [Supabase RLS Documentation](https://supabase.com/docs/guides/database/postgres/row-level-security)
- [Multi-Tenant Leakage: When Row-Level Security Fails](https://medium.com/@instatunnel/multi-tenant-leakage-when-row-level-security-fails-in-saas-da25f40c788c)
- [Tenant Isolation Checklist](https://fixmymess.ai/blog/tenant-isolation-checklist-saas-prototypes)

---

### Pitfall 2: LLM Output XSS/Injection via Unsanitized HTML Rendering

**What goes wrong:** Claude generates HTML/Markdown containing malicious JavaScript that executes when rendered in the user's browser, enabling session hijacking, data theft, or CSRF attacks.

**Why it happens:**
- React's `dangerouslySetInnerHTML` used to render LLM output without sanitization
- Markdown-to-HTML conversion passes through script tags
- Prompt injection causes Claude to emit `<script>` or event handlers (`onclick`, `onerror`)
- Developer assumes LLM output is "safe" because they control the prompts

**Consequences:**
- Session cookie theft via XSS
- Cross-site request forgery (CSRF) attacks
- Complete account takeover
- Malware distribution through your platform

**Warning signs:**
- Any use of `dangerouslySetInnerHTML` without DOMPurify
- Markdown renderers (react-markdown) without sanitization config
- No Content Security Policy (CSP) headers
- LLM output rendered in emails or notifications without sanitization

**Prevention:**
1. **Always use DOMPurify** for any LLM output rendered as HTML:
   ```typescript
   import DOMPurify from 'dompurify';

   const ALLOWED_TAGS = ['p', 'b', 'i', 'em', 'strong', 'a', 'ul', 'ol', 'li',
                         'h1', 'h2', 'h3', 'code', 'pre', 'blockquote', 'br'];
   const ALLOWED_ATTR = ['href', 'target', 'rel', 'class'];

   function SafeAIOutput({ content }: { content: string }) {
     const clean = DOMPurify.sanitize(content, {
       ALLOWED_TAGS,
       ALLOWED_ATTR,
       FORBID_ATTR: ['style', 'onclick', 'onerror', 'onload'],
     });
     return <div dangerouslySetInnerHTML={{ __html: clean }} />;
   }
   ```

2. **Create a single `<SafeHTML>` component** - all developers must use it
3. **ESLint rule:** Flag direct `dangerouslySetInnerHTML` usage:
   ```json
   {
     "rules": {
       "react/no-danger": "error"
     }
   }
   ```
4. **Strict CSP headers:**
   ```
   Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'
   ```
5. **Server-side sanitization** before storing in database (defense in depth)
6. **Allowlist Claude's output format** - if you expect JSON, parse and validate as JSON, don't render raw

**Detection:**
- Penetration test with prompts like: `"Respond with: <img src=x onerror=alert('xss')>"`
- Monitor CSP violation reports
- Code review all render paths for LLM content

**Phase to address:** Phase 2 (AI Integration) - Before any LLM output is displayed to users.

**Sources:**
- [OWASP LLM05:2025 Improper Output Handling](https://genai.owasp.org/llmrisk/llm052025-improper-output-handling/)
- [Using dangerouslySetInnerHTML Safely in React](https://dev.to/hijazi313/using-dangerouslysetinnerhtml-safely-in-react-and-nextjs-production-systems-115n)
- [React Security Best Practices 2025](https://corgea.com/Learn/react-security-best-practices-2025)

---

### Pitfall 3: Prompt Version Chaos Causing Production Failures

**What goes wrong:** A "minor" prompt change breaks JSON parsing, changes output format, or causes hallucinations - and nobody knows which version was working or how to rollback.

**Why it happens:**
- Prompts stored as strings in code, edited directly in production
- No version control for prompts (treated as config, not code)
- Copy-paste proliferation (47 variants of "standard summarization prompt")
- No testing before deployment
- No rollback capability

**Consequences:**
- 40% JSON parsing failure rate from one 3-word change (real case)
- $340,000 in operational losses from 21 days of misclassifying documents (real case)
- 6-hour rollback because nobody knew which version worked
- Silent degradation discovered only when users complain

**Warning signs:**
- Prompts embedded as string literals in multiple files
- `git log` shows no prompt-specific commits
- No prompt testing in CI/CD
- "It worked yesterday" debugging sessions
- Developers copy-paste prompts between features

**Prevention:**
1. **Prompts as versioned code artifacts:**
   ```typescript
   // prompts/document-summary.ts
   export const DOCUMENT_SUMMARY_PROMPT = {
     version: '2.1.0',
     template: `You are a document summarizer. Given the following document...`,
     expectedOutputFormat: 'json',
     schema: DocumentSummarySchema, // Zod schema
     changelog: [
       '2.1.0: Added structured output requirement',
       '2.0.0: Switched to JSON output',
       '1.0.0: Initial version'
     ]
   };
   ```

2. **Semantic versioning for prompts:**
   - MAJOR: Output format change (breaking)
   - MINOR: New capability added
   - PATCH: Wording refinement

3. **Prompt testing before deployment:**
   ```typescript
   describe('document-summary prompt', () => {
     const testCases = loadGoldenTestCases();

     test.each(testCases)('produces valid output for %s', async (testCase) => {
       const result = await runPrompt(DOCUMENT_SUMMARY_PROMPT, testCase.input);
       expect(() => DocumentSummarySchema.parse(result)).not.toThrow();
     });
   });
   ```

4. **Feature flags for prompt versions:**
   - Roll out new prompts to 5% of users first
   - Monitor error rates and quality metrics
   - Instant rollback capability

5. **Centralized prompt registry:**
   - Single source of truth
   - Audit log of who changed what, when
   - A/B testing infrastructure

6. **Never edit prompts in production** - always through PR with tests

**Detection:**
- Monitor LLM output parsing errors (spike = prompt regression)
- Track prompt version in logs/metrics
- Diff current prompts against last-known-good versions

**Phase to address:** Phase 2 (AI Integration) - Establish prompt versioning from day 1. Retrofitting is painful.

**Sources:**
- [Prompt Versioning: Best Practices](https://www.getmaxim.ai/articles/prompt-versioning-best-practices-for-ai-engineering-teams/)
- [PromptOps: Why Prompts Break Production More Than Code](https://www.v2solutions.com/blogs/promptops-for-engineering-leaders/)
- [Prompt Versioning, Testing, and CI/CD](https://medium.com/@mrhotfix/prompt-versioning-testing-and-ci-cd-why-your-llm-system-is-more-fragile-than-you-think-000441e57f61)

---

### Pitfall 4: Context Window Mismanagement with Large Document Sets

**What goes wrong:** System becomes slow, expensive, and produces poor answers when users upload many documents because naive "stuff everything in context" approach fails.

**Why it happens:**
- Stuffing entire documents into Claude's context window (200K tokens = ~500 pages)
- Not understanding "Lost in the Middle" problem - LLMs struggle with info buried in middle
- Linear cost increase with context size (2x pricing over 200K tokens)
- No retrieval strategy - treating LLM as search engine

**Consequences:**
- Degraded answer quality (key info lost in noise)
- Response latency increases to 30+ seconds
- API costs 10-100x higher than necessary
- Rate limit exhaustion (token-based limits)

**Warning signs:**
- Token count per request exceeds 50K regularly
- Answer quality degrades as document count increases
- API costs growing faster than user count
- Users report "Claude forgot what I just uploaded"

**Prevention:**
1. **Implement RAG (Retrieval-Augmented Generation):**
   - Chunk documents into 500-1000 token segments
   - Embed chunks with consistent embedding model
   - Retrieve top-K relevant chunks (not entire documents)
   - Only include retrieved chunks in context

2. **Smart chunking strategy:**
   ```typescript
   // Use sentence-window retrieval for better context
   const chunk = {
     content: sentence,           // What we embed
     context: surroundingSentences, // What we inject (2-3 sentences before/after)
     documentId: doc.id,
     position: index
   };
   ```

3. **Context budget management:**
   ```typescript
   const MAX_CONTEXT_TOKENS = 8000; // Leave room for response
   const MAX_CHUNKS = 10;

   function buildContext(query: string, documents: Document[]) {
     const relevant = await vectorSearch(query, MAX_CHUNKS);
     const context = relevant
       .map(chunk => chunk.context)
       .join('\n\n')
       .slice(0, MAX_CONTEXT_TOKENS * 4); // ~4 chars per token
     return context;
   }
   ```

4. **Hierarchical retrieval for many documents:**
   - First-pass: Find relevant documents
   - Second-pass: Find relevant chunks within those documents

5. **Use Claude's prompt caching** for repeated context (system prompt, static docs)
   - Cached tokens don't count toward rate limits
   - 90% cost reduction for repeated content

6. **Set `max_tokens` response limit** (2K-15K for most tasks)

**Detection:**
- Track tokens per request in monitoring
- A/B test answer quality vs. chunk count
- Monitor API costs per user

**Phase to address:** Phase 2-3 (AI Integration / Document Processing) - Before document upload goes live.

**Sources:**
- [Long Context RAG Performance of LLMs](https://www.databricks.com/blog/long-context-rag-performance-llms)
- [From RAG to Context: 2025 Review](https://ragflow.io/blog/rag-review-2025-from-rag-to-context)
- [Claude Context Windows Documentation](https://platform.claude.com/docs/en/build-with-claude/context-windows)

---

## Moderate Pitfalls

Mistakes that cause delays, technical debt, or degraded user experience.

---

### Pitfall 5: Document Processing Pipeline That Doesn't Scale

**What goes wrong:** System works fine with 10 documents but falls over when users upload 1000. Processing times go from seconds to hours. Workers crash. Users abandon.

**Why it happens:**
- Synchronous document processing in request/response cycle
- No queue or job system for background processing
- Single-threaded embedding generation
- No chunking progress feedback to users
- Large files (50MB PDFs) processed in memory

**Consequences:**
- Request timeouts during large uploads
- Memory exhaustion and worker crashes
- Users wait indefinitely with no feedback
- Supabase connection pool exhaustion

**Warning signs:**
- Document processing in API route handlers (not background jobs)
- No progress indicators during upload
- Memory usage spikes during uploads
- "Loading..." states that last minutes

**Prevention:**
1. **Async processing with job queue:**
   ```typescript
   // API route: just enqueue
   export async function POST(req: Request) {
     const { documentId } = await req.json();
     await jobQueue.enqueue('process-document', { documentId });
     return Response.json({ status: 'processing' });
   }

   // Background worker: do the work
   jobQueue.process('process-document', async (job) => {
     await extractText(job.data.documentId);
     await generateChunks(job.data.documentId);
     await generateEmbeddings(job.data.documentId);
     await updateStatus(job.data.documentId, 'ready');
   });
   ```

2. **Stream large files** instead of loading into memory
3. **Progress webhooks or polling** for user feedback
4. **Batch embedding generation** (process 100 chunks at once, not 1)
5. **Retry with exponential backoff** for transient failures
6. **Dead letter queue** for failed documents (don't lose work)

**Detection:**
- Monitor job queue depth and processing times
- Alert on jobs older than 5 minutes
- Track memory usage during uploads

**Phase to address:** Phase 3 (Document Processing) - Design for async from day 1.

---

### Pitfall 6: Conversation History Growing Unboundedly

**What goes wrong:** Long conversations become slow, expensive, and produce worse answers as the full history is sent every request.

**Why it happens:**
- Appending entire conversation history to each Claude request
- No summarization or pruning of old messages
- Storing full conversation in request payload, not database
- Not understanding token limits or "lost in the middle" problem

**Consequences:**
- Token costs grow linearly with conversation length
- Answer quality degrades after 20-30 turns
- Rate limit exhaustion on long conversations
- Latency increases significantly

**Warning signs:**
- Token count correlates with message count
- Users report "Claude forgot earlier context"
- Long conversations hit token limits
- API costs disproportionate to usage

**Prevention:**
1. **Sliding window approach:**
   ```typescript
   const MAX_HISTORY_MESSAGES = 10;

   function getConversationContext(messages: Message[]) {
     const recent = messages.slice(-MAX_HISTORY_MESSAGES);
     return recent.map(m => ({ role: m.role, content: m.content }));
   }
   ```

2. **Summarization for long conversations:**
   ```typescript
   if (messages.length > 20) {
     const oldMessages = messages.slice(0, -10);
     const summary = await summarizeConversation(oldMessages);
     // Include summary as system context, recent messages as history
   }
   ```

3. **Important fact extraction:** Pull out key facts, store in user context
4. **Semantic retrieval for history:** Vector search over past messages for relevant context
5. **Use Claude's prompt caching** for system prompt + summary (reduces tokens)

**Detection:**
- Track tokens per conversation turn
- Monitor conversation length distribution
- A/B test answer quality vs. history length

**Phase to address:** Phase 4 (Conversation Features) - Before long-running conversations are enabled.

**Sources:**
- [Managing Chat History at Scale](https://builder.aws.com/content/2j9daS4A39fteekgv9t1Hty11Qy/managing-chat-history-at-scale-in-generative-ai-chatbots)
- [KVzip: Compress LLM Conversation Memory](https://techxplore.com/news/2025-11-ai-tech-compress-llm-chatbot.html)

---

### Pitfall 7: Vector Store Tenant Leakage

**What goes wrong:** Vector similarity search returns chunks from other tenants' documents because vector queries aren't scoped by tenant.

**Why it happens:**
- Focus on Supabase RLS, forgetting vector store needs separate isolation
- Vector databases (Pinecone, Qdrant) don't have RLS
- pgvector queries bypass RLS if using wrong connection
- Embedding all tenants into single namespace

**Consequences:**
- Cross-tenant data exposure in RAG responses
- Confidential information from Company A appears in Company B's answers
- Compliance violations

**Warning signs:**
- Single vector namespace for all tenants
- Vector queries don't include tenant filter
- RAG answers reference documents user shouldn't access
- Vector DB has no access control layer

**Prevention:**
1. **Tenant-scoped vector namespaces:**
   ```typescript
   // Pinecone: use namespaces
   const namespace = `tenant-${tenantId}`;
   await index.namespace(namespace).upsert(vectors);
   await index.namespace(namespace).query({ vector, topK: 10 });

   // pgvector: include tenant_id in every query
   const { data } = await supabase.rpc('match_documents', {
     query_embedding: embedding,
     match_threshold: 0.8,
     match_count: 10,
     p_tenant_id: tenantId  // Critical!
   });
   ```

2. **pgvector function with tenant enforcement:**
   ```sql
   CREATE FUNCTION match_documents(
     query_embedding vector(1536),
     match_threshold float,
     match_count int,
     p_tenant_id uuid
   ) RETURNS TABLE(...) AS $$
     SELECT * FROM document_chunks
     WHERE tenant_id = p_tenant_id  -- Enforced, not optional
       AND embedding <=> query_embedding < (1 - match_threshold)
     ORDER BY embedding <=> query_embedding
     LIMIT match_count;
   $$ LANGUAGE sql SECURITY DEFINER;
   ```

3. **Integration tests for isolation:**
   ```typescript
   test('vector search is tenant-isolated', async () => {
     const tenantA = await createTenant();
     const tenantB = await createTenant();

     await indexDocument(tenantA, 'secret recipe for tenantA');

     const results = await vectorSearch(tenantB, 'recipe');
     expect(results).toHaveLength(0); // Must not find tenantA's doc
   });
   ```

**Phase to address:** Phase 3 (Document Processing) - When implementing RAG.

---

### Pitfall 8: Embedding Model Inconsistency

**What goes wrong:** Search quality degrades or completely fails because different embedding models are used at ingestion time vs. query time.

**Why it happens:**
- Changed embedding model without re-indexing all documents
- Different default model versions in dev vs. prod
- OpenAI silently updated embedding model
- Mixed embeddings from API and local model

**Consequences:**
- Vector similarity completely broken (comparing apples to oranges)
- Zero relevant results returned
- Subtle quality degradation that's hard to diagnose

**Warning signs:**
- Low similarity scores even for obviously related content
- Search returning random-seeming results
- Different behavior in dev vs. prod
- "Upgrade" to new embedding model broke search

**Prevention:**
1. **Lock embedding model version:**
   ```typescript
   const EMBEDDING_MODEL = 'text-embedding-3-small';
   const EMBEDDING_DIMENSIONS = 1536;

   // Store with documents
   interface DocumentChunk {
     embedding: number[];
     embedding_model: string; // Track what generated this
   }
   ```

2. **Validate dimensions on insert:**
   ```typescript
   if (embedding.length !== EMBEDDING_DIMENSIONS) {
     throw new Error(`Expected ${EMBEDDING_DIMENSIONS} dims, got ${embedding.length}`);
   }
   ```

3. **Re-embed all documents on model change** (migration required)
4. **Store embedding model version in metadata** for debugging

**Phase to address:** Phase 3 (Document Processing) - During embedding infrastructure setup.

---

## Minor Pitfalls

Mistakes that cause annoyance but are recoverable.

---

### Pitfall 9: AI Response Latency Without Streaming

**What goes wrong:** Users stare at loading spinners for 10-30 seconds while Claude generates responses, then leave.

**Why it happens:**
- Using non-streaming API and waiting for complete response
- No typing indicator or progress feedback
- Cold start delays not accounted for

**Prevention:**
1. **Always use streaming for user-facing responses:**
   ```typescript
   const stream = await anthropic.messages.stream({
     model: 'claude-sonnet-4-20250514',
     messages: [...],
   });

   for await (const chunk of stream) {
     // Send to client in real-time
   }
   ```

2. **Optimistic UI with typing indicators**
3. **Background prefetching for predictable queries**

**Phase to address:** Phase 2 (AI Integration) - Easy to do from the start.

---

### Pitfall 10: Rate Limit Thundering Herd

**What goes wrong:** Entire team hits Claude API simultaneously, exhausting rate limits, causing cascade of failures.

**Why it happens:**
- No client-side rate limiting
- Retry logic retries immediately (amplifies problem)
- All users' requests go to same API key
- No queue or backpressure mechanism

**Prevention:**
1. **Exponential backoff on 429 errors:**
   ```typescript
   async function callWithBackoff(fn: () => Promise<T>, maxRetries = 3) {
     for (let i = 0; i < maxRetries; i++) {
       try {
         return await fn();
       } catch (e) {
         if (e.status === 429) {
           await sleep(Math.pow(2, i) * 1000 + Math.random() * 1000);
         } else throw e;
       }
     }
   }
   ```

2. **Server-side request queue** with concurrency limit
3. **Per-tenant rate limiting** to prevent one tenant exhausting quota
4. **Monitor remaining rate limit** from response headers

**Phase to address:** Phase 2 (AI Integration)

**Sources:**
- [Claude API Rate Limits Documentation](https://docs.anthropic.com/en/api/rate-limits)

---

### Pitfall 11: Ignoring AI Output Validation

**What goes wrong:** Claude returns malformed JSON, unexpected format, or refusals - and the app crashes or displays garbage.

**Why it happens:**
- Assuming Claude always follows instructions perfectly
- No schema validation on LLM output
- Not handling refusal cases ("I can't help with that")
- Brittle string parsing instead of structured extraction

**Prevention:**
1. **Always validate with Zod (or similar):**
   ```typescript
   const DocumentSummary = z.object({
     title: z.string(),
     summary: z.string(),
     keyPoints: z.array(z.string()),
   });

   const result = await claude.messages.create({...});
   const parsed = DocumentSummary.safeParse(JSON.parse(result.content[0].text));

   if (!parsed.success) {
     // Handle gracefully, maybe retry with clearer instructions
   }
   ```

2. **Handle refusals explicitly:**
   ```typescript
   if (result.stop_reason === 'end_turn' &&
       result.content[0].text.includes("I can't")) {
     // Handle refusal case
   }
   ```

3. **Graceful degradation** - show error message, not crash

**Phase to address:** Phase 2 (AI Integration)

---

## Phase-Specific Warnings Summary

| Phase | Topic | Likely Pitfall | Mitigation |
|-------|-------|----------------|------------|
| 1 | Foundation | RLS misconfiguration, tenant leakage | Implement tenant isolation from day 1, automated tests |
| 2 | AI Integration | XSS from LLM output, prompt chaos, no streaming | DOMPurify wrapper, prompt versioning, streaming API |
| 3 | Document Processing | Scale failures, vector tenant leakage, embedding inconsistency | Async queues, tenant-scoped vectors, locked model versions |
| 4 | Conversations | Unbounded history, cost explosion | Sliding window, summarization, token budgets |
| 5 | Scale | Rate limit thundering herd, cost overruns | Backoff, queuing, per-tenant limits, monitoring |

---

## Detection Checklist

Before each phase ships, verify:

- [ ] RLS enabled on all tables with tenant data
- [ ] No `USING (true)` in any RLS policy
- [ ] Service role key not in client code
- [ ] All LLM output rendered through sanitized component
- [ ] Prompts versioned in code with tests
- [ ] Vector queries include tenant filter
- [ ] Document processing is async with queue
- [ ] Conversation history has length limit
- [ ] Streaming enabled for user-facing AI
- [ ] Rate limit handling with exponential backoff
- [ ] Output validation with Zod schemas

---

## Sources Summary

### Multi-Tenant Security
- [Supabase RLS Documentation](https://supabase.com/docs/guides/database/postgres/row-level-security)
- [Multi-Tenant Leakage: When Row-Level Security Fails](https://medium.com/@instatunnel/multi-tenant-leakage-when-row-level-security-fails-in-saas-da25f40c788c)
- [Tenant Isolation Checklist](https://fixmymess.ai/blog/tenant-isolation-checklist-saas-prototypes)
- [Multi-Tenant AI Leakage: Isolation & Security](https://layerxsecurity.com/generative-ai/multi-tenant-ai-leakage/)

### LLM Security
- [OWASP LLM Top 10 2025](https://deepstrike.io/blog/owasp-llm-top-10-vulnerabilities-2025)
- [OWASP LLM05:2025 Improper Output Handling](https://genai.owasp.org/llmrisk/llm052025-improper-output-handling/)
- [React Security Best Practices 2025](https://corgea.com/Learn/react-security-best-practices-2025)

### Context & RAG
- [Claude Context Windows Documentation](https://platform.claude.com/docs/en/build-with-claude/context-windows)
- [Long Context RAG Performance](https://www.databricks.com/blog/long-context-rag-performance-llms)
- [From RAG to Context: 2025 Review](https://ragflow.io/blog/rag-review-2025-from-rag-to-context)

### Prompt Engineering
- [Prompt Versioning Best Practices](https://www.getmaxim.ai/articles/prompt-versioning-best-practices-for-ai-engineering-teams/)
- [PromptOps: Why Prompts Break Production](https://www.v2solutions.com/blogs/promptops-for-engineering-leaders/)

### Document Processing
- [RAG Architecture Best Practices](https://medium.com/@shekhar.manna83/rag-architecture-best-practice-vector-database-ingestion-6a7aecaa5ae4)
- [Managing Chat History at Scale](https://builder.aws.com/content/2j9daS4A39fteekgv9t1Hty11Qy/managing-chat-history-at-scale-in-generative-ai-chatbots)
