#!/usr/bin/env python3
"""Overflow-check every slide in a carousel HTML file, then export 1080x1350 PNGs.

    python3 render.py out/carousel.html out/png            # check + export + contact sheets
    python3 render.py out/carousel.html out/png --check    # check only

Runs Chromium at a 420px base with device_scale_factor 1080/420, never at 1080 wide
(that reflows the layout). Exits non-zero if any slide crosses a guard. Also warns
(without failing) on dead paper above a pinned artifact, headlines wider than the
column, and annotation content escaping its box.
"""
import sys
from pathlib import Path

GUARD_BOTTOM, GUARD_RIGHT = 471, 374

CHECK_JS = """() => [...document.querySelectorAll('.sw')].map((sw, i) => {
  const box = sw.getBoundingClientRect(); let mb = 0, mr = 0, who = ''; const warn = [];
  const c = sw.querySelector('.content'); if (!c || sw.querySelector('.art')) return {i: i + 1, skip: true};
  const rel = r => ({t: r.top - box.top, b: r.bottom - box.top, l: r.left - box.left, r: r.right - box.left});
  c.querySelectorAll('*').forEach(el => { const cs = getComputedStyle(el);
    if (cs.position === 'absolute' || el.closest('[style*="position:absolute"]') || el.closest('svg') || el.closest('.cov-fig')) return;
    const r = el.getBoundingClientRect(); if (!r.width && !r.height) return;
    if (el.classList.contains('artifact') && el.children.length) return;
    const q = rel(r); if (q.b > mb) { mb = q.b; who = (typeof el.className === 'string' && el.className) || el.tagName; }
    mr = Math.max(mr, q.r); });
  // text that spills out of its own box: a section name still too wide at the 34px floor, a cover line
  sw.querySelectorAll('.h-sec, .h-cov > span').forEach(h => { if (h.scrollWidth > 343) { warn.push('headline too wide (' + h.textContent.trim() + ')'); mr = Math.max(mr, 32 + h.scrollWidth); } });
  sw.querySelectorAll('[data-short]').forEach(e => warn.push('text shrunk below its size floor to fit (' + e.textContent.trim().slice(0, 40) + '): shorten it'));
  // annotated boxes: every label and mock-up inside must stay inside the box and the right guard
  sw.querySelectorAll('.ann').forEach(a => { const ab = a.getBoundingClientRect();
    a.querySelectorAll('div').forEach(d => { const r = d.getBoundingClientRect(); if (!r.width) return;
      if (r.bottom > ab.bottom + 1) { warn.push('annotated content runs ' + Math.round(r.bottom - ab.bottom) + 'px below its box'); mb = Math.max(mb, rel(r).b + (box.top + 471 - ab.bottom)); }
      if (rel(r).r > 374.5) { warn.push('annotation past right guard by ' + Math.round(rel(r).r - 374) + 'px'); mr = Math.max(mr, rel(r).r); } }); });
  // content cut off inside a clipping box (cards, split panes)
  sw.querySelectorAll('.content .card, .content .box').forEach(bx => {
    if (bx.scrollHeight > bx.clientHeight + 1 || bx.scrollWidth > bx.clientWidth + 1)
      warn.push('content clipped inside a ' + (bx.classList.contains('box') ? 'split pane' : 'card') + ' by ' +
        Math.max(bx.scrollHeight - bx.clientHeight, bx.scrollWidth - bx.clientWidth) + 'px'); });
  // text running sideways out of any block
  c.querySelectorAll('div, p, span').forEach(e => { if (e.closest('svg') || e.closest('.ann')) return;
    const r = e.getBoundingClientRect(); if (r.width && rel(r).r > 374.5 && getComputedStyle(e).position !== 'absolute') {
      warn.push('content past the right guard by ' + Math.round(rel(r).r - 374) + 'px'); mr = Math.max(mr, rel(r).r); } });
  // dead paper above a pinned artifact
  const art = c.querySelector('.artifact'); let gap = null;
  if (art && art.firstElementChild && art.previousElementSibling) {
    gap = Math.round(art.firstElementChild.getBoundingClientRect().top - art.previousElementSibling.getBoundingClientRect().bottom);
    if (gap > 24) warn.push('artifact under-built: ' + gap + 'px of dead paper above it (target 14 to 18)');
    if (gap < 10) warn.push('artifact touching the rows: ' + gap + 'px gap'); }
  const h = [...sw.querySelectorAll('.h-sec')].map(e => e.style.fontSize || getComputedStyle(e).fontSize);
  return {i: i + 1, bottom: Math.round(mb), right: Math.round(mr), who, h, gap, warn: [...new Set(warn)].slice(0, 6)};
})"""


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src = Path(sys.argv[1]).resolve()
    out = Path(sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else src.parent / 'png')
    check_only = '--check' in sys.argv
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit('Playwright is missing: pip install playwright && python3 -m playwright install chromium\n'
                 'No browser available at all? Open the HTML file and use its Download PNG buttons instead.')
    if not check_only:
        out.mkdir(parents=True, exist_ok=True)
    bad = warns = 0
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1243/chrome-linux64/chrome", args=["--no-sandbox"])
        pg = b.new_page(viewport={'width': 420, 'height': 525}, device_scale_factor=1080 / 420)
        pg.goto(src.as_uri())
        pg.wait_for_function('window.ready === true', timeout=20000)
        pg.evaluate("document.body.classList.add('export')")
        pg.wait_for_timeout(300)
        for r in pg.evaluate(CHECK_JS):
            if r.get('skip'):
                print(f"slide-{r['i']:02d}  art cover, not measured")
                continue
            ok = r['bottom'] <= GUARD_BOTTOM and r['right'] <= GUARD_RIGHT
            bad += not ok
            extra = (f"  h-sec {r['h'][0]}" if r['h'] else '') + (f"  gap {r['gap']}" if r['gap'] is not None else '')
            print(f"slide-{r['i']:02d}  bottom {r['bottom']:>3} / {GUARD_BOTTOM}  right {r['right']:>3} / {GUARD_RIGHT}"
                  f"  {'OK' if ok else 'OVERFLOW at ' + str(r['who'])}{extra}")
            for w in r['warn']:
                print(f"           ! {w}")
            warns += len(r['warn'])
        if not check_only:
            slides = pg.query_selector_all('.sw')
            for i, el in enumerate(slides):
                el.screenshot(path=str(out / f'slide-{i + 1:02d}.png'))
            print(f'exported {len(slides)} PNGs to {out}')
        b.close()
    if not check_only:
        sheets(out)
    if warns:
        print(f'{warns} warning(s) above: look at those slides full size and fix them.')
    if bad:
        print(f'{bad} slide(s) cross a guard. Fix before shipping.')
        sys.exit(1)


def sheets(out):
    """Contact sheet at 270px and the 146px profile-grid strip. If a headline dies at 146, it dies on the grid."""
    try:
        from PIL import Image
    except ImportError:
        print('Pillow missing, skipping contact sheets'); return
    files = sorted(out.glob('slide-*.png'))
    if not files:
        return
    rv = out / 'review'          # kept out of the slide folder so the picker only sees slide-NN.png
    rv.mkdir(exist_ok=True)
    for w, name, cols in ((270, 'contact-sheet.png', 4), (146, 'grid-strip.png', len(files))):
        h = round(w * 1350 / 1080)
        rows = -(-len(files) // cols)
        sh = Image.new('RGB', (cols * (w + 8) + 8, rows * (h + 8) + 8), '#E9E4D6')
        for k, f in enumerate(files):
            sh.paste(Image.open(f).convert('RGB').resize((w, h), Image.LANCZOS), (8 + (k % cols) * (w + 8), 8 + (k // cols) * (h + 8)))
        sh.save(rv / name)
    print(f'wrote review/contact-sheet.png and review/grid-strip.png in {out}')


if __name__ == '__main__':
    main()
