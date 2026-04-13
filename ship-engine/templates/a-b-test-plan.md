# A/B Test Plan Template

> **Template version:** 1.0 | Ship Engine GTM Deliverable

---

## Overview

| Field | Value |
|-------|-------|
| **Test Name** | `[descriptive-slug]` |
| **Owner** | |
| **Start Date** | |
| **End Date** | |
| **Status** | Planning / Running / Concluded |

---

## 1. Hypothesis

> _What do you believe will happen, and why?_

**We believe that** `[change/variant]`  
**will result in** `[expected outcome]`  
**for** `[target audience segment]`  
**because** `[reasoning / prior evidence]`.

---

## 2. Goal & Primary Metric

| | |
|---|---|
| **Primary KPI** | e.g., Signup conversion rate |
| **Secondary KPIs** | e.g., CTR, Time on page, Bounce rate |
| **Minimum Detectable Effect (MDE)** | e.g., +10% relative lift |
| **Statistical Significance Target** | 95% |
| **Statistical Power** | 80% |

---

## 3. Variants

### Control (A)
- **Description:** Current state / baseline
- **URL / element:** 
- **Screenshot / spec link:**

### Variant B
- **Description:** What changes
- **URL / element:**
- **Screenshot / spec link:**

### Variant C _(optional)_
- **Description:**
- **URL / element:**

---

## 4. Audience & Traffic Split

| Segment | Criteria | Traffic % |
|---------|----------|-----------|
| Control A | | 50% |
| Variant B | | 50% |

**Exclusions:** (e.g., existing customers, internal IPs)

**Sample size needed:** `[calculated from MDE + significance]`  
**Estimated run time:** `[days/weeks based on daily traffic]`

---

## 5. Implementation

- **Tool / Platform:** (e.g., Google Optimize, VWO, custom flags)
- **Engineering effort:** Low / Medium / High
- **QA checklist:**
  - [ ] Variant renders correctly on mobile
  - [ ] Variant renders correctly on desktop
  - [ ] Analytics events fire correctly
  - [ ] No flickering (FOOC)
  - [ ] Holdout/cookie persists across sessions

---

## 6. Timeline

| Milestone | Date |
|-----------|------|
| Hypothesis finalized | |
| Design / copy ready | |
| Engineering build | |
| QA complete | |
| Test live | |
| Interim check (50% data) | |
| Decision deadline | |
| Retrospective | |

---

## 7. Decision Criteria

| Outcome | Action |
|---------|--------|
| Variant wins (stat sig) | Ship variant, document learnings |
| Control wins | Keep control, iterate on hypothesis |
| No significant difference | Run longer OR pivot hypothesis |
| Test broken / data invalid | Restart with fix |

**Stop early if:**
- Variant shows >20% harm to primary KPI
- Critical bug detected in variant

---

## 8. Results

> _Fill in after test concludes._

| Variant | Conversions | Visitors | Rate | Uplift | p-value |
|---------|-------------|----------|------|--------|---------|
| Control A | | | | — | — |
| Variant B | | | | | |

**Winner:** Control / Variant B / No winner  
**Confidence:** %  
**Revenue impact (estimated):**

---

## 9. Learnings & Next Steps

- **Key insight:**
- **What surprised us:**
- **Follow-up test:**
- **Ship decision:**

---

_Template: Ship Engine · NEO-231_
