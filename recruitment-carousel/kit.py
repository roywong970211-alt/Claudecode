#!/usr/bin/env python3
"""Carousel Studio component kit.

Import it from a build script, describe each slide with the helpers below, and call
`write_carousel()`. The output is ONE self-contained HTML file holding every slide
as a 420x525 `.sw` block. That file is both the preview (open it in a browser, it
has a download button per slide) and the input to `render.py`, which exports each
slide to a 1080x1350 PNG and runs the overflow check.

    import sys; sys.path.insert(0, '<skill>/scripts')
    from kit import *
    brand = load_brand('brand.json')
    slides = [cover_type(...), section(...), cta(...)]
    write_carousel('out/carousel.html', slides, brand)

The LOOK comes from brand.json: a starting preset plus the user's own overrides
(colours, fonts, texture, card, chip, marker, bullet). See references/onboarding.md.
Every size is in CSS pixels at the 420px base. Do not change the base width.
"""
import base64, json, math, os, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

# ----------------------------------------------------------------- style presets
# Starting points only. Onboarding always changes the accent and at least two
# other attributes, so no two users ship the same look.

PRESETS = {
    'paper': {  # the original look: notebook paper, warm serif, hand notes
        'label': 'Paper notebook', 'paper': '#F6F1E3', 'card': '#FBF8EF', 'rule': '#DCD3BE', 'ink': '#2C2A26', 'ink_soft': '#6E6A5F',
        'display': 'Young Serif', 'display_weight': 400, 'display_tracking': -0.018, 'display_case': 'none', 'display_lh': 1.07,
        'body': 'DM Sans', 'hand': 'Caveat', 'mono': 'JetBrains Mono',
        'texture': ['grid', 'grain'], 'card_style': 'offset', 'radius': 10, 'border': 1.5,
        'chip': 'block', 'marker': 'hand', 'bullet': 'arrow', 'sample_accent': '#D97757'},
    'swiss': {  # clean grotesk, white, hard edges, no handwriting
        'label': 'Swiss minimal', 'paper': '#FFFFFF', 'card': '#F5F5F3', 'rule': '#E2E2DE', 'ink': '#111111', 'ink_soft': '#6B6B6B',
        'display': 'Space Grotesk', 'display_weight': 700, 'display_tracking': -0.035, 'display_case': 'none', 'display_lh': 1.02,
        'body': 'Inter', 'hand': None, 'mono': 'IBM Plex Mono',
        'texture': [], 'card_style': 'flat', 'radius': 4, 'border': 1.5,
        'chip': 'outline', 'marker': 'bar', 'bullet': 'dash', 'sample_accent': '#1F5BFF'},
    'noir': {  # dark mode, chunky grotesk, marker highlights
        'label': 'Night mode', 'paper': '#131313', 'card': '#1E1E1E', 'rule': '#333333', 'ink': '#F2F0EA', 'ink_soft': '#A39E94',
        'display': 'Bricolage Grotesque', 'display_weight': 800, 'display_tracking': -0.03, 'display_case': 'none', 'display_lh': 1.0,
        'body': 'Manrope', 'hand': 'Gochi Hand', 'mono': 'Space Mono',
        'texture': ['grain'], 'card_style': 'flat', 'radius': 12, 'border': 1,
        'chip': 'pill', 'marker': 'highlight', 'bullet': 'dot', 'sample_accent': '#C6F432'},
    'soft': {  # rounded, friendly, pastel cards and soft shadows
        'label': 'Soft and rounded', 'paper': '#FBF5EF', 'card': '#FFFFFF', 'rule': '#EADFD4', 'ink': '#2B2733', 'ink_soft': '#7A7283',
        'display': 'Fraunces', 'display_weight': 600, 'display_tracking': -0.02, 'display_case': 'none', 'display_lh': 1.04,
        'body': 'Nunito', 'hand': 'Kalam', 'mono': 'DM Mono',
        'texture': ['dots'], 'card_style': 'soft', 'radius': 18, 'border': 0,
        'chip': 'accent', 'marker': 'hand', 'bullet': 'dot', 'sample_accent': '#E2557B'},
    'magazine': {  # high-contrast editorial serif, thin rules, numbered points
        'label': 'Magazine', 'paper': '#F3F0E8', 'card': '#FAF8F3', 'rule': '#D6D0C2', 'ink': '#151515', 'ink_soft': '#5F5A50',
        'display': 'DM Serif Display', 'display_weight': 400, 'display_tracking': -0.01, 'display_case': 'none', 'display_lh': 1.03,
        'body': 'Work Sans', 'hand': None, 'mono': 'IBM Plex Mono',
        'texture': ['lines'], 'card_style': 'flat', 'radius': 0, 'border': 1,
        'chip': 'outline', 'marker': 'bar', 'bullet': 'number', 'sample_accent': '#B3261E'},
    'terminal': {  # developer dark, monospace headlines, prompt bullets
        'label': 'Terminal', 'paper': '#0E1116', 'card': '#161B22', 'rule': '#30363D', 'ink': '#E6EDF3', 'ink_soft': '#8B949E',
        'display': 'JetBrains Mono', 'display_weight': 700, 'display_tracking': -0.04, 'display_case': 'none', 'display_lh': 1.05, 'h_size': 34, 'h_min': 27,
        'body': 'IBM Plex Sans', 'hand': None, 'mono': 'JetBrains Mono',
        'texture': ['grid'], 'card_style': 'flat', 'radius': 6, 'border': 1,
        'chip': 'accent', 'marker': 'none', 'bullet': 'prompt', 'sample_accent': '#3FB950'},
}

# Every font the kit can embed: family -> (fontsource package, weights available, kind)
FONTS = {
    # display
    'Young Serif': ('young-serif', (400,), 'display'), 'Fraunces': ('fraunces', (400, 500, 600, 700, 800), 'display'),
    'DM Serif Display': ('dm-serif-display', (400,), 'display'), 'Playfair Display': ('playfair-display', (400, 500, 600, 700, 800), 'display'),
    'Space Grotesk': ('space-grotesk', (400, 500, 600, 700), 'display'), 'Bricolage Grotesque': ('bricolage-grotesque', (400, 500, 600, 700, 800), 'display'),
    'Syne': ('syne', (500, 600, 700, 800), 'display'), 'Unbounded': ('unbounded', (400, 500, 600, 700, 800), 'display'),
    'Archivo Black': ('archivo-black', (400,), 'display'), 'Bebas Neue': ('bebas-neue', (400,), 'display'),
    'Anton': ('anton', (400,), 'display'), 'Oswald': ('oswald', (500, 600, 700), 'display'),
    'Instrument Serif': ('instrument-serif', (400,), 'display'), 'Montserrat': ('montserrat', (600, 700, 800), 'display'),
    # body
    'DM Sans': ('dm-sans', (400, 500, 600, 700), 'body'), 'Inter': ('inter', (400, 500, 600, 700, 800), 'body'),
    'Manrope': ('manrope', (400, 500, 600, 700, 800), 'body'), 'Nunito': ('nunito', (400, 500, 600, 700, 800), 'body'),
    'Work Sans': ('work-sans', (400, 500, 600, 700), 'body'), 'IBM Plex Sans': ('ibm-plex-sans', (400, 500, 600, 700), 'body'),
    'Plus Jakarta Sans': ('plus-jakarta-sans', (400, 500, 600, 700, 800), 'body'), 'Figtree': ('figtree', (400, 500, 600, 700, 800), 'body'),
    'Instrument Sans': ('instrument-sans', (400, 500, 600, 700), 'body'),
    # handwriting
    'Caveat': ('caveat', (600, 700), 'hand'), 'Kalam': ('kalam', (400, 700), 'hand'), 'Gochi Hand': ('gochi-hand', (400,), 'hand'),
    'Patrick Hand': ('patrick-hand', (400,), 'hand'),
    # mono
    'JetBrains Mono': ('jetbrains-mono', (400, 500, 600, 700), 'mono'), 'IBM Plex Mono': ('ibm-plex-mono', (400, 500, 600), 'mono'),
    'Space Mono': ('space-mono', (400, 700), 'mono'), 'DM Mono': ('dm-mono', (400, 500), 'mono'),
}
HAND_SIZE = {'Caveat': 16.5, 'Kalam': 13.5, 'Gochi Hand': 14.5, 'Patrick Hand': 15}
FALLBACK = {'display': 'serif', 'body': 'sans-serif', 'hand': 'cursive', 'mono': 'monospace'}

STYLE_KEYS = ('paper', 'card', 'rule', 'ink', 'ink_soft', 'accent', 'display', 'display_weight', 'display_tracking', 'display_case',
              'display_lh', 'h_size', 'h_min', 'body', 'hand', 'mono', 'texture', 'card_style', 'radius', 'border', 'chip', 'marker', 'bullet')

DEFAULT_BRAND = {
    'handle': '@yourhandle', 'tagline': '', 'avatar': None, 'mascot': None,
    'style': {'preset': 'paper'},
    'voice': {'swipe_cue': 'swipe', 'cta': 'keyword'},
}


def load_brand(path='brand.json'):
    """Read brand.json and resolve the full style: preset values, then the user's overrides.
    Relative asset paths resolve against the brand file's folder. Returns a flat dict with
    'style' (every key in STYLE_KEYS) and 'voice'."""
    b = json.loads(json.dumps(DEFAULT_BRAND))
    p = Path(path)
    if p.exists():
        user = json.loads(p.read_text())
        for k, v in user.items():
            if k in ('style', 'voice') and isinstance(v, dict):
                b[k].update(v)
            else:
                b[k] = v
        for k in ('avatar', 'mascot'):
            if b.get(k) and not Path(b[k]).is_absolute():
                b[k] = str((p.parent / b[k]).resolve())
            if b.get(k) and not Path(b[k]).exists():
                print(f'WARNING: {k} file {b[k]} not found, leaving it out.')
                b[k] = None
    else:
        print(f'WARNING: {path} not found, using the "paper" preset. Run the onboarding first.')
    if 'accent' in b and 'accent' not in b['style']:      # brand.json files from v1 kept accent at the top level
        b['style']['accent'] = b['accent']
    if 'swipe_cue' in b and 'swipe_cue' not in b['voice']:
        b['voice']['swipe_cue'] = b['swipe_cue']
    preset = PRESETS.get(b['style'].get('preset', 'paper'), PRESETS['paper'])
    st = {k: preset.get(k) for k in STYLE_KEYS}
    st['h_size'] = preset.get('h_size', 42); st['h_min'] = preset.get('h_min', 34)
    st['accent'] = preset['sample_accent']
    user = {k: v for k, v in b['style'].items() if k in STYLE_KEYS}
    st.update(user)
    st['preset'] = b['style'].get('preset', 'paper')
    # a new paper or ink without matching neutrals: derive card, rule and ink_soft so no preset colour is left behind
    if 'paper' in user or 'ink' in user:
        dark = _lum(st['paper']) < .4
        if 'card' not in user:
            st['card'] = _mix(st['paper'], '#FFFFFF' if not dark else st['ink'], .55 if not dark else .06)
        if 'rule' not in user:
            st['rule'] = _mix(st['paper'], st['ink'], .14 if not dark else .18)
        if 'ink_soft' not in user:
            st['ink_soft'] = _mix(st['ink'], st['paper'], .40)
    cr = _contrast(st['accent'], st['paper'])
    if cr < 2.5:
        print(f'WARNING: accent {st["accent"]} on paper {st["paper"]} has contrast {cr:.1f}:1 (large headlines need about 2.5:1 at minimum, 3:1 is safer). '
              'Pick a deeper accent or switch the background.')
    for k in ('display', 'body', 'mono'):
        if st[k] not in FONTS:
            print(f'WARNING: font "{st[k]}" is not in the kit catalogue; it will not be embedded.')
    b['style'] = st
    return b


def _mix(a, b, t):
    """Blend hex a toward hex b by t (0..1)."""
    ca, cb = [int(x) for x in _rgb(a).split(',')], [int(x) for x in _rgb(b).split(',')]
    return '#' + ''.join(f'{round(x + (y - x) * t):02X}' for x, y in zip(ca, cb))


def uniqueness(brand):
    """How far the locked style sits from its starting preset. Returns (ok, changed_keys, message)."""
    st, p = brand['style'], PRESETS.get(brand['style'].get('preset'), PRESETS['paper'])
    attrs = ['display', 'body', 'paper', 'texture', 'card_style', 'chip', 'marker', 'bullet', 'hand']
    changed = [k for k in attrs if (sorted(st[k]) if k == 'texture' else st[k]) != (sorted(p[k]) if k == 'texture' else p[k])]
    acc = st['accent'].upper() != p['sample_accent'].upper()
    need = 3 if st.get('preset') == 'paper' else 2
    if st.get('preset') == 'paper' and not ({'display', 'paper'} & set(changed)):
        need = 99
    ok = acc and len(changed) >= need
    msg = (f"uniqueness: accent {'changed' if acc else 'UNCHANGED'}, {len(changed)} other attribute(s) changed "
           f"({', '.join(changed) or 'none'}); needs accent + {min(need, 3)}"
           + (' incl. display or paper' if st.get('preset') == 'paper' else '') + f" -> {'OK' if ok else 'NOT YET UNIQUE'}")
    return ok, changed, msg


def _rgb(hex_):
    h = hex_.lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    return ','.join(str(int(h[i:i + 2], 16)) for i in (0, 2, 4))


def _lum(hex_):
    r, g, b = (int(x) / 255 for x in _rgb(hex_).split(','))
    return .2126 * r + .7152 * g + .0722 * b


def _contrast(a, b):
    def L(h):
        out = []
        for c in _rgb(h).split(','):
            c = int(c) / 255
            out.append(c / 12.92 if c <= .03928 else ((c + .055) / 1.055) ** 2.4)
        return .2126 * out[0] + .7152 * out[1] + .0722 * out[2]
    la, lb = sorted((L(a), L(b)), reverse=True)
    return (la + .05) / (lb + .05)


def needed_fonts(brand, extra=()):
    """(family, weight) pairs this brand needs, used by setup_fonts.py and font_css()."""
    st = brand['style']
    want = {}

    def add(fam, ws):
        if not fam or fam not in FONTS:
            return
        avail = FONTS[fam][1]
        for w in ws:
            best = min(avail, key=lambda a: abs(a - w))
            want.setdefault(fam, set()).add(best)
    add(st['display'], [st['display_weight']])
    add(st['body'], [400, 500, 600, 700])
    add(st['hand'], [600, 700] if st['hand'] == 'Caveat' else [400, 700])
    add(st['mono'], [400, 500, 600])
    for f in extra:
        add(f, FONTS.get(f, (None, (400,)))[1])
    return want


# ----------------------------------------------------------------- assets

def data_uri(path):
    """Base64-embed an image, sniffing its real format (a .png is often a JPEG)."""
    raw = Path(path).read_bytes()
    mime = ('image/png' if raw[:8] == b'\x89PNG\r\n\x1a\n' else
            'image/jpeg' if raw[:3] == b'\xff\xd8\xff' else
            'image/webp' if raw[8:12] == b'WEBP' else
            'image/gif' if raw[:4] == b'GIF8' else
            'image/svg+xml' if raw.lstrip()[:1] == b'<' else 'application/octet-stream')
    return f'data:{mime};base64,' + base64.b64encode(raw).decode()


# ----------------------------------------------------------------- fonts

def _font_root():
    for c in [os.environ.get('FONT_DIR'), Path.cwd() / 'node_modules/@fontsource', HERE / 'node_modules/@fontsource',
              Path(sys.argv[0]).resolve().parent / 'node_modules/@fontsource', Path.home() / 'node_modules/@fontsource']:
        if c and Path(c).exists():
            return Path(c)
    return None


def font_css(brand, extra=()):
    """@font-face rules with every file base64-embedded. Embedding is not optional:
    the render browser may have no network, and a missing font silently falls back
    to a system face. Run `python3 setup_fonts.py brand.json` once to install them.
    If files are missing, falls back to a Google Fonts import and says so."""
    root = _font_root()
    rules, missing = [], {}
    for fam, ws in needed_fonts(brand, extra).items():
        pkg = FONTS[fam][0]
        style = 'normal'
        for w in sorted(ws):
            f = root / pkg / 'files' / f'{pkg}-latin-{w}-{style}.woff2' if root else None
            if f and f.exists():
                rules.append(f"@font-face{{font-family:'{fam}';font-style:{style};font-weight:{w};font-display:block;"
                             f"src:url(data:font/woff2;base64,{base64.b64encode(f.read_bytes()).decode()}) format('woff2');}}")
            else:
                missing.setdefault(fam, set()).add(w)
    if 'Instrument Serif' in extra and root and (root / 'instrument-serif/files/instrument-serif-latin-400-italic.woff2').exists():
        f = root / 'instrument-serif/files/instrument-serif-latin-400-italic.woff2'
        rules.append(f"@font-face{{font-family:'Instrument Serif';font-style:italic;font-weight:400;font-display:block;"
                     f"src:url(data:font/woff2;base64,{base64.b64encode(f.read_bytes()).decode()}) format('woff2');}}")
    if missing:
        print('WARNING: fonts not installed, falling back to Google Fonts for:', ', '.join(missing),
              '\n  Run setup_fonts.py so the export does not depend on the network.')
        q = '&'.join(f"family={m.replace(' ', '+')}:wght@{';'.join(str(w) for w in sorted(ws))}" for m, ws in missing.items())
        rules.insert(0, f"@import url('https://fonts.googleapis.com/css2?{q}&display=block');")
    return ''.join(rules)


# ----------------------------------------------------------------- CSS

def style_vars(st):
    """Turn the resolved style into CSS custom properties and body classes."""
    dark = _lum(st['paper']) < .4
    ink = _rgb(st['ink'])
    fam = lambda k: (f"'{st[k]}'," if st.get(k) else '') + FALLBACK[k]
    hand = st['hand']
    shadow = {'offset': f'3px 3px 0 {"rgba(0,0,0,.55)" if dark else f"rgba({ink},.15)"}',
              'soft': f'0 8px 22px {"rgba(0,0,0,.45)" if dark else f"rgba({ink},.09)"}', 'flat': 'none'}[st['card_style']]
    v = {
        '--paper': st['paper'], '--card': st['card'], '--rule': st['rule'], '--ink': st['ink'], '--ink-soft': st['ink_soft'],
        '--ink-rgb': ink, '--accent': st['accent'], '--accent-rgb': _rgb(st['accent']),
        '--on-accent': '#111111' if _lum(st['accent']) > .55 else '#FFFFFF',
        '--bar-accent': st['accent'] if _contrast(st['accent'], st['ink']) >= 3 else 'rgba(' + _rgb(st['paper']) + ',.6)',
        '--f-display': fam('display'), '--f-body': fam('body'), '--f-mono': fam('mono'),
        '--f-hand': fam('hand') if hand else fam('body'),
        '--w-display': str(st['display_weight']), '--track': f"{st['display_tracking']}em", '--lh-display': str(st['display_lh']),
        '--case-display': st['display_case'], '--h-size': f"{st['h_size']}px", '--h-min': str(st['h_min']),
        '--hand-size': f"{HAND_SIZE.get(hand, 12.5)}px" if hand else '12.5px', '--hand-weight': '600' if hand == 'Caveat' else ('400' if hand else '600'),
        '--hand-style': 'normal',
        '--radius': f"{st['radius']}px", '--border': f"{st['border']}px", '--card-shadow': shadow,
        '--tex': f'rgba({ink},{.06 if dark else .033})', '--dot': f'rgba({ink},{.12 if dark else .10})',
        '--grain-blend': 'soft-light' if dark else 'multiply', '--grain-op': '.5' if dark else '.28',
    }
    classes = [f"tex-{t}" for t in (st['texture'] or ['none'])] + [f"chip-{st['chip']}", f"mk-{st['marker']}", f"bul-{st['bullet']}",
                                                               'is-dark' if dark else 'is-light', 'no-hand' if not hand else 'has-hand']
    return ':root{' + ';'.join(f'{k}:{val}' for k, val in v.items()) + '}', ' '.join(classes)


CSS = r"""
*{box-sizing:border-box;margin:0;padding:0}
html{background:#E9E4D6}
body{font-family:var(--f-body);color:var(--ink);display:flex;flex-direction:column;align-items:center;gap:28px;padding:70px 0 40px}
.sw{position:relative;width:420px;height:525px;overflow:hidden;background:var(--paper);flex:0 0 auto;box-shadow:0 10px 30px rgba(44,42,38,.18)}
.grid-l{position:absolute;inset:0;pointer-events:none;z-index:2;display:none}
.tex-grid .grid-l{display:block;background-image:linear-gradient(var(--tex) 1px,transparent 1px),linear-gradient(90deg,var(--tex) 1px,transparent 1px);background-size:22px 22px}
.tex-dots .grid-l{display:block;background-image:radial-gradient(var(--dot) 1.1px,transparent 1.5px);background-size:16px 16px;background-position:8px 8px}
.tex-lines .grid-l{display:block;background-image:linear-gradient(var(--tex) 1px,transparent 1px);background-size:100% 24px;background-position:0 12px}
.grain-l{position:absolute;inset:0;pointer-events:none;z-index:3;display:none;opacity:var(--grain-op);mix-blend-mode:var(--grain-blend);background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/></filter><rect width='300' height='300' filter='url(%23n)' opacity='0.55'/></svg>");background-size:300px 300px}
.tex-grain .grain-l{display:block}
.content{position:absolute;inset:0;z-index:4;padding:30px 46px 54px 32px;display:flex;flex-direction:column}
/* chip variants */
.chip{display:inline-block;font-family:var(--f-mono);font-size:9.5px;font-weight:500;letter-spacing:.18em;text-transform:uppercase;color:var(--paper);background:var(--ink);padding:5px 10px;border-radius:3px;align-self:flex-start;line-height:1}
.chip-pill .chip{border-radius:999px;padding:5px 12px}
.chip-outline .chip{background:transparent;color:var(--ink);border:1.2px solid var(--ink);padding:4px 9px;border-radius:2px}
.chip-accent .chip{background:var(--accent);color:var(--on-accent);border-radius:calc(var(--radius) / 3 + 2px)}
/* type */
.kicker{font-family:var(--f-display);font-weight:var(--w-display);letter-spacing:var(--track);font-size:24px;line-height:1.1;color:var(--ink-soft);margin-top:13px;text-transform:var(--case-display)}
.h-sec{font-family:var(--f-display);font-weight:var(--w-display);font-size:var(--h-size);line-height:var(--lh-display);letter-spacing:var(--track);color:var(--accent);white-space:nowrap;text-transform:var(--case-display)}
.mk-wrap{margin-top:9px;line-height:0}
.mk-none .mk-wrap,.mk-highlight .mk-wrap{display:none}
.mk-highlight .h-sec,.mk-highlight .h-cov .acc{color:var(--ink)}
.mk-highlight .hlx{background:linear-gradient(transparent 52%,rgba(var(--accent-rgb),.85) 52%,rgba(var(--accent-rgb),.85) 92%,transparent 92%);padding:0 3px;margin:0 -3px}
.is-dark.mk-highlight .hlx{color:var(--on-accent);background:linear-gradient(transparent 14%,var(--accent) 14%,var(--accent) 96%,transparent 96%)}
.mk-highlight .h-sec{margin-bottom:4px}
.rows{margin-top:14px;display:flex;flex-direction:column;gap:9px;counter-reset:r}
.row{display:flex;gap:7px;font-size:13px;line-height:1.5;color:var(--ink);counter-increment:r}
.row .ar{color:var(--accent);flex:0 0 auto;min-width:11px}
.bul-dot .ar svg,.bul-dash .ar svg,.bul-number .ar svg,.bul-prompt .ar svg{display:none!important}
.bul-dot .ar::before{content:'';display:block;width:6px;height:6px;border-radius:50%;background:var(--accent);margin:7px 2px 0}
.bul-dash .ar::before{content:'';display:block;width:10px;height:2px;background:var(--accent);margin-top:9px}
.bul-number .ar{min-width:17px}.bul-number .ar::before{content:counter(r,decimal-leading-zero);font:600 10px/19.5px var(--f-mono);color:var(--accent)}
.bul-prompt .ar::before{content:'>';font:600 12.5px/19.5px var(--f-mono);color:var(--accent)}
.rl{font-weight:600;color:var(--accent)}
.hand{font-family:var(--f-hand);font-weight:var(--hand-weight);font-size:var(--hand-size);line-height:1.2;color:var(--ink-soft)}
.no-hand .hand{font-style:italic}
.mono{font-family:var(--f-mono);font-size:8.5px;letter-spacing:.15em;text-transform:uppercase;color:var(--ink-soft)}
.accent{color:var(--accent)}
.hl{background:linear-gradient(transparent 30%,rgba(var(--accent-rgb),.42) 30%,rgba(var(--accent-rgb),.42) 88%,transparent 88%);-webkit-box-decoration-break:clone;box-decoration-break:clone}
/* artifacts */
.artifact{margin-top:auto;padding-top:14px}
.close{margin-top:10px}
.card{background:var(--card);border:var(--border) solid var(--ink);border-radius:var(--radius);box-shadow:var(--card-shadow);overflow:hidden}
.pop-bar{background:var(--ink);color:var(--paper);font-family:var(--f-mono);font-size:8.5px;letter-spacing:.15em;padding:8px 13px;display:flex;justify-content:space-between}
.pop-bar span{opacity:.85}.pop-bar b{font-weight:500;color:var(--bar-accent)}
.is-dark .pop-bar{background:rgba(var(--ink-rgb),.1);color:var(--ink);border-bottom:1px solid var(--rule)}.is-dark .pop-bar b{color:var(--accent)}
.cmd{background:rgba(var(--ink-rgb),.06);border-radius:calc(var(--radius) * .6);padding:8px 11px;font-family:var(--f-mono);font-size:10.5px;line-height:1.35;color:var(--ink)}
.cmd .p{color:var(--accent);margin-right:7px}
.banner{background:linear-gradient(rgba(var(--accent-rgb),.14),rgba(var(--accent-rgb),.14)),var(--paper);border-radius:calc(var(--radius) * .8);padding:9px 12px;font-size:12.5px;line-height:1.45}
.shot{display:block;width:100%}
/* split compare */
.split{display:flex;align-items:flex-start;justify-content:space-between}
.pane{width:150px;display:flex;flex-direction:column;align-items:center;gap:6px}
.pane .lb{font-family:var(--f-mono);font-size:8px;letter-spacing:.15em;color:var(--ink-soft);align-self:flex-start;white-space:nowrap}
.pane .box{width:150px;border-radius:var(--radius);padding:4.5px;overflow:hidden}
.pane.bad .box{border:1.5px dashed var(--ink-soft);background:transparent}
.pane.good .box{border:max(var(--border),1px) solid var(--ink);background:var(--card);box-shadow:var(--card-shadow)}
.pane .cv{font-family:var(--f-hand);font-weight:var(--hand-weight);font-size:calc(var(--hand-size) - .5px);color:var(--ink-soft);line-height:1}
.no-hand .pane .cv{font-style:italic}
.pane.good .cv{color:var(--accent)}
.s-ar{margin-top:72px;width:26px;flex:0 0 auto}
/* process flow */
.flow{display:flex;justify-content:space-between;align-items:flex-start}
.fstep{display:flex;flex-direction:column;align-items:center;gap:5px;width:78px}
.fstep .fl{font-size:11px;font-weight:500;color:var(--ink);text-align:center;line-height:1.25}
.f-ar{margin-top:16px;flex:0 0 auto}
/* cover */
.cov{padding-top:44px}
.h-cov{font-family:var(--f-display);font-weight:var(--w-display);font-size:48px;line-height:var(--lh-display);letter-spacing:var(--track);color:var(--ink);text-transform:var(--case-display)}
.h-cov .ln,.h-cov .acc{display:block;white-space:nowrap}.h-cov .acc{color:var(--accent)}
.cov-sub{font-family:var(--f-hand);font-weight:var(--hand-weight);font-size:calc(var(--hand-size) + 2.5px);line-height:1.25;color:var(--ink-soft);margin-top:14px}
.no-hand .cov-sub{font-style:normal;font-weight:500;font-size:14px}
.cue{display:flex;align-items:center;gap:9px;font-family:var(--f-hand);font-weight:700;font-size:calc(var(--hand-size) + 2.5px);color:var(--accent);margin-top:18px}
.no-hand .cue{font-family:var(--f-mono);font-size:10px;letter-spacing:.15em;text-transform:uppercase;font-weight:500}
.handle{position:absolute;left:32px;bottom:26px;font-family:var(--f-mono);font-size:9.5px;letter-spacing:.15em;color:var(--ink-soft);text-transform:uppercase;z-index:5}
.cov-fig{position:absolute;right:0;bottom:0;z-index:3;display:block}
.cov-mascot{display:block;margin-top:16px}
.cov-cards{margin-top:auto;margin-bottom:20px;display:flex;gap:9px}
.cc{flex:1;padding:10px 10px 11px;min-width:0}.cc .mono{font-size:7.5px;color:var(--accent)}
.cc-n{font-family:var(--f-display);font-weight:var(--w-display);letter-spacing:var(--track);font-size:15px;line-height:1.1;color:var(--ink);margin-top:5px}
/* art cover */
.art .bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.art .dim{position:absolute;left:0;right:0;top:0;height:240px;background:linear-gradient(180deg,rgba(6,10,18,.82),rgba(6,10,18,.5) 55%,rgba(6,10,18,0))}
.art .sc{position:absolute;left:0;right:0;bottom:0;height:110px;background:linear-gradient(180deg,rgba(0,0,0,0),rgba(0,0,0,.55))}
.art .hd{position:absolute;left:0;right:0;top:22px;text-align:center;color:#F8F5EC;line-height:.98;text-shadow:0 3px 16px rgba(0,0,0,.55);z-index:4}
.art .hd .big{color:var(--accent);line-height:.95}
.art .foot{position:absolute;left:24px;bottom:20px;display:flex;flex-direction:column;gap:8px;z-index:4}
.art .cue{color:#F8F5EC;margin-top:0;text-shadow:0 1px 8px rgba(0,0,0,.6)}
.art .hn{font-family:var(--f-mono);font-size:9.5px;letter-spacing:.15em;color:#F8F5EC;text-transform:uppercase}
/* cta */
.ctac{align-items:center;text-align:center;padding-top:62px}
.h-cta{font-family:var(--f-display);font-weight:var(--w-display);font-size:34px;line-height:1.13;letter-spacing:var(--track);color:var(--ink);text-transform:var(--case-display)}
.kw-block{margin-top:19px;width:100%;background:linear-gradient(rgba(var(--accent-rgb),.10),rgba(var(--accent-rgb),.10)),var(--paper);border:1.5px solid var(--accent);border-radius:calc(var(--radius) + 2px);padding:11px 16px 14px}
.kw-lb{font-size:12px;color:var(--ink-soft)}
.kw{font-family:var(--f-display);font-weight:var(--w-display);letter-spacing:var(--track);font-size:44px;line-height:1.02;color:var(--accent);margin-top:2px;white-space:nowrap}
.promise{font-size:14px;line-height:1.5;color:var(--ink);margin-top:14px}
.toolbar{margin-top:14px;width:100%;background:linear-gradient(rgba(var(--accent-rgb),.07),rgba(var(--accent-rgb),.07)),var(--paper);border-radius:calc(var(--radius) * .8);padding:8px 10px;font-size:11px;line-height:1.55;color:var(--ink)}
.lockup{display:flex;align-items:center;gap:14px;margin-top:auto;margin-bottom:4px}
.avf{background:var(--card);padding:4px;border:max(var(--border),1px) solid var(--ink);border-radius:calc(var(--radius) + 4px);box-shadow:var(--card-shadow);line-height:0}
.avf img{width:60px;height:60px;object-fit:cover;border-radius:var(--radius);display:block}
.avf .ini{width:60px;height:60px;border-radius:var(--radius);background:var(--accent);color:var(--on-accent);font-family:var(--f-display);font-weight:var(--w-display);font-size:28px;line-height:60px;text-align:center}
.lk-txt{text-align:left}
.lk-name{font-size:19px;font-weight:600;color:var(--ink);line-height:1.1}
.lk-tag{font-family:var(--f-hand);font-weight:var(--hand-weight);font-size:calc(var(--hand-size) + 2.5px);color:var(--ink-soft);margin-top:2px}
.no-hand .lk-tag{font-size:13px;font-weight:500}
/* progress */
.prog{position:absolute;left:0;right:0;bottom:0;padding:16px 28px 20px;z-index:6}
.prog-track{height:3px;background:rgba(var(--ink-rgb),.12);border-radius:2px;overflow:hidden}
.prog-fill{height:100%;background:var(--accent);border-radius:2px}
.pmark{position:absolute;bottom:21px;width:32px;transform:translateX(-50%);display:block}
.pdot{position:absolute;bottom:17.5px;width:10px;height:10px;border-radius:50%;background:var(--accent);transform:translateX(-50%);box-shadow:0 0 0 3px var(--paper)}
/* preview toolbar, never part of a slide */
.tb{position:fixed;top:0;left:0;right:0;z-index:99;display:flex;gap:10px;justify-content:center;align-items:center;padding:12px;background:rgba(246,241,227,.94);border-bottom:1px solid #DCD3BE;font:500 13px sans-serif;color:#2C2A26}
.tb button{font:600 12px sans-serif;padding:7px 12px;border-radius:7px;border:1.5px solid #2C2A26;background:#FBF8EF;color:#2C2A26;cursor:pointer}
body.export{padding:0;gap:0;background:var(--paper)} body.export .tb{display:none} body.export .sw{box-shadow:none}
"""

RUN_JS = r"""
document.fonts.ready.then(() => {
  const body = document.body.classList;
  // highlight-style marker: wrap the accent words in a highlighter span
  if (body.contains('mk-highlight')) document.querySelectorAll('.h-sec, .h-cov .acc').forEach(h => { h.innerHTML = '<span class="hlx">' + h.innerHTML + '</span>'; });
  // section names auto-fit the 342px column, from --h-size down to --h-min (42 to 34 by default)
  const HMIN = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--h-min')) || 34;
  // past the floor it keeps shrinking so nothing ever spills, and render.py warns to shorten the copy
  document.querySelectorAll('.h-sec').forEach(h => { let s = parseFloat(getComputedStyle(h).fontSize);
    while (h.scrollWidth > 342 && s > 22) { s -= .5; h.style.fontSize = s + 'px'; }
    if (s < HMIN) h.dataset.short = 'below floor'; });
  document.querySelectorAll('.kicker').forEach(k => { k.style.whiteSpace = 'nowrap'; let s = parseFloat(getComputedStyle(k).fontSize);
    while (k.scrollWidth > 342 && s > 16) { s -= .5; k.style.fontSize = s + 'px'; } if (s < 20) k.dataset.short = 'below floor'; });
  document.querySelectorAll('.h-cta').forEach(h => { h.style.whiteSpace = 'nowrap'; let s = parseFloat(getComputedStyle(h).fontSize);
    while (h.scrollWidth > 342 && s > 22) { s -= .5; h.style.fontSize = s + 'px'; } });
  // cover lines never wrap: the whole headline shrinks together, down to 38px
  document.querySelectorAll('.h-cov').forEach(h => { let s = parseFloat(getComputedStyle(h).fontSize);
    const wide = () => [...h.children].some(c => c.scrollWidth > 342);
    while (wide() && s > 28) { s -= .5; h.style.fontSize = s + 'px'; } if (s < 38) h.dataset.short = 'below floor'; });
  // the CTA keyword shrinks to fit its block
  document.querySelectorAll('.kw').forEach(k => { let s = parseFloat(getComputedStyle(k).fontSize);
    while (k.scrollWidth > k.clientWidth && s > 24) { s -= 1; k.style.fontSize = s + 'px'; } });
  // marker underline: stretched to the real rendered width of the text above it, plus 6px
  document.querySelectorAll('.mk-wrap').forEach(w => { const h = w.previousElementSibling, r = document.createRange();
    const x0 = h.getBoundingClientRect().left, tw = document.createTreeWalker(h, NodeFilter.SHOW_TEXT); let wd = 0, n;
    while ((n = tw.nextNode())) { r.selectNodeContents(n); for (const q of r.getClientRects()) wd = Math.max(wd, q.right - x0); }
    const svg = w.querySelector('svg'), W = Math.min(342, Math.round(wd + 6)); svg.setAttribute('width', W);
    if (body.contains('mk-bar')) { svg.setAttribute('viewBox', `0 0 ${W} 9`); svg.innerHTML = `<rect x="1" y="2" width="${W * .62}" height="4.5" fill="var(--accent)"/>`; } });
  window.ready = true;
});
function lib() { return window.htmlToImage ? Promise.resolve() : new Promise((ok, no) => { const s = document.createElement('script');
  s.src = 'https://cdnjs.cloudflare.com/ajax/libs/html-to-image/1.11.11/html-to-image.min.js'; s.onload = ok; s.onerror = no; document.head.appendChild(s); }); }
async function dl(i) {
  await lib();
  const el = document.querySelectorAll('.sw')[i];
  const url = await htmlToImage.toPng(el, {pixelRatio: 1080 / 420, width: 420, height: 525, style: {boxShadow: 'none'}});
  const a = document.createElement('a'); a.href = url; a.download = 'slide-' + String(i + 1).padStart(2, '0') + '.png'; a.click();
}
async function dlAll() { const n = document.querySelectorAll('.sw').length; for (let i = 0; i < n; i++) { await dl(i); await new Promise(r => setTimeout(r, 350)); } }
"""

# ----------------------------------------------------------------- drawing helpers


def hand_arrow(p0, p1, p2, p3, color='var(--ink-soft)', w=1.9):
    """One cubic bezier plus a two-stroke head computed from the tangent at the tip
    (P3 - P2), reversed and rotated +/-28 degrees, 11px barbs. Returns SVG paths to
    drop inside an <svg>. Keep the last third of the curve straighter than 28 degrees."""
    tx, ty = p3[0] - p2[0], p3[1] - p2[1]
    L = math.hypot(tx, ty) or 1
    ux, uy = -tx / L, -ty / L
    hs = []
    for a in (math.radians(28), -math.radians(28)):
        hs.append((p3[0] + (ux * math.cos(a) - uy * math.sin(a)) * 11, p3[1] + (ux * math.sin(a) + uy * math.cos(a)) * 11))
    d = f'M{p0[0]},{p0[1]} C{p1[0]},{p1[1]} {p2[0]},{p2[1]} {p3[0]},{p3[1]}'
    hd = f'M{hs[0][0]:.1f},{hs[0][1]:.1f} L{p3[0]},{p3[1]} L{hs[1][0]:.1f},{hs[1][1]:.1f}'
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<path d="{hd}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')


MARKER = ('<div class="mk-wrap"><svg width="150" height="9" viewBox="0 0 150 9" preserveAspectRatio="none">'
          '<path d="M2,6.2 C27,2.6 51,7.6 78,4.6 C102,2.2 126,6.8 148,4.0" fill="none" stroke="var(--accent)" stroke-width="2.6" stroke-linecap="round"/>'
          '<path d="M6,8.1 C39,5.6 69,8.8 99,6.4 C120,4.8 135,7.8 144,6.2" fill="none" stroke="var(--accent)" stroke-width="1.3" stroke-linecap="round" opacity=".72"/></svg></div>')

SPLIT_ARROW = ('<svg class="s-ar" viewBox="0 0 26 14" width="26" height="14"><path d="M2 7.4 C9 6.2 15 7.8 22 7" fill="none" stroke="var(--ink-soft)" '
               'stroke-width="1.8" stroke-linecap="round"/><path d="M17.5 2.8 L22.6 7 L17.8 11.4" fill="none" stroke="var(--ink-soft)" stroke-width="1.8" '
               'stroke-linecap="round" stroke-linejoin="round"/></svg>')

FLOW_ARROW = ('<svg class="f-ar" width="30" height="12" viewBox="0 0 30 12"><path d="M2 6.4 C10 5.4 17 6.8 25 6" fill="none" stroke="var(--ink-soft)" stroke-width="1.7" stroke-linecap="round"/>'
              '<path d="M20.5 2 L25.6 6 L20.8 10.2" fill="none" stroke="var(--ink-soft)" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def cue_arrow(color='currentColor'):
    return (f'<svg width="62" height="18" viewBox="0 0 62 18" fill="none" stroke="{color}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M3 9.4 C16 7.4, 34 10.6, 52 8.6"/><path d="M44 3 L53.5 8.6 L44.5 14.6"/></svg>')


def silhouette(w, color='#3B3833'):
    """A generic head-and-shoulders figure, for mock-up frames."""
    return (f'<svg width="{w}" height="{w * .92:.0f}" viewBox="0 0 100 92" style="position:absolute;left:50%;bottom:-2px;transform:translateX(-50%)">'
            f'<circle cx="50" cy="30" r="21" fill="{color}"/><path d="M6,92 C6,66 24,54 50,54 C76,54 94,66 94,92 Z" fill="{color}"/></svg>')


# ----------------------------------------------------------------- slide builders
# Each returns a dict {'kind', 'html'}; write_carousel() adds substrate and progress.

ROW_ARROW = ('<svg width="11" height="12" viewBox="0 0 11 12" style="display:block;margin-top:4px"><path d="M2 1.5 V7.5 H9" fill="none" '
             'stroke="var(--accent)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>'
             '<path d="M6.6 5 L9.2 7.5 L6.6 10" fill="none" stroke="var(--accent)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def rows_html(rows):
    """rows: list of (lead_in, rest). The lead-in is the opening words of the sentence, never a label.
    The bullet (arrow, dot, dash, number, prompt) comes from the style."""
    return ''.join(f'<div class="row"><span class="ar">{ROW_ARROW}</span><span><span class="rl">{a}</span> {b}</span></div>' for a, b in rows)


def section(chip, kicker, name, rows, artifact='', close=''):
    """The section slide: chip, kicker, accent name, marker, rows, pinned artifact, optional hand-note close."""
    cl = f'<div class="hand close">{close}</div>' if close else ''
    return {'kind': 'section', 'html':
            f'<div class="content"><span class="chip">{chip}</span><div class="kicker">{kicker}</div><h2 class="h-sec">{name}</h2>{MARKER}'
            f'<div class="rows">{rows_html(rows)}</div><div class="artifact">{artifact}</div>{cl}</div>'}


def cover_type(lines, accent=1, sub='', figure=None, figure_w=190, mascot=True, size=48, cards=None):
    """COVER_TYPE / COVER_BLEED. lines: the headline, three or four lines
    ("How to make", "carousels", "in 10 minutes"); accent: index of the line in the accent.
    size: headline px (48 default; auto-shrinks to 38 so no line wraps). With no figure or mascot,
    raise size or add a figure so the lower half is not empty paper.
    figure: optional transparent cutout bleeding off the bottom right. No chip, no progress bar.
    cards: optional list of up to 3 (eyebrow, name) pairs shown as a row of small cards above the
    handle, a preview of what is inside. The fix for an empty lower half when there is no figure."""
    row = ''
    if cards:
        row = ('<div class="cov-cards">' + ''.join(f'<div class="card cc"><div class="mono">{e}</div><div class="cc-n">{n}</div></div>'
                                                  for e, n in cards[:3]) + '</div>')
    head = ''.join(f'<span class="acc">{l}</span>' if k == accent else f'<span class="ln">{l}</span>' for k, l in enumerate(lines))
    fig = f'<img class="cov-fig" src="{data_uri(figure)}" style="width:{figure_w}px">' if figure else ''
    return {'kind': 'cover', 'figure': bool(figure), 'mascot': mascot, 'html':
            f'<div class="content cov"><h1 class="h-cov" style="font-size:{size}px">{head}</h1>{MARKER}'
            f'<div class="cov-sub">{sub}</div>__MASCOT__<div class="cue">__CUE__ {cue_arrow()}</div>{row}</div>{fig}<div class="handle">__HANDLE__</div>'}


def cover_art(image, l1, big, l3, font='Anton', big_px=86, small_px=34, cue=None):
    """Poster cover over full-bleed generated art. Pick a headline face that matches the art
    (Anton for cyberpunk or poster art); add it to write_carousel(extra_fonts=[...])."""
    return {'kind': 'art', 'cue': cue, 'html':
            f'<div class="art"><img class="bg" src="{data_uri(image)}"><div class="dim"></div><div class="sc"></div>'
            f'<div class="hd" style="font-family:\'{font}\'"><div style="font-size:{small_px}px">{l1}</div>'
            f'<div class="big" style="font-size:{big_px}px">{big}</div><div style="font-size:{small_px}px">{l3}</div></div>'
            f'<div class="foot"><div class="cue">__CUE__ {cue_arrow("#F8F5EC")}</div><div class="hn">__HANDLE__</div></div></div>'}


def cta(question, accent_q, keyword=None, promise=None, toolbar='', label=None, big=None):
    """CTA_STACK closer, in the mode voice.cta picks:
    keyword: cta(q, a, 'MOTION') -> "comment MOTION" is the largest element (for a DM automation)
    follow:  cta(q, a)           -> the handle is the largest element, with a follow ask
    save:    cta(q, a, big='save this', label='', promise='so it is here when you need it.')
    promise defaults to the right line for each mode."""
    tb = f'<div class="toolbar">{toolbar}</div>' if toolbar else ''
    if big:
        lb, promise = (label if label is not None else ''), (promise or '')
    elif keyword:
        big, lb = f'&ldquo;{keyword}&rdquo;', label or 'comment'
        promise = promise or 'and I&rsquo;ll DM you everything.'
    else:
        big, lb = '__HANDLE__', label or 'follow'
        promise = promise or 'for a new one every week.'
    return {'kind': 'cta', 'html':
            f'<div class="content ctac"><h2 class="h-cta">{question}<br><span class="accent">{accent_q}</span></h2>'
            f'<div class="kw-block"><div class="kw-lb">{lb}</div><div class="kw">{big}</div></div>'
            f'<p class="promise">{promise}</p>{tb}__LOCKUP__</div>'}


def raw(html, kind='section'):
    """Escape hatch: any custom content block. Wrap it in <div class="content">...</div>."""
    return {'kind': kind, 'html': html}


# ----------------------------------------------------------------- artifact builders


def card(body, bar=None, bar_right=''):
    top = f'<div class="pop-bar"><span>{bar}</span><b>{bar_right}</b></div>' if bar else ''
    return f'<div class="card">{top}{body}</div>'


def cmd(text):
    """A prompt line. Put it inside card(); bare on paper it looks unframed."""
    return f'<div class="cmd"><span class="p">&gt;</span>{text}</div>'


def output(text, label='CLAUDE', pad=(9, 12, 12), size=11.5):
    """A sample of the reply, set under a cmd() inside the same card. The usual way to grow
    an under-built SPEC_ROWS prompt card: prompt, then what comes back. To take up exactly N more
    px, add N to pad[0] and pad[2] between them, or raise size. Do not also label the card's
    bar with the same word as `label` (nothing said twice)."""
    t, x, b = pad
    return (f'<div style="padding:{t}px {x}px {b}px"><div class="mono" style="font-size:7.5px;margin-bottom:5px">{label}</div>'
            f'<div style="font-size:{size}px;line-height:1.5;color:var(--ink)">{text}</div></div>')


def split(lb_bad, bad, cv_bad, lb_good, good, cv_good):
    """SPLIT_COMPARE panes. bad/good: inner HTML, 138px wide (e.g. 138x150). Labels must fit one line."""
    return (f'<div class="split"><div class="pane bad"><div class="lb">{lb_bad}</div><div class="box">{bad}</div><div class="cv">{cv_bad}</div></div>'
            f'{SPLIT_ARROW}<div class="pane good"><div class="lb">{lb_good}</div><div class="box">{good}</div><div class="cv">{cv_good}</div></div></div>')


def flow(steps):
    """PROCESS_FLOW band. steps: list of (icon_html, label_html), 3 to 4 of them."""
    parts = [f'<div class="fstep">{ic}<div class="fl">{lb}</div></div>' for ic, lb in steps]
    return '<div class="flow">' + FLOW_ARROW.join(parts) + '</div>'


def annotated(inner, w, h, notes):
    """ANNOTATED_SHOT. inner: HTML of the thing being annotated, absolutely positioned inside a w x h box.
    notes: list of ((x, y), text, (p0, p1, p2, p3)); each arrow must end on a specific region.
    Start each arrow at the label's left edge, about 8px below its top for a one-line label
    (handwriting fonts sit low). Labels are w - x wide; break with <br> to avoid orphans.
    render.py checks that everything inside stays within the w x h box."""
    labels = ''.join(f'<div class="hand" style="position:absolute;left:{x}px;top:{y}px;max-width:{w - x}px;color:var(--ink)">{t}</div>'
                     for (x, y), t, _ in notes)
    arrows = ''.join(hand_arrow(*pts) for *_, pts in notes)
    return (f'<div class="ann" style="position:relative;height:{h}px">{inner}{labels}'
            f'<svg width="{w}" height="{h}" style="position:absolute;left:0;top:0;overflow:visible">{arrows}</svg></div>')


def screenshot(path, bar='SCREENSHOT', bar_right='', crop_h=None):
    """A real screenshot, always inside a card frame. crop_h crops to the band that matters (px at 342 wide)."""
    style = f'height:{crop_h}px;object-fit:cover;object-position:top' if crop_h else ''
    return card(f'<img class="shot" src="{data_uri(path)}" style="{style}">', bar, bar_right)


# ----------------------------------------------------------------- icons (ink with accent detail, follow the style)

_I, _C = 'var(--ink)', 'var(--card)'
ICON_BROWSER = (f'<svg width="44" height="40" viewBox="0 0 44 40"><rect x="2" y="4" width="40" height="32" rx="4" fill="{_C}" stroke="{_I}" stroke-width="1.6"/>'
                f'<path d="M2,12 L42,12" stroke="{_I}" stroke-width="1.6"/><circle cx="7" cy="8" r="1.4" fill="var(--accent)"/><circle cx="11.5" cy="8" r="1.4" fill="{_I}"/>'
                f'<rect x="8" y="17" width="16" height="13" rx="2" fill="var(--accent)" opacity=".85"/><path d="M28,19 L37,19 M28,24 L35,24 M28,29 L36,29" stroke="{_I}" stroke-width="1.5" stroke-linecap="round"/></svg>')
ICON_FOLDER = (f'<svg width="46" height="40" viewBox="0 0 46 40"><path d="M3,9 C3,7 4,6 6,6 L17,6 L21,10 L40,10 C42,10 43,11 43,13 L43,33 C43,35 42,36 40,36 L6,36 C4,36 3,35 3,33 Z" '
               f'fill="{_C}" stroke="{_I}" stroke-width="1.6" stroke-linejoin="round"/><path d="M3,15 L43,15" stroke="{_I}" stroke-width="1.4"/>'
               '<rect x="12" y="20" width="9" height="10" rx="1.5" fill="var(--accent)"/><rect x="24" y="20" width="9" height="10" rx="1.5" fill="none" stroke="var(--accent)" stroke-width="1.5"/></svg>')
ICON_CHAT = (f'<svg width="44" height="40" viewBox="0 0 44 40"><path d="M5,6 L39,6 C41,6 42,7 42,9 L42,26 C42,28 41,29 39,29 L18,29 L10,36 L10,29 L5,29 C3,29 2,28 2,26 L2,9 C2,7 3,6 5,6 Z" '
             f'fill="{_C}" stroke="{_I}" stroke-width="1.6" stroke-linejoin="round"/><path d="M10,14 L34,14 M10,21 L27,21" stroke="var(--accent)" stroke-width="2" stroke-linecap="round"/></svg>')
ICON_PHONE = (f'<svg width="30" height="40" viewBox="0 0 30 40"><rect x="3" y="2" width="24" height="36" rx="4" fill="{_C}" stroke="{_I}" stroke-width="1.6"/>'
              f'<rect x="7" y="8" width="16" height="20" rx="1.5" fill="var(--accent)" opacity=".85"/><circle cx="15" cy="33" r="1.6" fill="{_I}"/></svg>')
ICON_SPARK = ('<svg width="40" height="40" viewBox="0 0 40 40"><g stroke="var(--accent)" stroke-width="3.2" stroke-linecap="round">'
              + ''.join(f'<path d="M{20 + 5 * math.cos(a):.1f},{20 + 5 * math.sin(a):.1f} L{20 + 17 * math.cos(a):.1f},{20 + 17 * math.sin(a):.1f}"/>'
                        for a in [k * math.tau / 10 for k in range(10)]) + '</g></svg>')


# ----------------------------------------------------------------- assemble


def _progress(i, total, brand):
    pct = i / (total - 1)          # i is zero-indexed: the cover (0) has no bar, the closer shows 100%
    left = 28 + 364 * pct
    mark = (f'<img class="pmark" src="{data_uri(brand["mascot"])}" style="left:{left:.1f}px">' if brand.get('mascot')
            else f'<div class="pdot" style="left:{left:.1f}px"></div>')
    return (f'<div class="prog"><div class="prog-track"><div class="prog-fill" style="width:{pct * 100:.2f}%"></div></div>{mark}</div>')


def _lockup(brand):
    av = (f'<img src="{data_uri(brand["avatar"])}" alt="">' if brand.get('avatar')
          else f'<div class="ini">{brand["handle"].lstrip("@")[:1].upper()}</div>')
    return (f'<div class="lockup"><div class="avf">{av}</div><div class="lk-txt"><div class="lk-name">{brand["handle"]}</div>'
            f'<div class="lk-tag">{brand.get("tagline", "")}</div></div></div>')


def write_carousel(path, slides, brand, title='carousel', extra_fonts=(), extra_css='', quiet=False):
    """Assemble every slide into one self-contained HTML file. extra_css is appended after the kit's CSS."""
    total = len(slides)
    root_vars, body_cls = style_vars(brand['style'])
    out = []
    for i, s in enumerate(slides):
        h = s['html']
        if '__MASCOT__' in h:
            m = (f'<img class="cov-mascot" src="{data_uri(brand["mascot"])}" style="width:58px;transform:rotate(-6deg)">'
                 if brand.get('mascot') and s.get('mascot') else '')
            h = h.replace('__MASCOT__', m)
        h = (h.replace('__CUE__', s.get('cue') or brand['voice'].get('swipe_cue', 'swipe'))
              .replace('__LOCKUP__', _lockup(brand)).replace('__HANDLE__', brand['handle']))
        under = '' if s['kind'] == 'art' else '<div class="grid-l"></div><div class="grain-l"></div>'
        bar = '' if s['kind'] in ('cover', 'art') else _progress(i, total, brand)
        out.append(f'<div class="sw" id="s{i + 1}">{under}{h}{bar}</div>')
    btns = ''.join(f'<button onclick="dl({i})">{i + 1}</button>' for i in range(total))
    doc = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
           f'<title>{title}</title><style>{font_css(brand, extra_fonts)}{root_vars}{CSS}{extra_css}</style>'
           f'</head><body class="{body_cls}">'
           f'<div class="tb">Download PNG: {btns}<button onclick="dlAll()">all</button></div>{"".join(out)}'
           f'<script>{RUN_JS}</script></body></html>')
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(doc, encoding='utf-8')
    if not quiet:
        print(f'wrote {path} ({total} slides)')
    return path
