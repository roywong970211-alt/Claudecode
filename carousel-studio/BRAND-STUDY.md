# @healwithroy — Brand Identity Study (for carousels)

This file is the **analysis** behind the carousel system. It studies Roy's existing
brand — as encoded in his `healwithroy-content`, `true-heal-story-content`,
`healwithroy-client-plan` and `roy-recruitment-story-content` skills — and distils the
parts a carousel must obey. `PROJECT-INSTRUCTIONS.md` turns this study into rules;
`LAYOUT-LIBRARY.md` turns it into slide compositions; `brand.json` turns it into tokens.

Nothing here is invented. It is pulled from the brand playbook already in use.

---

## 1. Who the brand is

- **Handle:** @healwithroy (TikTok + Instagram)
- **What:** spine-recovery coaching — slip disc, sciatica, cervical spondylosis, stenosis
- **Markets:** Malaysia, Singapore, Brunei, Australia (🇲🇾🇸🇬🇧🇳🇦🇺)
- **The one job of every post:** move a person in chronic spine pain from
  scrolling → trusting Roy → DMing a keyword → booking a free 1-on-1 spine recovery assessment.

## 2. Positioning (locked — a carousel must never drift from this)

**Roy helps people rebuild failing discs through nutrition + movement, without surgery.**
The nutrition × spine fusion is the differentiator — most spine creators ignore nutrition,
most nutritionists never touch spine conditions. Roy owns the overlap.

The brand thesis, which should surface in almost every carousel in some form:

> Pain relief (surgery, painkillers, massage) removes the *symptom*, but the *environment*
> that caused the disc to fail is still there. Fix the environment.
> "Environment" = load patterns, posture, inflammation, nutrition, sleep, movement.

Never position against doctors. Position against **incomplete treatment**: doctors fix the
emergency, Roy fixes the environment so it doesn't come back.

## 3. Audience (decides the hook scenario)

- **Primary ~60%:** 50+ post-surgery or surgery-scheduled. Drivers: fear of relapse, fear of
  the knife, "nobody explained why this happened". Speak plainly, no fitness-bro jargon.
- **Secondary ~40%:** 35–55 desk workers in MY/SG. Early-stage disc issues, numbness, sciatica.
  Driver: "I don't want to end up like my uncle who had surgery twice."

Same mechanism-first style for both; only the hook scenario changes
(post-surgery relapse vs. sitting-all-day office worker).

## 4. Voice (decides the copy on every slide)

Calm authority. A trusted friend who happens to know spines — direct, plain-language,
slightly contrarian, never hype.

- Short sentences. Concrete anatomy ("the disc pressing on the nerve") over vague wellness
  talk ("your body's energy").
- No shouting, no "SECRET DOCTORS DON'T WANT YOU TO KNOW", no emoji walls.
- One idea per slide. Bigger type, fewer words.
- 90% English, 10% conversational Malay (bahasa pasar, not formal BM).

## 5. Compliance guardrails (non-negotiable on every slide)

- Never claim to **cure, reverse, or replace surgery**. Use "recovery environment",
  "support healing", "reduce the load that caused the failure".
- **Cauda equina is a surgical emergency** — any mention of red-flag symptoms (saddle numbness,
  bladder/bowel changes) must say "see a doctor immediately".
- No "throw away your painkillers / cancel your surgery". Instead: "ask your surgeon what
  happens to the environment after the operation".
- Testimonials: real, with permission, framed as individual results.
- Free assessment is an **assessment, not a diagnosis**. Roy is a coach/nutritionist, not a physician.

If a requested carousel would break these, flag it and offer the compliant version of the same idea.

## 6. Visual identity (pulled from the HealWithRoy care-plan template)

The existing `plan-template.html` already defines Roy's house visual language. The carousel
system reuses the same tokens so posts, DMs and plans all look like one brand.

| Token | Value | Use |
|---|---|---|
| Brand teal | `#0e7c6b` | primary accent, keywords, underlines |
| Brand teal (deep) | `#0a5c50` | headers, CTA blocks, gradients |
| Ink | `#1f2937` | body text |
| Muted | `#6b7280` | captions, labels |
| Line | `#e5e7eb` | hairlines, card borders |
| Surface | `#ffffff` | cards |
| Page | `#f4f6f8` | light background |
| Semantic — green | `#2e7d32` on `#eaf6ea` | fine / OK / "after" |
| Semantic — amber | `#b26a00` on `#fff6e6` | watch / depends |
| Semantic — red | `#c62828` on `#fdecec` | alarm / "before" / myth |
| Semantic — blue | `#1565c0` on `#e9f2fc` | info / mechanism note |

Form language from the same template: rounded cards (14–16px radius), a teal
`135deg` gradient header block, pill tags, left-border "flag" callouts, soft shadows,
a system sans stack. Calm, clinical-but-warm, never flashy.

**Carousel-specific additions** (consistent with, not contradicting, the above):
- Canvas: **1080 × 1350** (Instagram 4:5), the size Instagram wants.
- Dark cover option: deep-teal gradient background with white text, for the hook slide,
  so the cover stops the scroll; interior slides stay on the light `#f4f6f8` page.
- One display weight, one body weight. Keyword + geo line always teal.

## 7. How the existing story skills map to carousels

Roy's content playbook already names three carousel formats in its format router. The layout
library is built directly on them:

- **B1 Numbered List Carousel** → `numbered-list` layout. Home of the nutrition–spine bridge
  and "N things nobody talks about" value posts.
- **B4 Split-Screen Carousel (action / result)** → `action-result` layout. Chains of
  action → result, each slide raising the stakes.
- **C4 Split-Screen Carousel (assumption / hidden story)** → `assumption-reframe` layout.
  5–8 assumptions people hold, each reframed, final slide the larger truth.
- Mechanism explainers (the proven "surgery removed the pain, 2 years later same disc" format)
  → `mechanism` layout, following the playbook script spine:
  **Hook → Agitate → Mechanism (one idea) → Reframe (environment, not symptom) → CTA.**

## 8. CTA system (the last slide earns the DM)

- **One keyword per carousel**, matched to the condition: `DISC`, `SPINE`, `NECK`, `SCIATICA`.
- Closing slide: keyword in a comment/DM → free 1-on-1 spine recovery assessment → geo line
  🇲🇾🇸🇬🇧🇳🇦🇺.
- Roughly 6–7 of 10 posts carry a hard CTA; proof and myth posts may close on "follow for part 2"
  to balance reach vs. conversion.
