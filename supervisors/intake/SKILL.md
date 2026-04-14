---
name: ship-intake-supervisor
description: Own Stage 1 (Intake) deliverables for Ship Engine runs. Turns messy app input into a Product Brief + linked artifacts, then hands off to Validate.
---

# Ship Intake Supervisor

Own Stage 1 (INTAKE). Enforce the orchestrator contract: Inputs -> Deliverables -> Verification -> Artifacts.

## Shared Contracts (DRY)
Follow canonical contracts in `openclaw-config/skills/engine/WORKFLOW.md`:
- `Writeback Schema (Canonical)`
- `Deliverable Lifecycle States (Stage 9)`

Stage 1 does not open a owner hard gate, but it still uses the same status/writeback rules.

## Inputs (Required)
- owner-provided app context (URL(s), screenshots, notes, voice msg transcript, repo link)
- Linear run parent + Stage 1 ticket (or equivalent tracking surface)

## Deliverables (Required)
- [ ] Product brief doc linked in Linear
- [ ] Intake interview captured (Q&A) linked in Linear
- [ ] Research kickoff brief (for Validate) linked in Linear
- [ ] Artifact registry updated (Linear Artifacts section)
- [ ] Blackboard keys written using `{stage}.{artifact}`

### Product brief (minimum fields)
- App name + canonical URL
- One-liner (what it does)
- Target user (who has the pain)
- Current state (idea/MVP/live/billing)
- **`product_type`**: `oss_tool` | `saas` | `course` | `service` — drives stage behavior downstream
- Revenue model (free/freemium/paid/subscription)
- ICP guess (explicitly marked as a hypothesis)
- Core use cases (3)
- “First value moment” definition

#### `product_type: oss_tool` — additional required fields
- GitHub repo URL
- Install command (one-liner)
- Course upsell URL (if exists — can be TBD)
- Friction point (where in the install/use flow users hit a wall → course CTA fires here)
- Conversion goal: `github_star` | `newsletter` | `course_purchase`

### Intake interview (minimum fields)
- Primary goal for this run (1 sentence)
- Target market + geography + language
- Current distribution channels (if any)
- Constraints (brand, compliance, pricing, timelines)
- Proof assets available (case studies, testimonials, numbers)
- Competitors / alternatives you expect
- Access constraints (login walls, demo credentials, repos)

### Research kickoff brief (purpose)
- Provide enough context for Validate research agents to run immediately (no waiting on follow-ups)
- Declare unknowns explicitly so research can prioritize answering them

## Verification
- Product brief includes all minimum fields
- All referenced URLs/screenshots are accessible
- Linear ticket has Artifacts links filled
- In `production`, critic verdict is `PASS` before marking the brief `verified`

## Quality Gate (PASS/REVISE)
- PASS: brief is complete, linked, critic-verified (`PASS` in `production`), and blackboard keys are written
- REVISE: missing fields, broken links, no artifact registry, or critic verdict `REVISE`

## Writeback Contract
- Linear:
  - Update Stage 1 ticket description with required sections
  - Tick deliverables only when artifacts exist
  - Add final links under Artifacts
  - On each meaningful update, post `status_summary` + `next_steps`
- Blackboard:
  - `intake.product_brief` -> link/path
  - `intake.product_url` -> canonical URL
  - `intake.product_type` -> `oss_tool` | `saas` | `course` | `service`
  - `intake.interview` -> link/path
  - `intake.research_kickoff` -> link/path
  - Include `status_summary`, `next_steps`, and `critic_verdict` in `production`
- Pencil (optional): create board card linking to Product Brief

## Delegation Map
- Copy/formatting help: `content-copy`
- Landing page skeleton (optional preview only): `content-page`
- Deep research kickoff (must happen before Stage 2 completes): `research` or `gemini-deep-research`

## Failure Policy
- Missing input: comment on Stage 1 ticket with exact requested missing piece and continue with best-effort brief marked with TODOs
- Broken URL/login wall: request credentials or an alternate demo surface (screenshots/video)

## Done When
- Deliverables checklist is complete and verified
- Critic `PASS` is recorded in `production`
- Stage 1 ticket is in `In Review` (if verification pending) or `Done` (if verification recorded)
