# Meta Persona Callouts Pack: {product_name}

> Artifact bundle required before scaling persona-based content or ads.

## Artifact Index (Required)

| Artifact | Canonical path | Purpose | Status |
|----------|----------------|---------|--------|
| Persona hook library | `openclaw-config/skills/engine/templates/persona-hook-library.md` | Shared organic + paid hook definitions | ⬜ |
| Meta playbook | `openclaw-config/skills/engine/templates/meta-persona-callouts-playbook.md` | Lane-specific creative execution rules | ⬜ |
| Callouts pack (this file) | `openclaw-config/skills/engine/templates/meta-persona-callouts-pack.md` | Launch-ready matrix + reporting split | ⬜ |

## Active Avatar + Hook Selection

| Avatar | Hook IDs in run | Primary pain | Primary proof | Primary CTA | Notes |
|--------|------------------|--------------|---------------|-------------|-------|
| {avatar_id} | {H-1,H-2} | {pain} | {proof} | {cta} | {constraints} |

## Test Matrix (Execution Copy)

Schema: `Avatar x Hook x Proof x CTA x Format`

| Avatar | Hook ID | Proof variant | CTA variant | Format | Lane | Status | Result |
|--------|---------|---------------|-------------|--------|------|--------|--------|
| {avatar} | H-{n} | {proof} | {cta} | {reel/carousel/video/text} | {organic/paid.prospecting/paid.retargeting} | {todo/live} | {metric snapshot} |

## Reporting Split Contract (Required)

| Split level | Required buckets |
|-------------|------------------|
| Channel split | `organic` vs `paid` |
| Paid sub-split | `paid.prospecting` vs `paid.retargeting` |

## Scale Readiness Checklist
- [ ] All variants map back to persona hook library IDs.
- [ ] Organic learnings and paid learnings are reported separately.
- [ ] Paid results are split between prospecting and retargeting.
- [ ] Any promoted winner has at least one cold-audience pass.
- [ ] Kill/iterate/scale actions are logged for each hook family.
