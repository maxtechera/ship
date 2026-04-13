# Persona Hook Library: {product_name}

> Canonical source for persona callouts across organic + paid.
> Owner: Ship Engine (Strategy -> Awareness -> Measure).

## Operating Rules
- One shared library for organic and paid; channel changes format, not avatar definition.
- Active avatar band limit: 3-12 per cycle (default: 6).
- Granularity guardrail: avoid micro-niche avatars unless the strategy ticket explicitly constrains the niche.
- Every hook must map to a validated pain quote or evidence link.

## Avatar Band Table

| Mode | Min | Max | Default | Use case |
|------|-----|-----|---------|----------|
| Active test cycle | 3 | 12 | 6 | Weekly experimentation and optimization |
| Expansion cycle | 6 | 12 | 9 | After a stable winner is identified |
| Constrained launch | 1 | 3 | 2 | Only when explicitly approved in Strategy Lock |

## Hook Architecture (Required)

Use this structure for every hook variant:

`Persona + Pain + Outcome + Mechanism + Proof + CTA`

| Component | Requirement |
|-----------|-------------|
| Persona | Clear identity callout (role/context) |
| Pain | Specific friction or cost they feel now |
| Outcome | Tangible desired result |
| Mechanism | How the product creates the result |
| Proof | Credible evidence (quote, metric, case, demo) |
| CTA | Single action request tied to stage |

## Hook Library Schema

| Hook ID | Avatar | Persona callout | Pain line | Outcome line | Mechanism line | Proof asset | CTA | Formats |
|---------|--------|-----------------|-----------|--------------|----------------|-------------|-----|---------|
| H-{n} | {avatar_id} | {callout} | {pain} | {outcome} | {mechanism} | {proof_link} | {cta} | {reel/carousel/ad/story} |

## Test Matrix Schema

Use this exact schema for experiments:

`Avatar x Hook x Proof x CTA x Format`

| Avatar | Hook ID | Proof variant | CTA variant | Format | Channel | Stage | Result |
|--------|---------|---------------|-------------|--------|---------|-------|--------|
| {avatar} | H-{n} | {proof_a} | {cta_a} | {format} | {organic/paid} | {prospecting/retargeting} | {metric snapshot} |

## Decision Rules

| Decision | Rule |
|----------|------|
| Kill | Under baseline after minimum sample OR poor lead quality signal |
| Iterate | Near baseline but evidence/CTA mismatch is diagnosable |
| Scale | Beats baseline with stable conversion quality and repeatability |

## Bias Warning (Required)

- Warm-audience bias warning: do not promote a winner to prospecting based only on retargeting or follower traffic.
- Prospecting scale requires at least one cold-audience pass in the same hook architecture.

<!-- AUTO_HOOK_WINNERS:START -->
## Auto-Learned Winning Hooks

- No winning hooks logged yet.
<!-- AUTO_HOOK_WINNERS:END -->
