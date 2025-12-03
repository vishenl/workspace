# Mindvalley Quest Designer API

## For AI Systems

This document provides machine-readable documentation for AI systems to interact with the Quest Designer platform.

## Base URL

```
https://quest-designer.mindvalley.com/api
```

## Available Endpoints

### Schema Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/schema` | Complete schema document |
| GET | `/schema/quest` | Quest schema only |
| GET | `/schema/daily-lesson` | Daily Lesson schema |
| GET | `/schema/habit-scaffold` | Habit Scaffold schema |
| GET | `/schema/peer-groups` | Peer Groups schema |
| GET | `/schema/story-arc` | Story Arc schema |

### Operational Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/quest/validate` | Validate Quest JSON |
| POST | `/quest/preview` | Generate visual preview (v2) |
| GET | `/templates` | List all templates |
| GET | `/templates/{id}` | Get specific template |

## The 5 Pillars of Transformation

Every Mindvalley Quest is built on these foundational pillars:

### 1. Transcendent Practice
- **Purpose**: Daily exercises that shift consciousness
- **Examples**: Meditation, visualization, breathwork, flow states
- **Integration**: Usually 5-15 minutes daily

### 2. New Models of Reality
- **Purpose**: Paradigm shifts that change worldview
- **Examples**: Belief upgrades, mental models, reframing
- **Integration**: Introduced in video lessons, reinforced through tasks

### 3. Critical Reflection
- **Purpose**: Self-awareness and integration
- **Examples**: Journaling, self-assessment, insight exercises
- **Integration**: Daily reflection prompts, weekly reviews

### 4. Habit Scaffolding
- **Purpose**: Lasting behavior change through design
- **Examples**: Tiny habits, anchoring, identity-based change
- **Integration**: Progressive habit building over Quest duration

### 5. Community & Social Learning
- **Purpose**: Amplify transformation through belonging
- **Examples**: Peer groups, accountability partners, tribe connections
- **Integration**: Weekly calls, daily check-ins, shared challenges

## Quick Start for AI Systems

### Creating a Daily Lesson

```json
POST /api/quest/lesson
Content-Type: application/json

{
  "quest_title": "Becoming Limitless",
  "day": 7,
  "pillar": "critical_reflection",
  "story_stage": "tests_and_allies",
  "topic": "inner critic",
  "generate": {
    "title": true,
    "objective": true,
    "task": true,
    "reflection_prompt": true
  }
}
```

### Expected Response

```json
{
  "success": true,
  "daily_lesson": {
    "day": 7,
    "title": "Overcoming the Inner Critic",
    "objective": "Learner recognizes negative self-talk patterns and transforms them into empowering affirmations.",
    "task": "Track one negative belief today. Write it down, then rewrite it as an empowering affirmation. Say the new belief out loud 3 times.",
    "reflection_prompt": "What belief did you rewrite today? How did it feel to speak the new affirmation?",
    "pillar": "critical_reflection",
    "story_stage": "tests_and_allies"
  }
}
```

### Creating a Habit Scaffold

```json
POST /api/habit-scaffold
Content-Type: application/json

{
  "habit": "Morning meditation",
  "quest_duration": 21,
  "target_duration_minutes": 20,
  "generate": {
    "anchor": true,
    "tiny_version": true,
    "identity_label": true,
    "progression": true
  }
}
```

## Hero's Journey Mapping

Map your Quest to the Hero's Journey for emotional engagement:

| Stage | Typical Days (21-day) | Purpose |
|-------|----------------------|---------|
| Ordinary World | 1-3 | Establish current reality, pain points |
| Call to Adventure | 4-7 | Vision of transformation, why now |
| Crossing Threshold | 8-10 | First real commitment, breaking patterns |
| Tests & Allies | 11-17 | Practice, community, skill building |
| Transformation | 18-21 | Integration, new identity, lasting change |

## Validation Rules

When creating Quests, ensure:

1. **Duration**: 7-90 days (standard: 21, 30, 45, 60, 90)
2. **Pillars**: At least 2-3 pillars per Quest
3. **Daily Lessons**: Cover full duration
4. **Video Length**: 8-20 minutes per day
5. **Task Duration**: 10-30 minutes per day
6. **Reflection Prompts**: Required for all lessons

## Content Type

All API responses are `application/json` unless otherwise specified.

## Rate Limits

- 100 requests per minute for schema endpoints
- 20 requests per minute for generation endpoints

## Error Responses

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid pillar specified",
    "details": {
      "field": "pillar",
      "received": "invalid_pillar",
      "expected": ["transcendent_practice", "new_models_of_reality", "critical_reflection", "habit_scaffolding", "community_social"]
    }
  }
}
```

## Contact

For API support: api@mindvalley.com
