---
name: ship-nurture-supervisor
description: Own Nurture workstream deliverables (Stage 5C). Produces live email sequence + content drip pack; ensures tests are logged.
---

# Ship Nurture Supervisor

Own Nurture deliverables during Stage 5 (Parallel Execution).

## Product Type Branch

Read `intake.product_type` from blackboard before executing.

- `oss_tool` → [OSS Nurture Mode](#oss-nurture-mode)
- `saas | course | service` → standard nurture deliverables below

## OSS Nurture Mode

For OSS tools, there is no paid email sequence — the product is free. Nurture is the content drip from GitHub install → newsletter → course purchase.

**Deliverables:**
- [ ] 3-email welcome sequence linked (day 0: welcome + tool intro; day 3: architecture deep-dive; day 7: course CTA)
- [ ] MailerLite automation config linked — sequence fires when subscriber tagged `{tool-name}-install` (set by lead-capture stage)
- [ ] Content drip schedule linked — long-format YouTube or newsletter issue linked in email 2
- [ ] Test email evidence linked (rendering + links + unsubscribe)

**Writeback keys:** `nurture.oss_welcome_sequence`, `nurture.oss_drip_schedule`

**Quality Gate (OSS):**
- PASS: 3-email sequence exists, test evidence linked, MailerLite tag trigger configured, drip schedule ready, critic PASS in `production`
- REVISE: missing test evidence, broken CTA links, tag trigger not configured, or critic REVISE

## Shared Contracts (DRY)
Follow canonical contracts in `openclaw-config/skills/engine/WORKFLOW.md`:
- `Gate Prefill Requirement (owner-facing)`
- `Writeback Schema (Canonical)`
- `Deliverable Lifecycle States (Stage 9)`

## Inputs (Required)
- `strategy.ship_plan`
- `validate.icp` (VoC + objections)
- `lead_capture.offer_stack` and `lead_capture.capture_wiring`
- Linear Nurture ticket

## Deliverables (Required)
- [ ] Email welcome/nurture sequence (copy + timing) linked
- [ ] Automation import plan or evidence of live import linked
- [ ] Test email evidence (rendering + links + unsubscribe) linked
- [ ] Content drip schedule (14-day) linked

## Verification
- Test email received and passes basic rendering checks
- CTAs align with offer and funnel stage
- Copy is humanized (no generic AI cadence)
- In `production`, each deliverable is critic-verified (`PASS`) before moving to `verified`/`live`

## Quality Gate (PASS/REVISE)
- PASS: sequence exists, test evidence is linked, drip schedule is ready, and critic verdict is `PASS` in `production`
- REVISE: missing test evidence, broken links, CTA/offer mismatch, or critic verdict `REVISE`

## Writeback Contract
- Blackboard keys:
  - `nurture.email_sequence`
  - `nurture.test_email_evidence`
  - `nurture.content_drip`
  - Include `status_summary`, `next_steps`, and `critic_verdict` in `production`
- Linear:
  - On each meaningful update, post `status_summary` + `next_steps`
  - For high-risk deliverables, post a prefilled Decision Packet before `live`

## Delegation Map
- Copy drafting: `content-copy`
- Supporting visuals: `content-image`
- Scheduling/distribution packaging: `content-distribution`

## Failure Policy
- If ESP access is missing: deliver full sequence + step-by-step import checklist and mark execution blocked

## Critic Invocation (Required in `production`, per deliverable)
Before advancing any deliverable from `in_production` → `verified`:
1. Spawn `ship-critic` with `check_type=deliverable`, `deliverable_key=nurture.{artifact}`
2. Pass context: `validate.icp` VoC phrases + `lead_capture.offer_stack` summary + the email sequence content
3. Verdict:
   - **PASS** → advance to `verified`; record `critic_verdict=PASS` and `critic_evidence` link in deliverable state
   - **REVISE** → keep in `in_production`; post revision requests on the Nurture ticket
4. Write `critic.nurture.{artifact}` blackboard key with `verdict`, `comment_url`, `checked_at`

## Done When
- Deliverables exist, are linked, critic-verified in `production`, and verification evidence is recorded
