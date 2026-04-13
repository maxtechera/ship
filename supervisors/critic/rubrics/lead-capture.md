# Critic Rubric — Lead Capture (Stage 5B)

Applies to: offer stack, lead magnet, funnel infrastructure, UTM links, analytics

## Offer Stack Checks

| # | Check | PASS criteria | REVISE trigger |
|---|-------|--------------|----------------|
| 1 | Hormozi formula applied | Dream Outcome × Perceived Likelihood ÷ Time Delay ÷ Effort all addressed | Missing any formula element |
| 2 | Guarantee present | Explicit guarantee (money-back period or trial length) stated | No guarantee |
| 3 | Copy humanized | Offer copy reads naturally, no AI cadence | AI cadence detected |
| 4 | ICP pain trace | Offer addresses top-ranked ICP pain from validate.icp | Offer unrelated to top ICP pain |

## Lead Magnet Checks

| # | Check | PASS criteria | REVISE trigger |
|---|-------|--------------|----------------|
| 5 | Artifact exists | Downloadable file or configured free tier linked | Not created |
| 6 | Delivers genuine value | Content would be useful without the product | Purely promotional |

## Funnel Infrastructure Checks

| # | Check | PASS criteria | REVISE trigger |
|---|-------|--------------|----------------|
| 7 | Email group created | Provider group/list created (API call logged) | Missing |
| 8 | Signup form live | Form embedded on landing page, tested | Form not present or broken |
| 9 | UTM links generated | utm-links.csv with all channel × content × CTA combos | Missing file |
| 10 | End-to-end tracking verified | Test documented: UTM visit → form fill → event fired → email group joined | Not tested |
| 11 | GA4 events defined | signup/lead_magnet_download/checkout_start/purchase events configured | Missing events |

## REVISE output required
List each failing check + specific fix instruction.
