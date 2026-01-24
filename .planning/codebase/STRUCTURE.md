# Codebase Structure

**Analysis Date:** 2026-01-24

## Directory Layout

```
vibrantly/
├── app/                              # Next.js App Router
│   ├── page.tsx                      # Homepage
│   ├── layout.tsx                    # Root layout
│   ├── globals.css                   # Tailwind styles
│   ├── favicon.ico                   # Browser icon
│   ├── components/                   # Shared React components
│   │   ├── FileUploader.tsx          # Lab report file upload UI
│   │   ├── BiomarkerCard.tsx         # Individual biomarker display
│   │   └── Icons.tsx                 # SVG icon exports
│   ├── api/                          # API routes (serverless functions)
│   │   ├── analyze/route.ts          # POST: Lab report analysis (main LLM pipeline)
│   │   ├── biomarkers/route.ts       # GET: Biomarker reference data from Airtable
│   │   ├── auth/
│   │   │   ├── login/route.ts        # POST: User login
│   │   │   ├── register/route.ts     # POST: User registration
│   │   │   ├── logout/route.ts       # POST: User logout
│   │   │   └── me/route.ts           # GET: Current user session
│   │   ├── admin/
│   │   │   ├── users/route.ts        # GET/POST: User management
│   │   │   └── invite/route.ts       # POST: Admin invite generation
│   │   └── user/
│   │       ├── profile/route.ts      # GET/POST: User profile
│   │       └── health-data/route.ts  # GET/POST: Health data (bloodwork, metrics)
│   ├── register/page.tsx             # Registration page (client-side form)
│   ├── login/page.tsx                # Login page (client-side form)
│   ├── dashboard/page.tsx            # Main dashboard (protected, shows health metrics)
│   ├── results/page.tsx              # Biomarker results display (protected)
│   ├── upload/page.tsx               # Lab report upload form (protected)
│   ├── onboarding/page.tsx           # Onboarding wizard (protected)
│   ├── profile/page.tsx              # User profile settings (protected)
│   ├── admin/page.tsx                # Admin panel (admin only)
│   └── garys-advice/page.tsx         # Expert recommendations page
├── lib/                              # Business logic & utilities
│   ├── auth.ts                       # Session/auth helpers
│   ├── db.ts                         # JSON file persistence (users, sessions, health data)
│   ├── llm-council.ts                # Multi-model LLM analysis orchestration
│   ├── utils.ts                      # Shared utilities
│   └── supabase/                     # Supabase client & middleware
│       ├── server.ts                 # Server-side Supabase client
│       ├── client.ts                 # Client-side Supabase client
│       └── middleware.ts             # Auth middleware
├── public/                           # Static assets
│   └── sample-lab-report.txt         # Example lab report for testing
├── data/                             # Local JSON persistence (created at runtime)
│   ├── users.json                    # User accounts (id, email, passwordHash, etc)
│   ├── sessions.json                 # Active sessions (id, userId, expiresAt)
│   ├── health-data.json              # User health data (bloodwork, healthKit stats)
│   └── invites.json                  # Admin invites (id, token, email, usedAt)
├── middleware.ts                     # Next.js middleware for session validation
├── next.config.ts                    # Next.js config (25MB body size limit)
├── tsconfig.json                     # TypeScript config (paths: @/* → ./*/)
├── package.json                      # Dependencies
├── tailwind.config.ts                # Tailwind CSS config
├── postcss.config.ts                 # PostCSS config
└── .env.local                        # Environment variables (not committed)
```

## Directory Purposes

**`app/` - Next.js App Router:**
- Purpose: All routes, pages, and API endpoints
- Contains: TSX page components, TS API route handlers, component exports
- Key pattern: File-based routing (`/app/dashboard/page.tsx` → route `/dashboard`)

**`app/api/` - API Endpoints:**
- Purpose: Backend HTTP handlers for all operations
- Contains: Route handlers exporting `GET`, `POST`, `PUT`, `DELETE` functions
- Pattern: `app/api/[feature]/[sub]/route.ts` → `/api/feature/sub` endpoint

**`app/components/` - Reusable Components:**
- Purpose: UI components shared across pages
- Contains: `FileUploader`, `BiomarkerCard`, `Icons` exports
- Pattern: Export default component, can be imported in any page

**`lib/` - Business Logic:**
- Purpose: Non-UI code: auth, data access, LLM orchestration
- Contains: Functions, classes, interfaces, utilities
- Pattern: Import by `@/lib/[file]` via tsconfig path alias

**`lib/supabase/` - Supabase Integration:**
- Purpose: Supabase client initialization and middleware
- Contains: Server client, client-side client, middleware helpers
- Status: Available for production migration (currently hybrid JSON + Supabase)

**`data/` - Local Persistence:**
- Purpose: Runtime data storage (created on first run)
- Contains: JSON files for users, sessions, health data, invites
- Pattern: Read/write via `lib/db.ts` file I/O functions
- Lifespan: Persists between server restarts (stored on filesystem)

## Key File Locations

**Entry Points:**
- `app/page.tsx`: Public landing page (no auth required)
- `app/layout.tsx`: Root HTML layout with metadata
- `middleware.ts`: Session validation on every request

**Configuration:**
- `next.config.ts`: Max upload size 25MB
- `tsconfig.json`: Path alias `@/*` maps to project root
- `.env.local`: API keys (Anthropic, OpenRouter, Airtable, Supabase)

**Core Logic:**
- `lib/db.ts`: All user/session/health data CRUD operations (450+ lines)
- `lib/llm-council.ts`: Multi-model analysis orchestration (380+ lines)
- `lib/auth.ts`: Session helpers (`getSession()`, `requireAuth()`, `requireAdmin()`)

**Testing Assets:**
- `public/sample-lab-report.txt`: Example lab report for manual testing

## Naming Conventions

**Files:**
- Pages: `page.tsx` for route handlers
- API routes: `route.ts` for endpoint handlers
- Components: PascalCase with `.tsx` extension (e.g., `FileUploader.tsx`)
- Utilities: camelCase with `.ts` extension (e.g., `llm-council.ts`)
- Data files: kebab-case (e.g., `health-data.json`)

**Directories:**
- Feature directories: kebab-case (e.g., `app/api/auth/`, `app/api/user/`)
- Component folder: `components/` (lowercase)
- Library folder: `lib/` (lowercase)
- Data folder: `data/` (lowercase, created at runtime)

**Functions:**
- Async server functions: `camelCase` (e.g., `fetchHealthData()`, `analyzeWithCouncil()`)
- React components: PascalCase (e.g., `FileUploader`, `BiomarkerCard`)
- Hooks: `use` prefix (e.g., `useRouter`, `useState`)
- Type/Interface exports: PascalCase (e.g., `User`, `HealthData`, `Biomarker`)

**Database Functions:**
- Read: `get*()` (e.g., `getUserById()`, `getHealthData()`)
- Create: `create*()` (e.g., `createUser()`, `createSession()`)
- Update: `update*()` (e.g., `updateUser()`)
- Delete: `delete*()` (e.g., `deleteSession()`)

## Where to Add New Code

**New Feature (e.g., "Nutrition Tracker"):**
- Primary code: `app/nutrition/page.tsx` (UI) + `app/api/user/nutrition/route.ts` (API)
- Database: Add fields to `data/health-data.json` structure via `saveUserHealthData()` in `lib/db.ts`
- Tests: Create `app/nutrition/page.test.tsx` (not currently set up, but pattern)
- Recommendation: Keep component-specific logic in `app/[feature]/` directory

**New Component:**
- Implementation: `app/components/[ComponentName].tsx`
- Export: `export default function ComponentName() { ... }`
- Import: `import ComponentName from '@/app/components/ComponentName'` in any page
- Pattern: Functional component with TypeScript props interface at top

**New API Endpoint:**
- Implementation: `app/api/[feature]/[sub]/route.ts`
- Export: `export async function POST(request: NextRequest) { ... }`
- Response: Return `NextResponse.json({ ... }, { status: 200 })`
- Error handling: Catch errors, return 500 with error message
- Authentication: Call `requireAuth()` from `lib/auth.ts` if user-specific

**Database Schema Change:**
- Modify: User interface in `lib/db.ts` (lines 18-31)
- Migration: Update `createUser()`, `updateUser()` functions
- Existing data: Handle missing fields gracefully with fallbacks or defaults
- Example: Add `goal?: string` to User interface → update type annotations → set default in `createUser()`

**New Shared Utility:**
- Implementation: `lib/[utility-name].ts` (e.g., `lib/validators.ts`)
- Export: Named exports (e.g., `export function validateEmail() { ... }`)
- Import: `import { validateEmail } from '@/lib/validators'` in components/routes

## Special Directories

**`data/` - Runtime Data Storage:**
- Purpose: Persistent user data between server restarts
- Generated: Automatically created by `initializeAdmin()` in `lib/db.ts` if missing
- Committed: Should be in `.gitignore` (contains user/session secrets)
- Deletion: Deleting these files will reset the database (will create admin on next start)

**`public/` - Static Assets:**
- Purpose: Served as-is by Next.js (no processing)
- Committed: Yes, version-controlled
- Example: `sample-lab-report.txt` for testing the analysis pipeline

**.next/ - Build Output:**
- Purpose: Next.js build artifacts and cache
- Generated: Created by `npm run build` and `npm run dev`
- Committed: No (in .gitignore)
- Deletion: Safe to delete; will be regenerated

**`node_modules/` - Dependencies:**
- Purpose: npm/yarn package installations
- Generated: Created by `npm install` or `npm ci`
- Committed: No (in .gitignore)
- Deletion: Safe to delete; reinstall with `npm install`

---

*Structure analysis: 2026-01-24*
