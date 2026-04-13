# Closing — ROI Calculator

Stage: closing
Inputs: icp (documented time/money costs of the problem, willingness to pay signals, pain severity), ship_plan (pricing tiers, value proposition), validation_report (evidence of actual costs ICP incurs from pain), positioning (value prop — pain → solution → outcome)
Output: Interactive ROI calculator web component (HTML/JS) + supporting copy (landing page placement, email version), ready to embed in landing page or deploy as standalone `/roi` page
Token Budget: ~4,000 tokens
Quality Criteria: Calculator uses real ICP data for default values (not inflated estimates); math is honest and defensible (if challenged by a skeptical prospect, it should hold up); at least 2 input variables; output shows "cost of problem" vs "cost of solution" clearly; component is mobile-responsive; copy humanized; default values pre-fill with ICP-realistic numbers; no dark patterns or inflated savings claims

## System Prompt

You are a conversion copywriter and web developer who builds honest, data-backed ROI calculators. You know that a calculator that inflates results gets dismissed as marketing fluff, while one that's conservative and realistic becomes a trust-builder.

Rules:
- Default values MUST come from ICP validation data — use the pain frequency and time cost evidence from the validation report
- Math must be honest: "this saves you X hours/week × your hourly rate = Y/month in time cost" is defensible. "Increases revenue by 300%" is not.
- Use the ICP's own language for input labels — not financial jargon
- At least 2 adjustable inputs (e.g., "hours per week on this problem" and "your hourly rate")
- Output clearly shows: (1) current cost of the problem, (2) cost of solution, (3) net monthly/annual savings
- Include payback period: "Your investment pays for itself in X days"
- Component deploys as standalone HTML file or embeds as a `<div>` in existing page
- Mobile-responsive: single column on 375px, stacked inputs and output
- All copy humanized via the `humanize` skill with `channel=blog`
- Inputs are sliders or number fields — not dropdowns — for a real, interactive feel
- Calculation happens client-side (JavaScript) — no server required
- Standalone version deploys to `{product_slug}-roi.max-techera.app` or as `/roi` route on landing page

## User Prompt

**ICP (pain cost data from validation):**
{icp}

**Validation Report (evidence of time/money costs):**
{validation_report}

**Pricing:**
{pricing}

**Positioning (value prop — what problem does it solve?):**
{positioning}

Build the ROI calculator:

1. **ROI Narrative** — The honest math story in plain English
2. **Input Variable Definitions** — What users enter, with ICP-realistic defaults
3. **Output Variable Definitions** — What the calculator shows
4. **Calculator HTML/JS Component** — Complete, embeddable code
5. **Landing Page Placement Copy** — Headline + subhead + CTA that surrounds the calculator
6. **Email Version** — Text-based version for use in Day 7 Objection Killer email

## ROI Narrative Framework

The calculator tells this story:
1. **The Current Cost:** "You spend {X hours/week} on {the problem}. At your rate, that's ${Y/month}."
2. **The Solution Cost:** "{product_name} costs ${pricing}/month."
3. **The Net:** "You save ${Z/month} and get {X hours} back every month."
4. **The Payback Period:** "Your first month pays for {N months} of the subscription."

This story must be provable from ICP data. Every default value needs a source.

## Example Output

## ROI Narrative (This Product)

The problem: solopreneurs spend an average of 3.2 hours/week manually copying data between dashboards. At a typical solopreneur consulting rate of $75/hr, that's $240/month in time cost.

{product_name} Pro is $19/month.

Net savings in month 1: $240 - $19 = **$221 saved**.

Payback period: The subscription pays for itself in the first 2 hours of time saved in month 1.

*Data source: 12 Reddit threads in r/marketing and r/entrepreneur, avg of self-reported time costs in "how long do you spend on reporting?" discussions. Conservative estimate — some users report 5+ hours/week.*

## Input Variable Definitions

| Input | Label | Default | Range | Source of Default |
|-------|-------|---------|-------|------------------|
| `hours_per_week` | "Hours you spend syncing/copying data each week" | 3 | 0.5 – 20 | Average from 12 validation threads |
| `hourly_rate` | "What your time is worth per hour ($)" | 75 | 15 – 500 | ICP profile: bootstrapped solopreneur consulting/freelance rate |
| `team_size` | "Number of people affected by this problem" | 1 | 1 – 20 | Solo by default; team plan upsell trigger |

## Output Variable Definitions

| Output | Formula | Label |
|--------|---------|-------|
| `monthly_time_cost` | `hours_per_week × 4.33 × hourly_rate` | "Your current monthly cost" |
| `annual_time_cost` | `monthly_time_cost × 12` | "Per year" |
| `solution_cost_monthly` | `19` (Pro) or `49` (Business) | "{product_name} monthly cost" |
| `monthly_savings` | `monthly_time_cost - solution_cost_monthly` | "Net monthly savings" |
| `roi_ratio` | `monthly_time_cost / solution_cost_monthly` | "ROI" |
| `payback_hours` | `solution_cost_monthly / hourly_rate` | "Hours until it pays for itself" |

## Calculator HTML/JS Component

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{product_name} ROI Calculator</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f9fafb; color: #111; }
    .roi-calculator { max-width: 540px; margin: 0 auto; padding: 32px 20px; }
    .roi-calculator h2 { font-size: 1.5rem; font-weight: 700; margin-bottom: 8px; }
    .roi-calculator .subtitle { color: #6b7280; margin-bottom: 28px; font-size: 0.95rem; }
    .input-group { margin-bottom: 24px; }
    .input-group label { display: block; font-weight: 600; margin-bottom: 8px; font-size: 0.9rem; }
    .input-group .description { color: #6b7280; font-size: 0.8rem; margin-bottom: 8px; }
    .input-group input[type="range"] { width: 100%; height: 6px; accent-color: #6366f1; }
    .input-group .value-display { font-size: 1.1rem; font-weight: 700; color: #6366f1; margin-top: 4px; }
    .results { background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 12px; padding: 24px; margin-top: 32px; }
    .results h3 { font-size: 1rem; font-weight: 600; margin-bottom: 16px; color: #0369a1; }
    .result-row { display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid #e0f2fe; }
    .result-row:last-child { border-bottom: none; }
    .result-label { color: #374151; font-size: 0.9rem; }
    .result-value { font-weight: 700; font-size: 1rem; }
    .result-value.positive { color: #059669; }
    .result-value.cost { color: #dc2626; }
    .result-value.highlight { font-size: 1.4rem; color: #059669; }
    .payback { background: #ecfdf5; border-radius: 8px; padding: 16px; margin-top: 16px; text-align: center; }
    .payback .number { font-size: 2rem; font-weight: 800; color: #059669; display: block; }
    .payback .label { color: #065f46; font-size: 0.85rem; }
    .cta-wrapper { margin-top: 24px; text-align: center; }
    .cta-btn { background: #6366f1; color: white; border: none; padding: 14px 32px; border-radius: 8px; font-size: 1rem; font-weight: 600; cursor: pointer; text-decoration: none; display: inline-block; }
    .cta-btn:hover { background: #4f46e5; }
    @media (max-width: 400px) { .result-row { flex-direction: column; align-items: flex-start; gap: 4px; } }
  </style>
</head>
<body>
<div class="roi-calculator">
  <h2>See What {product_name} Saves You</h2>
  <p class="subtitle">Real math. No inflated claims. Adjust for your situation.</p>

  <div class="input-group">
    <label for="hours">Hours you spend syncing data each week</label>
    <p class="description">Include manual exports, copy-pasting, and fixing errors</p>
    <input type="range" id="hours" min="0.5" max="20" step="0.5" value="3">
    <div class="value-display"><span id="hours-display">3</span> hours/week</div>
  </div>

  <div class="input-group">
    <label for="rate">What your time is worth per hour ($)</label>
    <p class="description">Your consulting rate, salary equivalent, or what you could bill instead</p>
    <input type="range" id="rate" min="15" max="500" step="5" value="75">
    <div class="value-display">$<span id="rate-display">75</span>/hour</div>
  </div>

  <div class="results">
    <h3>Your ROI Estimate</h3>
    <div class="result-row">
      <span class="result-label">Monthly time wasted (current)</span>
      <span class="result-value cost" id="monthly-cost">$978</span>
    </div>
    <div class="result-row">
      <span class="result-label">{product_name} Pro cost</span>
      <span class="result-value cost">$19/mo</span>
    </div>
    <div class="result-row">
      <span class="result-label">Net monthly savings</span>
      <span class="result-value highlight" id="monthly-savings">$959</span>
    </div>
    <div class="result-row">
      <span class="result-label">Annual savings</span>
      <span class="result-value positive" id="annual-savings">$11,508</span>
    </div>
    <div class="payback">
      <span class="number" id="payback-hours">0.25</span>
      <span class="label">hours until {product_name} pays for itself this month</span>
    </div>
  </div>

  <div class="cta-wrapper">
    <a href="{product_url}/signup?utm_source=roi-calculator&utm_medium=web&utm_campaign=closing&utm_content=cta" class="cta-btn">
      Start free — see it in action
    </a>
    <p style="color:#6b7280;font-size:0.8rem;margin-top:8px;">Free tier. No credit card required.</p>
  </div>
</div>

<script>
  const hoursSlider = document.getElementById('hours');
  const rateSlider = document.getElementById('rate');

  function calculate() {
    const hours = parseFloat(hoursSlider.value);
    const rate = parseFloat(rateSlider.value);
    const solutionCost = 19; // Pro monthly

    document.getElementById('hours-display').textContent = hours;
    document.getElementById('rate-display').textContent = rate;

    const monthlyTimeCost = hours * 4.33 * rate;
    const monthlySavings = monthlyTimeCost - solutionCost;
    const annualSavings = monthlySavings * 12;
    const paybackHours = solutionCost / rate;

    document.getElementById('monthly-cost').textContent = '$' + Math.round(monthlyTimeCost).toLocaleString();
    document.getElementById('monthly-savings').textContent = monthlySavings > 0
      ? '$' + Math.round(monthlySavings).toLocaleString()
      : 'Break even at this rate';
    document.getElementById('annual-savings').textContent = '$' + Math.round(annualSavings).toLocaleString();
    document.getElementById('payback-hours').textContent = paybackHours.toFixed(1);
  }

  hoursSlider.addEventListener('input', calculate);
  rateSlider.addEventListener('input', calculate);
  calculate(); // Initial render
</script>
</body>
</html>
```

## Landing Page Placement Copy

**Placement:** After the pricing section, before the FAQ. Serves as the bridge between "here's the price" and "here's whether it's worth it."

**Headline:** Stop guessing — see exactly what this costs you to NOT have.
**Subheadline:** Adjust the sliders for your situation. The math does the rest.
*[Insert calculator component here]*
**Below calculator:** "Still not sure? The free tier is unlimited. No card required. The numbers above are what happens when you decide to upgrade."

## Email Version (Day 7 Objection Killer)

```
Subject option A: The honest math on what {product_name} saves you
Subject option B: You're probably losing more than you think
Subject option C: A simple calculation (and what it means for you)

---

Before I ask you to upgrade, I want to show you the math.

Here's how I think about it:

If you spend 3 hours/week syncing data manually — which is about average — that's 13 hours/month.

If your time is worth $50/hr (conservative), that's **$650/month in time cost**.

{product_name} Pro is $19/month.

Net: you save **$631/month**. Every month. Automatically.

If you want to plug in your own numbers, I built a quick calculator:
→ [Calculate my ROI]({product_url}/roi?utm_source=email&utm_medium=nurture&utm_campaign=objection-killer)

Even at $25/hr rate and 1 hour/week, the calculator shows you break even in your first session.

The free tier is still there if you want to see it work before committing.

— {sender_name}
```

### Blackboard Keys
- `closing.roi_calculator`: deployed URL or file path
- `closing.roi_default_hours`: 3 (from ICP validation data)
- `closing.roi_default_rate`: 75 (from ICP profile)


---
**Bilingual Output (MANDATORY per Decision #9):** Generate full output in English (EN) first, then generate the complete output again in Spanish (ES-419 Latin American Spanish). Use VoC language adapted authentically for each language — do NOT machine-translate. Label each section: `[EN]` and `[ES]`.
