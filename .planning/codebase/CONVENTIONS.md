# Coding Conventions

**Analysis Date:** 2026-01-24

## Naming Patterns

**Files:**
- React components: PascalCase (e.g., `FileUploader.tsx`, `BiomarkerCard.tsx`)
- Utility/helper files: camelCase (e.g., `utils.ts`, `auth.ts`, `db.ts`)
- API routes: lowercase with descriptive segments (e.g., `/api/auth/login/route.ts`, `/api/biomarkers/route.ts`)
- Pages: lowercase with hyphens when needed (e.g., `page.tsx`, `results/page.tsx`)

**Functions:**
- camelCase for all functions (e.g., `getStatusColor`, `fetchBiomarkerReferences`, `matchBiomarkers`)
- Async functions use `async`/`await` syntax
- Event handlers prefixed with `handle` (e.g., `handleDragEnter`, `handleFileInput`, `handleDrop`)
- Helper/utility functions: descriptive verbs (e.g., `readJsonFile`, `writeJsonFile`, `getUserById`)

**Variables:**
- camelCase for all variables and constants
- State hooks use explicit names (e.g., `isDragging`, `isExpanded`, `loading`)
- Type/interface definitions stored at module top, after imports
- Constants uppercase if global (e.g., `SESSION_COOKIE`, `DATA_DIR`)

**Types/Interfaces:**
- PascalCase for all interfaces (e.g., `BiomarkerReference`, `ExtractedBiomarker`, `FileUploaderProps`)
- Props interfaces suffixed with `Props` (e.g., `FileUploaderProps`, `BiomarkerCardProps`)
- Enum-like objects as `const` with as-const assertion for type safety

## Code Style

**Formatting:**
- No dedicated formatter configured (.prettierrc not present)
- Follows Next.js/TypeScript default formatting conventions
- Trailing semicolons used consistently
- Double quotes for strings (not single quotes)

**Linting:**
- ESLint available (`eslint` v9 in devDependencies)
- No custom `.eslintrc` file in root (uses Next.js ESLint config v16.0.1)
- Run command: `npm run lint` (from package.json)
- Lint includes standard Next.js rules but no additional custom rules detected

## Import Organization

**Order:**
1. External libraries (React, Next, third-party packages)
2. Internal lib imports (with @ path alias)
3. Component imports
4. Type imports (using `import type`)

**Path Aliases:**
- `@/*` maps to root directory (configured in tsconfig.json)
- Used extensively: `@/lib/supabase/server`, `@/lib/utils`, `@/components/`

**Example pattern from codebase:**
```typescript
import { NextRequest, NextResponse } from 'next/server';
import { createClient } from '@/lib/supabase/server';
import type { BiomarkerReference } from '../api/biomarkers/route';

interface FileUploaderProps {
  onFileSelect: (file: File) => void;
}
```

## Error Handling

**Patterns:**
- Try-catch blocks with error logging to console
- `console.error()` used for debugging (e.g., `console.error('Login error:', error)`)
- Error propagation in API routes returns structured JSON: `{ error: string, status: number }`
- Error details conditionally included: `error instanceof Error ? error.message : "Unknown error"`
- Graceful fallbacks for missing data (null checks, default values)

**API Error Response Format:**
```typescript
return NextResponse.json(
  { error: 'Email and password are required' },
  { status: 400 }
);
```

**Component Error Handling:**
- Minimal error handling in components (relies on backend)
- Validation happens before API calls
- User alerts via `alert()` for client-side validation failures

## Logging

**Framework:** `console` (no dedicated logging library)

**Patterns:**
- `console.error()` for errors with context (file names, operation names)
- `console.log()` avoided in production code (only comments note logging points)
- Initialization logs for admin user creation: `console.log('Admin user created')`
- Error context pattern: `console.error('Error fetching biomarkers from Airtable:', error)`

## Comments

**When to Comment:**
- File-level comments for complex operations (e.g., "Lazy initialization of Airtable to avoid build-time errors")
- Inline comments for non-obvious logic
- JSDoc used sparingly - no strict requirement observed

**Example patterns:**
```typescript
// Lazy initialization of Airtable to avoid build-time errors
function getAirtableBase() { ... }

// Also check file extension for .txt files (some systems report different MIME types)
const fileExtension = file.name.toLowerCase().split('.').pop();

// Remove expired sessions
const validSessions = sessions.filter(s => new Date(s.expiresAt) > now);
```

## Function Design

**Size:** Functions kept focused and under 100 lines for most cases. Larger functions (50-150 lines) contain multiple related operations.

**Parameters:**
- Destructuring used for object parameters (e.g., `{ email, password }`)
- Spread operators used for state merging (e.g., `{ ...users[index], ...updates }`)
- Type annotations always provided for parameters
- Default parameters used minimally

**Return Values:**
- Explicit return types declared for functions
- Async functions return `Promise<Type>`
- Data-access functions return union types: `Type | undefined`
- API routes return `NextResponse.json()`

**Example from codebase:**
```typescript
export async function POST(request: NextRequest) {
  try {
    const { email, password } = await request.json();
    // ...
    return NextResponse.json({
      user: profile,
      redirectTo,
    });
  } catch (error) {
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
```

## Module Design

**Exports:**
- Named exports preferred (e.g., `export function createUser()`, `export interface User`)
- Default exports used only for page components and route handlers
- Type exports use `export type` or `export interface`

**Barrel Files:**
- Not extensively used; direct imports from source files preferred
- Components directory imports directly from component files

**Organization by Concern:**
- API routes in `/app/api/[domain]/[operation]/route.ts`
- Components in `/app/components/` with PascalCase filenames
- Utilities in `/lib/` organized by feature (`/lib/supabase/`, `/lib/auth.ts`)
- Page components in `/app/[route]/page.tsx`

## TypeScript Usage

**Strict Mode:** Enabled (`"strict": true` in tsconfig.json)

**Type Definitions:**
- All function parameters typed
- Return types explicit for exported functions
- Interface definitions at top of files before usage
- Generic types used for reusable helpers (e.g., `readJsonFile<T>`, `writeJsonFile<T>`)

**Inference:**
- Type inference used for local variables when obvious
- Template literals used for string interpolation

## React Patterns

**Component Style:**
- Functional components throughout (no class components)
- "use client" pragma for client components (e.g., `FileUploader.tsx`, `BiomarkerCard.tsx`)
- Props interfaces explicitly defined above component
- Destructuring used in function parameters

**State Management:**
- `useState` hook used for component state
- sessionStorage used for temporary data (e.g., analysis results in results/page.tsx)
- Callback refs with `useRef` for DOM access

**Framer Motion Animations:**
- `motion` and `AnimatePresence` used for animations
- Staggered animations with `delay` for lists
- Expand/collapse patterns with `initial`, `animate`, `exit` states

## CSS & Styling

**Framework:** Tailwind CSS v4 (with @tailwindcss/postcss v4)

**Patterns:**
- Utility-first approach with inline Tailwind classes
- `cn()` utility (from `@/lib/utils.ts`) for conditional class merging
- `clsx` and `tailwind-merge` used in `cn()` function for class deduplication
- Responsive classes: `sm:`, `md:`, `lg:` prefixes for breakpoints

**Example from codebase:**
```typescript
className={cn(
  "border-2 border-dashed rounded-2xl p-12 transition-all duration-300",
  isDragging
    ? "border-primary bg-primary/5 scale-[1.02]"
    : "border-neutral-300 bg-white hover:border-primary/50"
)}
```

---

*Convention analysis: 2026-01-24*
