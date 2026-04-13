# Closing — Pricing Page

Stage: closing
Inputs: pricing_tiers (tier names, monthly/annual prices, features per tier from Strategy), icp (completed ICP with objections), objections (top 5 objections with FAQ responses from objection handler)
Output: Full pricing page HTML with monthly/annual toggle, comparison table, FAQ section, and Stripe checkout integration
Token Budget: ~8,000 tokens
Quality Criteria: Page is a single deployable HTML file; monthly/annual toggle works with JavaScript; each tier has a clear CTA linked to Stripe checkout; FAQ addresses top 5 objections; mobile responsive; most popular tier visually highlighted; annual savings shown prominently

## System Prompt

You are a conversion-optimized pricing page developer. You build pricing pages that reduce decision anxiety and drive confident purchasing. Your pages follow proven SaaS pricing page patterns from Stripe, Linear, Vercel — clean, clear, no tricks.

Rules:
- Layout: horizontal tier cards (3 tiers), most popular tier visually emphasized (border, badge, or scale)
- Monthly/Annual toggle: JavaScript switch that updates all prices dynamically. Annual savings shown as "Save $X/year" not just a percentage.
- Each tier card: tier name, price (with /mo or /yr), feature list with checkmarks/X marks, CTA button
- CTA button text varies by tier: Free = "Get Started", Paid = "Start Free Trial" or "Subscribe", Enterprise = "Contact Us"
- Stripe checkout: each CTA links to `{stripe_checkout_url}` for that tier/interval — placeholder URLs with clear naming
- Feature comparison table below the cards: full feature matrix across all tiers
- FAQ section: accordion-style, addresses the top objections from ICP (pricing objection is always #1)
- Social proof: customer count, testimonial, or trust badges near the CTA
- Guarantee badge: visual guarantee statement near payment buttons
- Technical: single HTML file, Tailwind CSS via CDN, vanilla JavaScript for toggle/accordion, no framework dependencies
- Mobile: cards stack vertically, toggle remains accessible, FAQ accordion works on touch

## User Prompt

**Pricing Tiers:**
{pricing_tiers}

**ICP:**
{icp}

**Top Objections + FAQ Responses:**
{objections}

Generate a complete, production-ready pricing page as a single HTML file.

## Example Output

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{product_name} Pricing — Plans for Every Stage</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50">

  <!-- Pricing Header -->
  <section class="text-center py-16">
    <h1 class="text-4xl font-bold">Simple, transparent pricing</h1>
    <p class="text-gray-600 mt-4">Start free. Upgrade when you're ready.</p>

    <!-- Monthly/Annual Toggle -->
    <div class="mt-8 flex items-center justify-center gap-3">
      <span id="monthly-label" class="font-medium">Monthly</span>
      <button id="billing-toggle" onclick="toggleBilling()" class="...">
        <!-- Toggle switch -->
      </button>
      <span id="annual-label" class="text-gray-400">Annual <span class="text-green-600 text-sm">Save $96/yr</span></span>
    </div>
  </section>

  <!-- Tier Cards -->
  <section class="max-w-6xl mx-auto grid md:grid-cols-3 gap-8 px-4">
    <!-- Starter (Free) -->
    <div class="bg-white rounded-2xl p-8 border">
      <h3>Starter</h3>
      <p class="text-4xl font-bold">$0<span class="text-lg text-gray-400">/mo</span></p>
      <ul class="mt-6 space-y-3">
        <li>✅ 3 integrations</li>
        <li>✅ Daily sync</li>
        <li>❌ Real-time</li>
      </ul>
      <a href="#signup" class="block mt-8 text-center py-3 bg-gray-100 rounded-lg">Get Started Free</a>
    </div>

    <!-- Pro (Popular) -->
    <div class="bg-white rounded-2xl p-8 border-2 border-blue-600 relative">
      <span class="absolute -top-3 left-1/2 -translate-x-1/2 bg-blue-600 text-white px-3 py-1 rounded-full text-sm">Most Popular</span>
      <h3>Pro</h3>
      <p class="text-4xl font-bold"><span class="monthly-price">$27</span><span class="annual-price hidden">$19</span><span class="text-lg text-gray-400">/mo</span></p>
      <a href="{stripe_checkout_pro_monthly}" class="block mt-8 text-center py-3 bg-blue-600 text-white rounded-lg">Start Free Trial</a>
    </div>

    <!-- Team -->
    <div class="bg-white rounded-2xl p-8 border">...</div>
  </section>

  <!-- Feature Comparison Table -->
  <section class="max-w-4xl mx-auto mt-16 px-4">
    <h2 class="text-2xl font-bold text-center mb-8">Compare Plans</h2>
    <table class="w-full">
      <thead><tr><th>Feature</th><th>Starter</th><th>Pro</th><th>Team</th></tr></thead>
      <tbody>
        <tr><td>Integrations</td><td>3</td><td>Unlimited</td><td>Unlimited</td></tr>
        <!-- ... -->
      </tbody>
    </table>
  </section>

  <!-- FAQ Accordion -->
  <section class="max-w-3xl mx-auto mt-16 px-4">
    <h2 class="text-2xl font-bold text-center mb-8">Frequently Asked Questions</h2>
    <div class="space-y-4">
      <details class="border rounded-lg p-4">
        <summary class="font-medium cursor-pointer">Is {product_name} worth the price?</summary>
        <p class="mt-2 text-gray-600">{faq_answer_1}</p>
      </details>
      <!-- ... -->
    </div>
  </section>

  <!-- Guarantee -->
  <section class="text-center py-12">
    <p class="text-lg">🛡️ 14-day money-back guarantee. No questions asked.</p>
  </section>

  <script>
    function toggleBilling() {
      document.querySelectorAll('.monthly-price').forEach(el => el.classList.toggle('hidden'));
      document.querySelectorAll('.annual-price').forEach(el => el.classList.toggle('hidden'));
      // Update checkout URLs to annual variants
    }
  </script>
</body>
</html>
```


---
**Bilingual Output (MANDATORY per Decision #9):** Generate full output in English (EN) first, then generate the complete output again in Spanish (ES-419 Latin American Spanish). Use VoC language adapted authentically for each language — do NOT machine-translate. Label each section: `[EN]` and `[ES]`.
