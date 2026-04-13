# Ship Engine — Template Index

Templates used by the Ship Engine skill across all GTM stages. Each template is a structured markdown document that an agent fills out for a specific product/campaign.

## How to Use
Templates are referenced in `SKILL.md` and `WORKFLOW.md`. When a stage requires a deliverable, the agent reads the template, fills it out, and saves the output to `data/content-outputs/<product>/<stage>/`.

## Template Catalog

| Template | Stage | Purpose |
|----------|-------|---------|
| `idea-brief.md` | INTAKE | Initial idea capture — problem, audience, format |
| `product-brief.md` | INTAKE / STRATEGY | Full product definition + positioning |
| `icp.md` | STRATEGY | Ideal Customer Profile (demographics, psychographics, pain points) |
| `voc-bank.md` | STRATEGY | Voice of Customer — raw language pulled from forums, reviews, interviews |
| `persona-hook-library.md` | STRATEGY | Hook variants mapped to ICP segments |
| `offer-validation-patterns.md` | VALIDATE | Validation test designs (smoke test, waitlist, DM test) |
| `validation-report.md` | VALIDATE | Results + Go/No-Go recommendation |
| `segment-definitions.md` | STRATEGY | Audience segments for targeting and messaging |
| `attribution-model.md` | STRATEGY / MEASURE | Channel attribution rules + first-touch / multi-touch model |
| `behavioral-triggers.md` | NURTURE | Trigger-based automation events (signup, visit, cart abandon, etc.) |
| `awareness-manifest.md` | AWARENESS | Content plan for top-of-funnel awareness channels |
| `content-calendar.md` | AWARENESS | Week-by-week content schedule |
| `b-roll-capture.md` | AWARENESS | B-roll shot list for video content |
| `meta-persona-callouts-playbook.md` | AWARENESS | Meta Ads persona callout strategy |
| `meta-persona-callouts-pack.md` | AWARENESS | Ready-to-use Meta Ads callout variants |
| `lead-capture.md` | LEAD CAPTURE | Lead magnet + form + landing page spec |
| `thank-you-page.md` | LEAD CAPTURE | Post-signup confirmation page + next-step CTA flow |
| `welcome-email.md` | LEAD CAPTURE / NURTURE | Immediate signup email to deliver value + drive activation |
| `nurture-sequence.md` | NURTURE | Email/DM nurture sequence (subject lines, body, CTA) |
| `customer-interview.md` | NURTURE / VALIDATE | Interview script + synthesis template |
| `closing-strategy.md` | CLOSING | Sales close tactics, objection handling, urgency levers |
| `checkout-flow-test-plan.md` | CLOSING | Checkout UX test plan + evidence-first success criteria |
| `refund-policy.md` | CLOSING | Refund/guarantee policy copy |
| `terms-of-service.md` | CLOSING | Terms of Service template aligned with billing/refunds |
| `beta-report.md` | BETA | Beta cohort results — conversion, NPS, blockers |
| `ship-plan.md` | LAUNCH | Launch day execution plan (timeline, owners, rollback) |
| `ship-checklist.md` | LAUNCH | Pre-launch QA checklist |
| `launch-checklist.md` | LAUNCH | Post-publish verification checklist |
| `cohort-analysis.md` | MEASURE | Cohort retention + revenue analysis |
| `weekly-report.md` | MEASURE | Weekly KPI report template |
| `post-launch-report.md` | MEASURE | 30-day post-launch retrospective |

## Directories
- `archive/` — Deprecated or superseded templates
- `prompts/` — LLM generation prompts that produce these template outputs (used by automation)
