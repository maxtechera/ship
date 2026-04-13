---
name: content-compose
version: "1.0.0"
description: "Compose a pillar content asset using hybrid retrieval — research evidence + voice samples + one-shot draft."
allowed-tools: Read, Write, Edit, Grep
user-invocable: true
---

# Content Compose

Create a pillar asset (script, post, article) grounded in real evidence.

## When to Use

- Starting a new piece with research material available
- Creating the "anchor" piece before waterfall derivatives
- When source material exists but needs shaping into a voice-aligned draft

## Inputs Required

- Topic/angle (from ticket or brief)
- Research evidence shortlist (source URLs + key takeaways + VoC pain points)
- Voice samples or exemplars (best-performing past content in the same format)
- Channel and format (reel script / caption / thread / blog)

## Process

### 1. Clarify with Targeted Questions

Before drafting, elicit 5-8 specifics from the owner:
- "What's the one thing the audience should remember?"
- "What proof or receipts do you have that others don't?"
- "What's the controversial or counterintuitive angle here?"
- "What's the exact moment a reader should think 'this is for me'?"

### 2. Ground in Evidence

For each major claim in the draft:
- Link to a source (research URL, VoC quote, or data point)
- If no evidence exists: mark claim with `[TODO: receipt needed]`
- Never fabricate specifics

### 3. Write the Pillar Draft

Apply voice constraints:
- Use real pain language from VoC, not abstract descriptions
- Avoid AI cadence phrases
- Hook structure: Persona + Pain + Outcome + Mechanism + Proof + CTA
- One dominant CTA — not multiple

### 4. Evidence References

Every draft includes an evidence section:
```
## Evidence Used
- [Claim] → [Source URL] ([date])
- [Statistic] → [Source URL] ([date])
- [Quote] → [VoC source + date]
```

## Required Outputs

- [ ] 5-8 targeted questions (with answers from owner before draft)
- [ ] Pillar one-shot draft (format-appropriate)
- [ ] Evidence refs linked (source URL per claim)
- [ ] Voice check passed (no AI filler, channel format correct)

## Failure Policy

- Missing evidence: draft with `[TODO: receipt needed]` markers, request the missing items
- Missing voice samples: draft conservatively, flag for review
- Ambiguous angle: ask before drafting, not after

## Handoff to Waterfall

After compose completes:
→ Pass pillar draft + evidence refs + offer/CTA rules to `content-waterfall`
→ Waterfall generates all platform derivatives
