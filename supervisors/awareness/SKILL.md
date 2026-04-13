---
name: ship-awareness-supervisor
description: Own Awareness workstream deliverables (Stage 5A). Produces deployable awareness assets: landing page, blog pack, social pack, image pack, b-roll manifest.
---

# Ship Awareness Supervisor

Own Awareness deliverables during Stage 5 (Parallel Execution).

## Shared Contracts (DRY)
Follow canonical contracts in `openclaw-config/skills/ship-engine/WORKFLOW.md`:
- `Gate Prefill Requirement (Max-Facing)`
- `Writeback Schema (Canonical)`
- `Deliverable Lifecycle States (Stage 9)`

## Inputs (Required)
- `strategy.ship_plan`
- `validate.icp`
- Live product URL (or demo surface)
- Linear Awareness ticket

## Deliverables (Required)
- [ ] B-roll capture library + `manifest.json` linked
- [ ] Landing page live preview URL linked
- [ ] Image pack (hero/OG/social) linked or committed
- [ ] Blog pack (PR-ready markdown) linked or committed
- [ ] Social content pack (per-platform) linked
- [ ] Content waterfall bundle drafted + scheduled (10+ derivatives) linked

Reference manifests/templates:
- `skills/ship-engine/templates/b-roll-capture.md`
- `skills/ship-engine/templates/awareness-manifest.md`

## Verification
- Landing page: mobile + desktop screenshots; OG preview looks correct
- Images: crop-safe center; thumbnail legible; consistent `style_seed`
- Blog pack: metadata present; internal links; VoC language used
- Social pack: platform formatting + CTAs align to offer
- In `production`, each deliverable is critic-verified (`PASS`) before moving to `verified`/`live`

## Quality Gate (PASS/REVISE)
- PASS: all required artifacts exist, are linked, critic-verified (`PASS` in `production`), and pass verification checks
- REVISE: any missing artifact, broken link, failed QA item, or critic verdict `REVISE`

## Writeback Contract
- Blackboard keys:
  - `awareness.broll_manifest`
  - `awareness.landing_page_url`
  - `awareness.image_pack`
  - `awareness.blog_pack`
  - `awareness.social_pack`
  - `awareness.content_waterfall`
  - `awareness.content_calendar`
  - `awareness.content_candidates`
  - Include `status_summary`, `next_steps`, and `critic_verdict` in `production`
- Linear:
  - Use deliverables checklist; link every artifact
  - On each meaningful update, post `status_summary` + `next_steps`
  - For high-risk deliverables, post a prefilled Decision Packet before `live`

## Delegation Map
- Research shortlist + VoC: `research` + `content-engine-supervisor`
- Pillar draft + Q&A: `content-compose`
- Waterfall bundle (10+): `content-waterfall`
- Draft autoscheduling + sync: `content-engine-supervisor`
- B-roll: `content-broll`
- Landing page: `content-page` + `content-copy`
- Images/mockups: `content-image`
- Blogs: `content-blog` + `content-copy`
- Distribution packaging: `content-distribution`

## Failure Policy
- If product access is blocked: proceed with screenshot-based mockups and mark limitations explicitly
- If any asset fails QA: revise before marking deliverable complete

## Critic Invocation (Required in `production`, per deliverable)
Before advancing any deliverable from `in_production` → `verified`:
1. Spawn `ship-critic` with `check_type=deliverable`, `deliverable_key=awareness.{artifact}`
2. Pass context: `intake.product_brief` summary + `validate.icp` VoC phrases + the deliverable content/URL
3. Verdict:
   - **PASS** → advance to `verified`; record `critic_verdict=PASS` and `critic_evidence` link in deliverable state
   - **REVISE** → keep in `in_production`; post revision requests as checklist or comment on the Awareness ticket
4. Write `critic.awareness.{artifact}` blackboard key with `verdict`, `comment_url`, `checked_at`

## Done When
- All required awareness artifacts exist, are linked, critic-verified in `production`, and pass verification
