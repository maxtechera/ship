# Checkout Flow Test Plan

This document outlines the test cases for the checkout process of the Ship Engine, ensuring robust payment processing and a seamless user experience.

## Test Scenarios

### 1. Add to Cart & Cart Management
- **TC-01: Add Single Item**: Verify a single item can be added to the cart and the cart count updates.
- **TC-02: Add Multiple Items**: Verify multiple different items can be added.
- **TC-03: Update Quantity**: Verify changing item quantity in cart updates subtotal and total correctly.
- **TC-04: Remove Item**: Verify items can be removed and totals decrease accordingly.
- **TC-05: Cart Persistence**: Verify cart contents persist across page refreshes (session-based).

### 2. Shipping Options & Information
- **TC-06: Address Validation**: Verify mandatory address fields (email, street, city, country) are validated.
- **TC-07: Shipping Method Selection**: Verify different shipping methods (Standard, Express, etc.) are selectable.
- **TC-08: Dynamic Shipping Costs**: Verify shipping costs update based on selected method and destination.

### 3. Payment Methods (Gateways)
- **TC-09: Stripe (Success)**: Use test cards to verify successful payment flow.
- **TC-10: Stripe (Failure - Card Declined)**: Verify error message when using a declined test card.
- **TC-11: Mercado Pago (Success)**: Verify redirection and successful callback from MP sandbox.
- **TC-12: Mercado Pago (Failure)**: Verify handling of rejected payments in MP.
- **TC-13: Currency Validation**: Verify the amount charged matches the cart total in the correct currency.

### 4. Confirmation Page & Post-Purchase
- **TC-14: Order Summary**: Verify the confirmation page displays the correct Order ID, items, and total paid.
- **TC-15: Success Redirect**: Verify automatic redirect to success page after payment gateway callback.
- **TC-16: Email Confirmation**: Verify a confirmation email is triggered to the user's email.

### 5. Error Handling & Edge Cases
- **TC-17: Expired Session**: Verify behavior when trying to pay with an expired session or empty cart.
- **TC-18: Network Interruption**: Verify system state if the connection is lost during the callback.
- **TC-19: Invalid Payment Details**: Verify UI feedback for invalid card format or expired dates.

### 6. Incomplete & Abandoned Payments
- **TC-20: Abandoned Checkout**: Verify that abandoning the flow at the payment step does not create a "Paid" order.
- **TC-21: Pending State**: Verify that payments in "Pending" status (common in MP) are handled as pending in the dashboard.
Use this template to validate that payment works **before launch** and to capture screenshot evidence.

## Run Context
- Product:
- Pricing page URL:
- Checkout provider(s): Stripe / Mercado Pago / Other
- Test date (UTC):
- Tester:

## Success Criteria (must all pass)
- [ ] User can start checkout from each active plan/tier CTA
- [ ] Correct plan name and amount are shown in checkout
- [ ] Coupon/launch discount applies correctly (if configured)
- [ ] Successful test payment reaches confirmation screen
- [ ] Purchase event is recorded (`checkout_start`, `purchase`)
- [ ] Webhook or fulfillment trigger runs (`checkout.session.completed` equivalent)
- [ ] Confirmation email/message is sent (if configured)

## Test Matrix

| Case ID | Scenario | Steps | Expected Result | Status (Pass/Fail) | Evidence |
|---|---|---|---|---|---|
| CF-01 | Tier CTA routes to checkout | Open pricing page, click Tier A CTA | Correct checkout opens for Tier A |  | Screenshot URL |
| CF-02 | Price integrity | Compare page price vs checkout price | Amount/currency match exactly |  | Screenshot URL |
| CF-03 | Coupon valid | Apply valid coupon code | Discount appears correctly |  | Screenshot URL |
| CF-04 | Coupon invalid | Apply invalid/expired code | Clear error message, no silent failure |  | Screenshot URL |
| CF-05 | Successful test payment | Complete checkout with test card/account | Confirmation page shown, transaction logged |  | Screenshot URL |
| CF-06 | Declined payment | Use declined card/test method | User sees actionable error, can retry |  | Screenshot URL |
| CF-07 | Interrupted checkout | Start checkout, close tab/back out, return | Session behavior is safe and clear |  | Screenshot URL |
| CF-08 | Terms + refund visibility | Verify links visible on pricing/checkout | Terms and refund links are present and working |  | Screenshot URL |
| CF-09 | Mobile checkout | Repeat CF-01/CF-05 on mobile viewport | Flow is usable and completes |  | Screenshot URL |
| CF-10 | Analytics + webhook verification | Validate dashboard/logs after CF-05 | Events/webhooks recorded with expected payload |  | Log link / screenshot |

## Test Data
- Valid payment method (sandbox/test):
- Declined payment method (sandbox/test):
- Valid coupon code:
- Invalid coupon code:
- Test account email:

## Evidence Checklist
- [ ] Pricing page CTA click screenshot for each tier
- [ ] Checkout page screenshot for each tier
- [ ] Successful payment confirmation screenshot
- [ ] Declined payment error screenshot
- [ ] Analytics event proof (`checkout_start`, `purchase`)
- [ ] Payment provider proof (dashboard event/transaction)
- [ ] Webhook fulfillment proof

## Defects / Notes
| ID | Severity | Description | Repro Steps | Owner | Status |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## Final Verdict
- Verdict: **GO / NO-GO**
- Blocking issues:
- Follow-up actions:
- Verified by:
- Verified at (UTC):
