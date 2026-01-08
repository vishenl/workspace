# Vibrantly Projects Feature - Comprehensive Proposal

## Executive Summary

Transform Vibrantly from a simple blood work analyzer into a **comprehensive health optimization project management system**. Users can create health improvement projects (e.g., "Optimize Testosterone," "Reduce Inflammation," "30-Day Detox"), assign tasks, track biomarker changes over time, and gain AI-powered productivity insights.

---

## Table of Contents

1. [Core Project Features](#1-core-project-features)
2. [Task Management System](#2-task-management-system)
3. [Project Intelligence & Analytics](#3-project-intelligence--analytics)
4. [Innovative Features](#4-innovative-features)
5. [Database Schema](#5-database-schema)
6. [UI/UX Proposals](#6-uiux-proposals)
7. [Implementation Phases](#7-implementation-phases)

---

## 1. Core Project Features

### 1.1 Project CRUD Operations

| Feature | Description |
|---------|-------------|
| **Create Project** | Name, description, target completion date, health goals linkage |
| **Edit Project** | Update details, reassign health data, modify timeline |
| **Delete Project** | Soft delete with archive, option to permanently delete |
| **Duplicate Project** | Clone a project as a template for new health initiatives |

### 1.2 Project States & Lifecycle

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   DRAFT     │───▶│   ACTIVE    │───▶│  COMPLETED  │    │  ARCHIVED   │
│  (Planning) │    │ (In Progress)│    │   (Done)    │    │  (Hidden)   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                          │                   │                   ▲
                          │                   └───────────────────┘
                          ▼
                   ┌─────────────┐
                   │   PAUSED    │
                   │  (On Hold)  │
                   └─────────────┘
```

**States:**
- **Draft**: Planning phase, no active tasks yet
- **Active**: Project is in progress, tasks being worked on
- **Paused**: Temporarily on hold (e.g., waiting for next blood work)
- **Completed**: All tasks done, goals achieved
- **Archived**: Hidden from view but preserved for history

### 1.3 Project Types (Health-Specific)

| Type | Description | Example |
|------|-------------|---------|
| **Biomarker Optimization** | Focus on improving specific biomarkers | "Increase Vitamin D to 60 ng/mL" |
| **Health Protocol** | Follow a structured health program | "Gary Brecka 30-30-30 Protocol" |
| **Supplement Stack** | Track supplement effectiveness | "Optimize Morning Stack" |
| **Lifestyle Change** | Track habit-based improvements | "90-Day Sleep Optimization" |
| **Medical Investigation** | Track diagnosis/treatment journey | "Thyroid Investigation" |
| **Comparative Analysis** | Compare blood work over time | "Q1 vs Q2 Health Comparison" |

### 1.4 Project Views

| View | Description |
|------|-------------|
| **List View** | Simple list with status, progress, due date |
| **Kanban Board** | Drag-and-drop cards across status columns |
| **Timeline/Gantt** | Visual timeline of project and task durations |
| **Calendar View** | Tasks and milestones on calendar |
| **Dashboard View** | Summary cards with key metrics |

---

## 2. Task Management System

### 2.1 Task Structure

```typescript
interface Task {
  id: string;
  project_id: string;
  title: string;
  description: string;
  type: TaskType;
  status: 'todo' | 'in_progress' | 'blocked' | 'completed' | 'cancelled';
  priority: 'low' | 'medium' | 'high' | 'critical';
  due_date: Date | null;
  scheduled_date: Date | null;
  completed_at: Date | null;
  assignee: string; // user_id (for future multi-user)
  parent_task_id: string | null; // for subtasks
  tags: string[];
  recurrence: RecurrenceRule | null;
  time_estimate: number; // in minutes
  actual_time: number; // tracked time
  linked_biomarkers: string[]; // biomarker IDs this task affects
  notes: string;
  attachments: Attachment[];
  created_at: Date;
  updated_at: Date;
}
```

### 2.2 Task Types (Health-Specific)

| Type | Icon | Description |
|------|------|-------------|
| **Blood Work** | 🩸 | Schedule and upload blood test |
| **Supplement** | 💊 | Take or adjust supplement |
| **Diet** | 🥗 | Dietary change or tracking |
| **Exercise** | 🏃 | Physical activity task |
| **Sleep** | 😴 | Sleep optimization task |
| **Meditation** | 🧘 | Mindfulness or stress management |
| **Doctor Visit** | 👨‍⚕️ | Medical appointment |
| **Research** | 📚 | Learn about health topic |
| **Measurement** | 📏 | Track weight, blood pressure, etc. |
| **Custom** | ⚡ | User-defined task |

### 2.3 Task Features

| Feature | Description |
|---------|-------------|
| **Subtasks** | Break down tasks into smaller steps |
| **Dependencies** | Task B can't start until Task A completes |
| **Recurring Tasks** | Daily/weekly/monthly repeat (e.g., "Take Vitamin D daily") |
| **Time Tracking** | Built-in timer or manual entry |
| **Reminders** | Push/email notifications before due dates |
| **Comments** | Add notes and updates to tasks |
| **File Attachments** | Attach PDFs, images, lab results |
| **Biomarker Linking** | Link tasks to specific biomarkers they affect |
| **Quick Actions** | Complete, reschedule, duplicate from list view |

### 2.4 Recurring Task Patterns

For health routines, support these patterns:

```
- Every day at 8:00 AM (supplements)
- Every Monday, Wednesday, Friday (exercise)
- Every 3 months (blood work)
- First Monday of each month (doctor check-in)
- Custom: Every X days/weeks/months
```

---

## 3. Project Intelligence & Analytics

### 3.1 Time Intelligence Dashboard

Track the full project lifecycle:

```
┌─────────────────────────────────────────────────────────────────┐
│                    PROJECT TIME INTELLIGENCE                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Created ──────▶ Started ──────▶ Completed                      │
│  Jan 15         Jan 18          Mar 22                          │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Planning Time│  │ Active Time  │  │ Total Time   │          │
│  │    3 days    │  │   63 days    │  │   66 days    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Tasks Done   │  │ On-Time %    │  │ Time/Task    │          │
│  │    24/24     │  │     87%      │  │   2.6 days   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Metrics Tracked

| Metric | Description |
|--------|-------------|
| **Planning Duration** | Time from creation to first task started |
| **Active Duration** | Time from first task to last task completed |
| **Total Duration** | Created to completed |
| **Estimated vs Actual** | Compare planned timeline to reality |
| **Task Velocity** | Tasks completed per day/week |
| **On-Time Rate** | % of tasks completed by due date |
| **Blocked Time** | Total time tasks spent blocked |
| **Time per Task Type** | Average time for supplements vs exercise, etc. |

### 3.3 Productivity Insights (AI-Powered)

```
┌─────────────────────────────────────────────────────────────────┐
│                    🧠 AI PRODUCTIVITY INSIGHTS                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  "You complete 73% more tasks on Tuesdays. Consider scheduling  │
│   important health tasks early in the week."                     │
│                                                                  │
│  "Projects with fewer than 10 tasks have a 2.3x higher          │
│   completion rate. Try breaking down 'Optimize Everything' into  │
│   smaller focused projects."                                     │
│                                                                  │
│  "Blood work tasks take an average of 14 days from scheduled    │
│   to completed. Plan ahead for your next test."                  │
│                                                                  │
│  "Your morning supplement routine has 94% adherence. Great job!" │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 3.4 Historical Analytics

| Feature | Description |
|---------|-------------|
| **Completed Projects Gallery** | Filterable archive of all finished projects |
| **Project Comparison** | Compare metrics across similar projects |
| **Trend Analysis** | How is your completion rate improving over time? |
| **Biomarker Correlation** | Did completing project X improve biomarker Y? |
| **Seasonal Patterns** | Are you more productive in certain seasons? |
| **Streak Tracking** | Consecutive days/weeks with completed tasks |

---

## 4. Innovative Features

### 4.1 🎯 Smart Project Templates

Pre-built templates for common health optimization journeys:

| Template | Duration | Tasks | Description |
|----------|----------|-------|-------------|
| **30-Day Vitamin D Optimization** | 30 days | 12 | Daily supplementation + blood work verification |
| **Gary Brecka Protocol** | 90 days | 45 | Complete 30-30-30 + supplements |
| **Inflammation Reset** | 60 days | 28 | Diet changes + supplements + blood work |
| **Sleep Optimization Journey** | 21 days | 21 | Daily sleep hygiene tasks |
| **Quarterly Health Check** | Recurring | 8 | Regular blood work + review cycle |

Users can also **save their own projects as templates**.

### 4.2 🤖 AI Project Assistant

**Auto-Generate Tasks from Goals:**
```
User: "I want to increase my testosterone naturally"

AI: Based on your current blood work (Total T: 380 ng/dL), I've created
    a project with these suggested tasks:

    Week 1-2: Baseline & Research
    □ Schedule comprehensive hormone panel
    □ Research natural T-boosting protocols
    □ Review current sleep patterns

    Week 3-8: Protocol Implementation
    □ Start Vitamin D3 (5000 IU/day)
    □ Add Zinc (30mg before bed)
    □ Implement strength training 3x/week
    □ Optimize sleep to 7-8 hours

    Week 12: Verification
    □ Schedule follow-up blood work
    □ Compare results and adjust

    [Create Project] [Customize First]
```

**Smart Task Suggestions:**
- When you add a task, AI suggests related tasks
- "You added 'Take Vitamin D' - would you also like to add 'Take with fat for absorption'?"

### 4.3 📊 Biomarker-Project Correlation

Link projects to biomarkers and track improvement:

```
┌─────────────────────────────────────────────────────────────────┐
│              PROJECT: Vitamin D Optimization                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  LINKED BIOMARKER: Vitamin D, 25-Hydroxy                        │
│                                                                  │
│       60 ┤                                        ●──────        │
│          │                              ●────────                │
│       40 ┤              ●──────────────                          │
│          │    ●────────                                          │
│       20 ┤                                                       │
│          └────┬─────────┬──────────────┬──────────┬─────────    │
│             Jan 1     Feb 1          Mar 1      Apr 1            │
│            (Start)                             (Current)         │
│                                                                  │
│  📈 IMPROVEMENT: +133% (22 → 51 ng/mL)                          │
│  🎯 TARGET: 60 ng/mL (85% of goal reached)                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 4.4 🔔 Smart Notifications & Reminders

| Trigger | Notification |
|---------|--------------|
| **Task Due Soon** | "Your blood work appointment is tomorrow" |
| **Streak at Risk** | "You've maintained a 14-day supplement streak! Take today's dose to keep it going" |
| **Project Stale** | "No activity on 'Inflammation Reset' for 7 days. Resume or pause?" |
| **Milestone Reached** | "Congratulations! You've completed 50% of your health protocol" |
| **Blood Work Due** | "It's been 3 months since your last blood work. Time for a check?" |
| **Goal Achievement** | "Your Vitamin D is now in optimal range! Project goal achieved" |

### 4.5 🏆 Gamification & Motivation

| Feature | Description |
|---------|-------------|
| **Health Score Impact** | Show how completing tasks affects overall health score |
| **Achievement Badges** | "Protocol Pioneer" (complete first project), "Streak Master" (30 days) |
| **Streak Calendar** | Visual heatmap of daily task completion |
| **Leaderboard** | Compare (anonymized) with similar users (opt-in) |
| **Celebration Moments** | Animations when completing projects/milestones |
| **Progress Sharing** | Share achievements to social (without sensitive data) |

### 4.6 📱 Quick Capture & Daily Review

**Quick Add Widget:**
- Floating button to quickly add tasks
- Voice input: "Add task take vitamin D tomorrow morning"
- Shortcut: Add from blood work results directly

**Daily Review Mode:**
```
┌─────────────────────────────────────────────────────────────────┐
│                    DAILY HEALTH REVIEW                           │
│                      Tuesday, Jan 7                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  MORNING ROUTINE (6 tasks)                    ⬚ Mark All Done   │
│  ☑ Wake up by 7 AM                                              │
│  ☑ Morning sunlight (10 min)                                    │
│  ☐ Take Vitamin D + K2                                          │
│  ☐ Take Omega-3                                                 │
│  ☐ 30-min walk                                                  │
│  ☐ Log weight                                                   │
│                                                                  │
│  TODAY'S FOCUS                                                   │
│  ☐ Schedule blood work appointment         📅 Due Today         │
│                                                                  │
│  COMING UP                                                       │
│  ☐ Doctor follow-up call                   📅 Tomorrow          │
│  ☐ Reorder supplements                     📅 Friday            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 4.7 🔗 External Integrations

| Integration | Purpose |
|-------------|---------|
| **Apple Health** | Import sleep, steps, heart rate data |
| **Google Fit** | Import activity data |
| **Oura Ring** | Import sleep & readiness scores |
| **Whoop** | Import strain & recovery data |
| **MyFitnessPal** | Import nutrition data |
| **Lab Corp/Quest** | Auto-import blood work results |
| **Calendar Sync** | Sync tasks to Google/Apple Calendar |

### 4.8 🧬 Personalized Recommendations

Based on user's profile and blood work:

```
"Based on your low Vitamin D (22 ng/mL) and goal of 'Increase Energy',
 I recommend starting the 'Vitamin D Optimization' project.

 Users with similar profiles who completed this project saw:
 - 68% improvement in Vitamin D levels
 - 45% reported increased energy
 - Average completion time: 42 days"
```

### 4.9 📋 Project Notes & Journal

Each project gets a rich-text journal for:
- Progress notes
- How you're feeling
- Side effects from supplements
- Photos (before/after, supplement bottles)
- Voice memos
- Links to research articles

### 4.10 🔄 Blood Work Comparison Timeline

```
┌─────────────────────────────────────────────────────────────────┐
│              BLOOD WORK TIMELINE: Testosterone Project           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  JAN 15          APR 20           JUL 22                        │
│  Baseline        Mid-Project      Post-Project                   │
│     ▼               ▼                ▼                           │
│  ┌──────┐       ┌──────┐         ┌──────┐                       │
│  │ 380  │  ───▶ │ 485  │  ───▶   │ 612  │  Total T (ng/dL)     │
│  └──────┘       └──────┘         └──────┘                       │
│                  +28%              +61%                          │
│                                                                  │
│  ┌──────┐       ┌──────┐         ┌──────┐                       │
│  │  22  │  ───▶ │  45  │  ───▶   │  58  │  Vitamin D (ng/mL)   │
│  └──────┘       └──────┘         └──────┘                       │
│                 +105%             +164%                          │
│                                                                  │
│  [View Full Comparison] [Export Report]                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. Database Schema

### 5.1 New Tables

```sql
-- Project Types Enum
CREATE TYPE project_type AS ENUM (
  'biomarker_optimization',
  'health_protocol',
  'supplement_stack',
  'lifestyle_change',
  'medical_investigation',
  'comparative_analysis',
  'custom'
);

-- Project Status Enum
CREATE TYPE project_status AS ENUM (
  'draft',
  'active',
  'paused',
  'completed',
  'archived'
);

-- Task Status Enum
CREATE TYPE task_status AS ENUM (
  'todo',
  'in_progress',
  'blocked',
  'completed',
  'cancelled'
);

-- Task Priority Enum
CREATE TYPE task_priority AS ENUM (
  'low',
  'medium',
  'high',
  'critical'
);

-- Task Type Enum
CREATE TYPE task_type AS ENUM (
  'blood_work',
  'supplement',
  'diet',
  'exercise',
  'sleep',
  'meditation',
  'doctor_visit',
  'research',
  'measurement',
  'custom'
);

-- ================================
-- PROJECTS TABLE
-- ================================
CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,

  -- Basic Info
  name VARCHAR(255) NOT NULL,
  description TEXT,
  type project_type DEFAULT 'custom',
  status project_status DEFAULT 'draft',
  color VARCHAR(7) DEFAULT '#7a12d4', -- Hex color for UI
  icon VARCHAR(50), -- Emoji or icon name

  -- Timeline
  target_start_date DATE,
  target_end_date DATE,
  actual_start_date DATE,
  actual_end_date DATE,

  -- Metadata
  is_template BOOLEAN DEFAULT FALSE,
  template_id UUID REFERENCES projects(id), -- If created from template

  -- Analytics (denormalized for performance)
  total_tasks INTEGER DEFAULT 0,
  completed_tasks INTEGER DEFAULT 0,
  progress_percentage DECIMAL(5,2) DEFAULT 0,

  -- Timestamps
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  completed_at TIMESTAMPTZ,
  archived_at TIMESTAMPTZ
);

-- ================================
-- TASKS TABLE
-- ================================
CREATE TABLE tasks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  parent_task_id UUID REFERENCES tasks(id) ON DELETE CASCADE, -- For subtasks

  -- Basic Info
  title VARCHAR(500) NOT NULL,
  description TEXT,
  type task_type DEFAULT 'custom',
  status task_status DEFAULT 'todo',
  priority task_priority DEFAULT 'medium',

  -- Scheduling
  scheduled_date DATE,
  due_date DATE,
  due_time TIME,

  -- Time Tracking
  time_estimate INTEGER, -- In minutes
  actual_time INTEGER DEFAULT 0, -- In minutes

  -- Recurrence
  is_recurring BOOLEAN DEFAULT FALSE,
  recurrence_rule JSONB, -- iCal RRULE format
  recurrence_parent_id UUID REFERENCES tasks(id), -- Original task for instances

  -- Dependencies
  depends_on UUID[] DEFAULT '{}', -- Array of task IDs

  -- Metadata
  tags TEXT[] DEFAULT '{}',
  notes TEXT,

  -- Position (for ordering)
  position INTEGER DEFAULT 0,

  -- Timestamps
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  started_at TIMESTAMPTZ,
  completed_at TIMESTAMPTZ,

  -- Indexes for common queries
  CONSTRAINT valid_dates CHECK (due_date IS NULL OR scheduled_date IS NULL OR scheduled_date <= due_date)
);

-- ================================
-- PROJECT-BIOMARKER LINKS
-- ================================
CREATE TABLE project_biomarkers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  biomarker_name VARCHAR(255) NOT NULL, -- e.g., "Vitamin D, 25-Hydroxy"
  target_value DECIMAL(10,2), -- Target level to achieve
  target_unit VARCHAR(50), -- e.g., "ng/mL"
  baseline_value DECIMAL(10,2), -- Value when project started
  current_value DECIMAL(10,2), -- Latest value
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),

  UNIQUE(project_id, biomarker_name)
);

-- ================================
-- TASK-BIOMARKER LINKS
-- ================================
CREATE TABLE task_biomarkers (
  task_id UUID NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
  biomarker_name VARCHAR(255) NOT NULL,
  PRIMARY KEY (task_id, biomarker_name)
);

-- ================================
-- PROJECT NOTES/JOURNAL
-- ================================
CREATE TABLE project_notes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  content TEXT NOT NULL, -- Rich text / Markdown
  attachments JSONB DEFAULT '[]', -- [{url, type, name}]
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ================================
-- TASK COMMENTS
-- ================================
CREATE TABLE task_comments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  task_id UUID NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  content TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ================================
-- TIME ENTRIES (for time tracking)
-- ================================
CREATE TABLE time_entries (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  task_id UUID NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  duration INTEGER NOT NULL, -- In minutes
  started_at TIMESTAMPTZ NOT NULL,
  ended_at TIMESTAMPTZ NOT NULL,
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ================================
-- PROJECT TEMPLATES (public templates)
-- ================================
CREATE TABLE project_templates (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  description TEXT,
  type project_type NOT NULL,
  estimated_duration INTEGER, -- In days
  tasks_json JSONB NOT NULL, -- Template tasks structure
  target_biomarkers TEXT[], -- Biomarkers this template targets
  created_by UUID REFERENCES profiles(id),
  is_public BOOLEAN DEFAULT FALSE,
  usage_count INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ================================
-- ACHIEVEMENTS/BADGES
-- ================================
CREATE TABLE user_achievements (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  achievement_type VARCHAR(100) NOT NULL, -- e.g., 'first_project', 'streak_7', 'protocol_pioneer'
  achieved_at TIMESTAMPTZ DEFAULT NOW(),
  metadata JSONB DEFAULT '{}', -- Additional context
  UNIQUE(user_id, achievement_type)
);

-- ================================
-- INDEXES
-- ================================
CREATE INDEX idx_projects_user ON projects(user_id);
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_tasks_project ON tasks(project_id);
CREATE INDEX idx_tasks_user ON tasks(user_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
CREATE INDEX idx_tasks_scheduled ON tasks(scheduled_date);
CREATE INDEX idx_time_entries_task ON time_entries(task_id);

-- ================================
-- ROW LEVEL SECURITY
-- ================================
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE project_biomarkers ENABLE ROW LEVEL SECURITY;
ALTER TABLE task_biomarkers ENABLE ROW LEVEL SECURITY;
ALTER TABLE project_notes ENABLE ROW LEVEL SECURITY;
ALTER TABLE task_comments ENABLE ROW LEVEL SECURITY;
ALTER TABLE time_entries ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_achievements ENABLE ROW LEVEL SECURITY;

-- Projects: Users can only see their own
CREATE POLICY "Users can manage their own projects"
  ON projects FOR ALL
  USING (user_id = auth.uid());

-- Tasks: Users can only see their own
CREATE POLICY "Users can manage their own tasks"
  ON tasks FOR ALL
  USING (user_id = auth.uid());

-- Similar policies for other tables...

-- ================================
-- UPDATE TRIGGERS
-- ================================
CREATE OR REPLACE FUNCTION update_project_progress()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE projects
  SET
    total_tasks = (SELECT COUNT(*) FROM tasks WHERE project_id = COALESCE(NEW.project_id, OLD.project_id)),
    completed_tasks = (SELECT COUNT(*) FROM tasks WHERE project_id = COALESCE(NEW.project_id, OLD.project_id) AND status = 'completed'),
    progress_percentage = (
      SELECT COALESCE(
        (COUNT(*) FILTER (WHERE status = 'completed')::DECIMAL / NULLIF(COUNT(*), 0) * 100),
        0
      )
      FROM tasks
      WHERE project_id = COALESCE(NEW.project_id, OLD.project_id)
    ),
    updated_at = NOW()
  WHERE id = COALESCE(NEW.project_id, OLD.project_id);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_project_progress
  AFTER INSERT OR UPDATE OR DELETE ON tasks
  FOR EACH ROW
  EXECUTE FUNCTION update_project_progress();
```

### 5.2 Modify Existing Tables

```sql
-- Add project reference to health_data
ALTER TABLE health_data
ADD COLUMN project_id UUID REFERENCES projects(id) ON DELETE SET NULL;

-- Index for quick lookup
CREATE INDEX idx_health_data_project ON health_data(project_id);
```

---

## 6. UI/UX Proposals

### 6.1 Navigation Updates

```
┌─────────────────────────────────┐
│          VIBRANTLY              │
├─────────────────────────────────┤
│  🏠 Dashboard                   │
│  📊 My Health                   │
│  ────────────────────           │
│  📁 Projects          ★ NEW    │
│    └── Active (3)               │
│    └── Completed (12)           │
│    └── Templates                │
│  ────────────────────           │
│  ✅ Today's Tasks      ★ NEW   │
│  📅 Calendar           ★ NEW   │
│  ────────────────────           │
│  📈 Analytics          ★ NEW   │
│  ⚙️ Settings                    │
└─────────────────────────────────┘
```

### 6.2 Project List Page (`/projects`)

```
┌─────────────────────────────────────────────────────────────────────┐
│  Projects                                          [+ New Project]  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─── ACTIVE ─────────────────────────────────────────────────────┐ │
│  │                                                                 │ │
│  │  ┌─────────────────────────────────────────────────────────┐  │ │
│  │  │ 🎯 Vitamin D Optimization                    75% ████░░ │  │ │
│  │  │    12 of 16 tasks completed                             │  │ │
│  │  │    Target: Mar 15  ·  On Track                          │  │ │
│  │  └─────────────────────────────────────────────────────────┘  │ │
│  │                                                                 │ │
│  │  ┌─────────────────────────────────────────────────────────┐  │ │
│  │  │ 💊 Morning Supplement Stack                  40% ██░░░░ │  │ │
│  │  │    8 of 20 tasks completed                              │  │ │
│  │  │    Target: Feb 28  ·  Behind Schedule                   │  │ │
│  │  └─────────────────────────────────────────────────────────┘  │ │
│  │                                                                 │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                                                                      │
│  ┌─── COMPLETED (Show 12) ────────────────────────────────────────┐ │
│  │  ✓ Sleep Optimization (Nov 2024) - 100%                        │ │
│  │  ✓ Q3 Blood Work Review (Sep 2024) - 100%                      │ │
│  │  ✓ Testosterone Protocol (Aug 2024) - 100%                     │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 6.3 Project Detail Page (`/projects/[id]`)

```
┌─────────────────────────────────────────────────────────────────────┐
│  ← Back     Vitamin D Optimization     [Edit] [Archive] [Complete]  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─── OVERVIEW ─────────────────────────────────────────────────┐   │
│  │  Status: Active                   Progress: 75% ████████░░░  │   │
│  │  Started: Jan 15, 2025            Target: Mar 15, 2025       │   │
│  │  Tasks: 12/16                     Days Remaining: 67         │   │
│  │                                                               │   │
│  │  Linked Biomarker: Vitamin D, 25-Hydroxy                     │   │
│  │  Baseline: 22 ng/mL → Current: 45 ng/mL → Target: 60 ng/mL   │   │
│  └───────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  [List View] [Kanban] [Timeline] [Notes]                            │
│                                                                      │
│  ┌─── TASKS ────────────────────────────────────────────────────┐   │
│  │                                                               │   │
│  │  ☑ Order Vitamin D3 5000 IU                    ✓ Jan 16     │   │
│  │  ☑ Order Vitamin K2 supplements                ✓ Jan 16     │   │
│  │  ☑ Start morning supplementation               ✓ Jan 18     │   │
│  │  ☐ Schedule follow-up blood work               📅 Feb 15    │   │
│  │  ☐ Upload blood work results                   📅 Feb 20    │   │
│  │  ☐ Adjust dosage if needed                     📅 Feb 22    │   │
│  │                                                               │   │
│  │  [+ Add Task]                                                 │   │
│  └───────────────────────────────────────────────────────────────┘   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 6.4 Today's Tasks Page (`/today`)

```
┌─────────────────────────────────────────────────────────────────────┐
│  Today's Tasks                              Wednesday, January 8    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  MORNING                                        5 of 6 completed    │
│  ──────────────────────────────────────────────────────────────     │
│  ☑ Wake up by 7 AM                                                  │
│  ☑ Morning sunlight exposure (10 min)                               │
│  ☑ Take Vitamin D3 5000 IU                     💊 Vitamin D Project │
│  ☑ Take Omega-3                                💊 Supplement Stack  │
│  ☑ 30-minute walk                              🏃 General Health    │
│  ☐ Log weight and body composition             📏 Tracking          │
│                                                                      │
│  AFTERNOON                                      0 of 2 completed    │
│  ──────────────────────────────────────────────────────────────     │
│  ☐ Review blood work results                   🩸 Vitamin D Project │
│  ☐ Schedule doctor appointment                 👨‍⚕️ Medical          │
│                                                                      │
│  EVENING                                        0 of 3 completed    │
│  ──────────────────────────────────────────────────────────────     │
│  ☐ Take Magnesium Glycinate                    💊 Sleep Protocol    │
│  ☐ 10-minute meditation                        🧘 Stress Mgmt       │
│  ☐ Prepare for bed by 10 PM                    😴 Sleep Protocol    │
│                                                                      │
│  ─────────────────────────────────────────────────────────────────  │
│  🔥 Current Streak: 14 days    📊 Completion Rate: 87% this week    │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 6.5 Analytics Dashboard (`/analytics`)

```
┌─────────────────────────────────────────────────────────────────────┐
│  Health Project Analytics                    [This Week ▾] [Export] │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │ Active       │  │ Completed    │  │ Completion   │              │
│  │ Projects     │  │ This Month   │  │ Rate         │              │
│  │      3       │  │      2       │  │     87%      │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
│                                                                      │
│  ┌─── TASK COMPLETION TREND ──────────────────────────────────────┐ │
│  │                                                                 │ │
│  │  100% ┤                           ●                            │ │
│  │   80% ┤     ●    ●        ●   ●                                │ │
│  │   60% ┤  ●          ●  ●                                       │ │
│  │   40% ┤                                                         │ │
│  │       └──Mon──Tue──Wed──Thu──Fri──Sat──Sun──                   │ │
│  │                                                                 │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                                                                      │
│  ┌─── AI INSIGHTS ────────────────────────────────────────────────┐ │
│  │                                                                 │ │
│  │  💡 "Your task completion peaks on Tuesdays (94%). Consider    │ │
│  │      scheduling important health tasks early in the week."     │ │
│  │                                                                 │ │
│  │  💡 "Supplement tasks have 96% adherence. Your morning routine │ │
│  │      is well-established!"                                     │ │
│  │                                                                 │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                                                                      │
│  ┌─── BIOMARKER PROGRESS ─────────────────────────────────────────┐ │
│  │                                                                 │ │
│  │  Vitamin D:  22 → 45 ng/mL     (+105%)  ████████░░░            │ │
│  │  Testosterone: 380 → 485      (+28%)   ███████░░░░             │ │
│  │  Ferritin:    45 → 62 ng/mL   (+38%)   █████░░░░░░             │ │
│  │                                                                 │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 7. Implementation Phases

### Phase 1: Foundation (Week 1-2)
- [ ] Database schema creation (projects, tasks tables)
- [ ] Basic CRUD API endpoints for projects
- [ ] Basic CRUD API endpoints for tasks
- [ ] Projects list page UI
- [ ] Project detail page UI
- [ ] Navigation updates

### Phase 2: Core Features (Week 3-4)
- [ ] Task creation and management UI
- [ ] Task status transitions
- [ ] Due dates and scheduling
- [ ] Link projects to health_data
- [ ] Project state machine (draft → active → completed)
- [ ] Delete/archive functionality

### Phase 3: Enhanced Tasks (Week 5-6)
- [ ] Subtasks support
- [ ] Task dependencies
- [ ] Recurring tasks
- [ ] Task types with icons
- [ ] Priority levels
- [ ] Tags/labels

### Phase 4: Intelligence (Week 7-8)
- [ ] Project timing analytics
- [ ] Task completion metrics
- [ ] Productivity insights dashboard
- [ ] AI-powered insights generation
- [ ] Biomarker-project correlation

### Phase 5: Advanced Features (Week 9-10)
- [ ] Project templates
- [ ] Today's Tasks view
- [ ] Calendar view
- [ ] Kanban board view
- [ ] Timeline/Gantt view
- [ ] Time tracking

### Phase 6: Polish & Innovation (Week 11-12)
- [ ] AI task suggestions
- [ ] Gamification (streaks, achievements)
- [ ] Smart notifications
- [ ] External integrations
- [ ] Completed projects history/gallery
- [ ] Progress sharing

---

## Summary of Key Innovations

| Innovation | Value Proposition |
|------------|-------------------|
| **AI Project Assistant** | Auto-generates tasks from health goals |
| **Biomarker Correlation** | Links projects to actual health outcomes |
| **Smart Templates** | Pre-built protocols for common health goals |
| **Time Intelligence** | Insights on productivity patterns |
| **Daily Review Mode** | Morning routine optimization |
| **Streak Tracking** | Motivation through gamification |
| **Progress Visualization** | See biomarker improvements over time |
| **Health-Specific Task Types** | Categorized for supplements, exercise, etc. |
| **Recurring Tasks** | Built for daily health routines |
| **External Integrations** | Connect wearables and health apps |

This transforms Vibrantly from a blood work analyzer into a **complete health optimization operating system**.
