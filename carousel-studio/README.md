# HealWithRoy Carousel Studio

A carousel design system built from Roy's **existing** brand identity (the `healwithroy-content`,
`true-heal-story-content`, and `healwithroy-client-plan` skills). It renders Instagram carousels as
real **1080×1350** PNGs in Roy's own teal-and-ink house style — not mockups, not descriptions.

## What's here

| File | What it is |
|---|---|
| `BRAND-STUDY.md` | The analysis of Roy's previous brand identity — voice, positioning, audience, compliance, visual tokens, and how his existing carousel formats map in. **Read this to see what was studied.** |
| `PROJECT-INSTRUCTIONS.md` | The operating spec a new chat reads before building any carousel. Brand is fixed; only topic / slide count / images are asked. |
| `LAYOUT-LIBRARY.md` | Named slide compositions (cover-hook, mechanism, numbered-list, action-result, assumption-reframe, myth-fix, before-after, stat, cta-keyword, cta-follow). |
| `brand.json` | Machine-readable style tokens (colors, type, canvas, CTA, compliance). |
| `templates/slide-base.html` | The HTML/CSS slide kit — every layout as a class, 1080×1350. |
| `scripts/render.mjs` | Renders each `<section class="slide">` to a PNG and runs the overflow check. |
| `work/` | Working carousel HTML files. |
| `exports/` | Finished `slide-01.png …` in swipe order. |
| `assets/` | `photos/ characters/ screenshots/ logos/` for images you include. |

## Build a carousel

1. In this project, say the topic, e.g.
   *"Make a 7-slide carousel: why your sciatica keeps coming back after physio. Keyword SCIATICA."*
2. Claude writes the copy (3 hook options), picks layouts, builds `work/<name>.html`.
3. Export:
   ```bash
   node scripts/render.mjs work/<name>.html exports/
   ```
   The script prints `✓` per slide or an overflow warning to fix.
4. Post `exports/slide-01.png …` in order. Instagram's picker sorts by filename.

## Rendering note (this environment)

Playwright + Chromium are pre-installed at `/opt/node-tools/node_modules`. A `node_modules`
symlink points there so `render.mjs` resolves `playwright`. If the symlink is missing, recreate it:

```bash
ln -sfn /opt/node-tools/node_modules node_modules
```

A sample 7-slide carousel ("Surgery removed the pain. 2 years later — same disc.") is already
rendered in `exports/` to show the house style.
