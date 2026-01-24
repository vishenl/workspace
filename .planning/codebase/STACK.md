# Technology Stack

**Analysis Date:** 2026-01-24

## Languages

**Primary:**
- TypeScript 5.x - Full codebase (web apps and API routes)
- JavaScript - Build config and scripts

**Secondary:**
- SQL - Database schema (Supabase PostgreSQL)
- HTML/CSS - Inline styles in Next.js components

## Runtime

**Environment:**
- Node.js (version not specified in .nvmrc or package.json, inferred 20.x+ from Next.js 16)

**Package Manager:**
- npm
- Lockfile: `package-lock.json` present

## Frameworks

**Core:**
- Next.js 16.x - Full-stack web framework for Vibrantly and Learning Accelerator apps
- React 19.2.x - UI library for client-side rendering

**UI & Styling:**
- Tailwind CSS 4.x - Utility-first CSS framework
- PostCSS 4.x - CSS transformation (@tailwindcss/postcss)
- Framer Motion 12.x - Animation library (Vibrantly only)
- clsx 2.1.x - Conditional className utility
- tailwind-merge 3.x - Merge Tailwind classes intelligently

**Testing:**
- No detected testing framework configured (no Jest/Vitest in dependencies)

**Build/Dev:**
- TypeScript compiler (via tsconfig)
- ESLint 9.x - Code linting (with eslint-config-next)
- PostCSS - CSS processing

## Key Dependencies

**Critical:**
- `@anthropic-ai/sdk` (0.68.0 - Vibrantly, 0.71.2 - Learning Accelerator) - Claude API for medical/learning analysis
- `@supabase/supabase-js` (2.86.0 - Vibrantly, 2.87.1 - Learning Accelerator) - Database and auth
- `@supabase/ssr` (0.8.0) - Server-side Supabase client for session handling

**AI/LLM Integration:**
- `ai` (5.0.113) - Learning Accelerator - Vercel AI SDK for streaming
- `@ai-sdk/anthropic` (2.0.56) - Learning Accelerator - Anthropic provider for AI SDK

**Data & Utilities:**
- `bcryptjs` (3.0.3) - Vibrantly - Password hashing
- `jsonwebtoken` (9.0.2) - Vibrantly - JWT session management
- `uuid` (13.0.0) - ID generation
- `airtable` (0.12.2) - Vibrantly - Biomarker reference data access
- `date-fns` (4.1.0) - Learning Accelerator - Date manipulation
- `zustand` (5.0.9) - Learning Accelerator - State management
- `lucide-react` (0.561.0) - Learning Accelerator - Icon library

**Development:**
- `puppeteer` (21.6.1) - Root package - Screenshot component automation
- `@types/*` packages - TypeScript definitions for Node, React, JWT, bcrypt, uuid

## Configuration

**Environment:**
- `.env.local` (development) - Local environment variables
- `.env.local.example` - Template for required variables

**Build:**
- `next.config.ts` - Next.js configuration
  - Vibrantly: Sets `serverActions.bodySizeLimit: '25mb'` for large file uploads
  - Learning Accelerator: Minimal config
- `tsconfig.json` - TypeScript configuration (separate per app)
  - Path alias: `@/*` maps to app root (`./` for Vibrantly, `./src/*` for Learning Accelerator)
  - Target: ES2017
  - Strict mode enabled
- `postcss.config.mjs` - PostCSS configuration for Tailwind
- `eslint.config.mjs` - ESLint configuration

## Platform Requirements

**Development:**
- Node.js 20+ (inferred from Next.js 16 compatibility)
- npm 8+ for package management
- Modern browser with ES2017+ support

**Production:**
- Deployment to Vercel (inferred from Next.js and @supabase/ssr usage patterns)
- Supabase hosted PostgreSQL instance
- Anthropic API access (Claude)
- Airtable API access (Vibrantly biomarker references)
- OpenRouter API access (optional, for LLM Council feature in Vibrantly)

## Package Structure

**Root:**
- `package.json` - Minimal root with puppeteer for screenshot automation
- `package-lock.json` - Dependency lock

**Vibrantly (`/vibrantly`):**
- Standalone Next.js application
- 25 dependencies + dev dependencies
- Entry point: `app/page.tsx`

**Learning Accelerator (`/learning-accelerator-app`):**
- Standalone Next.js application
- 23 dependencies + dev dependencies
- Entry point: `src/app/page.tsx`

---

*Stack analysis: 2026-01-24*
