# Conversion Kit

Reusable React + Tailwind landing-page blocks, distilled from the **IM8 Health**
e-commerce teardown. Each component encodes **one persuasion job** and is fully
props-driven, so you can rebuild a high-ticket DTC landing page for any product
by swapping data — not code.

## Files

| File | What it is |
|---|---|
| `ConversionKit.jsx` | The component library — 12 blocks + `StarRating`, all exported. |
| `DemoLandingPage.jsx` | Reference page wiring every block in the recommended order. |

## Requirements

- React 17+
- Tailwind CSS (utility classes are used directly; no other UI deps)

If you don't use Tailwind, the class names are the only thing to swap — the
component structure and props stay the same.

## Usage

```jsx
import { Hero, PricingOffer } from "./ConversionKit";

<Hero
  authorityLine="Co-founded with experts from leading institutions"
  headline="90 Nutrients in One Daily Drink"
  rating={{ stars: 4.8, count: "12,000+" }}
  ctaLabel="Shop Now"
  ctaHref="#offer"
  image={{ src: "/hero.png", alt: "Product" }}
/>
```

See `DemoLandingPage.jsx` for a full, copy-pasteable example.

## The page order IS the psychology

The components are designed to be stacked in this sequence. Each block answers
the doubt the previous one raises, and **price comes last** — only after value
is stacked above it.

| # | Component | Persuasion job | Principle |
|---|---|---|---|
| 1 | `AnnouncementBar` | Remove risk + state offer before scroll | Risk reversal |
| 2 | `Hero` | Borrow authority + state outcome in <2s | Authority + Social proof |
| 3 | `ProblemSection` | Agitate the pain | PAS (Problem/Agitate) |
| 4 | `PromiseSection` | Collapse problem into one dream outcome | PAS (Solve) + Cognitive ease |
| 5 | `FeatureProof` | Specifics = believability | FAB + Authority |
| 6 | `HowItWorks` | Lower perceived effort to ~zero | Commitment rehearsal |
| 7 | `TrustWall` | Outsource credibility via certs | Authority |
| 8 | `SocialProof` | "Thousands already chose this" | Social proof / Bandwagon |
| 9 | `PricingOffer` | Anchor value, default to subscription, stack bonuses | Anchoring + Decoy + Reciprocity |
| 10 | `Guarantee` | Reverse risk at decision point | Loss aversion |
| 11 | `FAQ` | Kill last objections before checkout | Objection handling |
| 12 | `FinalCTA` | Emotional close + repeat CTA | Consistency |

## Key reusable patterns baked in

- **Anchor against the expensive alternative** — `PricingOffer.anchor`
  ("Replaces 16 supplements & $4,000+/yr").
- **Default-to-subscription with a decoy** — mark the recurring plan
  `recommended` and `badge`; the one-time plan exists to make it look smart.
- **Stack physical bonuses over deeper discounts** — `plan.bonuses` with
  dollar-valued freebies.
- **Reframe price per-day/serving** — `plan.perUnit` ("$2.63 / serving").
- **Sequence trust signals** to disarm doubts where they arise, not in the footer.

## Customizing

Every component accepts a `className` prop that merges with its defaults, so you
can override colors/spacing per use. To re-theme globally, change the
`emerald-600` / `neutral-900` accent classes in `ConversionKit.jsx`.
