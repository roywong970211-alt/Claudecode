# HealWithRoy Carousel — Layout Library

Named slide compositions, all in Roy's house visual language (teal + ink on light page, rounded
cards, pill tags, flag callouts). Each maps to a format Roy already uses. Every layout corresponds
to a CSS class in `templates/slide-base.html`. Keep the layout identical across slides within one
carousel unless a slide is deliberately breaking the pattern for the payoff.

Canvas is always 1080×1350. Safe margin: keep text inside a 72px inset on all sides.

---

## Covers (slide 01 — must stop the scroll)

### `cover-hook` — deep-teal gradient hook
Full-bleed `#0e7c6b → #0a5c50` gradient, white text. Large hook (name the condition/treatment/
scenario in line one), small kicker label above it (e.g. "SLIP DISC"), swipe cue bottom-right,
`@healwithroy` bottom-left. Use for mechanism, myth, and value carousels.

### `cover-quote` — problem-statement cover (maps to C5 energy)
The thing people say, in quotation marks, large and white on teal gradient ("Back pain is just
old age."). Sets up a reframe the interior slides deliver. Swipe cue + handle.

---

## Interior layouts

### `mechanism` — one-idea explainer (maps to the proven script spine)
Light page. A short teal eyebrow label, one bold statement (the single idea for this slide), one
short supporting line in muted ink. Optional blue `flag` callout for a mechanism note
("the disc is 80% water, almost no blood supply"). Use across a Hook → Agitate → Mechanism →
Reframe → CTA sequence, one beat per slide.

### `numbered-list` — numbered point (maps to B1)
Big teal number (01, 02, …) top-left, bold one-line point, one supporting line. Identical template
every slide. Home of the nutrition–spine bridge and "N things nobody talks about" value posts.
Strongest point first or last.

### `action-result` — split action / result (maps to B4)
Card split top/bottom. Top = the action taken (amber eyebrow "DO THIS"), bottom = the result
(green eyebrow "WHAT HAPPENS"). Each slide raises the stakes. Final slide breaks the pattern to
deliver the payoff or the thesis.

### `assumption-reframe` — assumption / hidden story (maps to C4)
Two stacked cards. Top (muted/red eyebrow) = the assumption people hold
("Surgery fixed it, so I'm done."). Bottom (teal eyebrow) = the reframe that recontextualises it,
not just explains. 5–8 of these; final slide = the larger truth (environment, not symptom).

### `myth-fix` — myth-busting (maps to myth pillar)
Top red `flag` = the popular fix in quotes ("Just rest until it heals."). Middle = why it feels
right short-term (muted). Bottom green `flag` = what actually changes the environment. One myth per slide.

### `before-after` — transformation / proof (maps to B5 / proof pillar)
Two labelled halves — red-tinted "BEFORE" and green-tinted "AFTER". Payoff is **function regained**
("can carry her grandchild again"), never a cure claim. Space for a photo or a client-message
screenshot. Must have permission.

### `stat` — single number
One large teal number/stat centred, one line of context below, source/qualifier in muted. For a
disc-hydration %, a timeframe, a "9 hours sitting" style data point. Don't overfill.

---

## Closing layouts (last slide)

### `cta-keyword` — the DM ask (hard CTA, ~6–7 of 10 posts)
Deep-teal gradient again to bookend the cover. One keyword big and clear
(`DISC` / `SPINE` / `NECK` / `SCIATICA`) → "comment it for a free 1-on-1 spine recovery assessment"
→ geo line 🇲🇾🇸🇬🇧🇳🇦🇺. `@healwithroy`.

### `cta-follow` — soft close (proof / myth posts)
"Follow for part 2" or "save this for your next flare-up." Teal accent, handle. Use to balance
reach vs. conversion when a hard CTA would be too much.

---

## Choosing a layout (quick router)

| Carousel intent | Cover | Interior | Close |
|---|---|---|---|
| Mechanism explainer | `cover-hook` | `mechanism` | `cta-keyword` |
| Nutrition–spine / value list | `cover-hook` | `numbered-list` | `cta-keyword` |
| Myth-busting | `cover-quote` | `myth-fix` | `cta-follow` |
| Client transformation | `cover-hook` | `before-after` + `action-result` | `cta-keyword` |
| "Things people assume" | `cover-quote` | `assumption-reframe` | `cta-follow` |

One idea per slide. Lowest-complexity layout that still does the job. Keep the template identical
within a carousel; break it only for a deliberate payoff slide.
