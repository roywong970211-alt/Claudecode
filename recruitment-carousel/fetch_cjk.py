#!/usr/bin/env python3
"""Fetch an exact-subset Noto Sans SC (only glyphs used here) and embed as @font-face."""
import re, ssl, base64, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
WEIGHTS = [400, 800]
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

# gather every char we render, from the copy sources
text = ''
for f in ['build.py', 'brand.json']:
    text += (HERE / f).read_text(encoding='utf-8')
chars = sorted(set(c for c in text if c.strip() and ord(c) > 31))
# keep CJK, CJK punctuation, fullwidth, arrows, plus all ASCII printable
def keep(c):
    o = ord(c)
    return (o < 127 or 0x2000 <= o <= 0x206F or 0x3000 <= o <= 0x303F or
            0x3400 <= o <= 0x9FFF or 0xFF00 <= o <= 0xFFEF or 0x2190 <= o <= 0x21FF)
subset = ''.join(c for c in chars if keep(c))
print(f'{len(subset)} unique glyphs')

ctx = ssl.create_default_context(cafile='/root/.ccr/ca-bundle.crt')
fam = 'Noto+Sans+SC:wght@' + ';'.join(str(w) for w in WEIGHTS)
import urllib.parse
url = ('https://fonts.googleapis.com/css2?family=' + fam +
       '&text=' + urllib.parse.quote(subset) + '&display=block')
req = urllib.request.Request(url, headers={'User-Agent': UA})
css = urllib.request.urlopen(req, context=ctx, timeout=60).read().decode()

# pair each @font-face's weight with its woff2 url
faces = re.findall(r'@font-face\s*\{([^}]*)\}', css)
out = []
for body in faces:
    w = re.search(r'font-weight:\s*(\d+)', body)
    u = re.search(r'url\((https://[^)]+)\)', body)
    if not (w and u):
        continue
    raw = urllib.request.urlopen(urllib.request.Request(u.group(1), headers={'User-Agent': UA}),
                                 context=ctx, timeout=60).read()
    b64 = base64.b64encode(raw).decode()
    out.append("@font-face{font-family:'Noto Sans SC';font-style:normal;font-weight:%s;font-display:block;"
               "src:url(data:font/woff2;base64,%s) format('woff2');}" % (w.group(1), b64))
    print(f'  weight {w.group(1)}: {len(raw)} bytes')

(HERE / 'cjk_face.css').write_text(''.join(out), encoding='utf-8')
print('wrote cjk_face.css,', len(out), 'faces')
