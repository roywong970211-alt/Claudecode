# Observed Lessons → Application

Distilled from the actual IM8 Health mobile screenshots. Each observed
tactic is mapped to the component/prop that implements it, so you can apply
it directly.

## 1. The product card IS a sales page
Every card carries badges, price, proof, and CTA — a shopper can convert
without scrolling further.
→ `ProductCard` (StoreBlocks.jsx)

## 2. Dual trust-badge bar with anti-shill micro-copy
"Clinicians' Choice — *shared with patients without compensation*" + NSF.
The "without compensation" line kills the paid-endorsement objection.
→ `TrustBadgeBar` (`clinicianNote` prop)

## 3. Price stack: total → discount → per-serving
Big `From RM506.66 /mo` + gold `30% OFF` pill + `= RM16.89/serving`.
Show the scary number and the comforting number together.
→ `PriceBlock` (`price` / `discountLabel` / `perUnit`)

## 4. Benefit pills = a MIX of 4 jobs, not a feature list
① differentiation ② quantified outcome ("95% felt more energy…")
③ certification ④ risk reversal. One of each.
→ `BenefitPills` — order your `benefits` array as the 4 jobs.

## 5. Localized currency
Geo-priced in MYR for a Malaysian viewer → relevance + trust.
→ `formatPrice(amount, { currency, locale })`

## 6. Good-Better-Best laddering with a flagged hero tier
Longevity → Essentials Pro → **Beckham Stack** (bundle). The bundle gets a
premium frame + "BEST VALUE" crown + founder photo + the strongest anchor
("Replaces $4,000+/year for $6 a day"). The bundle anchors the singles.
→ `ProductCarousel` + `ProductCard bestValue`

## 7. Founder as proof, in lifestyle context
Beckham in an aspirational kitchen with the product = "he actually uses it."
→ `ProductCard image` on the bestValue tier (lifestyle, not pack shot).

## 8. Sticky offer bar with a persistent CTA
"SAVE 30% + FREE WELCOME GIFTS / Free Shipping" + SHOP NOW, pinned on screen.
→ `StickyOfferBar`

## 9. Frictionless buying + steer to high AOV
"ADD TO CART" on the grid itself; bundle wears a "BEST VALUE" badge to pull
the eye to the highest cart value.
→ `ProductCard ctaLabel="Add to Cart"`, `bestValue` highlight.

## 10. Tags sell emotion, not category
"STAY YOUNG TOMORROW", "THE ULTIMATE DAILY RITUAL" — never "Supplement."
→ `ProductCard eyebrow` — write the outcome, not the SKU type.

## 11. Store blended with a magazine (E-E-A-T)
Doctor-bylined editorial keeps the visitor on-site as a reader and borrows
medical authority.
→ `AuthorityArticleCard`

## 12. Funnel = paid IG ad → in-app browser → mobile card
The URL chrome read "im8health.com — Instagram." Everything is designed
mobile-first for that single-thumb path. Keep cards full-width, CTAs large,
price reframing immediate.

## Craft notes (visual)
- Maroon serif headlines = heritage / medical-journal authority; sans body.
- Warm orange = energy/longevity; deep red = premium. (Tailwind `red-900`,
  `orange-100` gradients used in `ProductCard`.)
- Persistent live-chat bubble defuses last-second purchase anxiety.
