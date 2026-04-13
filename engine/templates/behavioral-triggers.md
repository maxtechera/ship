# Behavioral Triggers: {product_name}

> **Template version:** 1.0 — Ship Engine Nurture Stage (5C)
> **Owner:** `ship-nurture-supervisor`
> **Inputs required:** Segment Definitions (`segment-definitions.md`), nurture sequence timing, email provider automations
> **Outputs:** Trigger map wired in email provider; each trigger = one automation branch

---

## Overview

Behavioral triggers convert static drip sequences into adaptive nurture flows. Instead of sending email #4 on Day 5 regardless of subscriber behavior, triggers detect intent signals and respond in real time.

**Rule:** Every trigger maps to exactly one action. No trigger fires twice for the same subscriber in the same window.

---

## Trigger Map

### T1 — New Signup (Entry Trigger)

| Field | Value |
|-------|-------|
| **Trigger name** | `trigger.new_signup` |
| **Signal** | Subscriber joins group `{lead_capture_group}` |
| **Delay** | Immediate (Day 0) |
| **Action** | Start nurture sequence; send Email 1 (Welcome + Lead Magnet) |
| **Segment tag applied** | `seg:new` |
| **Notes** | Wired by Lead Capture Agent. Do not duplicate — check that group join fires only once per subscriber. |

---

### T2 — First Click (Hot Signal)

| Field | Value |
|-------|-------|
| **Trigger name** | `trigger.first_click` |
| **Signal** | Subscriber clicks any link in Email 1 or Email 2 |
| **Delay** | Immediate |
| **Action** | Add tag `seg:engaged-active`; add +25 to `engagement_score`; if score ≥ 80 → apply Hot track modifier (pull forward Day 7 email to Day 5) |
| **Segment transition** | `seg:new` → `seg:engaged-active` |
| **Notes** | Only fires once. Subsequent clicks contribute to score but don't re-fire this trigger. |

---

### T3 — No Open After 3 Days (Cold Recovery)

| Field | Value |
|-------|-------|
| **Trigger name** | `trigger.no_open_3d` |
| **Signal** | Subscriber has not opened Email 1 within 72 hours of send |
| **Delay** | 72h after Email 1 send time |
| **Action** | Resend Email 1 with alternate subject line variant B; add tag `ms:cold-entry` |
| **Segment transition** | `seg:new` → `seg:engaged-cold` if no open after resend (additional 48h) |
| **Notes** | Only one resend allowed. If still no open after resend → apply T5. |

---

### T4 — Product Activation (Converter Signal)

| Field | Value |
|-------|-------|
| **Trigger name** | `trigger.activation` |
| **Signal** | Subscriber accesses product / completes onboarding step (via API webhook or UTM event) |
| **Delay** | Immediate |
| **Action** | Pause nurture sequence; add tag `seg:converter`; start post-purchase onboarding sequence (separate automation); add +40 to `engagement_score` |
| **Segment transition** | Any nurture segment → `seg:converter` |
| **Notes** | Wired via MailerLite API webhook. Confirm with product team what activation event to track (`{activation_event}`). |

---

### T5 — Sequence Mid-Drop (Re-engagement)

| Field | Value |
|-------|-------|
| **Trigger name** | `trigger.mid_drop` |
| **Signal** | Subscriber's `engagement_score` drops below 20 at any point during the sequence (Day 3–10) |
| **Delay** | Next scheduled send window (within 24h of score drop) |
| **Action** | Pause standard sequence; insert re-engagement sub-sequence (3 emails over 6 days); if no response → T7 |
| **Sub-sequence emails:** | |
| → Re-engagement Email 1 | "Still interested in {product_name}?" — value reminder; no selling |
| → Re-engagement Email 2 | "One thing I should have said earlier" — personal story hook |
| → Re-engagement Email 3 | "Last one — I promise" — direct ask to stay or unsubscribe |
| **Segment transition** | `seg:engaged-active` → `seg:engaged-cold` |
| **Notes** | If subscriber opens any re-engagement email → score +10; resume standard sequence at next scheduled email. |

---

### T6 — Pricing Page Visit (High-Intent Signal)

| Field | Value |
|-------|-------|
| **Trigger name** | `trigger.pricing_visit` |
| **Signal** | Subscriber clicks pricing link (UTM: `utm_content=pricing`) in any email |
| **Delay** | 1 hour after click |
| **Action** | Add tag `ms:high-intent`; add +20 to `engagement_score`; if currently on Day 1–5 of sequence → skip to Day 7 Objection email immediately |
| **Segment transition** | No segment change; tag only |
| **Notes** | This is the highest-intent pre-purchase signal. Treat it as a soft hand-raise. Closing Agent should receive a daily report of `ms:high-intent` subscribers for potential direct follow-up. |

---

### T7 — Purchase / Payment Confirmed

| Field | Value |
|-------|-------|
| **Trigger name** | `trigger.purchase` |
| **Signal** | Payment webhook received from `{payment_provider}` (Stripe / Lemon Squeezy / etc.) |
| **Delay** | Immediate |
| **Action** | Stop all nurture sequences; add tag `seg:converter`; start post-purchase sequence; add +100 to `engagement_score`; notify Closing Agent |
| **Segment transition** | Any → `seg:converter` |
| **Notes** | Must be wired to payment provider webhook. Test with a $0 test charge before launch. Confirm MailerLite automation fires correctly end-to-end. |

---

### T8 — Last Call No-Response (Sunset)

| Field | Value |
|-------|-------|
| **Trigger name** | `trigger.last_call_no_response` |
| **Signal** | Email 7 (Last Call) sent and no open within 48h |
| **Delay** | 48h after Email 7 send time |
| **Action** | Add tag `seg:dormant`; start sunset sequence (2-email max); if no response → unsub and add to suppression list |
| **Sunset Email 1** | "We'll miss you — but we understand" — final value drop, no CTA to buy |
| **Sunset Email 2** | "Removing you from our list" — final send; unsubscribe link prominent |
| **Segment transition** | `seg:engaged-cold` → `seg:dormant` → `seg:unsub` |
| **Notes** | List hygiene: removing unengaged subscribers improves deliverability. Better a smaller clean list than a large cold one. |

---

## Trigger Priority & Conflict Resolution

When multiple triggers could fire simultaneously, apply this priority order:

```
Priority 1 (highest): T7 — Purchase (terminates all other triggers)
Priority 2:           T4 — Activation (pauses nurture; starts post-purchase)
Priority 3:           T6 — Pricing Page Visit (high-intent acceleration)
Priority 4:           T2 — First Click (engagement scoring)
Priority 5:           T5 — Mid-Drop Re-engagement
Priority 6:           T3 — No Open Recovery
Priority 7 (lowest):  T8 — Last Call No-Response (sunset)
```

**Conflict rule:** Higher-priority trigger wins. Lower-priority trigger is cancelled for that send window.

---

## Drip Sequence Trigger Wiring Summary

```
[Subscribe] ──► T1 (Entry) ──► Email 1 (Day 0)
                │
                ├─ [Opened/Clicked] ──► T2 (Hot Signal) ──► Score +25; segment = Active
                │
                ├─ [No open 72h] ──► T3 (Cold Recovery) ──► Resend Email 1 alt subject
                │                         └─ [Still no open] ──► T5 (Re-engagement)
                │
                ├─ Email 2 (Day 1) ──► Email 3 (Day 3) ──► ...standard sequence...
                │         │
                │         └─ [Score < 20] ──► T5 (Mid-Drop) ──► Re-eng sub-sequence
                │
                ├─ [Pricing click] ──► T6 (High-Intent) ──► Skip to objection email
                │
                ├─ [Activation event] ──► T4 (Activation) ──► Post-purchase sequence
                │
                ├─ [Purchase webhook] ──► T7 (Purchase) ──► Post-purchase sequence ✅
                │
                └─ [Last Call sent; no open] ──► T8 (Sunset) ──► Suppress
```

---

## Implementation Checklist

### MailerLite Automation Setup

- [ ] **T1** — Group join automation created; Email 1 fires immediately on join
- [ ] **T2** — Click event → engagement score field increment; segment tag applied
- [ ] **T3** — Condition step: "Email opened? No → Wait 72h → Send alternate subject"
- [ ] **T4** — Webhook endpoint configured for activation event (`{activation_event_url}`)
- [ ] **T5** — Score-based condition: `engagement_score < 20` → branch to re-engagement emails
- [ ] **T6** — Click tracking on pricing link; URL condition step in automation
- [ ] **T7** — Payment webhook configured; purchase event → stop nurture; start post-purchase
- [ ] **T8** — No-open condition after Email 7; sunset branch active

### Pre-Launch Verification (Required Before Gate-L)

- [ ] T1 fires correctly: test subscriber joined group → Email 1 received within 5 min
- [ ] T2 fires correctly: clicked test link → score incremented in custom field
- [ ] T3 fires correctly: no-open condition detected in sandbox; resend triggered
- [ ] T4 fires correctly: activation webhook POST → nurture paused; post-purchase started
- [ ] T5 fires correctly: score artificially set to 15 → re-engagement emails queued
- [ ] T6 fires correctly: pricing link clicked → email skipped; objection email delivered next
- [ ] T7 fires correctly: test purchase event → all nurture automation stopped
- [ ] T8 fires correctly: no-open flag after Email 7 → sunset email 1 queued 48h later
- [ ] No duplicate sends detected in test subscriber inbox
- [ ] Suppression list applied before any real send

---

## Handoff Notes

**→ Segment Definitions:** All trigger-applied tags must match segment identifiers in `segment-definitions.md` exactly. Cross-check before automation import.

**→ Lead Capture Agent:** Confirm group name `{lead_capture_group}` and UTM parameter spec before T1 goes live.

**→ Closing Agent:** Receive daily export of `ms:high-intent` subscribers (T6). Use for direct outreach if strategy approved.

**→ Awareness Agent (Retargeting):** Export `seg:dormant` 48h after T8 fires — feed into Meta custom audience for retargeting ads.

---

*Generated by `ship-nurture-supervisor` | Template: `skills/engine/templates/behavioral-triggers.md`*
