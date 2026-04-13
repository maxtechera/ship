# Prompt: Generate Refund Policy (SaaS) + ToS Alignment

**Objective:** Draft a production-ready Refund Policy aligned with Terms of Service and practical billing operations.

## Context
You are a legal-operations writer producing plain-language policy docs for a SaaS product. The output must be clear, enforceable, and customer-facing.

## Inputs
- Company name: `{company_name}`
- Legal entity: `{legal_entity_name}`
- Product name: `{product_name}`
- Jurisdiction: `{jurisdiction}`
- Support email: `{support_email}`
- Support URL: `{support_url}`
- Terms URL: `{terms_url}`
- Website URL: `{website_url}`
- Refund window (days): `{refund_window_days}`
- Non-refundable items: `{non_refundable_items}`
- Trial/renewal rules: `{trial_and_renewal_rules}`

## Required Sections
1. Eligibility
2. Trial and renewal rules
3. Refund request process
4. Review and processing timelines
5. Abuse/fraud exceptions
6. Terms of Service relationship
7. Consumer law carve-out
8. Contact information

## Output Constraints
- Use markdown headings and concise bullets
- Avoid legal jargon where plain language works
- Include placeholders only when input is missing
- No contradictory clauses between refunds and ToS relationship

## Secondary Output
After the refund policy, include a short "ToS cross-check" checklist:
- [ ] Refund policy link included in ToS
- [ ] ToS link included in refund policy
- [ ] Jurisdiction consistent across both docs
- [ ] Cancellation + renewal language consistent
