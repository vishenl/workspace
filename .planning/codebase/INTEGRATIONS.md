# External Integrations

**Analysis Date:** 2026-01-24

## APIs & External Services

**AI/LLM Services:**
- **Anthropic Claude** - Medical report analysis and learning assistant
  - SDK: `@anthropic-ai/sdk` (0.68.0 Vibrantly, 0.71.2 Learning Accelerator)
  - Auth: `ANTHROPIC_API_KEY` (required)
  - Usage: Document parsing, biomarker extraction, Eve chatbot responses
  - Models: `claude-sonnet-4-20250514`

- **OpenRouter** - LLM council voting system (optional, Vibrantly)
  - Auth: `OPENROUTER_API_KEY` (optional)
  - Usage: Multi-model consensus analysis via LLM council
  - Models: Claude Sonnet 4, GPT-4o, Gemini 2.0 Flash Exp
  - Fallback: Uses direct Anthropic API if OpenRouter unavailable

**Content & Data Management:**
- **Airtable** - Biomarker reference database (Vibrantly only)
  - SDK: `airtable` (0.12.2)
  - Auth: `AIRTABLE_API_KEY` (required for Vibrantly)
  - Base: `AIRTABLE_BASE_ID` (appPTWTOOt1hfGmFk)
  - Table: `AIRTABLE_TABLE_ID` (tbl2Y0CYIee7BYqau)
  - View: `AIRTABLE_VIEW_ID` (viwEUUA5WOTyxArN0, default "Men (45-60)")
  - Usage: Fetch biomarker definitions, reference ranges, interventions, study links
  - Endpoint: `GET /api/biomarkers`

## Data Storage

**Databases:**
- **Supabase PostgreSQL** - Both apps
  - Provider: Supabase (hosted at agtdlealucfrhvbezrxj.supabase.co)
  - Connection: `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`
  - Service Role: `SUPABASE_SERVICE_ROLE_KEY` (server-only operations)
  - Client: `@supabase/supabase-js` + `@supabase/ssr` for Next.js
  - Auth Integration: Built-in Supabase Auth via JWT

**Vibrantly Schema:**
- `profiles` - User profiles extending Supabase Auth (RLS enabled)
- `health_data` - Uploaded lab reports, health kit exports
- `biomarker_results` - Parsed biomarker values from health data
- `invites` - Admin invitation tokens for user registration

**Learning Accelerator Schema:**
- `content_sources` - Courses, podcasts, whitepapers, articles
- `content_items` - Lessons, episodes, sections within sources
- `content_progress` - User progress tracking
- `user_content_library` - User's content library management
- `insights`, `techniques`, `notes`, `quiz_questions` - Content metadata
- All tables use RLS (Row Level Security)

**File Storage:**
- Local filesystem - Development (via Node.js `fs` module)
- Assumed cloud storage in production (not configured in visible code)

**Caching:**
- None detected - Using direct database queries

## Authentication & Identity

**Auth Provider:**
- Supabase Auth (built-in PostgreSQL Auth)
  - Provider: Native email/password
  - JWT tokens stored in Supabase cookies
  - Session management via `@supabase/ssr` middleware

**Vibrantly Auth:**
- Session handling: `lib/supabase/middleware.ts` for cookie-based sessions
- Password hashing: bcryptjs (3.0.3)
- JWT signing: jsonwebtoken (9.0.2)
- Auth endpoints:
  - `POST /api/auth/register` - User registration with optional invite token
  - `POST /api/auth/login` - Email/password login
  - `POST /api/auth/logout` - Session termination
  - `GET /api/auth/me` - Current user info
  - Admin: `POST /api/admin/invite` - Generate registration invites

**Learning Accelerator Auth:**
- No explicit auth implementation visible (assumes Supabase Auth)
- Eve chat requires implicit user context

## Monitoring & Observability

**Error Tracking:**
- None detected

**Logs:**
- Console logging (development)
- Server-side logging in API routes via `console.log`
- Vibrantly logs: File upload processing, API key validation, analysis metadata

## CI/CD & Deployment

**Hosting:**
- Vercel (inferred from Next.js framework choice and @supabase/ssr patterns)

**CI Pipeline:**
- None detected (no GitHub Actions, Jenkins config visible)

## Environment Configuration

**Required env vars - Vibrantly:**
- `NEXT_PUBLIC_SUPABASE_URL` - Supabase instance URL
- `NEXT_PUBLIC_SUPABASE_ANON_KEY` - Public auth key for browser clients
- `SUPABASE_SERVICE_ROLE_KEY` - Server-only admin access
- `ANTHROPIC_API_KEY` - Claude API access
- `AIRTABLE_API_KEY` - Biomarker reference data access
- Optional: `OPENROUTER_API_KEY` - For LLM council feature

**Required env vars - Learning Accelerator:**
- `NEXT_PUBLIC_SUPABASE_URL` - Supabase instance URL
- `NEXT_PUBLIC_SUPABASE_ANON_KEY` - Public auth key for browser clients
- `SUPABASE_SERVICE_ROLE_KEY` - Server-only admin access
- `ANTHROPIC_API_KEY` - Claude API for Eve chatbot

**Secrets location:**
- `.env.local` (development) - Must be created from `.env.local.example`
- Environment variables in deployment platform (Vercel, etc.)

## Data Flow & API Patterns

**Vibrantly - Lab Report Analysis:**
1. User uploads lab report (PDF, image, or text) via `FileUploader` component
2. `POST /api/analyze` receives FormData with file
3. Server-side: Extract text using Claude's document/image vision
4. Parse text for biomarkers using either:
   - LLM Council: Query multiple models via OpenRouter, have chairman synthesize
   - Single Model: Direct Anthropic Claude
5. Return JSON array of biomarkers with confidence scores
6. Frontend saves to Supabase `health_data` and `biomarker_results` tables
7. Fetch reference ranges from `GET /api/biomarkers` (Airtable)

**Vibrantly - User Management:**
1. Admin generates invite token via `POST /api/admin/invite`
2. User registers with invite token via `POST /api/auth/register`
3. Supabase trigger auto-creates profile in `profiles` table
4. JWT stored in HttpOnly cookie
5. Middleware refreshes session on each request

**Learning Accelerator - Eve Chat:**
1. User sends message in EveChat component
2. `POST /api/eve/chat` receives message + conversation history
3. Builds system prompt with context (course, lesson, goals, memories)
4. Calls Claude Sonnet with conversation history
5. Returns response as JSON
6. TODO: Memory extraction from conversations

**Learning Accelerator - Content Management:**
1. User can add content sources (courses, podcasts, etc.)
2. `POST /api/content/save` saves source to `content_sources`
3. Optional: Intelligent parsing via `POST /api/content/intelligent-parse`
4. Quiz generation via `POST /api/quiz/generate` (Claude-powered)
5. User notes/goals/memories tracked in respective Supabase tables

## Webhooks & Callbacks

**Incoming:**
- None detected

**Outgoing:**
- None detected

## API Endpoints Reference

**Vibrantly:**
- `POST /api/analyze` - Upload lab report, get biomarker extraction
- `GET /api/biomarkers` - Fetch biomarker reference data from Airtable
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/me` - Current user profile
- `GET /api/user/profile` - User profile details
- `POST /api/user/health-data` - Save health data
- `GET /api/user/health-data` - Retrieve user's health data
- `POST /api/admin/invite` - Create registration invite (admin only)
- `GET /api/admin/users` - List all users (admin only)

**Learning Accelerator:**
- `POST /api/eve/chat` - Chat with Eve (Claude-powered)
- `GET /api/courses` - List courses
- `GET /api/courses/[courseId]` - Get course details
- `POST /api/content/sources` - Create content source
- `GET /api/content/sources` - List content sources
- `GET /api/content/sources/[sourceId]` - Get source details
- `POST /api/content/save` - Save content item
- `POST /api/content/process` - Process content
- `POST /api/content/parse-content` - Parse single content
- `POST /api/content/intelligent-parse` - AI-powered content parsing
- `POST /api/content/parse-course` - Parse entire course
- `POST /api/quiz/generate` - Generate quiz from content
- `GET /api/user/goals` - Retrieve user goals
- `POST /api/user/goals` - Save user goals
- `GET /api/user/notes` - Retrieve user notes
- `POST /api/user/notes` - Save user notes
- `GET /api/user/memories` - Retrieve Eve memories
- `POST /api/user/memories` - Save Eve memories

---

*Integration audit: 2026-01-24*
