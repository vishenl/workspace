# Codebase Concerns

**Analysis Date:** 2026-01-24

## Critical Security Issues

**Hardcoded API Keys in Repository:**
- Issue: Production API keys are committed to `.env.local` and visible in git history
- Files: `/vibrantly/.env.local`
- Impact: Anthropic API key, Airtable API key, and Supabase ANON key exposed. Attackers can:
  - Make unauthorized API calls using Claude/Airtable credentials
  - Access user data via compromised Supabase key
  - Incur unexpected API costs
- Fix approach:
  1. Rotate all exposed API keys immediately
  2. Add `.env.local` to `.gitignore` (ensure it's not already tracked)
  3. Use GitHub Secrets for CI/CD pipelines
  4. Scan git history and force-push to remove exposed keys
  5. Document env setup in `env.local.example` only

**Insufficient Authorization Checks on Admin Endpoints:**
- Issue: Admin endpoints check role but don't consistently validate response sanitization
- Files: `/vibrantly/app/api/admin/users/route.ts`, `/vibrantly/app/api/admin/invite/route.ts`
- Impact: While role-based checks exist, there's no validation that admin endpoints don't leak sensitive data (e.g., password hashes if accidentally queried)
- Fix approach:
  1. Explicitly whitelist which fields can be returned in admin responses
  2. Never return `passwordHash` or sensitive auth fields
  3. Add consistent error logging for failed auth attempts
  4. Consider implementing request rate limiting

**Missing Input Validation on AI Analysis Endpoints:**
- Issue: `/vibrantly/app/api/analyze/route.ts` accepts form data without strict content-type validation
- Files: `/vibrantly/app/api/analyze/route.ts`
- Impact: Could be exploited to upload non-PDF/image files or bypass intended file size limits
- Fix approach:
  1. Validate `file.type` matches allowed MIME types
  2. Verify actual file content (magic bytes) matches declared type
  3. Add strict file size enforcement at middleware level
  4. Implement virus/malware scanning for uploaded files

**Missing CSRF Protection on State-Changing Operations:**
- Issue: No CSRF token validation on POST endpoints like `/api/admin/invite`, `/api/auth/register`
- Files: `/vibrantly/app/api/admin/invite/route.ts`, `/vibrantly/app/api/auth/register/route.ts`
- Impact: Malicious sites could trigger invite creation or registration on behalf of authenticated users
- Fix approach:
  1. Implement CSRF token generation and validation
  2. Use double-submit cookie or synchronizer token pattern
  3. Consider Next.js middleware-based CSRF protection

**Plaintext Admin Password in Source:**
- Issue: Default admin account uses hardcoded plaintext password "vibrant health" in initialization
- Files: `/vibrantly/lib/db.ts` line 88
- Impact: Anyone with code access can log in as admin
- Fix approach:
  1. Remove hardcoded passwords entirely
  2. Generate one-time setup token for first admin registration
  3. Force password change on first login
  4. Only initialize admin account when explicitly triggered via setup route

## Authentication & Session Management Issues

**Weak Session Storage Mechanism:**
- Issue: Sessions stored in local JSON files with no encryption
- Files: `/vibrantly/lib/db.ts` (sessions.json)
- Impact: Compromised file system = compromised all user sessions; no audit trail
- Fix approach:
  1. Migrate to Supabase Auth sessions (already partially implemented)
  2. Use `@supabase/ssr` exclusively, remove custom session management
  3. Implement session invalidation on password change
  4. Add session revocation list for security events

**No Rate Limiting on Auth Endpoints:**
- Issue: Login, register, and token verification endpoints have no rate limiting
- Files: `/vibrantly/app/api/auth/login/route.ts`, `/vibrantly/app/api/auth/register/route.ts`
- Impact: Brute force attacks possible; account enumeration via timing attacks
- Fix approach:
  1. Implement rate limiting (e.g., 5 login attempts per minute per IP)
  2. Use package like `upstash/ratelimit` or similar
  3. Add progressive delays after failed attempts
  4. Lock accounts temporarily after multiple failures

**Password Validation Too Weak:**
- Issue: Only checks minimum 8 characters, no complexity requirements
- Files: `/vibrantly/app/api/auth/register/route.ts` line 108
- Impact: Users can set weak passwords (e.g., "password123")
- Fix approach:
  1. Enforce: uppercase, lowercase, number, special character requirements
  2. Check against common password lists
  3. Validate password entropy minimum
  4. Consider passphrase support (longer, more memorable)

## Data Privacy & Handling Issues

**Unencrypted Sensitive Data in JSONB:**
- Issue: Health data stored as unencrypted JSONB in Supabase
- Files: `/vibrantly/supabase-schema.sql` (health_data table), `/vibrantly/app/api/user/health-data/route.ts`
- Impact: Medical information (biomarkers, lab reports) readable in plaintext at database level; fails HIPAA compliance
- Fix approach:
  1. Implement field-level encryption using `pgsql-crypto` or similar
  2. Encrypt PII fields before sending to database
  3. Use encryption keys stored separately (e.g., AWS KMS, Supabase Vault)
  4. Implement audit logging for data access

**No Data Retention Policy:**
- Issue: No mechanism to delete or archive old health data
- Files: No cleanup endpoints exist
- Impact: Indefinite storage of sensitive medical information; GDPR/CCPA violation risk
- Fix approach:
  1. Implement data retention schedule (e.g., 7 years max)
  2. Add delete/archive endpoints with strong auth
  3. Support GDPR "right to be forgotten" requests
  4. Log all data deletion events

**Large File Upload Without Scanning:**
- Issue: 25MB PDF uploads accepted without virus/malware scanning
- Files: `/vibrantly/next.config.ts`, `/vibrantly/app/api/analyze/route.ts`
- Impact: Malicious files (disguised as PDFs) could be stored and processed
- Fix approach:
  1. Implement ClamAV or similar malware scanning
  2. Scan before storing, quarantine suspicious files
  3. Add file type verification beyond extension checking
  4. Limit file upload features to authenticated users only

## Data Extraction & AI Analysis Issues

**Unbounded LLM Council Token Usage:**
- Issue: No token limits or cost controls on OpenRouter LLM Council analysis
- Files: `/vibrantly/lib/llm-council.ts`, `/vibrantly/app/api/analyze/route.ts`
- Impact:
  - Single large document could cost hundreds of dollars (querying 3 models + chairman)
  - No per-user quota enforcement
  - Potential DoS via large file uploads
- Fix approach:
  1. Implement per-user monthly quota (e.g., 10 analyses)
  2. Add token estimation before running council
  3. Implement cost tracking and alerts
  4. Use smaller models for initial screening
  5. Add max tokens limit per model call

**No Validation of LLM Output:**
- Issue: JSON parsing assumes LLM output is valid and well-formed
- Files: `/vibrantly/lib/llm-council.ts` lines 142-172
- Impact: Malformed responses crash analysis or return invalid biomarker data
- Fix approach:
  1. Validate parsed biomarkers against strict schema using Zod
  2. Add confidence thresholds before accepting extracted data
  3. Log invalid responses for debugging
  4. Return graceful errors instead of crashing

**Airtable API Key Exposed & Lazy Initialization:**
- Issue: Airtable API key in `.env.local` + lazy initialization could fail at runtime
- Files: `/vibrantly/app/api/biomarkers/route.ts`, `.env.local`
- Impact: API key exposed; service fails silently without proper error messaging
- Fix approach:
  1. Rotate Airtable API key
  2. Validate env vars at startup, fail fast if missing
  3. Implement fallback biomarker data if Airtable unavailable
  4. Add circuit breaker for Airtable API calls

## Architecture & Dependency Issues

**Dual Authentication Systems (Supabase vs Custom):**
- Issue: Code uses both Supabase Auth AND custom JWT/session management
- Files: `/vibrantly/lib/auth.ts`, `/vibrantly/lib/supabase/middleware.ts`, various API routes
- Impact: Confusing, maintenance burden, potential security gaps; session sync issues
- Fix approach:
  1. Standardize on Supabase Auth exclusively
  2. Remove `/vibrantly/lib/auth.ts` and custom session functions
  3. Use Supabase middleware for all protected routes
  4. Update all API routes to use Supabase client exclusively

**No Input Sanitization or Escaping:**
- Issue: User inputs passed directly to Supabase without explicit validation
- Files: All API routes accepting user input
- Impact: While Supabase parameterization helps, application-level validation is missing
- Fix approach:
  1. Add Zod schemas for all request bodies
  2. Validate and sanitize user inputs at API boundary
  3. Implement request validation middleware
  4. Document all expected input formats

**Inconsistent Error Handling:**
- Issue: Some endpoints return detailed error messages, others generic ones
- Files: Various API routes
- Impact: Information disclosure; inconsistent user experience
- Fix approach:
  1. Standardize error response format
  2. Log detailed errors server-side only
  3. Return generic errors to clients (no stack traces or DB details)
  4. Add structured logging with correlation IDs

## Testing & Quality Issues

**No Automated Tests:**
- Issue: Zero test files in application code (only node_modules)
- Files: No `.test.ts` or `.spec.ts` files in `/vibrantly/app` or `/vibrantly/lib`
- Impact:
  - Regressions go undetected
  - Auth logic untested
  - AI integration untested
  - Refactoring is high-risk
- Fix approach:
  1. Add Jest or Vitest setup
  2. Write tests for all API endpoints (auth, admin, biomarkers)
  3. Test authorization logic thoroughly
  4. Add integration tests for Supabase interactions
  5. Target 80%+ coverage for critical paths

**No TypeScript Type Strictness:**
- Issue: `tsconfig.json` likely uses lenient settings; many `any` types in code
- Files: `/vibrantly/app/api/biomarkers/route.ts` line 42 (Record<string, unknown>)
- Impact: Type safety issues go undetected; refactoring risky
- Fix approach:
  1. Enable `strict: true` in tsconfig.json
  2. Remove all `any` type usage
  3. Validate Airtable and API responses with proper types
  4. Use type guards for runtime validation

**Missing Integration Tests:**
- Issue: No tests for Supabase, Anthropic, or OpenRouter integrations
- Files: No test files
- Impact:
  - API key rotation could break silently
  - LLM output changes go unnoticed
  - Database schema changes could break app
- Fix approach:
  1. Use Supabase local development setup for testing
  2. Mock external APIs (Anthropic, OpenRouter) in tests
  3. Test critical user flows end-to-end
  4. Add API contract tests

## Monitoring & Observability Issues

**No Structured Logging:**
- Issue: Uses `console.log/error` throughout; no structured logging
- Files: All API routes and libraries
- Impact: Difficult to debug production issues; can't aggregate/filter logs
- Fix approach:
  1. Implement structured logging with timestamp, level, context
  2. Use `winston` or `pino` library
  3. Include correlation IDs for request tracing
  4. Stream logs to centralized service (e.g., Datadog, LogRocket)

**No Error Tracking:**
- Issue: No Sentry or similar error tracking service
- Files: N/A
- Impact: Production errors are silent; no alerting for critical failures
- Fix approach:
  1. Integrate Sentry or similar service
  2. Capture and report all unhandled errors
  3. Set up alerts for error rate thresholds
  4. Track performance metrics (response times, API latencies)

**No Usage Analytics or Cost Monitoring:**
- Issue: No tracking of API costs (Anthropic, OpenRouter, Airtable)
- Files: `/vibrantly/app/api/analyze/route.ts`
- Impact: Can't track budget; potential cost surprises
- Fix approach:
  1. Log all LLM API calls with tokens used
  2. Implement cost tracking dashboard
  3. Set monthly budget alerts
  4. Track usage per user for quota enforcement

## Fragile Areas & High-Risk Code

**LLM Council Synthesis is Single Point of Failure:**
- Issue: If chairman LLM fails, fallback manual merge is brittle
- Files: `/vibrantly/lib/llm-council.ts` lines 275-288
- Impact: Failed synthesis silently degrades to lower-quality results
- Fix approach:
  1. Add explicit error handling for chairman failures
  2. Implement retry logic with exponential backoff
  3. Fall back to single-model analysis with warning
  4. Alert on repeated synthesis failures

**PDF Extraction Dependency on Claude Vision:**
- Issue: Document extraction entirely dependent on Claude's vision capability
- Files: `/vibrantly/app/api/analyze/route.ts` lines 25-103
- Impact: If Claude API changes or becomes unavailable, all analysis fails
- Fix approach:
  1. Implement fallback extraction method (e.g., pdf-parse library)
  2. Support OCR for image-based PDFs
  3. Add circuit breaker for Claude API failures
  4. Cache successful extractions

**Middleware Route Protection is Incomplete:**
- Issue: Middleware only protects certain paths; no protection for `/api/*` routes
- Files: `/vibrantly/middleware.ts`
- Impact: Some API routes rely on individual authorization checks (inconsistent)
- Fix approach:
  1. Extend middleware to protect all `/api/admin/*` routes
  2. Verify auth token at middleware level before route handler
  3. Add consistent auth checks for all endpoints
  4. Use middleware to enforce HTTPS in production

## Dependencies & Vendor Risks

**Outdated/Vulnerable Dependencies:**
- Issue: No evidence of dependency scanning; potential security vulnerabilities
- Files: `/vibrantly/package.json`
- Impact: Could have known vulnerabilities in transitive dependencies
- Fix approach:
  1. Run `npm audit` regularly
  2. Set up Dependabot for automated updates
  3. Use `npm ci` in CI/CD (not `npm install`)
  4. Keep major dependencies current (Next.js, React, etc.)

**Breaking Change Risk: Next.js 16 + React 19:**
- Issue: Using very recent versions with limited production track record
- Files: `/vibrantly/package.json` (next@16.0.7, react@19.2.0)
- Impact: Potential unknown bugs or breaking changes; ecosystem not fully updated
- Fix approach:
  1. Thoroughly test before production deployment
  2. Use Vercel deployment for production (official support)
  3. Monitor Next.js release notes for issues
  4. Have rollback plan to LTS versions ready

**OpenRouter as Single Point for LLM Access:**
- Issue: All multi-model analysis depends on OpenRouter API
- Files: `/vibrantly/lib/llm-council.ts`
- Impact: Service outage = no biomarker analysis capability
- Fix approach:
  1. Implement fallback to single Anthropic model
  2. Add monitoring for OpenRouter availability
  3. Consider direct vendor APIs as backup
  4. Implement request queuing for API overload scenarios

## Security Configuration Issues

**Missing Security Headers:**
- Issue: No X-Frame-Options, X-Content-Type-Options, CSP headers configured
- Files: `/vibrantly/next.config.ts`
- Impact: Vulnerable to clickjacking and MIME type sniffing
- Fix approach:
  1. Add security headers middleware
  2. Implement Content Security Policy
  3. Set X-Frame-Options: DENY
  4. Add X-Content-Type-Options: nosniff

**CORS Not Explicitly Configured:**
- Issue: API routes don't explicitly set CORS headers
- Files: All `/app/api/*` routes
- Impact: Default browser CORS behavior; could accidentally expose APIs
- Fix approach:
  1. Implement CORS middleware with explicit origin whitelist
  2. Only allow expected frontend domains
  3. Restrict methods (no GET for state-changing ops)
  4. Add CORS preflight handling

**Supabase Row Level Security Gaps:**
- Issue: "Anyone can check invite token" policy allows unauthenticated access
- Files: `/vibrantly/supabase-schema.sql` line 161
- Impact: Could enumerate valid invite tokens
- Fix approach:
  1. Restrict invite checking to authenticated users
  2. Implement challenge-response for invite verification
  3. Add rate limiting at database level
  4. Audit all RLS policies for over-permissiveness

## Known Bugs & Workarounds

**Middleware setAll Silent Failure:**
- Issue: `/vibrantly/lib/supabase/server.ts` catches all errors in setAll
- Files: `/vibrantly/lib/supabase/server.ts` line 20-24
- Impact: Session updates could fail silently; user stays logged in when shouldn't
- Fix approach:
  1. Log caught errors for debugging
  2. Only catch specific Server Component errors
  3. Implement fallback session handling
  4. Alert if session refresh fails repeatedly

**Health Data Query Returns Only One Record:**
- Issue: `find()` only gets first of each type, ignores history
- Files: `/vibrantly/app/api/user/health-data/route.ts` lines 33-34
- Impact: Users can't see historical data or multiple uploads
- Fix approach:
  1. Return all health data records, not just latest
  2. Implement pagination for large histories
  3. Add filtering by date range
  4. Expose full upload history in UI

## Missing Critical Features

**No Audit Logging:**
- Issue: No logging of who accessed/modified sensitive health data
- Files: No audit log implementation
- Impact: Can't detect data breaches; no compliance with HIPAA/GDPR
- Fix approach:
  1. Implement audit log table in Supabase
  2. Log all data access and modifications
  3. Include user ID, timestamp, action, IP address
  4. Retain logs per regulatory requirements

**No Data Export/Portability:**
- Issue: No way for users to export their health data
- Files: No endpoints for data export
- Impact: GDPR violation; poor UX
- Fix approach:
  1. Add endpoint to export user data as JSON/CSV
  2. Implement bulk data download
  3. Support scheduled exports to email
  4. Document data portability in privacy policy

**No Account Deletion Mechanism:**
- Issue: No way for users to delete their accounts and data
- Files: No delete endpoints
- Impact: Privacy concern; compliance issue
- Fix approach:
  1. Implement full account deletion endpoint
  2. Cascade delete all user data (health_data, biomarker_results, invites)
  3. Add grace period before permanent deletion
  4. Log deletions for compliance

**No Notifications or Alerts:**
- Issue: Users aren't notified of security events, new analyses, etc.
- Files: No email/notification system
- Impact: Poor UX; users unaware of account activity
- Fix approach:
  1. Implement email notifications (send via SendGrid or similar)
  2. Alert on: failed login attempts, new device login, data uploads
  3. Allow users to control notification preferences
  4. Add in-app notification center

---

*Concerns audit: 2026-01-24*
