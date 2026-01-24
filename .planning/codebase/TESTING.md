# Testing Patterns

**Analysis Date:** 2026-01-24

## Test Framework

**Status:** Not currently configured

**Runner:** None detected
- No test runner configured (Jest, Vitest, etc.)
- No test configuration files present (jest.config.js, vitest.config.ts)
- No test scripts in package.json beyond `lint`

**Assertion Library:** None detected

**Run Commands:**
```bash
npm run lint              # Code linting only
npm run dev              # Development server (no test mode)
npm run build            # Production build
npm run start            # Start production server
```

## Test File Organization

**Current State:** No test files exist in source code

**Recommended Structure (when implemented):**
- Co-located pattern preferred: `[Component].test.tsx` next to `[Component].tsx`
- API route tests: `app/api/[route]/__tests__/route.test.ts`
- Utility tests: `lib/__tests__/[utility].test.ts`

**Naming Convention (recommended):**
- `.test.ts` or `.test.tsx` for test files
- `.spec.ts` or `.spec.tsx` as alternative

## Test Structure

**Current Code Organization Supports Testing:**

The codebase is structured to support unit and integration tests:

- **Pure Functions:** Utility functions like `cn()`, `readJsonFile()`, `writeJsonFile()` are easily testable
- **Database Functions:** Data access layer in `lib/db.ts` contains pure functions with clear contracts
- **API Routes:** Separate concerns with Supabase client injection (`createClient()`)
- **Components:** Props-driven React components with clear input/output contracts

**Recommended Test Pattern (based on existing code):**

```typescript
// Example test structure for FileUploader component
describe('FileUploader', () => {
  it('should accept valid file types', () => {
    const validFile = new File(['content'], 'test.pdf', { type: 'application/pdf' });
    const onFileSelect = jest.fn();

    // Test file selection handler
    expect(onFileSelect).toHaveBeenCalledWith(validFile);
  });

  it('should reject invalid file types', () => {
    const invalidFile = new File(['content'], 'test.exe', { type: 'application/exe' });
    const onFileSelect = jest.fn();

    // Test validation logic
  });
});
```

**Recommended Test Pattern for API Routes:**

```typescript
// Example test for auth login route
describe('/api/auth/login', () => {
  it('should return user and redirect on successful login', async () => {
    const request = new NextRequest('http://localhost/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email: 'test@example.com', password: 'password' })
    });

    const response = await POST(request);
    const data = await response.json();

    expect(response.status).toBe(200);
    expect(data.user).toBeDefined();
    expect(data.redirectTo).toBeDefined();
  });

  it('should return 400 on missing credentials', async () => {
    const request = new NextRequest('http://localhost/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email: 'test@example.com' })
    });

    const response = await POST(request);
    const data = await response.json();

    expect(response.status).toBe(400);
    expect(data.error).toBeDefined();
  });
});
```

## Mocking

**Framework:** Not configured (would use Jest, Vitest, or similar when testing implemented)

**Recommended Mocking Strategy:**

**Mock External Services:**
- Supabase client: Mock in tests, use real calls only in integration tests
- Airtable API: Mock responses for biomarker fetching tests
- Anthropic SDK: Mock LLM responses

**What to Mock:**
- External API calls (Supabase, Airtable, Anthropic)
- File system operations (`readFileSync`, `writeFileSync` in `lib/db.ts`)
- Browser APIs (localStorage, sessionStorage)
- Next.js router functions

**What NOT to Mock:**
- Pure utility functions (`cn()`, data transformation functions)
- Business logic in components
- Validation logic

**Example Mocking Pattern (recommended):**

```typescript
// Mock Supabase client
jest.mock('@/lib/supabase/server', () => ({
  createClient: jest.fn(() => ({
    auth: {
      signInWithPassword: jest.fn().mockResolvedValue({
        data: { user: { id: 'test-user-id' } },
        error: null
      })
    },
    from: jest.fn().mockReturnValue({
      select: jest.fn().mockReturnValue({
        eq: jest.fn().mockReturnValue({
          single: jest.fn().mockResolvedValue({
            data: { id: 'test-user-id', role: 'user' },
            error: null
          })
        })
      })
    })
  }))
}));

// Mock file system
jest.mock('fs', () => ({
  readFileSync: jest.fn(() => '[]'),
  writeFileSync: jest.fn(),
  existsSync: jest.fn(() => true),
  mkdirSync: jest.fn()
}));
```

## Fixtures and Factories

**Test Data Patterns (from existing code):**

The codebase defines clear data structures suitable for fixtures:

```typescript
// User fixture (from lib/db.ts User interface)
const mockUser: User = {
  id: 'test-user-id',
  email: 'test@example.com',
  passwordHash: 'hashed-password',
  firstName: 'Test',
  lastName: 'User',
  role: 'user',
  createdAt: '2026-01-24T00:00:00Z',
  onboardingComplete: false
};

// Biomarker fixture (from BiomarkerReference interface)
const mockBiomarker: BiomarkerReference = {
  id: 'bio-001',
  name: 'ApoB',
  domain: ['Cardiovascular'],
  gender: 'male',
  ageRange: '40-60',
  type: 'Blood Work',
  role: 'Core (Medical)',
  whatItMeasures: 'Apolipoprotein B...',
  whyChosen: 'Strongest predictor of cardiovascular risk...',
  interventions: 'Reduce refined carbs...',
  pubmedLink: 'https://pubmed.ncbi.nlm.nih.gov/...'
};

// Session fixture
const mockSession: Session = {
  id: 'session-id',
  userId: 'test-user-id',
  expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString()
};
```

**Recommended Fixture Location:**
- `lib/__tests__/fixtures.ts` - Shared test data
- `app/api/__tests__/fixtures.ts` - API-specific fixtures

**Factory Pattern (recommended):**

```typescript
// Factory for creating test users
function createTestUser(overrides?: Partial<User>): User {
  return {
    id: 'test-user-id',
    email: 'test@example.com',
    passwordHash: 'hashed-password',
    firstName: 'Test',
    lastName: 'User',
    role: 'user',
    createdAt: new Date().toISOString(),
    onboardingComplete: false,
    ...overrides
  };
}

// Factory for creating test biomarkers
function createTestBiomarker(overrides?: Partial<BiomarkerReference>): BiomarkerReference {
  return {
    id: 'bio-001',
    name: 'ApoB',
    domain: ['Cardiovascular'],
    gender: 'male',
    ageRange: '40-60',
    type: 'Blood Work',
    role: 'Core (Medical)',
    whatItMeasures: 'Test measure',
    whyChosen: 'Test reason',
    interventions: 'Test interventions',
    ...overrides
  };
}
```

## Coverage

**Requirements:** None enforced currently

**Recommended Target:** 80%+ coverage for:
- Utility functions (lib/*.ts)
- Data access functions (lib/db.ts)
- API route handlers (app/api/**/route.ts)
- React component critical paths

**View Coverage (when implemented):**
```bash
npm run test -- --coverage
npm run test:coverage
```

## Test Types

**Unit Tests (Recommended Priority):**
- Scope: Individual functions, components, utilities
- Location: `lib/__tests__/`, `app/components/__tests__/`
- Approach: Mock external dependencies, test pure business logic
- Example: Testing `matchBiomarkers()` logic in isolation

**Integration Tests (Recommended):**
- Scope: Component + hooks, API route + database layer
- Location: `app/api/__tests__/`, `app/__tests__/`
- Approach: Mock external services (Supabase, Airtable) but test full flow
- Example: Test login flow with mocked Supabase

**E2E Tests (Optional):**
- Framework: Not configured; would recommend Playwright or Cypress
- Scope: Full user workflows (register → upload → view results)
- Approach: Run against live application or staging environment

## Common Patterns

**Async Testing (recommended):**
```typescript
describe('Biomarker Fetching', () => {
  it('should fetch biomarkers from Airtable', async () => {
    const response = await GET();
    const data = await response.json();

    expect(data.success).toBe(true);
    expect(Array.isArray(data.biomarkers)).toBe(true);
  });

  it('should handle Airtable errors', async () => {
    // Mock Airtable to throw error
    jest.mocked(getAirtableBase).mockImplementation(() => {
      throw new Error('API Key missing');
    });

    const response = await GET();
    const data = await response.json();

    expect(response.status).toBe(500);
    expect(data.error).toBeDefined();
  });
});
```

**Error Testing (recommended):**
```typescript
describe('Auth Error Handling', () => {
  it('should return 400 for missing email', async () => {
    const request = new NextRequest('...', {
      method: 'POST',
      body: JSON.stringify({ password: 'test' })
    });

    const response = await POST(request);

    expect(response.status).toBe(400);
    expect(await response.json()).toEqual({
      error: 'Email and password are required'
    });
  });

  it('should return 401 for invalid credentials', async () => {
    // Mock Supabase to return auth error
    jest.mocked(createClient).mockResolvedValue({
      auth: {
        signInWithPassword: jest.fn().mockResolvedValue({
          data: null,
          error: { message: 'Invalid credentials' }
        })
      }
    });

    const response = await POST(request);

    expect(response.status).toBe(401);
  });
});
```

**Component Testing (recommended):**
```typescript
describe('FileUploader Component', () => {
  it('should call onFileSelect when file is dropped', async () => {
    const onFileSelect = jest.fn();
    const { container } = render(<FileUploader onFileSelect={onFileSelect} />);

    const dropZone = container.querySelector('[data-testid="drop-zone"]');
    fireEvent.drop(dropZone, {
      dataTransfer: {
        files: [new File(['content'], 'test.pdf', { type: 'application/pdf' })]
      }
    });

    await waitFor(() => {
      expect(onFileSelect).toHaveBeenCalled();
    });
  });

  it('should show error for oversized files', () => {
    const largeFile = new File(['x'.repeat(25 * 1024 * 1024)], 'large.pdf', { type: 'application/pdf' });
    const onFileSelect = jest.fn();

    render(<FileUploader onFileSelect={onFileSelect} />);

    // Simulate file validation
    // Should NOT call onFileSelect and should alert user
    expect(onFileSelect).not.toHaveBeenCalled();
  });
});
```

---

*Testing analysis: 2026-01-24*
