# Technology Stack

**Project:** AI Brain - Conversational AI Workspace
**Researched:** 2026-01-24
**Research Type:** Brownfield Stack Extension

## Existing Stack (DO NOT RE-RESEARCH)

| Technology | Version | Purpose |
|------------|---------|---------|
| React | 18 | UI Framework |
| Vite | - | Build tooling |
| Tailwind CSS | - | Styling |
| Supabase Auth | - | Authentication |
| Supabase PostgreSQL | - | Database |
| Anthropic Claude | - | AI Provider |

---

## Recommended Additional Stack

### 1. AI Chat Interface

| Technology | Version | Purpose | Why | Confidence |
|------------|---------|---------|-----|------------|
| `ai` (Vercel AI SDK) | ^6.0.49 | Streaming chat, hooks, provider abstraction | De facto standard for AI chat in React. Provides `useChat` hook that handles streaming, message state, retries. Works with your existing Anthropic integration. | HIGH |
| `@ai-sdk/react` | ^6.0.x | React-specific hooks | Part of AI SDK 6. Provides `useChat`, `useCompletion`, `useObject` hooks with TypeScript support. | HIGH |
| `@ai-sdk/anthropic` | ^3.0.13 | Anthropic provider for AI SDK | Official provider. Supports Claude models, streaming, tool calling, thinking/reasoning. No need to change your Anthropic setup, just wrap it. | HIGH |

**Why AI SDK over raw Anthropic SDK:**
- `useChat` hook manages message state, streaming, auto-scrolling, error handling
- Unified interface if you later add other models (GPT-4, Gemini)
- Built-in streaming protocol that works with React
- Active development (6.0.49 released Jan 23, 2026)

**Alternative Considered:** assistant-ui
- Adds 20+ pre-built chat UI components on top of AI SDK
- Overkill if you want custom UI - better to use AI SDK directly and build your own components
- Good option if you want drop-in chat interface quickly

### 2. Document Upload & Processing

| Technology | Version | Purpose | Why | Confidence |
|------------|---------|---------|-----|------------|
| `react-dropzone` | ^14.x | File upload UI | Standard React file upload. Provides `useDropzone` hook for drag-drop + click-to-select. Not a full uploader - just the UI. | HIGH |
| `unpdf` | ^0.12.x | PDF text extraction | Modern, TypeScript-first, works in Node/browser/serverless. Built on PDF.js v5.4.394. Better than pdf-parse (unmaintained). | MEDIUM |
| Supabase Storage | (existing) | File storage | Already in your stack. Use private buckets + signed URLs for document access control. | HIGH |

**PDF Processing Strategy:**

```
Client uploads file → Supabase Storage (private bucket)
                   ↓
Server/Edge Function fetches file → unpdf extracts text
                   ↓
Text stored in PostgreSQL (for search, embedding, retrieval)
Original file remains in Storage (for download, re-processing)
```

**Why unpdf over alternatives:**
- `pdf-parse`: Unmaintained, last update 2019. Still works but risky for long-term.
- `pdfjs-dist`: More powerful (rendering, detailed parsing) but heavier and overkill for text extraction.
- `unpdf`: Modern TypeScript APIs, serverless-ready, specifically designed for AI/summarization use cases.

**For text files (.txt, .md):** No library needed. Read as string directly.

**For transcripts:** If structured (like VTT/SRT), consider simple regex parsing. If unstructured text, treat as plain text.

### 3. Markdown Rendering & Code Highlighting

| Technology | Version | Purpose | Why | Confidence |
|------------|---------|---------|-----|------------|
| `react-markdown` | ^10.x | Markdown to React | Safe by default (no dangerouslySetInnerHTML). Extensible with plugins. 100% CommonMark compliant. | HIGH |
| `remark-gfm` | ^4.x | GitHub Flavored Markdown | Tables, strikethrough, task lists, autolinks. Essential for chat that references code/lists. | HIGH |
| `rehype-highlight` | ^7.x | Code syntax highlighting | Uses highlight.js. Lighter than Shiki (which requires WASM). Good for chat where bundle size matters. | MEDIUM |

**Why react-markdown over markdown-to-jsx:**
- Better security model (builds virtual DOM, never uses dangerouslySetInnerHTML)
- Larger plugin ecosystem (remark/rehype)
- More actively maintained

**Syntax Highlighting Decision:**
- **rehype-highlight (recommended):** Lighter, client-side friendly, works with highlight.js themes
- **Shiki:** Superior quality (VS Code grammars) but 250KB+ and WASM dependency. Better for SSR/build-time.

For real-time chat, bundle size matters more than perfect highlighting. Choose rehype-highlight.

### 4. HTML Sanitization (for Output)

| Technology | Version | Purpose | Why | Confidence |
|------------|---------|---------|-----|------------|
| `isomorphic-dompurify` | ^2.x | XSS-safe HTML sanitization | Wraps DOMPurify for both client and server. Essential if you're rendering AI-generated HTML. | HIGH |

**When to use:**
- If you render raw HTML from AI (not markdown)
- If user content is embedded in outputs
- If outputs use dangerouslySetInnerHTML anywhere

**When NOT needed:**
- If you only use react-markdown (it's safe by default)
- If outputs are pure markdown transformed to React components

### 5. Unique IDs (for messages, documents, outputs)

| Technology | Version | Purpose | Why | Confidence |
|------------|---------|---------|-----|------------|
| `nanoid` | ^5.1.6 | URL-friendly unique IDs | 118 bytes, cryptographically secure, 21 chars vs UUID's 36. Perfect for shareable URLs. | HIGH |

**Why nanoid over UUID:**
- 60% faster
- Shorter IDs (21 chars vs 36)
- URL-safe by default (no encoding needed)
- Same collision probability as UUID v4

Example: `V1StGXR8_Z5jdHi6B-myT` vs `550e8400-e29b-41d4-a716-446655440000`

### 6. Supabase Realtime (for live updates)

| Technology | Version | Purpose | Why | Confidence |
|------------|---------|---------|-----|------------|
| `@supabase/supabase-js` | ^2.90.1 | Already in stack | Use existing. Has built-in realtime subscriptions. | HIGH |

**Note:** No additional libraries needed. Supabase JS client includes:
- `supabase.channel()` for custom channels
- `.on('INSERT', ...)` for table change subscriptions
- Presence for showing who's online

**Caution:** Channel names must be unique per component. If two hooks use same channel name, first gets closed.

---

## NOT Recommended (What to Avoid)

| Library | Why Avoid | Use Instead |
|---------|-----------|-------------|
| `pdf-parse` | Unmaintained since 2019 | `unpdf` |
| `pdfjs-dist` (direct) | Overkill for text extraction, complex API | `unpdf` (wraps PDF.js) |
| `@anthropic-ai/sdk` (direct in frontend) | Exposes API keys, no streaming hooks | `@ai-sdk/anthropic` |
| `Shiki` | 250KB+ WASM bundle, overkill for chat | `rehype-highlight` |
| `Slate.js` | Steep learning curve, poor Android support | Not needed if just rendering markdown |
| `react-syntax-highlighter` | Legacy, uses Prism/hljs internally | `rehype-highlight` (direct) |
| `sanitize-html` | Server-only, doesn't work in browser | `isomorphic-dompurify` |

---

## Installation

```bash
# AI Chat Interface
npm install ai @ai-sdk/react @ai-sdk/anthropic

# Document Upload & Processing
npm install react-dropzone unpdf

# Markdown Rendering
npm install react-markdown remark-gfm rehype-highlight

# HTML Sanitization (if needed)
npm install isomorphic-dompurify

# Unique IDs
npm install nanoid
```

**Dev Dependencies (if not already installed):**
```bash
npm install -D @types/dompurify
```

---

## Version Matrix

| Package | Recommended Version | Node.js | React | Notes |
|---------|---------------------|---------|-------|-------|
| `ai` | ^6.0.49 | 18+ | 18+ | AI SDK 6.0 |
| `@ai-sdk/react` | ^6.0.x | 18+ | 18+ | Part of AI SDK |
| `@ai-sdk/anthropic` | ^3.0.13 | 18+ | - | Provider package |
| `react-dropzone` | ^14.x | 16+ | 16.8+ | Hooks-based |
| `unpdf` | ^0.12.x | 20+ | - | Server-side |
| `react-markdown` | ^10.x | 16+ | 18+ | ESM-only |
| `remark-gfm` | ^4.x | 16+ | - | Markdown plugin |
| `rehype-highlight` | ^7.x | 16+ | - | Syntax plugin |
| `isomorphic-dompurify` | ^2.x | 18+ | - | Works SSR + client |
| `nanoid` | ^5.1.6 | 18+ | - | Crypto-safe IDs |
| `@supabase/supabase-js` | ^2.90.1 | 20+ | - | Dropped Node 18 in 2.79 |

**Compatibility Note:** Supabase JS 2.79+ requires Node 20+. If deploying to Node 18 environments, pin to 2.78.0.

---

## Architecture Integration

### Where Libraries Run

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT (React)                        │
├─────────────────────────────────────────────────────────────┤
│  react-dropzone     → File selection UI                      │
│  @ai-sdk/react      → useChat hook, streaming UI             │
│  react-markdown     → Render AI responses                    │
│  remark-gfm         → GFM syntax support                     │
│  rehype-highlight   → Code block highlighting                │
│  isomorphic-dompurify → Sanitize if rendering raw HTML       │
│  nanoid             → Generate message/output IDs            │
│  @supabase/supabase-js → File upload, realtime subscriptions │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   SERVER (Supabase Edge / Node)              │
├─────────────────────────────────────────────────────────────┤
│  ai                 → streamText(), AI SDK core              │
│  @ai-sdk/anthropic  → Claude integration                     │
│  unpdf              → PDF text extraction                    │
│  isomorphic-dompurify → Server-side sanitization (if SSR)    │
│  nanoid             → Generate output IDs for storage        │
│  @supabase/supabase-js → Storage access, DB writes           │
└─────────────────────────────────────────────────────────────┘
```

---

## Sources

### HIGH Confidence (Official Documentation)
- [Vercel AI SDK Documentation](https://ai-sdk.dev/docs/introduction) - AI SDK 6.0, useChat, streaming
- [AI SDK Anthropic Provider](https://ai-sdk.dev/providers/ai-sdk-providers/anthropic) - Claude integration
- [AI SDK GitHub Releases](https://github.com/vercel/ai/releases) - Version 6.0.49, Jan 2026
- [Supabase Storage Docs](https://supabase.com/docs/guides/storage/uploads/standard-uploads) - Upload patterns
- [Supabase Signed URLs](https://supabase.com/docs/reference/javascript/storage-from-createsignedurl) - Document sharing
- [react-markdown GitHub](https://github.com/remarkjs/react-markdown) - Version 10, security model
- [remark-gfm GitHub](https://github.com/remarkjs/remark-gfm) - Version 4.x
- [unpdf GitHub](https://github.com/unjs/unpdf) - PDF.js v5.4.394 serverless build
- [DOMPurify GitHub](https://github.com/cure53/DOMPurify) - v3.3.1
- [isomorphic-dompurify GitHub](https://github.com/kkomelin/isomorphic-dompurify) - SSR wrapper
- [nanoid GitHub](https://github.com/ai/nanoid) - v5.1.6, 118 bytes

### MEDIUM Confidence (Verified WebSearch)
- [7 PDF Parsing Libraries for Node.js](https://strapi.io/blog/7-best-javascript-pdf-parsing-libraries-nodejs-2025) - unpdf vs pdf-parse comparison
- [React AI Stack 2026](https://www.builder.io/blog/react-ai-stack-2026) - AI SDK ecosystem overview
- [assistant-ui GitHub](https://github.com/assistant-ui/assistant-ui) - Alternative UI library
- [Prism vs Shiki Comparison](https://npm-compare.com/highlight.js,prismjs,react-syntax-highlighter,shiki) - Syntax highlighting tradeoffs

### LOW Confidence (Needs Validation)
- react-dropzone version (v14.x assumed based on React 16.8+ requirement)
- rehype-highlight version (v7.x based on ecosystem patterns)

---

## Quick Decision Reference

| Need | Use | Version |
|------|-----|---------|
| Chat streaming | `ai` + `@ai-sdk/react` | ^6.0.x |
| Anthropic Claude | `@ai-sdk/anthropic` | ^3.0.13 |
| File drag-drop UI | `react-dropzone` | ^14.x |
| PDF text extraction | `unpdf` | ^0.12.x |
| Markdown rendering | `react-markdown` | ^10.x |
| GFM tables/lists | `remark-gfm` | ^4.x |
| Code highlighting | `rehype-highlight` | ^7.x |
| HTML sanitization | `isomorphic-dompurify` | ^2.x |
| Unique IDs | `nanoid` | ^5.1.6 |
| File storage | Supabase Storage | (existing) |
| Realtime updates | `@supabase/supabase-js` | ^2.90.1 |
