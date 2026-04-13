# Offer Validation Pattern Map (Validate -> Gate-V -> Strategy -> Gate-S)

Use this map to convert evidence into gate decisions without skipping confidence caveats.

## Pattern Matrix

| Pattern | Validate (evidence) | Gate-V (decision test) | Strategy (design choice) | Gate-S (lock check) | Source |
|--------|----------------------|-------------------------|---------------------------|---------------------|--------|
| Value equation decomposition | Fill Dream Outcome, Perceived Likelihood, Time Delay, Effort/Sacrifice from raw VoC quotes | At least 3 assumptions include one variable from the value equation and a falsifiable kill condition | Build angle-to-value-equation mapping table in ship plan | Strategy lock includes at least 3 winning angles tied to value equation levers | https://www.acquisition.com/hubfs/Offer%20Checklists%20-%20PDF%20Downloads/Pricing-Value-Checklist.pdf?hsLang=en |
| Obstacle and delivery cube | Capture "why now", "what blocks them", and current workaround pain | Disconfirming section must include at least one obstacle that weakens perceived likelihood | Turn top obstacles into offer components, bonuses, and delivery sequence | Offer stack explicitly maps each obstacle to a concrete mechanism | https://www.acquisition.com/hubfs/Offer%20Checklists%20-%20PDF%20Downloads/Offer+Creation+Checklist.pdf |
| Risk reversal (guarantee) | Collect buyer-risk language in quotes (fear of wasting money/time) | Confidence note must state unknowns a guarantee must absorb | Define guarantee type, terms, and abuse safeguards | Strategy lock includes guarantee copy + policy + owner | https://www.acquisition.com/hubfs/Offer%20Checklists%20-%20PDF%20Downloads/Unbeatable-Guarantee-Checklist.pdf?hsLang=en |
| Scarcity and urgency integrity | Validate constraints with real capacity/time signals (not fake scarcity) | Reject artificial urgency claims unsupported by evidence | Define scarcity mechanism (cohort cap, bonus expiration, price step-up) | Lock only if mechanism is verifiable and can be audited post-launch | https://www.acquisition.com/hubfs/Offer%20Checklists%20-%20PDF%20Downloads/Scarcity-Urgency-Checklist.pdf?hsLang=en |
| Bonus stack relevance | Tag repeated pain fragments that can be removed with narrow tactical assets | Require bonus hypothesis for top unresolved objections | Add bonus list tied to each objection and segment trigger | Lock bonus stack with activation conditions and removal date | https://www.acquisition.com/hubfs/Offer%20Checklists%20-%20PDF%20Downloads/Bonus-Creation-Checklist.pdf?hsLang=en |
| Niche-first segment selection | Score segment specificity from evidence table (role, context, channel) | Default revise if segment remains broad or generic | Set primary, deferred, and excluded segment lock | Parallel fanout blocked if excluded segments are missing | https://www.acquisition.com/hubfs/Offer%20Checklists%20-%20PDF%20Downloads/Pick-Your-Niche-Checklist.pdf?hsLang=en |
| MVP and behavior-over-opinion | Include behavioral signals (actual spend, churn complaints, failed workarounds) | Cap confidence at 0.79 if behavioral evidence ratio < 50% | Prioritize smallest testable angle with measurable conversion boundary | Lock 30-day experiment map with pass/fail thresholds and owner | http://www.startuplessonslearned.com/2009/08/minimum-viable-product-guide.html |
| Hands-on demand validation | Include direct user contact logs or real interaction traces when possible | Confidence caveat required if no direct user interaction occurred | Choose channels where direct conversations can continue (community + outreach) | Lock first-batch execution around feedback-rich channels before broad fanout | https://www.paulgraham.com/ds.html |

## Confidence and Attribution Caveat Rule

- Mark `attribution_confidence: high` when pattern comes directly from official checklist language.
- Mark `attribution_confidence: medium` when pattern is an operational interpretation, not explicit wording.
- Mark `attribution_confidence: low` when pattern is inferred from adjacent frameworks; include a caveat in Gate-V notes.

## Minimum Gate Packet Addendum

Append this block to Gate-V and Gate-S decision packets:

```md
## pattern_evidence_coverage
- value_equation_linked: {yes/no}
- obstacle_map_linked: {yes/no}
- guarantee_defined: {yes/no}
- scarcity_mechanism_verifiable: {yes/no}
- segment_lock_specific: {yes/no}
- behavioral_evidence_ratio: {0.00-1.00}
- attribution_confidence: {high/medium/low}
- caveats: {none or explicit caveat text}
```
