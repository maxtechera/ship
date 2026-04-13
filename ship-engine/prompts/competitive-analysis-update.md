# Prompt Template: Competitive Analysis Update

> **Use when**: A competitor ships a new feature, changes pricing, or enters the Uruguay market.
> **Output**: Updated rows in `competitive-feature-matrix.md` + updated sections in `competitive-positioning.md`.
> **Trigger**: Quarterly review, or ad-hoc when competitive intelligence surfaces new info.

---

## Prompt

```
You are a competitive analyst for Conta.uy, a Uruguay-specific accounting and compliance SaaS for freelancers and small businesses.

## Context
Conta.uy's core differentiators:
- Native DGI (Dirección General Impositiva) integration and CFE e-invoicing
- BPS (Banco de Previsión Social) payroll and social security management
- MTSS labor compliance and BPS GAFI
- WhatsApp-native customer support
- Uruguay-specific tax rates (IRPF, IVA, IRAE) and reports
- Pricing: ~990–2,490 UYU/month (target: Uruguayan freelancers and SMBs)

## Current Competitor Set
- Xero (international, no UY compliance)
- QuickBooks (US-focused, no UY compliance)
- Alegra (LATAM, no UY-specific DGI/BPS modules as of last review)
- Local Accountants (manual, high-cost)
- [ADD NEW COMPETITOR IF APPLICABLE]

## Your Task
A competitor has updated their product. Here is what changed:

**Competitor**: [INSERT COMPETITOR NAME]
**Change detected**: [DESCRIBE THE NEW FEATURE OR PRICING CHANGE]
**Source**: [URL or description of where you found this information]
**Date detected**: [YYYY-MM-DD]

Please:

1. **Assess impact** — Does this change erode any of Conta.uy's competitive advantages? Rate severity: Critical / High / Medium / Low.

2. **Update the feature matrix row(s)** — Provide the updated markdown table row(s) for `competitive-feature-matrix.md`. Use the existing legend:
   - ✅ Full = Fully supported, native
   - ⚠️ Partial = Exists but incomplete/requires workaround
   - ❌ None = Not supported
   - 💰 Paid add-on = Available at extra cost

3. **Update the positioning rebuttal** — If the change affects an existing objection, provide an updated rebuttal. If it creates a new objection, draft a new one using this format:
   - Objection: "..."
   - When you hear it: [scenario]
   - Rebuttal: [2–4 sentence response]
   - Supporting facts: [3 bullet points]

4. **Update the feature gap watch list** — Adjust the timeline risk and recommended response for any affected rows.

5. **Recommend a messaging response** — Should Conta.uy:
   a) Update website copy to address the new competitor claim?
   b) Create a comparison landing page (e.g., "Conta.uy vs [Competitor]")?
   c) Brief the support team on new objection handling?
   d) Accelerate development of a competing feature?
   Rank recommendations by urgency.

6. **Summary for stakeholders** — 3-bullet executive summary of what changed and what Conta.uy should do about it.

## Output Format
Return your response in this structure:

### Impact Assessment
[Severity: Critical/High/Medium/Low] + 1-sentence rationale

### Updated Feature Matrix Rows
```markdown
[paste updated table rows here]
```

### Updated / New Positioning Rebuttal
[rebuttal text]

### Updated Feature Gap Watch List Row
[updated table row]

### Messaging Response Recommendations
1. [highest priority action]
2. [second priority]
...

### Executive Summary
- [bullet 1]
- [bullet 2]
- [bullet 3]
```

---

## Usage Instructions

1. **Collect intel** — Use the Competitive Intelligence Checklist in `competitive-positioning.md` quarterly, or monitor competitor changelogs.
2. **Fill in the prompt variables** — Replace `[COMPETITOR NAME]`, `[CHANGE DETECTED]`, `[SOURCE]`, `[DATE]`.
3. **Run the prompt** — Submit to Claude or your preferred LLM.
4. **Review output** — Validate facts before updating docs; competitor feature claims should be verified.
5. **Update files** — Apply changes to `competitive-feature-matrix.md` and `competitive-positioning.md`.
6. **Commit changes** — Use branch `feat/competitive-update-YYYY-MM-DD` and open a PR for review.
7. **Update `Last updated` date** — In both matrix and positioning files.

---

## Quick-Start Example

```
Competitor: Alegra
Change detected: Alegra announced an "Uruguay mode" beta with DGI API connection for CFE emission, launching Q3 2026
Source: https://alegra.com/blog/uruguay-mode-announcement
Date detected: 2026-06-01
```

→ Run the full prompt above with those variables filled in.

---

## Maintenance Notes

- Keep the competitor set current — add new entrants as they appear.
- Verify exchange rates (UYU/USD) when updating pricing rows.
- Cross-reference with ICP assumptions in `icp.md` and VOC data in `voc-bank.md`.
- Tag competitive updates in Linear with label `competitive-intel` for tracking.
