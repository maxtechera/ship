---
name: content-engine-supervisor
version: "1.0.0"
description: "Always-on content engine control loop. Wakes on cron/webhook/manual — pulls research, delegates production, syncs artifacts, triggers measurement."
allowed-tools: Bash, Read, Write, Edit, Agent
user-invocable: false
---

# Content Engine Supervisor (Always-On)

Content Engine is skills-first. This supervisor runs bounded one-cycle wakes and exits. It does not stay alive between cycles.

## Inputs

- Active ship-engine runs (Linear tickets tagged with run stage)
- Research intel shortlist (ranked by recency + relevance + ROI)
- Semantic inspiration (voice samples, best performers, proven offers)
- Calendar state (current queue status)
- Analytics evidence (for live assets: day-1 and week-1 data)

## Core Loop (One Cycle)

```
1. For each active run → fetch strategy/ICP context (blackboard + stage ticket artifacts)
   - Require intake preflight before creating downstream artifacts:
     intake.product_brief, intake.interview, intake.research_kickoff

2. Pull ranked research shortlist
   - ROI gate: only research with strong engagement signal
   - Dedup: skip topics already in queue or recently published
   - Recency: prefer fresh evidence (< 30 days)

3. Write context keys:
   - awareness.content_candidates
   - validate.research_dataset (if applicable)

4. If awareness content is missing for active run → delegate:
   - content-compose → pillar draft
   - content-waterfall → platform bundle

5. Auto-schedule derivatives
   - Drafts only — no publishing
   - Respect locked items in the calendar
   - Fill gaps, don't overwrite confirmed posts

6. Sync artifacts to Linear and run state:
   - outputs.content_calendar
   - outputs.content_waterfall
   - awareness.content_calendar (blackboard key)
   - awareness.content_waterfall (blackboard key)

7. If live permalinks exist → delegate measurement:
   - content-measure → measure.kpis + measure.feedback_events

8. Apply learning gate:
   - Always log observations
   - Update pattern files only when N≥3 data points exist for the pattern
   - Update skill defaults only with explicit confirmation
```

## Guardrails

- **Draft scheduling is allowed; auto-publishing is not** — the owner publishes
- Never fabricate research evidence or metrics
- Never mark deliverables `verified` or `live` without a real permalink
- Intake preflight is mandatory before creating awareness content for a run
- One cycle = one wake → do work → exit (no persistent loop)

## Writeback Contract

After each cycle:
- Post `status_summary` + `next_steps` to the relevant Linear ticket
- Update blackboard keys as listed in the core loop
- Log what was created, what was skipped, and why

## Handoff to Ship Engine

Content engine supervisor operates within ship-engine's stage boundaries:
- Awareness stage: generates content candidates + waterfall bundles
- Measure stage: triggers measurement + feedback loop

Ship-engine's stage supervisors call this supervisor — it does not call them.
All gate decisions (PASS/REVISE) are made by `supervisors/critic/`, not here.
