# Validation Report: {name}

## Pain Score Card

| Signal | Score (1-5) | Weight | Weighted |
|--------|-------------|--------|----------|
| Pain frequency | {X} | 25% | {X} |
| Willingness to pay | {X} | 25% | {X} |
| Competition gap | {X} | 20% | {X} |
| Audience fit | {X} | 15% | {X} |
| Market timing | {X} | 15% | {X} |
| **TOTAL** | | | **{X}/5.0** |

**Verdict: {SHIP 🟢 / EXPLORE 🟡 / KILL 🔴}**

---

## Riskiest Assumptions (Gate-V readiness)

| Assumption | Test method | Kill condition | Status |
|------------|-------------|----------------|--------|
| {A1} | {how tested next} | {what invalidates this} | {unvalidated/partial/validated} |
| {A2} | {how tested next} | {what invalidates this} | {unvalidated/partial/validated} |
| {A3} | {how tested next} | {what invalidates this} | {unvalidated/partial/validated} |

---

## Offer-Validation Pattern Coverage (for Gate-V packet)

Reference: `templates/offer-validation-patterns.md`

| Pattern | Evidence linked | Confidence | Caveat |
|--------|------------------|------------|--------|
| Value equation decomposition | {link} | {high/medium/low} | {if needed} |
| Obstacle and delivery cube | {link} | {high/medium/low} | {if needed} |
| Risk reversal (guarantee) | {link} | {high/medium/low} | {if needed} |
| Scarcity and urgency integrity | {link} | {high/medium/low} | {if needed} |
| Bonus stack relevance | {link} | {high/medium/low} | {if needed} |
| Niche-first segment selection | {link} | {high/medium/low} | {if needed} |

---

## Level 1: Pain Discovery

### Reddit Signals
| Subreddit | Threads Found | Top Thread | Upvotes | Sentiment |
|-----------|--------------|------------|---------|-----------|
| {sub} | {N} | [{title}]({url}) | {N} | {positive/negative/desperate} |

**Key quotes:**
> "{actual quote from user expressing pain}" — u/{user}, {sub} ([link]({url}))
> "{another}" — u/{user}, {sub} ([link]({url}))

### Twitter/X Signals
- Complaints found: {N} in last 90 days
- "I wish..." / "why is there no..." tweets: {N}
- Notable tweets:
  > "{tweet text}" — @{handle} ({likes} likes) ([link]({url}))

### Forum Signals
| Source | Threads | Key Finding |
|--------|---------|-------------|
| Indie Hackers | {N} | {finding} |
| Hacker News | {N} | {finding} |
| Product Hunt | {N} | {finding} |
| Quora | {N} | {finding} |

### App Store Pain (competitor reviews)
| Competitor | Rating | 1-star reviews | Top complaint |
|-----------|--------|----------------|---------------|
| {name} | {X}/5 | {N} | "{complaint}" |

### Evidence Ledger (Required)
| quote | source_url | captured_at | source_date | engagement | evidence_type | confidence_note |
|------|------------|-------------|-------------|------------|---------------|-----------------|
| "{quote}" | {url} | {YYYY-MM-DD} | {date or age} | {upvotes/comments/likes} | {behavioral/opinion} | {confidence context} |
| "{quote}" | {url} | {YYYY-MM-DD} | {date or age} | {upvotes/comments/likes} | {behavioral/opinion} | {confidence context} |

---

## Level 2: Demand Quantification

### Search Demand
| Keyword | Monthly Volume | Trend (12mo) | CPC |
|---------|---------------|--------------|-----|
| {keyword} | {vol} | {↑/↓/→} | ${X} |

### Google Trends
- Trend direction: {growing / stable / declining}
- Seasonal patterns: {any?}
- Related rising queries: {list}

### Competitor Landscape
| Competitor | Est. Traffic/mo | Pricing | Strengths | Gap we fill |
|-----------|----------------|---------|-----------|-------------|
| {name} | {N} | {$X/mo} | {what} | {what's missing} |

### Existing Spend
- Are people paying for alternatives? **{YES/NO}**
- Price range of existing solutions: ${min} - ${max}/mo
- Open-source alternatives: {list + GitHub stars}

---

## Level 3: Willingness to Pay

### Direct Evidence
{3-5 real threads/comments where someone explicitly asked for this or said they'd pay}

1. **[{title}]({url})** — {source}
   > "{quote showing willingness to pay or desperation}"
   - {N} upvotes/likes, {N} comments agreeing

2. **[{title}]({url})** — {source}
   > "{quote}"

3. **[{title}]({url})** — {source}
   > "{quote}"

### Workaround Analysis
- Are people building DIY solutions? **{YES/NO}**
- Common workarounds: {list}
- Workaround pain: {what sucks about the workaround}

### Price Anchoring
- Adjacent tools charge: ${X}-${Y}/mo
- Recommended price point: ${X}/mo
- Reasoning: {why this price}

---

## Level 4: Audience-Market Fit

### Max's Audience Match
- **Pain overlap:** {do Max's followers have this problem?} (1-5)
- **Authority:** {can Max credibly sell this?} (1-5)
- **Distribution:** {can IG + newsletter + Skool reach buyers?} (1-5)
- **Content potential:** {can Max make 5+ content pieces about this?} (1-5)

### Language Market Analysis
- **Spanish market:** {competition level, opportunity}
- **English market:** {competition level, TAM}
- **Recommendation:** {ES / EN / Both} — {reasoning}

---

## Level 5: Risk Assessment

### Top Risks
1. **{risk}** — Mitigation: {how}
2. **{risk}** — Mitigation: {how}
3. **{risk}** — Mitigation: {how}

### Disconfirming Evidence
- {signal that contradicts our thesis}
- {what this contradiction implies and how we address it}

### Assumptions to Validate Post-Launch
- {assumption 1}
- {assumption 2}

---

## Final Verdict

**Score: {X}/5.0 → {SHIP 🟢 / EXPLORE 🟡 / KILL 🔴}**

**One-line summary:** {why ship or why kill, backed by the strongest data point}

**If SHIP:** {recommended next step}
**If KILL:** {what we learned, worth revisiting when?}

**Behavioral evidence ratio:** {X}% behavioral / {Y}% opinion

**Evidence strength:** {N} real threads, {N} direct quotes, {N} data points

**Evidence breadth checklist:**
- Independent source types used: {N} (minimum target: 3)
- Disconfirming signals logged: {N} (minimum target: 2)
- High-impact assumptions with kill conditions: {N} (minimum target: 3)
