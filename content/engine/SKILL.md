---
name: content-engine
version: "1.0.0"
description: "Content production queue — manage idea → scheduling → scripting → publishing → measurement lifecycle."
allowed-tools: Bash, Read, Write, Edit, Glob
user-invocable: true
triggers:
  - content queue
  - content pipeline
  - content engine
user-invocable: false
---

# Content Engine

Content planning and production queue management. Manages the full lifecycle: ideation → scheduling → scripting → posting → measurement.

## Core Functions

### 1. Queue Management

Maintain a prioritized list of content ideas:
```
id, topic, format, platform, priority, status, scheduled_date, published_url
```

Statuses: `idea → scripted → recorded → edited → scheduled → published → measured`

### 2. Idea Intake

When a new idea arrives:
- Classify: format (reel / carousel / thread / blog), platform, priority (1-4)
- Deduplicate: check if similar idea is already in queue
- If it fits an active ship-engine run: tag it with the run ID and stage

### 3. Research → Content Pipeline

For each approved idea:
1. Pull relevant research evidence (VoC, data, sources)
2. Delegate to `content-compose` for pillar draft
3. Delegate to `content-waterfall` for platform derivatives
4. Auto-schedule derivatives (drafts only — no auto-publish)

### 4. Intake Preflight

Before creating content artifacts for a ship-engine run, require:
- `intake.product_brief` present
- `intake.interview` present
- `intake.research_kickoff` present

If any are missing: block content creation, log missing items, request from run owner.

### 5. Calendar State

Track what's scheduled vs what's published:
```
scheduled_this_week: [list of scheduled items with dates/times]
published_this_month: [list with permalinks + initial metrics]
```

### 6. Analytics Sync

When live permalinks exist:
- Trigger `content-measure` for day-1 and week-1 snapshots
- Store results in queue item record
- Pass feedback events to `content-feedback-loop`

## Guardrails

- Draft autoscheduling is allowed; auto-publishing to social accounts is not
- Never fabricate research evidence or metrics
- Never mark content `verified` or `live` without a live permalink
- Respect locked/confirmed items in the schedule — only reschedule drafts

## Outputs

- Updated content queue with statuses and scheduled dates
- Artifact links per item (pillar draft, waterfall bundle, published URL)
- Calendar view for the current week
- Measurement summary when snapshots exist
