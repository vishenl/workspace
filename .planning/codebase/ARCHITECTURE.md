# Architecture

**Analysis Date:** 2026-01-24

## Pattern Overview

**Overall:** Full-stack Next.js application with hybrid persistence (JSON file-based + Supabase integration) and multi-model LLM analysis.

**Key Characteristics:**
- Server-side API endpoints (App Router pattern)
- Client-side React components with client-side state management
- Hybrid data persistence: Local JSON files for fast MVP, Supabase integration for production scaling
- LLM Council pattern: Multi-model consensus analysis for medical data extraction
- Document processing: PDF/image text extraction with Claude, biomarker parsing with multi-model validation

## Layers

**Presentation Layer (Pages & Components):**
- Purpose: Server-rendered landing pages and client-side interactive dashboards
- Location: `app/page.tsx` (homepage), `app/[route]/page.tsx` (all other pages)
- Contains: React pages, form components, dashboard charts, navigation
- Depends on: API routes, client-side state
- Used by: Web browsers

**API Layer:**
- Purpose: HTTP endpoints handling authentication, health data, analysis
- Location: `app/api/[route]/route.ts`
- Contains: Auth handlers, file upload processing, biomarker analysis, health data CRUD
- Depends on: Database layer, LLM services, Airtable, Supabase
- Used by: Frontend pages, external integrations

**Business Logic Layer:**
- Purpose: Core algorithms and analysis routines
- Location: `lib/llm-council.ts` (multi-model analysis), `lib/db.ts` (data access)
- Contains: LLM Council orchestration, JSON file persistence, session management
- Depends on: External APIs (OpenRouter, Anthropic), filesystem
- Used by: API routes

**Infrastructure Layer:**
- Purpose: External service integrations and configuration
- Location: `lib/auth.ts` (auth helpers), `lib/supabase/` (Supabase client)
- Contains: Authentication middleware, Supabase client initialization, environment config
- Depends on: Supabase SDK, cookies, Next.js utilities
- Used by: API routes, middleware

## Data Flow

**Authentication Flow:**

1. User submits email/password at `app/register` or `app/login`
2. Form POSTs to `app/api/auth/register` or `app/api/auth/login`
3. Route handler creates user in JSON file (`lib/db.ts` → `data/users.json`) or validates against Supabase
4. Session created in `data/sessions.json` with 7-day expiry
5. Session ID stored in `vibrantly_session` cookie
6. Middleware (`middleware.ts`) validates session on each request
7. Protected routes call `requireAuth()` from `lib/auth.ts` to check session

**Lab Report Analysis Flow:**

1. User selects file at `app/upload` (FileUploader component)
2. FormData posted to `app/api/analyze/route.ts` with file + `useCouncil` flag
3. **Stage 1: Text Extraction** - Claude vision model extracts text from PDF/image via Anthropic API
4. **Stage 2: Multi-Model Analysis** - Three LLM Council models query in parallel via OpenRouter:
   - `anthropic/claude-sonnet-4-20250514`
   - `openai/gpt-4o`
   - `google/gemini-2.0-flash-exp`
5. Each model parses biomarkers from extracted text as JSON
6. **Stage 3: Consensus** - Chairman LLM synthesizes responses, adds confidence scores
7. Fallback: If synthesis fails, manual merge by counting biomarker occurrences
8. Results returned with metadata (model count, success rate, processing time)
9. Results saved to `data/health-data.json` via `app/api/user/health-data`
10. Dashboard displays biomarkers at `app/results` or `app/dashboard`

**Biomarker Reference Data Flow:**

1. `app/api/biomarkers/route.ts` fetches reference biomarkers from Airtable
2. Airtable view: "Men (45-60)" with 100 max records
3. Fields mapped: Measure/Index, Domain, Gender, Age Range, Type, Role, Interventions, Links
4. Used by: Results page to provide context and recommendations for user's extracted biomarkers

**State Management:**

- **Server-side:** JSON files in `data/` directory for users, sessions, health data, invites
- **Client-side:** React useState hooks in page components (user state, form data, loading states)
- **Session:** Persistent cookie + server-side session file validation
- **Health data:** Stored per user in health-data.json, fetched on dashboard load

## Key Abstractions

**LLM Council:**
- Purpose: Achieve higher accuracy through multi-model consensus for medical data extraction
- Examples: `lib/llm-council.ts` exports `analyzeWithCouncil()` and `analyzeWithSingleModel()`
- Pattern: Parallel model queries → Chairman synthesis → Confidence scoring
- Fallback: Manual merge by occurrence count if chairman fails
- Configuration: `COUNCIL_MODELS`, `CHAIRMAN_MODEL` constants

**Session Management:**
- Purpose: Persist user authentication across requests
- Examples: `lib/auth.ts` exports `getSession()`, `requireAuth()`, `requireAdmin()`
- Pattern: Cookie-based session ID → JSON file lookup → User validation
- Cookie name: `vibrantly_session`
- Expiry: 7 days

**Health Data Storage:**
- Purpose: Persist biomarkers and health metrics per user
- Examples: `lib/db.ts` exports `saveUserHealthData()`, `getUserHealthData()`
- Pattern: userId-keyed records in JSON file with uploadedAt timestamps
- Structure: `{ bloodWork: { uploadedAt, data }, healthKit: { uploadedAt, stats } }`

**Biomarker Reference:**
- Purpose: Provide domain-specific context for analyzing user's biomarker values
- Examples: `app/api/biomarkers/route.ts` queries Airtable for reference definitions
- Pattern: Fetch-on-demand from Airtable during results display
- Fields: Name, domains, gender, age range, interventions, study links

## Entry Points

**Homepage (Public):**
- Location: `app/page.tsx`
- Triggers: User visits `/` (root URL)
- Responsibilities: Hero section, "How It Works" explainer, biomarker categories, CTAs to register/login

**Registration:**
- Location: `app/register/page.tsx` (client component)
- Triggers: User clicks "Get Started Free" or "Create Account"
- Responsibilities: Form submission to `POST /api/auth/register`, state management, validation

**Login:**
- Location: `app/login/page.tsx`
- Triggers: User clicks "Sign In" or is redirected from protected routes
- Responsibilities: Email/password form, submission to `POST /api/auth/login`

**Dashboard (Protected):**
- Location: `app/dashboard/page.tsx`
- Triggers: User accesses `/dashboard` after auth
- Responsibilities: Health score display, biomarker trends, companion app navigation, "Ask Eliza" search

**Upload Lab Report:**
- Location: `app/upload/page.tsx`
- Triggers: User navigates from dashboard or direct `/upload` link
- Responsibilities: File upload UI, calls `POST /api/analyze`, shows loading state

**Results Display:**
- Location: `app/results/page.tsx`
- Triggers: After analysis completes at `POST /api/analyze`
- Responsibilities: Display parsed biomarkers, confidence scores, reference ranges, interventions

**Expert Advice (Gary's Advice):**
- Location: `app/garys-advice/page.tsx`
- Triggers: User clicks "Gary's Advice" in dashboard sidebar
- Responsibilities: Personalized health recommendations based on user's biomarker data

**Admin Panel:**
- Location: `app/admin/page.tsx`
- Triggers: Admin user accesses `/admin`
- Responsibilities: User management, invite creation, system health monitoring

## Error Handling

**Strategy:** Centralized error responses with HTTP status codes, client-side try-catch with user-friendly messages.

**Patterns:**

- **Auth errors:** 401 Unauthorized for missing/invalid session, 403 Forbidden for insufficient permissions
- **Validation errors:** 400 Bad Request for missing required fields or invalid data
- **Server errors:** 500 Internal Server Error with sanitized error details logged to console
- **File processing:** 400 if no file, 500 if extraction/analysis fails with error message
- **API key missing:** 500 with clear message instructing to set environment variable (e.g., "OPENROUTER_API_KEY not configured")
- **LLM Council fallback:** Single model analysis if council fails; manual merge if chairman synthesis fails
- **Client-side:** Form validation before submission, error state display in UI, redirect to login on 401

## Cross-Cutting Concerns

**Logging:** Console.log statements for debugging analysis pipeline steps, Airtable queries, auth flow. Log format: `[Component] Message` (e.g., `[Analyze] Extracting text from document...`)

**Validation:**
- Email: Standard HTML5 email input validation
- Password: 8+ character minimum enforced on client and server
- File upload: Check file type (PDF, images), size limit 25MB
- Biomarker data: JSON schema validation for extracted biomarkers

**Authentication:**
- Session-based with cookies for web clients
- Admin role check via `requireAdmin()` for protected routes
- Onboarding flow enforcement: redirect to `/onboarding` if `onboardingComplete` is false

**Environment Configuration:**
- `ANTHROPIC_API_KEY`: Claude API for document extraction
- `OPENROUTER_API_KEY`: Multi-model access for LLM Council
- `AIRTABLE_API_KEY`, `AIRTABLE_BASE_ID`, `AIRTABLE_TABLE_ID`, `AIRTABLE_VIEW_ID`: Biomarker reference data
- `SUPABASE_URL`, `SUPABASE_ANON_KEY`: Supabase client initialization (in `lib/supabase/`)

---

*Architecture analysis: 2026-01-24*
