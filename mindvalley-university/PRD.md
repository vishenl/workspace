# Mindvalley University — Product Requirements Document

## Executive Summary

Mindvalley University is the unified ecosystem that brings together all Vibe Inc modules into a cohesive life operating layer for Mindvalley's most engaged users. It serves as the central hub where ELIZA (the AI interface) and TIE (The Intelligence Engine) orchestrate health, learning, relationships, and productivity into one personalized experience.

**Vision**: One plan, one explanation, one voice — helping Mindvalley members live their most extraordinary life.

**Target Launch**: Mindvalley Mastery Program students (high-intent, high-value users already invested in transformation)

---

## The Problem

Mindvalley members currently experience fragmentation across:

1. **Learning**: Quests, Masterclasses, and programs exist in silos without personalized guidance on what to learn next
2. **Health**: No integration between Mindvalley's wellness content and members' actual health data
3. **Community**: A-Fest, local chapters, and online connections are disconnected from daily life
4. **Productivity**: No system to translate insights into daily action
5. **Progress**: Members can't see holistic growth across life categories

**Result**: Transformation happens in bursts, not as a sustained operating system for life.

---

## The Solution: Mindvalley University

### Core Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         ELIZA                                    │
│              (The Voice & Interface Layer)                       │
│     Natural language • Explanations • Confirmations              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                          TIE                                     │
│              (The Intelligence Engine)                           │
│     Cross-domain reasoning • Life model • Orchestration          │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────┬─────────┬─────────┬─────────┬─────────┐
        ▼         ▼         ▼         ▼         ▼         ▼
   ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
   │Vibrantly│ │   SIX   │ │Learning │ │   Day   │ │  3 MIQ  │ │Connectors│
   │ Health  │ │Relations│ │Accelerat│ │ Planner │ │ Goals   │ │  Inputs  │
   └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘
```

### The Trust Loop

Every action follows this principle:

```
INGEST → INTERPRET → ORCHESTRATE → CONFIRM → COMMIT
```

- **Nothing commits silently** — users always confirm before action
- **Everything is explainable** — every recommendation includes reasoning
- **One audit trail** — users can see why decisions were made

---

## Core Modules

### 1. Morning Brief (Daily Entry Point)
The primary touchpoint that surfaces the day's priorities.

**Features**:
- Today's top 3 priorities across all life domains
- Health check-in (sleep, energy, readiness)
- Learning recommendation (what to study today)
- Connection nudge (who to reach out to)
- Calendar overview with energy-aligned scheduling

**Example Morning Brief**:
```
Good morning, Vishen. Based on your Oura data, you slept 7.2 hours
with 85% sleep score. Your HRV is elevated — great day for creative work.

TODAY'S FOCUS:
1. Deep work: Finish Vibe Inc investor deck (9am-12pm)
2. Learn: Continue "Superbrain" Quest - Chapter 7 (25 min)
3. Connect: Follow up with Jason (A-Fest connection)

Your energy dips around 3pm. I've blocked that for admin tasks.
```

### 2. Vibrantly (Health Intelligence)
Longevity and health optimization powered by real data.

**Features**:
- Lab results analysis and tracking
- Supplement recommendations with interaction checks
- Recovery optimization (sleep, HRV, activity)
- Biomarker trends over time
- Personalized health insights from Mindvalley's longevity content

**Integration Points**:
- Oura, Whoop, Apple Health
- Lab providers (Function Health, Quest, etc.)
- Mindvalley health Quests and experts

### 3. SIX (Relationship Intelligence)
The social layer for meaningful connections.

**Features**:
- Relationship health scoring across 6 key relationships
- Connection reminders based on relationship decay
- A-Fest and event networking optimization
- Local chapter integration
- Gratitude and appreciation prompts

**The SIX Framework**:
1. Romantic Partner
2. Family
3. Inner Circle (5 closest friends)
4. Colleagues & Collaborators
5. Mentors & Guides
6. Community & Tribe

### 4. Learning Accelerator
Personalized learning paths from Mindvalley's content library.

**Features**:
- AI-curated "what to learn next" based on goals
- Progress tracking across all Quests
- Spaced repetition for key concepts
- Application reminders (put learning into practice)
- Expert Q&A with grounded AI (answers only from actual content)

**Smart Recommendations**:
```
Based on your goal to "improve public speaking," here's your path:

Week 1-2: "Speak and Inspire" with Lisa Nichols (foundations)
Week 3-4: "The Art of Stage Presence" with Michael Beckwith
Ongoing: Daily 5-min practice prompts from "Ultralearning"

You're 34% through this journey. Next lesson: 18 minutes.
```

### 5. Day Planner
Execution layer that turns intentions into completed tasks.

**Features**:
- Unified calendar from Google, Outlook, etc.
- Energy-aware scheduling (align tasks with biorhythms)
- Deep work block protection
- Task prioritization using 3 MIQ goals
- End-of-day review and tomorrow preparation

### 6. 3 MIQ (Three Most Important Questions)
Goal clarity and life direction compass.

**Features**:
- Guided process to define 3 life priorities
- Quarterly review rituals
- Progress visualization
- Goal decomposition into actionable milestones
- Alignment check (are daily actions serving 3 MIQ?)

**The 3 MIQ Framework**:
1. **Experiences**: What experiences do I want to have?
2. **Growth**: How do I want to grow and develop?
3. **Contribution**: How do I want to contribute to the world?

---

## User Personas

### Primary: Mastery Program Student
- Already invested $5,000+ in Mindvalley programs
- High intent for transformation
- Busy professional (limited time)
- Values systems and optimization
- Willing to pay for premium tools

**Jobs to be Done**:
- "Help me apply what I'm learning"
- "Show me what to focus on today"
- "Keep me connected to my community"
- "Track my growth over time"

### Secondary: A-Fest Alumni
- Attended A-Fest, deeply connected to tribe
- Wants to maintain event connections
- Interested in holistic life design
- Ambassador for Mindvalley

---

## Information Architecture

```
Mindvalley University
│
├── Morning Brief (Home)
│   ├── Today's Priorities
│   ├── Quick Actions
│   └── ELIZA Chat
│
├── Vibrantly (Health)
│   ├── Dashboard
│   ├── Biomarkers
│   ├── Supplements
│   └── Recovery
│
├── SIX (Relationships)
│   ├── Relationship Map
│   ├── Connection Queue
│   ├── Events & Community
│   └── Appreciation Log
│
├── Learning
│   ├── My Path
│   ├── Quest Library
│   ├── Progress
│   └── Expert Q&A
│
├── Planner
│   ├── Today
│   ├── Calendar
│   ├── Tasks
│   └── Reviews
│
├── 3 MIQ (Goals)
│   ├── My Questions
│   ├── Progress
│   └── Quarterly Review
│
├── ELIZA (AI Assistant)
│   ├── Chat Interface
│   ├── History
│   └── Preferences
│
└── Settings
    ├── Profile
    ├── Connections
    ├── Privacy
    └── Preferences
```

---

## Key User Flows

### Flow 1: Morning Ritual
1. User opens app → Morning Brief loads
2. Sees sleep score, energy forecast, top 3 priorities
3. Reviews and confirms/adjusts priorities
4. ELIZA offers to add learning block to calendar
5. User confirms → Day is set

### Flow 2: Learning Session
1. User has 20 minutes free
2. Opens Learning → "Quick Learn" suggested
3. ELIZA recommends specific lesson based on progress + time
4. User completes lesson
5. Key takeaway logged, practice reminder scheduled

### Flow 3: Connection Nudge
1. SIX surfaces "You haven't connected with [Name] in 30 days"
2. User sees context: "A-Fest 2024 connection, discussed AI startups"
3. ELIZA suggests: "Want me to draft a quick check-in message?"
4. User reviews, edits, sends
5. Relationship score updates

### Flow 4: Health Check
1. User syncs new lab results
2. Vibrantly analyzes against baseline
3. ELIZA explains: "Your Vitamin D is up 40% since starting supplements"
4. Suggests adjustment to supplement protocol
5. User confirms → Protocol updated

---

## Technical Requirements

### Platform
- **Web**: Progressive Web App (PWA) for desktop and mobile web
- **Mobile**: Native iOS and Android apps (Phase 2)

### Tech Stack
- **Frontend**: React 18 + Vite + TailwindCSS
- **Backend**: Supabase (Auth, Database, Realtime, Edge Functions)
- **AI**: OpenAI GPT-4 + Anthropic Claude for different use cases
- **Integrations**: OAuth connectors for health apps, calendars, etc.

### Security
- Row-Level Security (RLS) on all data
- End-to-end encryption for sensitive health data
- SOC 2 compliance pathway
- GDPR/CCPA compliant data handling

### Integrations (Phase 1)
- Google Calendar, Outlook
- Oura, Apple Health
- Mindvalley Platform (Quests, Progress)
- Function Health (labs)

---

## Design Principles

### 1. Calm Over Chaos
- White space, clean typography
- No notification overload
- Morning Brief as single daily touchpoint

### 2. Explain Everything
- Every recommendation has a "Why?" button
- No black box decisions
- Build trust through transparency

### 3. Confirm Before Commit
- Nothing happens automatically without user consent
- Easy undo for all actions
- User remains in control

### 4. Progressive Disclosure
- Start simple, reveal complexity on demand
- New users see essentials
- Power users access advanced features

### 5. Delight in Details
- Micro-animations that feel premium
- Personalized touches (name, context)
- Celebration of milestones

---

## Success Metrics

### Engagement
- Daily Active Users (DAU) / Monthly Active Users (MAU)
- Morning Brief completion rate
- Average session duration
- Feature adoption across modules

### Outcomes
- Quest completion rate (vs. non-University users)
- Self-reported life satisfaction scores
- Goal achievement rate (3 MIQ)
- Connection frequency (SIX engagement)

### Business
- Conversion rate from trial to paid
- Retention at 30/60/90 days
- Net Promoter Score (NPS)
- Revenue per user

---

## Monetization

### Subscription Tiers

**Mindvalley University Essentials** — Included with Membership
- Morning Brief
- Basic Learning Accelerator
- Limited SIX features
- 3 MIQ goal setting

**Mindvalley University Pro** — $29/month
- Full ELIZA AI access
- Complete Vibrantly health module
- Full SIX relationship features
- Advanced Day Planner
- Unlimited Learning Accelerator
- Priority support

**Mindvalley University Elite** — $99/month
- Everything in Pro
- 1:1 monthly coaching call
- Early access to new features
- VIP community access
- White-glove onboarding

---

## Roadmap

### Phase 1: Foundation (Months 1-3)
- [ ] Morning Brief MVP
- [ ] Basic ELIZA chat
- [ ] Learning Accelerator (Quest integration)
- [ ] 3 MIQ goal setting
- [ ] Mindvalley SSO integration

### Phase 2: Health & Connections (Months 4-6)
- [ ] Vibrantly health module
- [ ] SIX relationship module
- [ ] Oura/Apple Health integration
- [ ] A-Fest attendee import

### Phase 3: Productivity (Months 7-9)
- [ ] Day Planner with calendar sync
- [ ] Energy-aware scheduling
- [ ] Task management
- [ ] End-of-day reviews

### Phase 4: Intelligence (Months 10-12)
- [ ] TIE cross-module reasoning
- [ ] Personalized life model
- [ ] Predictive recommendations
- [ ] Advanced analytics

---

## Appendix: ELIZA Personality

ELIZA is warm, insightful, and gently encouraging. She speaks like a wise mentor who knows you well.

**Voice Characteristics**:
- Uses your name naturally
- References past conversations and progress
- Celebrates wins, both big and small
- Asks permission before taking action
- Explains reasoning in simple terms
- Never condescending or robotic

**Example Interactions**:

```
User: "I'm feeling overwhelmed today"

ELIZA: "I hear you, Vishen. Looking at your calendar, you have 6
meetings scheduled and your Oura shows lower HRV than usual.

Would you like me to suggest which meetings could be rescheduled?
Or I can block 30 minutes for a breathing exercise — Jim Kwik's
'Brain Reboot' technique might help here."
```

```
User: "What should I learn today?"

ELIZA: "Based on your 3 MIQ goal to 'become a better public speaker,'
I'd suggest continuing Lisa Nichols' 'Speak and Inspire' — you're
on Chapter 4 about storytelling. It's 22 minutes.

Or, since you mentioned feeling creative today, we could switch to
'The Art of Innovation' which you saved last week. What feels right?"
```

---

*Document Version: 1.0*
*Created: January 2026*
*Status: Draft for Review*
