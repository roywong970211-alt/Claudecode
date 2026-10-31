// HealWithRoy carousel renderer.
// Usage: node scripts/render.mjs <carousel.html> [outDir]
// Screenshots every <section class="slide"> at 1080x1350 -> slide-01.png, slide-02.png, ...
// and runs an overflow check: warns if any text/box crosses the 72px safe margin.

import { chromium } from 'playwright';
import { fileURLToPath, pathToFileURL } from 'url';
import path from 'path';
import fs from 'fs';

const htmlArg = process.argv[2];
const outDir = process.argv[3] || 'exports';
if (!htmlArg) { console.error('Usage: node scripts/render.mjs <carousel.html> [outDir]'); process.exit(1); }

const htmlPath = path.resolve(htmlArg);
if (!fs.existsSync(htmlPath)) { console.error('Not found:', htmlPath); process.exit(1); }
fs.mkdirSync(path.resolve(outDir), { recursive: true });

const SAFE = 72; // px inset that text must stay inside

const browser = await chromium.launch({ args: ['--no-sandbox'] });
const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 2 });
await page.goto(pathToFileURL(htmlPath).href, { waitUntil: 'networkidle' });

const count = await page.locator('section.slide').count();
if (!count) { console.error('No <section class="slide"> found.'); await browser.close(); process.exit(1); }

console.log(`Rendering ${count} slide(s) from ${path.basename(htmlPath)}\n`);
let warnings = 0;

for (let i = 0; i < count; i++) {
  const slide = page.locator('section.slide').nth(i);
  const n = String(i + 1).padStart(2, '0');
  const file = path.join(path.resolve(outDir), `slide-${n}.png`);
  await slide.screenshot({ path: file });

  // Overflow check: measure every text-bearing descendant against the safe box.
  const issues = await slide.evaluate((el, safe) => {
    const r = el.getBoundingClientRect();
    const top = r.top + safe, left = r.left + safe, right = r.right - safe, bottom = r.bottom - safe;
    const out = [];
    // content overflowing the slide itself (scroll)
    if (el.scrollHeight > el.clientHeight + 2) out.push(`content taller than slide by ${el.scrollHeight - el.clientHeight}px`);
    el.querySelectorAll('h1,h2,h3,p,.num,.keyword,.big,.flag,.eyebrow,.geo').forEach(node => {
      const b = node.getBoundingClientRect();
      if (b.width === 0 || b.height === 0) return;
      const tag = (node.className || node.tagName).toString().split(' ')[0];
      if (b.top < top - 1) out.push(`${tag} above safe top`);
      if (b.bottom > bottom + 1) out.push(`${tag} below safe bottom`);
      if (b.left < left - 1) out.push(`${tag} past safe left`);
      if (b.right > right + 1) out.push(`${tag} past safe right`);
    });
    return [...new Set(out)];
  }, SAFE);

  if (issues.length) {
    warnings += issues.length;
    console.log(`  slide-${n}.png  ⚠  ${issues.join('; ')}`);
  } else {
    console.log(`  slide-${n}.png  ✓`);
  }
}

await browser.close();
console.log(`\nDone. ${count} PNG(s) in ${outDir}/` + (warnings ? `  — ${warnings} overflow warning(s): cut words and re-export.` : '  — no overflow warnings.'));
process.exit(warnings ? 2 : 0);
