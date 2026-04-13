---
name: content-feedback-loop
version: "1.0.0"
description: "Ship → Measure → Log → Apply. Extract patterns from performance data and route them to the right destination."
allowed-tools: Read, Write, Edit
user-invocable: true
---

# Content Feedback Loop

Every piece of content teaches something. This skill ensures those lessons are captured and applied.

```
SHIP → MEASURE → LOG → APPLY → next cycle
```

## Phase 1: Ship (immediately after publishing)

When a piece publishes:
1. Record the live URL / permalink
2. Note the publish timestamp and platform
3. Set the measurement window (when to check metrics: 24h / 7d)
4. Flag any pre-publish notes (what we expected, what we tried differently)

## Phase 2: Measure (when metrics come in)

Pull metrics from the live asset (use `content-measure`):
- Capture day-1 and week-1 snapshots
- Compare against your baseline and batch average
- Note what's above and below expectations

## Phase 3: Log (extract the pattern)

For each piece that underperformed or overperformed, extract a pattern:

```
Date: YYYY-MM-DD
Asset: [URL or ID]
Result: [metric + value vs baseline]
Pattern: [what this tells us — the repeatable insight, not the one-time fact]
Category: hook / format / timing / platform / topic / CTA
```

**Pattern categories:**
| Category | Log here when... |
|----------|-----------------|
| `hook_works` | A hook type drove above-average 3s retention |
| `hook_fails` | A hook type caused early drop-off |
| `format_wins` | A specific format (carousel, reel, thread) outperformed batch |
| `timing_pattern` | Posting time correlated with reach |
| `topic_resonance` | Specific topic cluster drove saves/shares |
| `cta_conversion` | A specific CTA wording drove above-average clicks |

## Phase 4: Apply (route the learning)

Route each pattern to the right destination:

| Pattern type | Route to |
|-------------|---------|
| Hook formula | Storyboard → hook section rules |
| Format preference | Waterfall → platform priority order |
| Voice/copy | Copy skill → voice constraints |
| Timing | Distribution → schedule defaults |
| Topic cluster | Compose → next pillar topic shortlist |
| CTA wording | Offer + copy skills |

**Routing format:**
```
Pattern: [insight]
Route: [skill/file] → [specific section]
Change: [what to update or add]
```

## Rules

- Patterns require evidence — a sample of 1 is not a pattern, it's an observation
- Patterns with N≥3 data points can update skill defaults
- Single-data-point observations: log as "observation", not "pattern"
- Never update strategy-level defaults from a single outlier

## Done Criteria

- [ ] Publish log entry created (URL + timestamp + platform)
- [ ] Metrics captured with date range and source
- [ ] Pattern extracted (not just the number — the why)
- [ ] Pattern routed to correct skill/file
- [ ] If N≥3 for a pattern: skill default updated or flag raised
