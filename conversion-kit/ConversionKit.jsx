/**
 * ConversionKit.jsx
 * ------------------------------------------------------------------
 * A reusable, props-driven set of landing-page blocks distilled from
 * the IM8 Health teardown. Each component encodes ONE persuasion job
 * and is fully configurable via props, so you can rebuild a
 * high-ticket DTC landing page for any product.
 *
 * Stack: React + Tailwind CSS (no other UI deps).
 * Order of components below === recommended top-to-bottom page order.
 *
 * Conversion logic encoded in the sequence:
 *   Authority -> Problem -> Promise -> Proof -> Ease -> Trust
 *   -> Social proof -> Offer (price LAST) -> Risk reversal -> FAQ -> Close
 * ------------------------------------------------------------------
 */

import React, { useState } from "react";

/* Tiny helper so consumers can override / merge Tailwind classes. */
const cx = (...c) => c.filter(Boolean).join(" ");

/* ----------------------------------------------------------------- */
/* 1. AnnouncementBar                                                */
/* Job: remove risk + state the offer before the user even scrolls.  */
/* ----------------------------------------------------------------- */
export function AnnouncementBar({ items = [], className }) {
  if (!items.length) return null;
  return (
    <div className={cx("w-full bg-neutral-900 text-white text-sm", className)}>
      <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-center gap-x-8 gap-y-1 px-4 py-2 text-center">
        {items.map((item, i) => (
          <span key={i} className="font-medium tracking-wide">
            {item}
          </span>
        ))}
      </div>
    </div>
  );
}

/* ----------------------------------------------------------------- */
/* 2. Hero                                                            */
/* Job: borrow authority + state outcome in <2s. Rating = social     */
/* proof above the fold. CTA scrolls to the offer.                   */
/* ----------------------------------------------------------------- */
export function Hero({
  authorityLine,      // e.g. "Co-Founded by David Beckham + experts from Mayo Clinic & NASA"
  headline,           // outcome-led, e.g. "90 Nutrients in One Delicious Drink"
  subheadline,
  rating,             // { stars: 4.8, count: "12,000+" }
  ctaLabel = "Shop Now",
  ctaHref = "#offer",
  image,              // { src, alt }
  className,
}) {
  return (
    <section className={cx("bg-neutral-50", className)}>
      <div className="mx-auto grid max-w-6xl items-center gap-10 px-4 py-16 md:grid-cols-2">
        <div>
          {authorityLine && (
            <p className="mb-3 text-xs font-semibold uppercase tracking-widest text-emerald-700">
              {authorityLine}
            </p>
          )}
          <h1 className="text-4xl font-bold leading-tight text-neutral-900 md:text-5xl">
            {headline}
          </h1>
          {subheadline && (
            <p className="mt-4 max-w-prose text-lg text-neutral-600">{subheadline}</p>
          )}
          {rating && <StarRating {...rating} className="mt-5" />}
          <a
            href={ctaHref}
            className="mt-7 inline-block rounded-full bg-emerald-600 px-8 py-4 text-base font-semibold text-white shadow-sm transition hover:bg-emerald-700"
          >
            {ctaLabel}
          </a>
        </div>
        {image && (
          <img
            src={image.src}
            alt={image.alt}
            className="mx-auto w-full max-w-md rounded-2xl object-cover"
          />
        )}
      </div>
    </section>
  );
}

/* Reusable star rating, used in Hero and SocialProof. */
export function StarRating({ stars = 5, count, className }) {
  const full = Math.round(stars);
  return (
    <div className={cx("flex items-center gap-2", className)}>
      <span className="text-amber-500" aria-hidden>
        {"★".repeat(full)}
        <span className="text-neutral-300">{"★".repeat(5 - full)}</span>
      </span>
      <span className="text-sm text-neutral-600">
        <strong className="text-neutral-900">{stars}</strong>
        {count && <> · {count} reviews</>}
      </span>
    </div>
  );
}

/* ----------------------------------------------------------------- */
/* 3. ProblemSection (PAS: Problem + Agitate)                        */
/* Job: agitate the pain so the promise feels like relief.           */
/* ----------------------------------------------------------------- */
export function ProblemSection({ eyebrow, headline, painPoints = [], className }) {
  return (
    <section className={cx("bg-white", className)}>
      <div className="mx-auto max-w-4xl px-4 py-16 text-center">
        {eyebrow && (
          <p className="mb-2 text-xs font-semibold uppercase tracking-widest text-neutral-400">
            {eyebrow}
          </p>
        )}
        <h2 className="text-3xl font-bold text-neutral-900">{headline}</h2>
        <ul className="mt-8 grid gap-4 text-left sm:grid-cols-2">
          {painPoints.map((p, i) => (
            <li key={i} className="flex gap-3 rounded-xl bg-neutral-50 p-4">
              <span className="text-red-500">✕</span>
              <span className="text-neutral-700">{p}</span>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}

/* ----------------------------------------------------------------- */
/* 4. PromiseSection (PAS: Solve)                                    */
/* Job: collapse the problem into one simple dream outcome.          */
/* ----------------------------------------------------------------- */
export function PromiseSection({ headline, body, highlights = [], className }) {
  return (
    <section className={cx("bg-emerald-50", className)}>
      <div className="mx-auto max-w-4xl px-4 py-16 text-center">
        <h2 className="text-3xl font-bold text-neutral-900">{headline}</h2>
        {body && <p className="mx-auto mt-4 max-w-prose text-lg text-neutral-600">{body}</p>}
        {highlights.length > 0 && (
          <div className="mt-8 flex flex-wrap justify-center gap-3">
            {highlights.map((h, i) => (
              <span
                key={i}
                className="rounded-full bg-white px-4 py-2 text-sm font-medium text-emerald-800 shadow-sm"
              >
                {h}
              </span>
            ))}
          </div>
        )}
      </div>
    </section>
  );
}

/* ----------------------------------------------------------------- */
/* 5. IngredientProof / FeatureProof (FAB: Feature->Advantage->Benefit)*/
/* Job: specificity = believability. Use exact numbers + ™ names.    */
/* ----------------------------------------------------------------- */
export function FeatureProof({ headline, features = [], className }) {
  // feature: { name, detail, benefit }
  return (
    <section className={cx("bg-white", className)}>
      <div className="mx-auto max-w-6xl px-4 py-16">
        <h2 className="text-center text-3xl font-bold text-neutral-900">{headline}</h2>
        <div className="mt-10 grid gap-6 md:grid-cols-3">
          {features.map((f, i) => (
            <div key={i} className="rounded-2xl border border-neutral-200 p-6">
              <h3 className="text-lg font-semibold text-neutral-900">{f.name}</h3>
              {f.detail && <p className="mt-1 text-sm font-medium text-emerald-700">{f.detail}</p>}
              {f.benefit && <p className="mt-3 text-neutral-600">{f.benefit}</p>}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ----------------------------------------------------------------- */
/* 6. HowItWorks                                                     */
/* Job: lower perceived effort to near zero (commitment rehearsal).  */
/* ----------------------------------------------------------------- */
export function HowItWorks({ headline = "How It Works", steps = [], className }) {
  return (
    <section className={cx("bg-neutral-50", className)}>
      <div className="mx-auto max-w-5xl px-4 py-16">
        <h2 className="text-center text-3xl font-bold text-neutral-900">{headline}</h2>
        <ol className="mt-10 grid gap-8 sm:grid-cols-3">
          {steps.map((s, i) => (
            <li key={i} className="text-center">
              <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-emerald-600 text-lg font-bold text-white">
                {i + 1}
              </div>
              <h3 className="mt-4 font-semibold text-neutral-900">{s.title}</h3>
              {s.body && <p className="mt-1 text-sm text-neutral-600">{s.body}</p>}
            </li>
          ))}
        </ol>
      </div>
    </section>
  );
}

/* ----------------------------------------------------------------- */
/* 7. TrustWall                                                      */
/* Job: outsource credibility via badges/certs at the doubt moment.  */
/* ----------------------------------------------------------------- */
export function TrustWall({ headline, badges = [], statement, className }) {
  // badge: { label, src? }
  return (
    <section className={cx("bg-white", className)}>
      <div className="mx-auto max-w-5xl px-4 py-14 text-center">
        {headline && <h2 className="text-2xl font-bold text-neutral-900">{headline}</h2>}
        <div className="mt-8 flex flex-wrap items-center justify-center gap-6">
          {badges.map((b, i) =>
            b.src ? (
              <img key={i} src={b.src} alt={b.label} className="h-14 w-auto" />
            ) : (
              <span
                key={i}
                className="rounded-lg border border-neutral-200 px-4 py-2 text-sm font-semibold text-neutral-700"
              >
                {b.label}
              </span>
            )
          )}
        </div>
        {statement && (
          <p className="mx-auto mt-6 max-w-prose text-neutral-600">{statement}</p>
        )}
      </div>
    </section>
  );
}

/* ----------------------------------------------------------------- */
/* 8. SocialProof                                                    */
/* Job: bandwagon — thousands already decided this is safe.          */
/* ----------------------------------------------------------------- */
export function SocialProof({ headline, rating, testimonials = [], className }) {
  // testimonial: { quote, author, detail? }
  return (
    <section className={cx("bg-neutral-50", className)}>
      <div className="mx-auto max-w-6xl px-4 py-16">
        <div className="text-center">
          <h2 className="text-3xl font-bold text-neutral-900">{headline}</h2>
          {rating && <StarRating {...rating} className="mt-4 justify-center" />}
        </div>
        <div className="mt-10 grid gap-6 md:grid-cols-3">
          {testimonials.map((t, i) => (
            <figure key={i} className="rounded-2xl bg-white p-6 shadow-sm">
              <div className="text-amber-500" aria-hidden>★★★★★</div>
              <blockquote className="mt-3 text-neutral-700">“{t.quote}”</blockquote>
              <figcaption className="mt-4 text-sm font-semibold text-neutral-900">
                {t.author}
                {t.detail && <span className="font-normal text-neutral-500"> · {t.detail}</span>}
              </figcaption>
            </figure>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ----------------------------------------------------------------- */
/* 9. PricingOffer                                                   */
/* Job: anchor value, default to subscription, stack physical bonuses*/
/* The recommended plan is highlighted; the other acts as a decoy.   */
/* ----------------------------------------------------------------- */
export function PricingOffer({
  id = "offer",
  headline,
  anchor,         // e.g. "Replaces 16 supplements & $4,000+/yr"
  plans = [],     // see plan shape below
  className,
}) {
  // plan: {
  //   name, price, suffix ("/mo"), perUnit ("$2.63/serving"),
  //   recommended?, badge?, bonuses: [string], ctaLabel, ctaHref
  // }
  return (
    <section id={id} className={cx("bg-white", className)}>
      <div className="mx-auto max-w-5xl px-4 py-16">
        <div className="text-center">
          <h2 className="text-3xl font-bold text-neutral-900">{headline}</h2>
          {anchor && (
            <p className="mt-3 inline-block rounded-full bg-amber-100 px-4 py-1 text-sm font-semibold text-amber-800">
              {anchor}
            </p>
          )}
        </div>
        <div className="mt-10 grid gap-6 md:grid-cols-2">
          {plans.map((plan, i) => (
            <div
              key={i}
              className={cx(
                "relative rounded-2xl border p-7",
                plan.recommended
                  ? "border-emerald-600 ring-2 ring-emerald-600 shadow-md"
                  : "border-neutral-200"
              )}
            >
              {plan.badge && (
                <span className="absolute -top-3 left-1/2 -translate-x-1/2 rounded-full bg-emerald-600 px-3 py-1 text-xs font-bold uppercase tracking-wide text-white">
                  {plan.badge}
                </span>
              )}
              <h3 className="text-lg font-semibold text-neutral-900">{plan.name}</h3>
              <div className="mt-3 flex items-baseline gap-1">
                <span className="text-4xl font-bold text-neutral-900">{plan.price}</span>
                {plan.suffix && <span className="text-neutral-500">{plan.suffix}</span>}
              </div>
              {plan.perUnit && (
                <p className="mt-1 text-sm text-neutral-500">{plan.perUnit}</p>
              )}
              {plan.bonuses?.length > 0 && (
                <ul className="mt-5 space-y-2">
                  {plan.bonuses.map((b, j) => (
                    <li key={j} className="flex gap-2 text-sm text-neutral-700">
                      <span className="text-emerald-600">✓</span>
                      {b}
                    </li>
                  ))}
                </ul>
              )}
              <a
                href={plan.ctaHref || "#"}
                className={cx(
                  "mt-7 block rounded-full px-6 py-3 text-center font-semibold transition",
                  plan.recommended
                    ? "bg-emerald-600 text-white hover:bg-emerald-700"
                    : "border border-neutral-300 text-neutral-800 hover:bg-neutral-50"
                )}
              >
                {plan.ctaLabel}
              </a>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ----------------------------------------------------------------- */
/* 10. Guarantee                                                     */
/* Job: reverse risk at the point of decision (loss aversion).       */
/* ----------------------------------------------------------------- */
export function Guarantee({ headline, body, badge = "100%", className }) {
  return (
    <section className={cx("bg-emerald-600 text-white", className)}>
      <div className="mx-auto flex max-w-4xl flex-col items-center gap-4 px-4 py-14 text-center">
        <div className="flex h-20 w-20 items-center justify-center rounded-full border-4 border-white text-xl font-bold">
          {badge}
        </div>
        <h2 className="text-2xl font-bold">{headline}</h2>
        {body && <p className="max-w-prose text-emerald-50">{body}</p>}
      </div>
    </section>
  );
}

/* ----------------------------------------------------------------- */
/* 11. FAQ (accordion)                                               */
/* Job: kill the last objections right before checkout.             */
/* ----------------------------------------------------------------- */
export function FAQ({ headline = "Frequently Asked Questions", items = [], className }) {
  const [open, setOpen] = useState(null);
  return (
    <section className={cx("bg-white", className)}>
      <div className="mx-auto max-w-3xl px-4 py-16">
        <h2 className="text-center text-3xl font-bold text-neutral-900">{headline}</h2>
        <dl className="mt-10 divide-y divide-neutral-200">
          {items.map((item, i) => (
            <div key={i} className="py-4">
              <dt>
                <button
                  onClick={() => setOpen(open === i ? null : i)}
                  className="flex w-full items-center justify-between text-left text-lg font-medium text-neutral-900"
                  aria-expanded={open === i}
                >
                  {item.q}
                  <span className="ml-4 text-emerald-600">{open === i ? "–" : "+"}</span>
                </button>
              </dt>
              {open === i && <dd className="mt-2 text-neutral-600">{item.a}</dd>}
            </div>
          ))}
        </dl>
      </div>
    </section>
  );
}

/* ----------------------------------------------------------------- */
/* 12. FinalCTA                                                      */
/* Job: emotional close + repeat the primary action.                */
/* ----------------------------------------------------------------- */
export function FinalCTA({ headline, body, ctaLabel = "Get Started", ctaHref = "#offer", className }) {
  return (
    <section className={cx("bg-neutral-900 text-white", className)}>
      <div className="mx-auto max-w-3xl px-4 py-20 text-center">
        <h2 className="text-3xl font-bold md:text-4xl">{headline}</h2>
        {body && <p className="mx-auto mt-4 max-w-prose text-neutral-300">{body}</p>}
        <a
          href={ctaHref}
          className="mt-8 inline-block rounded-full bg-emerald-600 px-10 py-4 text-lg font-semibold text-white transition hover:bg-emerald-700"
        >
          {ctaLabel}
        </a>
      </div>
    </section>
  );
}
