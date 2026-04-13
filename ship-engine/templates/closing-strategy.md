# Closing Strategy: {name}

## Pricing
| Tier | Price | Features | Target User |
|------|-------|----------|-------------|
| Free | $0 | {limited features} | {tire kickers, word of mouth} |
| Pro | ${X}/mo | {full features} | {core user} |
| Team | ${X}/mo | {pro + collab} | {teams, if applicable} |

**Launch pricing:** {50% off for first 50 / lifetime deal / early bird}
**Annual discount:** {2 months free on annual billing}
**Guarantee:** {30-day money-back, no questions asked}

## Payment Setup
- [ ] Stripe product created
- [ ] Pricing tiers configured
- [ ] Checkout flow tested
- [ ] Webhook handler for fulfillment
- [ ] Receipt/invoice automation
- [ ] Revenue dashboard access

## Conversion Triggers
| Trigger | When | Implementation |
|---------|------|---------------|
| Free tier limit | User hits usage cap | In-app upgrade modal |
| Trial expiry | Day {X} of trial | Email + in-app banner |
| Feature gate | User clicks locked feature | Upgrade prompt with feature preview |
| Social proof | On pricing page | "X people signed up this week" |
| Urgency | Pre-launch period | Countdown timer on pricing |
| Scarcity | If applicable | "X spots left at this price" |

## Objection Handling Matrix
| Objection | Response | Where to Deploy |
|-----------|----------|----------------|
| "Too expensive" | ROI calc: {pain costs $X/mo, tool costs $Y/mo} | Pricing page, Email 7 |
| "Can build it myself" | Time calc: {X hours × $rate = $cost} vs ${Y}/mo | FAQ, landing page |
| "Doesn't work for me" | 30-day guarantee + {specific use case examples} | Checkout page |
| "I'll do it later" | Early bird expires {date}, price increases to ${X} | Email 10, popup |
| "Need to ask my team" | Share link with summary, team trial | Email follow-up |

## Post-Purchase Flow
| Action | Timing | Channel | Content |
|--------|--------|---------|---------|
| Onboarding | Immediate | Email | Get to first value in <5 min |
| Setup guide | Immediate | In-app | Interactive walkthrough |
| Check-in | Day 3 | Email | "How's it going? Need help?" |
| Testimonial ask | Day 7 | Email | "Would you share your experience?" |
| Feature highlight | Day 14 | Email | "Did you know about {feature}?" |
| Referral | Day 21 | Email | "Give ${X}, get ${X}" |
| Upsell | Day 30 | Email | "Unlock {tier} for {benefit}" |

## Revenue Targets
| Period | Target | Metric |
|--------|--------|--------|
| Week 1 | {X} paying customers | ${X} revenue |
| Month 1 | {X} paying customers | ${X} MRR |
| Month 3 | {X} paying customers | ${X} MRR |

## Churn Prevention
| Signal | Action |
|--------|--------|
| No login in 7 days | Re-engagement email |
| Downgrade request | Offer discount or pause |
| Cancellation | Exit survey + win-back offer |
| Payment failure | Dunning emails (3 attempts) |
