# Prompt: Generate Press Release from Press Kit
<!-- NEO-221 | Ship Engine: Launch Deliverable -->
<!-- Context: Conta.uy — Uruguay-first accounting SaaS for freelancers -->
<!-- Usage: Fill in the INPUTS section below, then pass the full prompt to Claude/GPT-4. -->
<!-- Output: A 400–600 word press release ready for distribution. -->

---

## PROMPT (copy everything below the dashed line into your AI chat)

---

You are an experienced tech journalist and PR copywriter. Your task is to write a compelling, publication-ready press release for a software product launch.

Use the press kit information provided below to produce a press release that:
- Follows the **inverted pyramid** structure (most important info first)
- Uses **AP Style** (third person, active voice, no hyperbole)
- Is **400–600 words** (body only, excluding headline and boilerplate)
- Includes a **compelling headline** (under 12 words, benefit-first)
- Includes a **sub-headline** (one sentence, adds context to headline)
- Contains **two quotes**: one from the founder, one from a beta user or advisor
- Ends with the **standard "About" boilerplate** and media contact info
- Targets **tech and business journalists** covering Latin American startups, fintech, and SaaS

---

### PRESS KIT INPUTS

**Company Name:** {{COMPANY_NAME}}
**Product Name:** {{PRODUCT_NAME}}
**Tagline:** {{TAGLINE}}
**Launch Date:** {{LAUNCH_DATE}}
**City, Country:** {{CITY}}, {{COUNTRY}}

**What the product does (1–3 sentences):**
{{PRODUCT_DESCRIPTION}}

**Target user:**
{{TARGET_USER}} — e.g., "Independent freelancers and self-employed professionals in Uruguay who need to manage invoices, taxes, and cash flow without an accountant."

**Key differentiator (why this product, why now):**
{{KEY_DIFFERENTIATOR}} — e.g., "First accounting SaaS built specifically for Uruguay's freelance tax system (monotributo), with automatic BPS/DGI compliance built in."

**3 key stats or milestones:**
1. {{STAT_1}} — e.g., "500+ freelancers on the waitlist before launch"
2. {{STAT_2}} — e.g., "Average user saves 3 hours/month on invoicing"
3. {{STAT_3}} — e.g., "Supports all invoice types required by DGI as of 2025"

**Founder name + title:**
{{FOUNDER_NAME}}, {{FOUNDER_TITLE}}

**Founder quote (authentic, specific, avoid clichés like "thrilled" or "excited"):**
"{{FOUNDER_QUOTE}}"

**Beta user / customer quote (name + descriptor):**
"{{USER_QUOTE}}"
— {{USER_NAME}}, {{USER_DESCRIPTOR}} (e.g., "freelance graphic designer, Montevideo")

**Pricing:**
{{PRICING}} — e.g., "Free plan available; Pro plan at $X/month"

**Website:**
{{WEBSITE_URL}}

**Media contact:**
Name: {{CONTACT_NAME}}
Email: {{PRESS_EMAIL}}
Phone: {{PHONE}} (optional)

**Company boilerplate (copy from press kit):**
{{BOILERPLATE}}

---

### OUTPUT FORMAT

Structure the press release exactly like this:

```
FOR IMMEDIATE RELEASE

[HEADLINE]
[SUB-HEADLINE]

[CITY, COUNTRY] — [DATE] — [Opening paragraph: who, what, where, when, why — 2-3 sentences]

[Body paragraph 1: Problem / context — what pain does this solve?]

[Body paragraph 2: Solution / product description — key features, differentiator]

[Founder quote]

[Body paragraph 3: Traction, stats, market opportunity]

[Beta user / customer quote]

[Body paragraph 4: Availability, pricing, call to action]

###

About [COMPANY NAME]
[Boilerplate]

Media Contact:
[Contact block]
```

---

### TONE & STYLE GUIDELINES

- **Avoid:** "thrilled," "excited," "game-changing," "revolutionary," "disrupting," "world-class"
- **Use instead:** Specific numbers, concrete outcomes, direct statements
- **Voice:** Confident, factual, human — not corporate
- **Regional flavor:** Acknowledge that this is a Uruguay-first launch and explain why that market matters
- **Length:** Tight. Every sentence must earn its place.

---

### OPTIONAL VARIATIONS (request one at a time after the base version)

After generating the base press release, you can request:

1. **Spanish version** — "Translate the press release into Rioplatense Spanish, keeping AP Style equivalent (estilo periodístico neutro)"
2. **Short pitch email version** — "Condense this into a 150-word journalist pitch email with subject line"
3. **Social media announcement (Twitter/X thread)** — "Rewrite this as a 5-tweet launch thread"
4. **LinkedIn founder post version** — "Rewrite this as a first-person LinkedIn post from the founder's perspective (300–400 words, professional but personal)"

---

_Prompt version: 1.0 | NEO-221 | Last updated: {{DATE}}_
