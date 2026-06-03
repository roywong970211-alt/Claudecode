/**
 * DemoLandingPage.jsx
 * ------------------------------------------------------------------
 * Reference implementation: every ConversionKit block wired together
 * in the recommended order, with placeholder copy modeled on the IM8
 * teardown. Swap the data objects below for your own product — the
 * components don't change.
 * ------------------------------------------------------------------
 */

import React from "react";
import {
  AnnouncementBar,
  Hero,
  ProblemSection,
  PromiseSection,
  FeatureProof,
  HowItWorks,
  TrustWall,
  SocialProof,
  PricingOffer,
  Guarantee,
  FAQ,
  FinalCTA,
} from "./ConversionKit";

export default function DemoLandingPage() {
  return (
    <main className="font-sans text-neutral-900">
      <AnnouncementBar
        items={[
          "Free shipping on subscriptions",
          "90-day money-back guarantee",
          "Cancel anytime — one click",
        ]}
      />

      <Hero
        authorityLine="Co-founded with experts from leading research institutions"
        headline="90 Nutrients in One Delicious Daily Drink"
        subheadline="Replace a shelf full of pills with a single scoop. Clinically dosed, third-party tested, and built to simplify your routine."
        rating={{ stars: 4.8, count: "12,000+" }}
        ctaLabel="Shop Now"
        ctaHref="#offer"
        image={{ src: "/hero-product.png", alt: "Product pack shot" }}
      />

      <ProblemSection
        eyebrow="The problem"
        headline="The average optimizer takes 16 supplements a day"
        painPoints={[
          "$4,000+ a year spent across a dozen bottles",
          "Most are under-dosed below clinical levels",
          "No idea which ones actually work together",
          "A cluttered shelf you forget to use anyway",
        ]}
      />

      <PromiseSection
        headline="One scoop. Everything you need. Nothing you don't."
        body="We combined 90 nutrient-rich ingredients at clinical dosages into one great-tasting daily drink — for about the price of a coffee."
        highlights={["Vitamins & minerals", "Pre/pro/post-biotics", "CoQ10 + MSM", "Greens & antioxidants"]}
      />

      <FeatureProof
        headline="Specifics matter. Here's exactly what's inside."
        features={[
          { name: "CoQ10", detail: "Clinical 100mg dose", benefit: "Cellular energy production and heart support." },
          { name: "CRT8™ Complex", detail: "Proprietary blend", benefit: "Our signature longevity stack you won't find elsewhere." },
          { name: "Vitamin B12", detail: "200mcg Methylcobalamin", benefit: "Bioactive form for energy and focus." },
        ]}
      />

      <HowItWorks
        steps={[
          { title: "Scoop", body: "One serving of powder." },
          { title: "Add water", body: "8–12oz of water or your favorite smoothie." },
          { title: "Done", body: "Drink daily — that's the whole routine." },
        ]}
      />

      <TrustWall
        headline="Tested. Certified. Transparent."
        badges={[{ label: "NSF Certified for Sport" }, { label: "3rd-Party Tested" }, { label: "Vegan" }, { label: "Gluten-Free" }]}
        statement="Every ingredient and dosage is independently lab-tested. What's on the label is what's in the tub — no proprietary fairy dust."
      />

      <SocialProof
        headline="Loved by thousands"
        rating={{ stars: 4.8, count: "12,000+" }}
        testimonials={[
          { quote: "More energy by week two and my shelf is finally empty.", author: "Jordan M.", detail: "Verified buyer" },
          { quote: "Tastes great and replaced six different bottles.", author: "Priya S.", detail: "Verified buyer" },
          { quote: "The only supplement I've actually stuck with.", author: "Marcus T.", detail: "Verified buyer" },
        ]}
      />

      <PricingOffer
        headline="Choose your plan"
        anchor="Replaces 16 supplements & $4,000+/yr — for about $6/day"
        plans={[
          {
            name: "Subscribe & Save",
            price: "$79",
            suffix: "/mo",
            perUnit: "$2.63 / serving · 20% off",
            recommended: true,
            badge: "Most popular",
            bonuses: [
              "Free shipping",
              "Welcome kit + signature cup ($28 value)",
              "5 travel sachets ($18 value)",
              "Cancel anytime, one click",
            ],
            ctaLabel: "Start subscription",
            ctaHref: "/checkout?plan=sub",
          },
          {
            name: "One-time purchase",
            price: "$99",
            perUnit: "$3.30 / serving",
            bonuses: ["30 servings", "Ships once"],
            ctaLabel: "Buy once",
            ctaHref: "/checkout?plan=once",
          },
        ]}
      />

      <Guarantee
        badge="90-DAY"
        headline="Love it or your money back"
        body="Try it risk-free. If you don't feel the difference within 90 days, we'll refund you in full — keep the cup."
      />

      <FAQ
        items={[
          { q: "How do I take it?", a: "Mix one scoop with 8–12oz of water or a smoothie, once daily." },
          { q: "Can I cancel my subscription?", a: "Yes — anytime, in one click, with no penalties." },
          { q: "Is it third-party tested?", a: "Every batch is independently lab-tested for purity and potency." },
          { q: "When will I see results?", a: "Most customers report more energy and better digestion within 2–3 weeks." },
        ]}
      />

      <FinalCTA
        headline="Simplify your health in one scoop"
        body="Join thousands who replaced the shelf with a single daily drink."
        ctaLabel="Get started"
        ctaHref="#offer"
      />
    </main>
  );
}
