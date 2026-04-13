---
name: content-distribution
version: "1.0.0"
description: "Publish and distribute content across platforms with UTM generation and schedule management."
allowed-tools: Bash, Read, Write, Edit
user-invocable: true
---

# Content Distribution

Publish content to the right platforms at the right time.

## Channel Tiers

### Tier 1 — API/Automation Ready
- **Instagram** — reels, carousels, stories via Meta Graph API
- **Newsletter** — MailerLite campaigns and subscriber management
- **Telegram** — direct messaging to groups

### Tier 2 — Semi-Manual (prepare assets, upload via platform UI)
- **TikTok** — prepare captions + hashtags, manual upload
- **YouTube Shorts** — prepare metadata, manual upload
- **Twitter/X** — compose + schedule via platform
- **LinkedIn** — compose + post via platform

## Pre-Distribution Checklist

Before publishing any asset:
- [ ] Asset QA complete (copy humanized, visuals crop-safe)
- [ ] UTM links generated for all CTAs
- [ ] Platform formatting verified (aspect ratio, caption length, hashtags)
- [ ] Event tracking confirmed (GA4 events will fire on click)
- [ ] Schedule confirmed (time + timezone)

## UTM Generation

Every link in published content must include UTM parameters:

```
utm_source   = platform (instagram, newsletter, tiktok, linkedin)
utm_medium   = format (reel, carousel, story, email, post)
utm_campaign = run name or content series slug
utm_content  = specific asset identifier
```

Generate a UTM manifest (CSV) for each content batch:
```
asset_id, platform, format, url, utm_source, utm_medium, utm_campaign, utm_content, full_utm_url
```

## Schedule Format

```json
[
  {
    "date": "YYYY-MM-DD",
    "time": "HH:MM",
    "platform": "instagram",
    "format": "reel",
    "asset_id": "...",
    "caption": "...",
    "hashtags": [...],
    "link_in_bio": true
  }
]
```

## Post-Publish Confirmation

After publishing, log:
- Published URL / permalink
- Timestamp
- Platform and format
- UTM link confirmed in post

This becomes the measurement baseline for `content-measure`.

## Rules

- Never auto-publish to personal social accounts — prepare + confirm with owner
- Draft autoscheduling is allowed; live publishing requires explicit approval
- Hashtag research per platform (Instagram: 5-10 relevant, TikTok: 3-5)
- Cross-posting: adapt format per platform, never copy-paste across

## Done Criteria

- [ ] UTM manifest generated (all CTAs covered)
- [ ] Schedule documented with dates, times, platforms
- [ ] Platform-specific formatting applied
- [ ] Post-publish URLs logged
- [ ] Measurement baseline set for `content-measure`
