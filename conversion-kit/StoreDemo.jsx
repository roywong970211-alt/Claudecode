/**
 * StoreDemo.jsx
 * ------------------------------------------------------------------
 * Reference store built from the actual IM8 mobile screenshots:
 * sticky offer bar -> good-better-best product carousel (Beckham Stack
 * flagged BEST VALUE) -> authority article. Prices use the observed
 * MYR localization. Swap data for your own product.
 * ------------------------------------------------------------------
 */

import React from "react";
import {
  StickyOfferBar,
  ProductCarousel,
  AuthorityArticleCard,
} from "./StoreBlocks";

export default function StoreDemo() {
  return (
    <main className="font-sans">
      <StickyOfferBar
        headline="SAVE 30% + GET FREE WELCOME GIFTS"
        subline="Free Shipping on All Subscriptions"
        ctaLabel="Shop Now"
      />

      <ProductCarousel
        products={[
          {
            eyebrow: "HEALTHY AGING",
            title: "Daily Ultimate Longevity",
            description: "10 clinically proven compounds in one drink to target all 12 hallmarks of aging.",
            image: { src: "/longevity.png", alt: "Daily Ultimate Longevity" },
            price: "From RM506.66 MYR",
            cadence: "/mo",
            discountLabel: "30% OFF",
            perUnit: "RM16.89 MYR/serving",
            benefits: [
              "Only supplement targeting every aging hallmark", // differentiation
              "Restore cellular energy and activate autophagy",  // mechanism/benefit
              "NSF Certified for Sport",                          // certification
              "90-day money-back guarantee",                      // risk reversal
            ],
            ctaLabel: "Add to Cart",
          },
          {
            eyebrow: "ALL-IN-ONE DAILY SUPPLEMENT",
            title: "Daily Ultimate Essentials Pro",
            description: "90 ingredients in one daily drink. Co-founded by David Beckham and developed with a world-class scientific advisory team.",
            image: { src: "/essentials-pro.png", alt: "Daily Ultimate Essentials Pro" },
            price: "From RM395.33 MYR",
            cadence: "/mo",
            discountLabel: "30% OFF",
            perUnit: "RM13.18 MYR/serving",
            benefits: [
              "Replaces 16 supplements",                                  // anchor
              "95% felt more energy. 85% better digestion. 80% improved sleep.", // quantified outcome
              "NSF Certified for Sport",                                   // certification
              "90-day money-back guarantee",                               // risk reversal
            ],
            ctaLabel: "Add to Cart",
          },
          {
            bestValue: true,
            bestValueLabel: "BEST VALUE — DAVID'S DAILY RITUAL",
            eyebrow: "ESSENTIALS PRO + LONGEVITY SET",
            title: "The Beckham Stack",
            description: "90 ingredients + 10 longevity compounds in one daily ritual. Co-founded by David Beckham and developed with a world-class scientific advisory team.",
            image: { src: "/beckham-stack.png", alt: "The Beckham Stack" },
            price: "From RM901.33 MYR",
            cadence: "/mo",
            discountLabel: "30% OFF",
            perUnit: "RM30.04 MYR/serving",
            benefits: [
              "The complete daily system — nutrition today, longevity tomorrow",
              "90-day money-back guarantee",
              "NSF Certified for Sport",
              "Replaces $4,000+/year in supplements for $6 a day", // the strongest anchor on the flagship tier
            ],
            ctaLabel: "Add to Cart",
          },
        ]}
      />

      <div className="bg-white py-10">
        <AuthorityArticleCard
          tag="WELLNESS"
          image={{ src: "/doctor.png", alt: "Cardiologist" }}
          title="Mastering Heart Health: My Journey to Revolutionizing Cardiovascular Wellness"
          ctaLabel="Read More"
        />
      </div>
    </main>
  );
}
