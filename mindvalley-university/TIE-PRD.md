# TIE (The Intelligence Engine) — Technical PRD

## Executive Summary

TIE is the **headless AI reasoning layer** that powers the entire Vibe Inc ecosystem. It is extracted from any single application and operates as a **shared intelligence service** that all apps (Life Manager, Vibrantly, SIX, Learning Accelerator) connect to via well-defined APIs.

**Core Principle**: TIE is the brain; apps are the limbs. Apps handle UI/UX and domain-specific interactions. TIE handles cross-domain reasoning, personalization, and orchestration.

---

## Architecture Decision: Where Does TIE Live?

### Recommendation: **Separate Supabase Project + Dedicated Microservices**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         TIE INFRASTRUCTURE                               │
│                    (Separate Supabase Project)                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   User       │  │   Context    │  │   Decision   │  │   Action     │ │
│  │   Memory     │  │   Store      │  │   Log        │  │   Queue      │ │
│  │   (postgres) │  │   (postgres) │  │   (postgres) │  │   (postgres) │ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘ │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                    TIE Edge Functions                             │   │
│  │  • /api/tie/ingest      — Receive signals from apps               │   │
│  │  • /api/tie/interpret   — Process and understand context          │   │
│  │  • /api/tie/orchestrate — Generate recommendations                │   │
│  │  • /api/tie/confirm     — Handle user confirmations               │   │
│  │  • /api/tie/commit      — Execute confirmed actions               │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                    LLM Orchestration Layer                        │   │
│  │  • Claude (primary reasoning)                                     │   │
│  │  • GPT-4 (specialized tasks)                                      │   │
│  │  • Embeddings service (context retrieval)                         │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
            ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
            │ Life Manager│ │  Vibrantly  │ │    SIX      │
            │ (Supabase)  │ │ (Supabase)  │ │ (Supabase)  │
            └─────────────┘ └─────────────┘ └─────────────┘
```

### Why Separate Supabase Project?

| Factor | Shared DB | Separate Project ✓ |
|--------|-----------|-------------------|
| **Scaling** | Bottleneck as apps grow | Independent scaling |
| **Security** | Apps can access TIE internals | Clean API boundaries |
| **Team Ownership** | Unclear ownership | TIE team owns TIE |
| **Deployment** | Risk of cascading failures | Isolated deployments |
| **Cost Attribution** | Hard to track | Clear per-project costs |
| **Data Isolation** | Apps share everything | Apps only see their data + TIE responses |

### Alternative Considered: Single Supabase with Schema Separation

Not recommended because:
- RLS complexity explodes with cross-schema access
- Single point of failure
- Team boundaries become blurry
- Harder to scale TIE independently

---

## TIE Data Model

### Core Tables (TIE Supabase Project)

```sql
-- ============================================
-- USER MEMORY: Long-term user understanding
-- ============================================
CREATE TABLE tie.user_profiles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL UNIQUE,        -- External user ID (from auth provider)
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now(),

  -- Core identity
  name TEXT,
  timezone TEXT DEFAULT 'UTC',

  -- Life model (computed, updated periodically)
  life_model JSONB DEFAULT '{}',       -- 3 MIQ, values, patterns

  -- Preferences (explicit settings)
  preferences JSONB DEFAULT '{}'       -- notification prefs, energy patterns, etc.
);

CREATE TABLE tie.user_memory (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES tie.user_profiles(user_id),
  created_at TIMESTAMPTZ DEFAULT now(),

  memory_type TEXT NOT NULL,           -- 'fact', 'preference', 'pattern', 'goal'
  domain TEXT,                          -- 'health', 'learning', 'social', 'work', NULL for cross-domain
  content TEXT NOT NULL,               -- The actual memory
  embedding VECTOR(1536),              -- For semantic retrieval
  confidence FLOAT DEFAULT 1.0,        -- How confident TIE is in this memory
  source TEXT,                          -- Which app/signal created this
  expires_at TIMESTAMPTZ               -- NULL = permanent, or auto-expire
);

-- ============================================
-- CONTEXT STORE: Recent signals and state
-- ============================================
CREATE TABLE tie.context_signals (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES tie.user_profiles(user_id),
  received_at TIMESTAMPTZ DEFAULT now(),

  source_app TEXT NOT NULL,            -- 'life_manager', 'vibrantly', 'six', etc.
  signal_type TEXT NOT NULL,           -- 'health_metric', 'task_completed', 'connection_made', etc.
  payload JSONB NOT NULL,              -- Signal-specific data

  -- For efficient querying
  domain TEXT,                          -- 'health', 'learning', 'social', 'work'
  importance FLOAT DEFAULT 0.5         -- 0-1 scale, affects reasoning priority
);

CREATE TABLE tie.active_context (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES tie.user_profiles(user_id) UNIQUE,
  updated_at TIMESTAMPTZ DEFAULT now(),

  -- Current state snapshot
  current_energy TEXT,                 -- 'high', 'medium', 'low', 'unknown'
  current_focus TEXT,                  -- What they're working on
  today_priorities JSONB DEFAULT '[]', -- Top 3 for today
  pending_decisions JSONB DEFAULT '[]' -- Waiting for user confirmation
);

-- ============================================
-- DECISION LOG: Audit trail of all decisions
-- ============================================
CREATE TABLE tie.decisions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES tie.user_profiles(user_id),
  created_at TIMESTAMPTZ DEFAULT now(),

  decision_type TEXT NOT NULL,         -- 'recommendation', 'suggestion', 'action'
  domain TEXT,

  -- The decision
  title TEXT NOT NULL,
  description TEXT,
  reasoning TEXT NOT NULL,             -- Why TIE made this decision (transparency)

  -- Input context (what TIE considered)
  context_snapshot JSONB NOT NULL,     -- Signals, memories used

  -- Status
  status TEXT DEFAULT 'pending',       -- 'pending', 'confirmed', 'rejected', 'expired'
  confirmed_at TIMESTAMPTZ,
  executed_at TIMESTAMPTZ,

  -- Feedback loop
  user_feedback TEXT,                  -- 'helpful', 'not_helpful', NULL
  feedback_notes TEXT
);

-- ============================================
-- ACTION QUEUE: Confirmed actions to execute
-- ============================================
CREATE TABLE tie.action_queue (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES tie.user_profiles(user_id),
  decision_id UUID REFERENCES tie.decisions(id),
  created_at TIMESTAMPTZ DEFAULT now(),

  target_app TEXT NOT NULL,            -- Which app should execute
  action_type TEXT NOT NULL,           -- 'create_task', 'send_notification', etc.
  payload JSONB NOT NULL,              -- Action-specific data

  priority INT DEFAULT 5,              -- 1 = highest, 10 = lowest
  execute_at TIMESTAMPTZ,              -- NULL = immediate, or scheduled

  status TEXT DEFAULT 'queued',        -- 'queued', 'processing', 'completed', 'failed'
  processed_at TIMESTAMPTZ,
  error_message TEXT
);

-- ============================================
-- INDEXES
-- ============================================
CREATE INDEX idx_memory_user_domain ON tie.user_memory(user_id, domain);
CREATE INDEX idx_memory_embedding ON tie.user_memory USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX idx_signals_user_time ON tie.context_signals(user_id, received_at DESC);
CREATE INDEX idx_decisions_user_status ON tie.decisions(user_id, status);
CREATE INDEX idx_actions_status ON tie.action_queue(status, execute_at);
```

---

## API Specifications

### Authentication

All TIE APIs require:
- `Authorization: Bearer <service_token>` — App-level service token
- `X-User-ID: <user_id>` — The user context for the request

Service tokens are issued per-app and have scoped permissions.

---

### API 1: INGEST — Receive Signals

**Endpoint**: `POST /api/tie/ingest`

**Purpose**: Apps send signals (events, metrics, state changes) to TIE for processing.

**Request**:
```typescript
interface IngestRequest {
  signals: Signal[];
}

interface Signal {
  type: string;           // e.g., 'health.sleep_score', 'task.completed', 'social.connection_made'
  domain: 'health' | 'learning' | 'social' | 'work' | 'general';
  payload: Record<string, any>;
  timestamp?: string;     // ISO 8601, defaults to now
  importance?: number;    // 0-1, defaults to 0.5
}
```

**Example — Vibrantly sends sleep data**:
```json
POST /api/tie/ingest
Authorization: Bearer vibrantly_service_token_xxx
X-User-ID: user_abc123

{
  "signals": [
    {
      "type": "health.sleep_score",
      "domain": "health",
      "payload": {
        "score": 85,
        "duration_hours": 7.2,
        "deep_sleep_pct": 22,
        "rem_pct": 24,
        "hrv": 45,
        "source": "oura"
      },
      "timestamp": "2026-01-12T07:30:00Z",
      "importance": 0.8
    }
  ]
}
```

**Response**:
```json
{
  "status": "accepted",
  "signals_processed": 1,
  "signal_ids": ["sig_xxx123"]
}
```

**Common Signal Types**:

| Signal Type | Domain | Payload Fields |
|------------|--------|----------------|
| `health.sleep_score` | health | score, duration, hrv, source |
| `health.workout` | health | type, duration, intensity, calories |
| `health.lab_result` | health | biomarker, value, unit, reference_range |
| `task.created` | work | title, due_date, priority, project |
| `task.completed` | work | task_id, duration_minutes |
| `learning.lesson_completed` | learning | quest_id, lesson_id, duration |
| `learning.quiz_score` | learning | quest_id, score, topic |
| `social.connection_made` | social | contact_id, context, relationship_type |
| `social.event_attended` | social | event_id, connections_made |
| `goal.updated` | general | goal_type, goal_text, progress |

---

### API 2: INTERPRET — Request Context Understanding

**Endpoint**: `POST /api/tie/interpret`

**Purpose**: Apps ask TIE to interpret a situation or user state. Returns structured understanding.

**Request**:
```typescript
interface InterpretRequest {
  query: string;          // What the app wants to understand
  context_window?: string; // 'today', 'week', 'month', 'all'
  domains?: string[];     // Filter to specific domains
  include_reasoning?: boolean;
}
```

**Example — Life Manager asks about user's current state**:
```json
POST /api/tie/interpret
Authorization: Bearer life_manager_service_token_xxx
X-User-ID: user_abc123

{
  "query": "What is the user's current energy level and readiness for deep work?",
  "context_window": "today",
  "domains": ["health", "work"],
  "include_reasoning": true
}
```

**Response**:
```json
{
  "interpretation": {
    "energy_level": "high",
    "deep_work_readiness": 0.85,
    "optimal_work_window": {
      "start": "09:00",
      "end": "12:00"
    },
    "factors": [
      {
        "factor": "sleep_quality",
        "value": "85/100",
        "impact": "positive"
      },
      {
        "factor": "hrv",
        "value": "elevated",
        "impact": "positive"
      },
      {
        "factor": "calendar_density",
        "value": "3 meetings",
        "impact": "neutral"
      }
    ]
  },
  "reasoning": "User's Oura data shows 85% sleep score with elevated HRV (45ms vs 38ms baseline). This indicates good recovery and high readiness for cognitively demanding work. Calendar shows meetings clustered in afternoon, leaving morning optimal for deep work.",
  "confidence": 0.82,
  "context_used": {
    "signals_analyzed": 12,
    "memories_retrieved": 3,
    "time_range": "last 24 hours"
  }
}
```

---

### API 3: ORCHESTRATE — Request Recommendations

**Endpoint**: `POST /api/tie/orchestrate`

**Purpose**: Apps ask TIE for actionable recommendations. This is the core "intelligence" endpoint.

**Request**:
```typescript
interface OrchestrateRequest {
  intent: string;                    // What the user/app wants to accomplish
  constraints?: Constraint[];        // Time, energy, preference constraints
  max_recommendations?: number;      // Default 3
  require_confirmation?: boolean;    // Default true (nothing commits silently)
}

interface Constraint {
  type: 'time' | 'energy' | 'priority' | 'domain';
  value: string | number;
}
```

**Example — Morning Brief requests today's priorities**:
```json
POST /api/tie/orchestrate
Authorization: Bearer life_manager_service_token_xxx
X-User-ID: user_abc123

{
  "intent": "Generate today's top 3 priorities across all life domains",
  "constraints": [
    { "type": "time", "value": "today" },
    { "type": "energy", "value": "high_morning" }
  ],
  "max_recommendations": 3,
  "require_confirmation": true
}
```

**Response**:
```json
{
  "recommendations": [
    {
      "id": "rec_001",
      "priority": 1,
      "domain": "work",
      "title": "Complete investor deck deep work session",
      "description": "Your HRV is elevated — ideal for creative work. Block 9am-12pm.",
      "reasoning": "This task is your #1 priority from yesterday, aligns with your 3 MIQ goal 'Build Vibe Inc', and your energy is optimal for creative work.",
      "actions": [
        {
          "action_type": "block_calendar",
          "target_app": "life_manager",
          "payload": {
            "title": "Deep Work: Investor Deck",
            "start": "2026-01-12T09:00:00",
            "end": "2026-01-12T12:00:00"
          }
        }
      ],
      "status": "pending_confirmation"
    },
    {
      "id": "rec_002",
      "priority": 2,
      "domain": "learning",
      "title": "Continue Superbrain Quest — Chapter 7",
      "description": "25 minutes. Fits perfectly in your afternoon energy dip.",
      "reasoning": "You're 68% through this Quest and mentioned wanting to improve memory. Afternoon learning aligns with your lower energy window.",
      "actions": [
        {
          "action_type": "schedule_learning",
          "target_app": "learning_accelerator",
          "payload": {
            "quest_id": "superbrain",
            "chapter": 7,
            "suggested_time": "2026-01-12T15:00:00"
          }
        }
      ],
      "status": "pending_confirmation"
    },
    {
      "id": "rec_003",
      "priority": 3,
      "domain": "social",
      "title": "Reconnect with Jason (A-Fest connection)",
      "description": "You haven't connected in 32 days. He's interested in AI startups.",
      "reasoning": "SIX flagged relationship decay. Jason aligns with your professional network goals. Quick message maintains the connection.",
      "actions": [
        {
          "action_type": "suggest_message",
          "target_app": "six",
          "payload": {
            "contact_id": "contact_jason_123",
            "message_draft": "Hey Jason, hope you're doing well! Been thinking about our A-Fest conversation on AI. Would love to catch up — any time this week?"
          }
        }
      ],
      "status": "pending_confirmation"
    }
  ],
  "meta": {
    "generated_at": "2026-01-12T07:45:00Z",
    "context_signals_used": 28,
    "memories_used": 7,
    "expires_at": "2026-01-12T23:59:59Z"
  }
}
```

---

### API 4: CONFIRM — Handle User Confirmations

**Endpoint**: `POST /api/tie/confirm`

**Purpose**: Apps send user's confirmation/rejection of recommendations back to TIE.

**Request**:
```typescript
interface ConfirmRequest {
  recommendation_id: string;
  action: 'confirm' | 'reject' | 'modify';
  modifications?: Record<string, any>;  // If action is 'modify'
  feedback?: string;                     // Optional user feedback
}
```

**Example — User confirms first recommendation**:
```json
POST /api/tie/confirm
Authorization: Bearer life_manager_service_token_xxx
X-User-ID: user_abc123

{
  "recommendation_id": "rec_001",
  "action": "confirm"
}
```

**Response**:
```json
{
  "status": "confirmed",
  "actions_queued": 1,
  "action_ids": ["act_xxx123"],
  "message": "Deep work block added to your calendar for 9am-12pm."
}
```

**Example — User rejects with feedback**:
```json
POST /api/tie/confirm
Authorization: Bearer life_manager_service_token_xxx
X-User-ID: user_abc123

{
  "recommendation_id": "rec_003",
  "action": "reject",
  "feedback": "Already messaged Jason yesterday"
}
```

**Response**:
```json
{
  "status": "rejected",
  "feedback_recorded": true,
  "memory_updated": true,
  "message": "Got it. I'll remember you connected with Jason recently."
}
```

---

### API 5: COMMIT — Execute Actions (Internal)

**Endpoint**: `POST /api/tie/commit`

**Purpose**: Execute confirmed actions. Called by TIE's internal action processor, but apps can also trigger immediate execution.

**Request**:
```typescript
interface CommitRequest {
  action_ids?: string[];     // Specific actions to execute
  process_queue?: boolean;   // Process all queued actions for user
}
```

**Response**:
```json
{
  "executed": [
    {
      "action_id": "act_xxx123",
      "status": "completed",
      "result": {
        "calendar_event_id": "cal_abc789"
      }
    }
  ],
  "failed": [],
  "pending": []
}
```

---

### API 6: QUERY — Retrieve TIE Data

**Endpoint**: `GET /api/tie/query`

**Purpose**: Apps query TIE for specific data (memories, decisions, user state).

**Query Parameters**:
```typescript
interface QueryParams {
  type: 'memories' | 'decisions' | 'context' | 'profile';
  domain?: string;
  status?: string;          // For decisions
  limit?: number;
  since?: string;           // ISO timestamp
}
```

**Example — Get user's memories about learning**:
```
GET /api/tie/query?type=memories&domain=learning&limit=10
Authorization: Bearer learning_accelerator_service_token_xxx
X-User-ID: user_abc123
```

**Response**:
```json
{
  "memories": [
    {
      "id": "mem_001",
      "type": "goal",
      "content": "Wants to improve public speaking skills",
      "confidence": 0.95,
      "source": "life_manager",
      "created_at": "2026-01-01T10:00:00Z"
    },
    {
      "id": "mem_002",
      "type": "pattern",
      "content": "Prefers learning in 20-30 minute sessions",
      "confidence": 0.78,
      "source": "learning_accelerator",
      "created_at": "2026-01-05T14:30:00Z"
    }
  ]
}
```

---

### API 7: MEMORY — Manage User Memory

**Endpoint**: `POST /api/tie/memory`

**Purpose**: Apps can explicitly add, update, or remove memories.

**Request**:
```typescript
interface MemoryRequest {
  action: 'add' | 'update' | 'remove';
  memory?: {
    type: 'fact' | 'preference' | 'pattern' | 'goal';
    domain?: string;
    content: string;
    confidence?: number;
    expires_at?: string;
  };
  memory_id?: string;       // For update/remove
}
```

**Example — SIX adds a relationship memory**:
```json
POST /api/tie/memory
Authorization: Bearer six_service_token_xxx
X-User-ID: user_abc123

{
  "action": "add",
  "memory": {
    "type": "fact",
    "domain": "social",
    "content": "Met Sarah at A-Fest 2025. She runs a health tech startup in Singapore.",
    "confidence": 1.0
  }
}
```

---

## How Life Manager Interacts with TIE

### Life Manager's Role
Life Manager is the **primary UI** for TIE's decisions. It renders the Morning Brief, Day Planner, and task management — all powered by TIE.

### Integration Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      LIFE MANAGER APP                            │
│                    (React + Supabase)                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌────────────────┐ │
│  │   Morning Brief  │  │    Day Planner   │  │   Task List    │ │
│  │      Screen      │  │      Screen      │  │     Screen     │ │
│  └────────┬─────────┘  └────────┬─────────┘  └───────┬────────┘ │
│           │                     │                     │          │
│           └─────────────────────┼─────────────────────┘          │
│                                 │                                │
│  ┌──────────────────────────────▼───────────────────────────────┐│
│  │                    TIE CLIENT SDK                             ││
│  │  • tieClient.orchestrate()  — Get recommendations             ││
│  │  • tieClient.confirm()      — Confirm/reject actions          ││
│  │  • tieClient.interpret()    — Understand context              ││
│  │  • tieClient.ingest()       — Send signals                    ││
│  └──────────────────────────────┬───────────────────────────────┘│
│                                 │                                │
└─────────────────────────────────┼────────────────────────────────┘
                                  │ HTTPS
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                           TIE API                                │
└─────────────────────────────────────────────────────────────────┘
```

### Key Integration Points

#### 1. Morning Brief Generation

```typescript
// Life Manager: src/services/tie-integration.ts

async function generateMorningBrief(userId: string): Promise<MorningBrief> {
  // Step 1: Get today's context interpretation
  const context = await tieClient.interpret({
    query: "Summarize user's current state: sleep, energy, mood, and pending priorities",
    context_window: 'today',
    domains: ['health', 'work', 'learning', 'social']
  });

  // Step 2: Get prioritized recommendations
  const recommendations = await tieClient.orchestrate({
    intent: "Generate today's top 3 priorities across all life domains",
    constraints: [
      { type: 'time', value: 'today' }
    ],
    max_recommendations: 3
  });

  // Step 3: Combine into Morning Brief
  return {
    greeting: generateGreeting(context),
    healthSummary: {
      sleepScore: context.interpretation.factors.find(f => f.factor === 'sleep_quality')?.value,
      energyLevel: context.interpretation.energy_level,
      recommendation: context.interpretation.recommendation
    },
    priorities: recommendations.recommendations.map(r => ({
      id: r.id,
      title: r.title,
      domain: r.domain,
      reasoning: r.reasoning,
      pendingConfirmation: r.status === 'pending_confirmation'
    })),
    calendarOverview: await getCalendarSummary(userId)
  };
}
```

#### 2. Task Completion → TIE Signal

```typescript
// Life Manager: When user completes a task

async function onTaskCompleted(task: Task) {
  // Update local state
  await supabase.from('tasks').update({ status: 'completed' }).eq('id', task.id);

  // Send signal to TIE (async, non-blocking)
  tieClient.ingest({
    signals: [{
      type: 'task.completed',
      domain: 'work',
      payload: {
        task_id: task.id,
        title: task.title,
        duration_minutes: task.actualDuration,
        was_priority: task.isPriority,
        completion_quality: task.completionRating  // If user rated
      },
      importance: task.isPriority ? 0.9 : 0.5
    }]
  });
}
```

#### 3. User Confirms Recommendation

```typescript
// Life Manager: Morning Brief UI

async function handleRecommendationAction(
  recId: string,
  action: 'confirm' | 'reject' | 'modify',
  modifications?: any
) {
  const result = await tieClient.confirm({
    recommendation_id: recId,
    action,
    modifications
  });

  if (result.status === 'confirmed') {
    // Refresh UI to show the confirmed action
    toast.success(result.message);
    await refreshMorningBrief();
  } else if (result.status === 'rejected') {
    // Remove from pending
    removePendingRecommendation(recId);
  }
}
```

#### 4. Calendar Sync → TIE Awareness

```typescript
// Life Manager: After Google Calendar sync

async function syncCalendarToTIE(events: CalendarEvent[]) {
  const signals = events.map(event => ({
    type: 'calendar.event_scheduled',
    domain: 'work',
    payload: {
      event_id: event.id,
      title: event.title,
      start: event.start,
      end: event.end,
      is_meeting: event.attendees?.length > 0,
      attendee_count: event.attendees?.length || 0
    },
    importance: event.priority === 'high' ? 0.8 : 0.5
  }));

  await tieClient.ingest({ signals });
}
```

---

## TIE Client SDK

### Installation

```bash
npm install @vibe/tie-client
```

### Configuration

```typescript
// Life Manager: src/lib/tie.ts

import { TIEClient } from '@vibe/tie-client';

export const tieClient = new TIEClient({
  baseUrl: process.env.TIE_API_URL,
  serviceToken: process.env.TIE_SERVICE_TOKEN,
  appName: 'life_manager',

  // Retry configuration
  retries: 3,
  retryDelay: 1000,

  // Timeout
  timeout: 30000,  // 30 seconds for AI operations

  // Hooks
  onError: (error) => {
    captureException(error);  // Sentry
  }
});
```

### SDK Methods

```typescript
interface TIEClient {
  // Core Trust Loop
  ingest(request: IngestRequest): Promise<IngestResponse>;
  interpret(request: InterpretRequest): Promise<InterpretResponse>;
  orchestrate(request: OrchestrateRequest): Promise<OrchestrateResponse>;
  confirm(request: ConfirmRequest): Promise<ConfirmResponse>;

  // Data Access
  query(params: QueryParams): Promise<QueryResponse>;
  memory(request: MemoryRequest): Promise<MemoryResponse>;

  // User Context
  setUserId(userId: string): void;
  getUserProfile(): Promise<UserProfile>;

  // Utilities
  isHealthy(): Promise<boolean>;
  getVersion(): string;
}
```

---

## Team Requirements

### TIE Core Team (4-6 people)

| Role | Responsibilities | Skills |
|------|-----------------|--------|
| **Tech Lead / Architect** | Overall TIE architecture, API design, cross-app integration | Senior backend, distributed systems, AI/ML |
| **ML Engineer** | LLM orchestration, prompt engineering, embeddings, memory retrieval | Python, LLM APIs, RAG systems |
| **Backend Engineer (2)** | Edge functions, database, action queue, integrations | TypeScript, Supabase, PostgreSQL |
| **DevOps / Platform** | Infrastructure, monitoring, security, scaling | Supabase, Vercel/Railway, observability |
| **Product Manager** | PRD ownership, cross-app coordination, user feedback | Technical PM experience, AI products |

### Hiring Priority

1. **ML Engineer** — Critical for TIE's intelligence quality
2. **Tech Lead** — Architecture decisions and API design
3. **Backend Engineer** — Build the core Trust Loop
4. **PM** — Coordinate with app teams

### Cross-Team Collaboration

```
TIE Team
    │
    ├── Weekly sync with Life Manager team (primary consumer)
    ├── Weekly sync with Vibrantly team (health signals)
    ├── Bi-weekly sync with SIX team (social signals)
    └── Bi-weekly sync with Learning team (learning signals)
```

---

## Implementation Roadmap

### Phase 1: Foundation (Months 1-2)

- [ ] Set up TIE Supabase project
- [ ] Implement core database schema
- [ ] Build Ingest API
- [ ] Build basic Interpret API (single-domain)
- [ ] TIE Client SDK v0.1
- [ ] Life Manager integration for task signals

### Phase 2: Intelligence (Months 3-4)

- [ ] Implement Orchestrate API
- [ ] Build LLM orchestration layer
- [ ] Memory system with embeddings
- [ ] Confirm/Commit flow
- [ ] Morning Brief powered by TIE
- [ ] Vibrantly health signal integration

### Phase 3: Cross-Domain (Months 5-6)

- [ ] Multi-domain reasoning
- [ ] SIX social signal integration
- [ ] Learning Accelerator integration
- [ ] Full Trust Loop audit trail
- [ ] User feedback loop

### Phase 4: Scale (Months 7-9)

- [ ] Performance optimization
- [ ] Advanced personalization
- [ ] Marketplace plugin API
- [ ] Enterprise features

---

## Security & Privacy

### Data Handling

| Data Type | Storage | Encryption | Retention |
|-----------|---------|------------|-----------|
| User profile | TIE Supabase | At rest + transit | Until account deletion |
| Signals | TIE Supabase | At rest + transit | 90 days rolling |
| Memories | TIE Supabase | At rest + transit | Until explicit removal |
| Decisions | TIE Supabase | At rest + transit | 1 year (audit trail) |
| Health data | TIE Supabase | At rest + transit + field-level | Per user preference |

### API Security

- All API calls require valid service token
- Service tokens are scoped per-app
- User ID must match authenticated session
- Rate limiting: 100 requests/minute per user
- All PII redacted from logs

### Compliance

- GDPR: Data export, right to deletion
- CCPA: Opt-out mechanisms
- SOC 2: Audit trail, access controls
- HIPAA-adjacent: Health data encryption (not full HIPAA)

---

## Success Metrics

### Technical KPIs

| Metric | Target | Measurement |
|--------|--------|-------------|
| API latency (p95) | < 500ms | Interpret, Orchestrate |
| API availability | 99.9% | All endpoints |
| Recommendation acceptance rate | > 60% | Confirm actions / Total recommendations |
| Memory retrieval accuracy | > 85% | Relevant memories surfaced |

### Product KPIs

| Metric | Target | Measurement |
|--------|--------|-------------|
| Morning Brief completion | > 70% | Users who review full brief |
| Cross-domain recommendations | > 30% | Recommendations spanning 2+ domains |
| User trust score | > 4.2/5 | Weekly survey |
| Time to first recommendation | < 3 seconds | From app load |

---

## Appendix: Example Full Flow

### Scenario: User wakes up, opens Life Manager

```
1. Life Manager loads
   └── Calls: GET /api/tie/query?type=context
       └── TIE returns: Current active context for user

2. Life Manager requests Morning Brief
   └── Calls: POST /api/tie/interpret
       └── TIE analyzes: Sleep data (Vibrantly), yesterday's tasks, 3 MIQ goals
       └── Returns: Energy = high, deep_work_readiness = 85%

3. Life Manager requests priorities
   └── Calls: POST /api/tie/orchestrate
       └── TIE considers: Calendar, pending tasks, learning progress, relationship decay
       └── Returns: 3 prioritized recommendations with reasoning

4. User confirms recommendation #1
   └── Life Manager calls: POST /api/tie/confirm
       └── TIE queues action, updates decision log
       └── Returns: Success + calendar event created

5. User rejects recommendation #3 with feedback
   └── Life Manager calls: POST /api/tie/confirm (action: reject)
       └── TIE logs feedback, updates memory ("User prefers X over Y")
       └── Returns: Acknowledged

6. User completes a task at 11am
   └── Life Manager calls: POST /api/tie/ingest
       └── TIE records signal, updates active context
       └── May trigger: New recommendation for next priority

7. End of day: Life Manager triggers review
   └── Calls: POST /api/tie/orchestrate (intent: "end of day review")
       └── TIE analyzes: Completed tasks, energy patterns, what didn't get done
       └── Returns: Summary + suggestions for tomorrow
```

---

*Document Version: 1.0*
*Created: January 2026*
*Status: Technical PRD for Review*
