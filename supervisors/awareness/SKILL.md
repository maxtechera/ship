---
name: ship-awareness-supervisor
description: Own Awareness workstream deliverables (Stage 5A). Produces deployable awareness assets: landing page, blog pack, social pack, image pack, b-roll manifest.
---

# Ship Awareness Supervisor

Own Awareness deliverables during Stage 5 (Parallel Execution).

## Product Type Branch

Read `intake.product_type` before producing any deliverables.

- **`oss_tool`** → run [OSS Demo-First Mode](#oss-demo-first-mode) instead of standard awareness pack
- **`saas` | `course` | `service`** → run standard awareness deliverables below

## Shared Contracts (DRY)
Follow canonical contracts in `openclaw-config/skills/engine/WORKFLOW.md`:
- `Gate Prefill Requirement (owner-facing)`
- `Writeback Schema (Canonical)`
- `Deliverable Lifecycle States (Stage 9)`

---

## OSS Demo-First Mode (when `intake.product_type: oss_tool`)

**Core principle:** Demo-first > readme-first. Nobody reads docs and decides to buy. They try it, get impressed, and convert. The free content IS the sales page.

### OSS Awareness Inputs (Required)
- `intake.product_brief` (includes GitHub repo, install command, friction point)
- `validate.oss_pain_quotes` (10+ real quotes)
- `validate.friction_point` (where course CTA fires)
- `validate.search_intent_map` (5-10 keywords)

### OSS Awareness Deliverables (Required)
- [ ] **Reel scripts — Problem** (15-30s): show the pain moment, no solution yet. CTA: GitHub repo URL.
- [ ] **Reel scripts — Fix** (30-45s): show the install + the moment it works. CTA: link in bio → free install.
- [ ] **Reel scripts — Architecture** (45-60s): show how it works under the hood. CTA: course link.
- [ ] **Long-format script** (10-20min YouTube): full demo end-to-end — install, real use case, result. CTA: GitHub + newsletter + course.
- [ ] **Newsletter issue draft**: written breakdown of the architecture for NODO subscribers.
- [ ] **GitHub README CTA copy**: 2-3 lines added to README pointing to course at the friction point.
- [ ] **Hook library**: 5-10 hooks per reel format (problem/fix/architecture) sourced from `validate.oss_pain_quotes`.

### OSS Reel Template

Each tool gets 3 reels following this structure:

**Reel 1 — The Problem (15-30s)**
```
Hook: [verbatim pain quote or common frustration]
Show: the failure moment (agent forgets / says done but it's wrong / launch pipeline breaks)
End: "There's a fix." + GitHub URL on screen
CTA: "[tool name] — free on GitHub"
```

**Reel 2 — The Fix (30-45s)**
```
Hook: "Install this in 30 seconds"
Show: install command → setup → the moment it works (the money shot)
End: "Free. Open source." + install command on screen
CTA: "Link in bio → free install"
```

**Reel 3 — The Architecture (45-60s)**
```
Hook: "Here's how it actually works"
Show: internals (the interesting technical decision)
End: "Want the full course?" + course link
CTA: "Full course — [price] — link in bio"
```

### OSS Conversion Chain
```
Reel → GitHub install → friction point → README CTA → newsletter → course purchase
```
Every OSS awareness asset must link to the next step in this chain. No dead ends.

### OSS Awareness Verification
- All 3 reel scripts written and reviewed
- Long-format script complete with screen-recording shot list
- Hook library has ≥5 options per reel type
- README CTA copy is written and ready to commit
- Newsletter issue drafted
- Every asset links to the next step in the conversion chain

### OSS Writeback Keys
- `awareness.oss_reel_scripts` — 3 reel scripts (problem/fix/architecture)
- `awareness.oss_longformat_script` — long-format video script + shot list
- `awareness.oss_hook_library` — hook variants per reel type
- `awareness.oss_newsletter_draft` — newsletter issue
- `awareness.oss_readme_cta` — README CTA copy ready to commit

---

## Standard Awareness Mode (saas | course | service)

### Inputs (Required)
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
- `skills/engine/templates/b-roll-capture.md`
- `skills/engine/templates/awareness-manifest.md`

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
