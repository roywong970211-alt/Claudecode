/**
 * StoreBlocks.jsx
 * ------------------------------------------------------------------
 * Store / collection-level blocks distilled from the REAL IM8 mobile
 * screenshots (product cards, good-better-best carousel, sticky offer
 * bar, authority article card). Pairs with ConversionKit.jsx.
 *
 * Every pattern here was observed on im8health.com mobile:
 *   - dual trust-badge bar with "without compensation" micro-copy
 *   - big price -> 30% OFF pill -> per-serving reframe
 *   - benefit "pills" mixing 4 jobs (differentiation/outcome/cert/risk)
 *   - localized currency
 *   - BEST VALUE highlighted tier with founder lifestyle image
 *   - sticky "SAVE 30% + FREE GIFTS" header with persistent CTA
 *
 * Stack: React + Tailwind. Brand accent defaults to maroon/red like IM8.
 * ------------------------------------------------------------------
 */

import React from "react";

const cx = (...c) => c.filter(Boolean).join(" ");

/* ----------------------------------------------------------------- */
/* formatPrice — localized currency, the way IM8 geo-prices in MYR.   */
/* ----------------------------------------------------------------- */
export function formatPrice(amount, { currency = "USD", locale = "en-US" } = {}) {
  return new Intl.NumberFormat(locale, { style: "currency", currency }).format(amount);
}

/* ----------------------------------------------------------------- */
/* StickyOfferBar                                                    */
/* Job: keep the offer + a CTA on screen at all times (observed       */
/* pinned to top inside the IG in-app browser).                       */
/* ----------------------------------------------------------------- */
export function StickyOfferBar({
  headline = "SAVE 30% + GET FREE WELCOME GIFTS",
  subline = "Free Shipping on All Subscriptions",
  ctaLabel = "SHOP NOW",
  ctaHref = "#offer",
  className,
}) {
  return (
    <div className={cx("sticky top-0 z-50 bg-red-900 text-white", className)}>
      <div className="mx-auto flex max-w-3xl items-center justify-between gap-3 px-4 py-3">
        <div className="min-w-0">
          <p className="truncate text-xs font-bold uppercase tracking-widest text-amber-300">
            {headline}
          </p>
          <p className="truncate text-xs text-red-100">{subline}</p>
        </div>
        <a
          href={ctaHref}
          className="shrink-0 rounded-full bg-red-600 px-5 py-2 text-sm font-bold uppercase tracking-wide text-white"
        >
          {ctaLabel} →
        </a>
      </div>
    </div>
  );
}

/* ----------------------------------------------------------------- */
/* TrustBadgeBar — the dual badge row sitting ON the product image.   */
/* The `clinicianNote` carries the "without compensation" micro-copy  */
/* that neutralizes the paid-endorsement objection.                   */
/* ----------------------------------------------------------------- */
export function TrustBadgeBar({
  clinicianLabel = "Clinicians' Choice",
  clinicianNote = "Hundreds of clinicians shared this with their patients without compensation.",
  certLabel = "NSF Certified for Sport",
  className,
}) {
  return (
    <div className={cx("flex items-start justify-between gap-2 p-3", className)}>
      <div className="flex max-w-[60%] items-start gap-2 rounded-lg bg-white/80 px-2 py-1 backdrop-blur">
        <span className="text-xs font-bold text-neutral-800">❦ {clinicianLabel}</span>
        <span className="text-[10px] leading-tight text-neutral-500">{clinicianNote}</span>
      </div>
      <span className="rounded bg-red-900 px-2 py-1 text-[10px] font-bold uppercase leading-tight text-white">
        {certLabel}
      </span>
    </div>
  );
}

/* ----------------------------------------------------------------- */
/* PriceBlock — big price, 30% OFF pill, then per-serving reframe.     */
/* This exact stack (total -> discount -> per-unit) is the IM8 move.   */
/* ----------------------------------------------------------------- */
export function PriceBlock({ price, cadence = "/mo", discountLabel, perUnit, className }) {
  return (
    <div className={className}>
      <div className="text-5xl font-bold leading-none text-red-900">{price}</div>
      <div className="mt-3 flex items-center gap-3">
        <span className="text-neutral-500">{cadence}</span>
        {discountLabel && (
          <span className="rounded-full bg-amber-300/70 px-3 py-1 text-sm font-extrabold uppercase text-amber-900">
            {discountLabel}
          </span>
        )}
      </div>
      {perUnit && <p className="mt-2 text-neutral-600">= {perUnit}</p>}
    </div>
  );
}

/* ----------------------------------------------------------------- */
/* BenefitPills — outlined pills with a check. Pass a MIX of jobs:     */
/* differentiation, quantified outcome, certification, risk-reversal.  */
/* ----------------------------------------------------------------- */
export function BenefitPills({ items = [], className }) {
  return (
    <ul className={cx("space-y-3", className)}>
      {items.map((text, i) => (
        <li
          key={i}
          className="flex items-start gap-3 rounded-2xl border border-neutral-200 px-4 py-3"
        >
          <span className="mt-0.5 text-red-700">✓</span>
          <span className="font-semibold text-red-900">{text}</span>
        </li>
      ))}
    </ul>
  );
}

/* ----------------------------------------------------------------- */
/* ProductCard — the self-contained "card = sales page" unit.         */
/* Set `bestValue` to give it the premium frame + crown banner and a   */
/* founder/lifestyle image, exactly like the Beckham Stack.            */
/* ----------------------------------------------------------------- */
export function ProductCard({
  eyebrow,            // "ALL-IN-ONE DAILY SUPPLEMENT"
  title,              // "Daily Ultimate Essentials Pro"
  description,        // founder + science line
  image,              // { src, alt }
  badges = true,      // show TrustBadgeBar
  price,              // pass-through to PriceBlock
  cadence,
  discountLabel,
  perUnit,
  benefits = [],      // mix of 4 job types
  bestValue = false,
  bestValueLabel = "BEST VALUE — DAVID'S DAILY RITUAL",
  ctaLabel = "Add to Cart",
  ctaHref = "#",
  className,
}) {
  return (
    <article
      className={cx(
        "flex w-full shrink-0 flex-col overflow-hidden rounded-3xl bg-white",
        bestValue ? "border-4 border-red-900" : "border border-neutral-200",
        className
      )}
    >
      {bestValue && (
        <div className="bg-red-900 py-2 text-center text-sm font-bold uppercase tracking-wide text-amber-300">
          ★ {bestValueLabel}
        </div>
      )}

      <div className="relative bg-gradient-to-b from-orange-100 to-red-100">
        {badges && <TrustBadgeBar className="absolute inset-x-0 top-0" />}
        {image && <img src={image.src} alt={image.alt} className="w-full object-contain p-6 pt-16" />}
      </div>

      <div className="flex flex-1 flex-col p-6">
        {eyebrow && (
          <p className="text-xs font-bold uppercase tracking-widest text-red-800">{eyebrow}</p>
        )}
        <h3 className="mt-1 font-serif text-3xl font-bold text-red-900">{title}</h3>
        {description && <p className="mt-2 text-neutral-700">{description}</p>}

        <hr className="my-5 border-neutral-200" />

        <PriceBlock
          price={price}
          cadence={cadence}
          discountLabel={discountLabel}
          perUnit={perUnit}
        />

        <BenefitPills items={benefits} className="mt-6" />

        <a
          href={ctaHref}
          className="mt-6 block rounded-full bg-red-700 px-6 py-4 text-center text-lg font-bold uppercase tracking-wide text-white transition hover:bg-red-800"
        >
          {ctaLabel}
        </a>
      </div>
    </article>
  );
}

/* ----------------------------------------------------------------- */
/* ProductCarousel — horizontal scroll-snap of ProductCards.          */
/* Order them good-better-best and flag the bundle as bestValue so the */
/* premium tier anchors the others (observed swipe layout).            */
/* ----------------------------------------------------------------- */
export function ProductCarousel({ products = [], className }) {
  return (
    <section className={cx("bg-neutral-50 py-8", className)}>
      <div className="flex snap-x snap-mandatory gap-4 overflow-x-auto px-4 pb-4 [scrollbar-width:none]">
        {products.map((p, i) => (
          <ProductCard
            key={i}
            {...p}
            className="max-w-sm snap-center md:max-w-md"
          />
        ))}
      </div>
    </section>
  );
}

/* ----------------------------------------------------------------- */
/* AuthorityArticleCard — store-as-magazine. Doctor-bylined editorial  */
/* that builds E-E-A-T and keeps the visitor on-site as a reader.      */
/* ----------------------------------------------------------------- */
export function AuthorityArticleCard({
  tag = "WELLNESS",
  image,              // doctor/expert portrait { src, alt }
  title,
  ctaLabel = "Read More",
  ctaHref = "#",
  className,
}) {
  return (
    <article className={cx("mx-auto max-w-md overflow-hidden rounded-3xl bg-red-50", className)}>
      <div className="relative">
        {image && <img src={image.src} alt={image.alt} className="w-full object-cover" />}
        <span className="absolute left-4 top-4 rounded-full bg-white px-3 py-1 text-xs font-bold uppercase tracking-widest text-neutral-700">
          {tag}
        </span>
      </div>
      <div className="p-6">
        <h3 className="font-serif text-2xl font-bold text-red-900">{title}</h3>
        <a
          href={ctaHref}
          className="mt-5 block rounded-full bg-red-700 px-6 py-3 text-center font-bold uppercase tracking-wide text-white"
        >
          {ctaLabel}
        </a>
      </div>
    </article>
  );
}
