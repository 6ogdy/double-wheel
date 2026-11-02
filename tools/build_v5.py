"""v5: reference look, flat wheel + new rounded gems.
usage: build_v5.py [full|whole]   (run from the repo root; needs pillow, numpy, scipy; run build_v4.py first)
- ring: thick rims removed, flat track with a thin bronze outline, flatter medallion
- gems: new rounded faceted sprites, no pale frame, stronger drop shadow so they sit on the wheel
Reads assets/wheel-v4/game-published, writes assets/wheel-v5/game-published.
'full' writes assets/wheel-v5full instead: outer band + inner band + carved separators between the gems.
'whole' writes assets/wheel-v5whole: the entire ring is one uniform carved Greek-key ornament (identical rows, no separators)."""
import os, re, sys, shutil, numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy.ndimage import map_coordinates

SRC = 'assets/wheel-v4/game-published'
MODE = next((a for a in sys.argv[1:] if a in ('full', 'whole')), '')
FULL = MODE == 'full'
WHOLE = MODE == 'whole'
N = int(os.environ.get('N', 20))       # wheel positions; N=25 matches the live game (assets/wheel-v5<mode>-25)
STEP = 360 / N
SH = 0 if N == 20 else 14      # N=25: medallion and inner key band move out by SH px, so the gap gem-inner band equals the gap gem-outer band (gems: 29 vs 15 px before)
ROOT = 'assets/wheel-v5' + MODE + ('' if N == 20 else f'-{N}')
OUT = f'{ROOT}/game-published'
MED = 'static/media'
C = 500.0

def smooth(a, b, x): t = np.clip((x - a) / (b - a), 0, 1); return t * t * (3 - 2 * t)
def load(p): return np.asarray(Image.open(p).convert('RGBA')).astype(np.float32) / 255
def save_webp(a, p): Image.fromarray((np.clip(a, 0, 1) * 255 + .5).astype(np.uint8), 'RGBA').save(p, quality=92)

# ---------------------------------------------------------------- ring
BAND_IN, BAND_OUT = 470.0, 496.0      # outer ornament band (outside the gems, which end ~455)
N_KEY = 64                              # Greek-key repeats around the wheel (outer band)

def key_strip(n_key=N_KEY, r_in=BAND_IN, r_out=BAND_OUT):
    """Greek-key (stepped meander) band as a flat strip: height = band, width = n_key repeats."""
    SSs = 4
    H = int((r_out - r_in) * SSs); u = H / 7.0           # 7 grid units tall
    per = int(6 * u); Wd = per * n_key
    im = Image.new('L', (Wd, H), 0); d = ImageDraw.Draw(im)
    lw = max(2, int(u * 1.0))
    for k in range(n_key):
        x0 = k * per
        pts = [(0, 6), (0, 1), (5, 1), (5, 4), (2, 4), (2, 3), (3, 3)]       # the hook
        d.line([(x0 + a * u, b * u) for a, b in pts], fill=255, width=lw, joint='curve')
        d.line([(x0, 6 * u), (x0 + 6 * u, 6 * u)], fill=255, width=lw)       # base line joins the repeats
    return im, per / SSs

def key_band(col, rho, ang, r_in, r_out, n_key, bed=None, keyc=None, strength=1.0):
    """darker bed with a carved Greek-key relief (light edge up-left, shade down-right)"""
    strip, per = key_strip(n_key, r_in, r_out)
    Hs, Ws = strip.size[1], strip.size[0]
    sa = np.asarray(strip.filter(ImageFilter.GaussianBlur(1.6)), np.float32) / 255
    u_ = (ang % (2 * np.pi)) / (2 * np.pi) * Ws
    v_ = (rho - r_in) / (r_out - r_in) * Hs
    relief = map_coordinates(sa, [np.clip(v_, 0, Hs - 1), u_ % Ws], order=1, mode='nearest')
    gy, gx = np.gradient(relief)
    lit = np.clip((-gx * np.sin(ang) - gy * np.cos(ang)) * 5, -1, 1)   # light from the upper left, projected on the screen
    bed = np.array([.12, .07, .035] if bed is None else bed, np.float32)
    keyc = np.array([.34, .215, .105] if keyc is None else keyc, np.float32)
    band = bed * (1 - relief[..., None]) + keyc * relief[..., None]
    band = np.clip(band * (1 + .55 * lit[..., None]), 0, 1)
    bm = (smooth(r_in - 1.5, r_in + 1, rho) * (1 - smooth(r_out - 1.5, r_out + .5, rho)))[..., None]
    bm = bm * strength
    return col * (1 - bm) + band * bm

def separators(col, rho, ang):
    """Carved divider between neighbouring gems (the gems sit at (n-2)*18 deg, so the gaps are at 9 + 18k deg):
    a raised bar with a lit edge, a shaded edge and a groove down the middle."""
    step = np.radians(STEP)
    off = (ang % step) - step / 2                                        # signed angle to the nearest gap (gems sit at multiples of step)
    arc = off * rho                                                       # signed distance across the bar, px
    zone = smooth(298, 304, rho) * (1 - smooth(462, 468, rho))
    bar = (1 - smooth(3.2, 4.6, np.abs(arc))) * zone
    groove = (1 - smooth(.5, 1.4, np.abs(arc))) * zone
    edge = np.clip(-arc / 4.0, -1, 1) * bar                               # lit on one side, shaded on the other
    light = np.array([.30, .19, .09], np.float32)
    out = col * (1 - bar[..., None] * .8) + light * (bar[..., None] * .8)
    out = out * (1 + .5 * edge[..., None]) * (1 - .55 * groove[..., None])
    return np.clip(out, 0, 1)

def grow_medallion(img):
    """new radius -> source radius: [0, 262+SH] <- [0, 262], beyond that the track is shifted by SH"""
    if not SH: return img
    h, w = img.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    dx, dy = xx + .5 - C, yy + .5 - C
    rho = np.hypot(dx, dy)
    old = np.where(rho < 262 + SH, rho * 262 / (262 + SH), rho - SH)
    k = old / np.maximum(rho, 1e-6)
    coords = [np.clip(C + dy * k - .5, 0, h - 1), np.clip(C + dx * k - .5, 0, w - 1)]
    return np.dstack([map_coordinates(img[..., i], coords, order=1, mode='nearest') for i in range(img.shape[2])])

def flat_ring(img, flat):
    img = grow_medallion(img)
    h, w = img.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    dx, dy = xx + .5 - C, yy + .5 - C
    rho = np.hypot(dx, dy); ang = np.arctan2(dy, dx)
    # track colour: mean of the real track (sampling a single radius would smear radial streaks into the rim zones)
    ring = (rho > 320) & (rho < 450)
    track = np.broadcast_to(img[..., :3][ring].mean(0), img[..., :3].shape)
    out = img.copy()
    rgb = img[..., :3]
    # medallion: flatter, calendar pattern only faintly visible, soft darkening towards the edge
    flat = np.array(flat, np.float32)
    med = rgb * .45 + flat * .55
    med = med * (1 - .35 * smooth(215, 266 + SH, rho))[..., None]
    mm = (1 - smooth(260 + SH, 268 + SH, rho))[..., None]
    base = med * mm
    # track zone (everything between the medallion and the outer edge)
    tz = (smooth(260 + SH, 268 + SH, rho) * (1 - smooth(478, 481, rho)))[..., None]
    wz = np.clip((smooth(262 + SH, 270 + SH, rho) * (1 - smooth(296 + SH, 304 + SH, rho)) + smooth(456, 464, rho))[..., None], 0, 1)
    col = base * (1 - tz) + (rgb * (1 - wz) + track * wz) * tz
    # no highlighted outlines (reference has none): only a soft shade where the track meets the medallion and the outer edge
    shade = 1 - .22 * (1 - smooth(266 + SH, 290 + SH, rho)) * smooth(262 + SH, 270 + SH, rho) - .28 * smooth(458, 480, rho)
    col = col * shade[..., None]
    if WHOLE:
        # one uniform ornament over the whole ring, medallion edge to outer edge: identical rows, one size, one colour, one relief
        t = np.array(track[0, 0], np.float32)
        r0, r1, rows = 268.0, BAND_OUT, 8
        for i in range(rows):
            a, b = r0 + (r1 - r0) * i / rows, r0 + (r1 - r0) * (i + 1) / rows
            col = key_band(col, rho, ang, a, b, round(2 * np.pi * (a + b) / 2 / (6 * (b - a) / 7)), bed=t * .78, keyc=t * 1.34)
    else:
        col = key_band(col, rho, ang, BAND_IN, BAND_OUT, N_KEY)
    if FULL:
        col = key_band(col, rho, ang, 270.0 + SH, 296.0 + SH, round(2 * np.pi * (283 + SH) / (6 * 26 / 7)))
        if N == 20: col = separators(col, rho, ang)   # no carved dividers at N=25: gems are bigger
    out[..., :3] = col
    out[..., 3] = 1 - smooth(BAND_OUT - 1.0, BAND_OUT + 1.2, rho)
    return out

# ---------------------------------------------------------------- gems
GEM_W, GEM_H, SS = 450, 342, 3

def gem_sprite(rgb):
    W, H = GEM_W * SS, GEM_H * SS
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    x = (xx + .5 - W / 2) / (W / 2 - 6 * SS); y = (yy + .5 - H / 2) / (H / 2 - 6 * SS)
    # rounded rectangle with soft chamfers: superellipse intersected with a diamond
    se = np.abs(x) ** 4.2 + np.abs(y) ** 4.2
    dia = (np.abs(x) + np.abs(y)) / 1.62
    f = np.maximum(se, dia ** 4)
    inside = f <= 1.0
    d = 1 - f                                            # >0 inside; grows towards the centre
    base = np.array(rgb, np.float32) / 255
    dark = base * .42; mid = base; light = base * .55 + .45
    t = smooth(0, .30, d)[..., None]
    col = dark * (1 - t) + mid * t
    glow = np.exp(-((x * .9) ** 2 + (y * 1.1) ** 2) * 2.2)[..., None]
    col = col * (1 - .55 * glow) + light * .55 * glow
    # facets: table octagon + 8 triangles, alternate lighter / darker
    L = Image.new('L', (W, H), 128); dr = ImageDraw.Draw(L)
    cx, cy = W / 2, H / 2
    def P(u, v): return (cx + u * (W / 2 - 6 * SS), cy + v * (H / 2 - 6 * SS))
    outer = [(-.78, -.98), (.78, -.98), (.98, -.70), (.98, .70), (.78, .98), (-.78, .98), (-.98, .70), (-.98, -.70)]
    table = [(-.46, -.52), (.46, -.52), (.60, -.30), (.60, .30), (.46, .52), (-.46, .52), (-.60, .30), (-.60, -.30)]
    mid = lambda a, b: ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    for i in range(8):
        j = (i + 1) % 8
        m = mid(outer[i], outer[j])
        dr.polygon([P(*outer[i]), P(*m), P(*table[i])], fill=(215 if i % 2 else 55))
        dr.polygon([P(*m), P(*outer[j]), P(*table[j]), P(*table[i])], fill=(95 if i % 2 else 185))
    # table: four kite facets around a bright crown
    c0 = (0, 0)
    dr.polygon([P(*q) for q in table], fill=150)
    dr.polygon([P(-.46, -.52), P(0, -.1), P(-.6, 0)], fill=205); dr.polygon([P(.46, -.52), P(.6, 0), P(0, -.1)], fill=95)
    dr.polygon([P(-.6, 0), P(0, .12), P(-.46, .52)], fill=110); dr.polygon([P(.6, 0), P(.46, .52), P(0, .12)], fill=190)
    dr.polygon([P(-.46, -.52), P(.46, -.52), P(0, -.1)], fill=225)
    L = L.filter(ImageFilter.GaussianBlur(1.2 * SS))
    k = (np.asarray(L).astype(np.float32) / 128 - 1)[..., None]
    col = np.clip(col * (1 + .42 * k), 0, 1)
    # thin bright facet edges
    E = Image.new('L', (W, H), 0); de = ImageDraw.Draw(E)
    for i in range(8):
        j = (i + 1) % 8
        de.line([P(*table[i]), P(*table[j])], fill=150, width=2 * SS)
        de.line([P(*table[i]), P(*outer[i])], fill=110, width=2 * SS)
    E = np.asarray(E.filter(ImageFilter.GaussianBlur(.8 * SS))).astype(np.float32)[..., None] / 255
    col = col + (1 - col) * E * .55
    # jewel rim: light line just inside the border, dark outline outside it
    rim = (smooth(.015, .05, d) * (1 - smooth(.06, .11, d)))[..., None]
    col = col + (light - col) * rim * .85
    edge = (1 - smooth(0, .035, d))[..., None]
    col = col * (1 - edge * .65)
    # gloss band top-left and sparkles
    gl = np.exp(-(((x + .42) / .55) ** 2 + ((y + .52) / .22) ** 2))[..., None] * (d[..., None] > .08)
    col = col + (1 - col) * gl * .42
    for sx, sy, r in ((-.5, -.55, .13), (.42, .5, .09), (.1, .05, .07)):
        s = np.exp(-((np.abs(x - sx) * 9) ** 1.2 + (np.abs(y - sy) * 9) ** 1.2) * 1.0) * r * 6
        s = np.clip(np.exp(-(np.hypot(x - sx, y - sy) / (r * .35)) ** 1.5) + .6 * np.exp(-(np.minimum(np.abs(x - sx), np.abs(y - sy)) / (r * .05)) ** 2) * np.exp(-(np.hypot(x - sx, y - sy) / r) ** 2), 0, 1)[..., None]
        col = col + (1 - col) * s
    alpha = smooth(0, .012, d)
    out = np.dstack([np.clip(col, 0, 1), alpha])
    im = Image.fromarray((out * 255 + .5).astype(np.uint8), 'RGBA').resize((GEM_W, GEM_H), Image.LANCZOS)
    return im

GEMS = {'gold.d53168443bfda397846e': (255, 138, 18), 'green.f25c93dd911fde41af2f': (24, 200, 70),
        'blue.52c7c705f881c6ec951f': (36, 130, 255), 'pink.8cfdeb4e09969b101163': (226, 40, 226),
        'violet.fe2430dc563bad88d219': (140, 62, 232)}

if os.path.exists(ROOT): shutil.rmtree(ROOT)
shutil.copytree(SRC, OUT)
for n, flat in (('blw.aca7b4f092b7011ac227.webp', (.20, .035, .13)), ('brw.f635fb57c5c829d76274.webp', (.03, .15, .05))):
    save_webp(flat_ring(load(f'{SRC}/{MED}/{n}'), flat), f'{OUT}/{MED}/{n}')
# gems: the owner chose the original sprites (v2/v3a) over the generated ones (gem_sprite above, kept for reference)
ORIG = 'assets/wheel-v3a/game-published'
for n in GEMS:
    shutil.copyfile(f'{ORIG}/{MED}/{n}.webp', f'{OUT}/{MED}/{n}.webp')

# no fall-in when entering the game: the wheels are already in place; later rounds keep their drop
js = f'{OUT}/static/js/main.d348ebcc.js'
code = open(js, encoding='utf-8').read()
def sub(old, new):
    global code
    assert code.count(old) == 1, old
    code = code.replace(old, new)
sub('nu.set(".wheel_stonesCon",{y:-1500,opacity:0}),"IN_PROGRESS"', 'nu.set(".wheel_stonesCon",{y:0,opacity:1}),"IN_PROGRESS"')
sub('nu.set(".wheel_stonesCon2",{y:1500,opacity:0}),"IN_PROGRESS"', 'nu.set(".wheel_stonesCon2",{y:0,opacity:1}),"IN_PROGRESS"')
sub('nu.set(".wheel_stonesCon",{y:-1500,opacity:0}),nu.set(this.finalValue,{opacity:0}),nu.to(".wheel_stonesCon",{y:0,opacity:1,duration:1,ease:"bounce.out"})',
    'window.__w1?(nu.set(".wheel_stonesCon",{y:-1500,opacity:0}),nu.set(this.finalValue,{opacity:0}),nu.to(".wheel_stonesCon",{y:0,opacity:1,duration:1,ease:"bounce.out"})):(window.__w1=1,nu.set(this.finalValue,{opacity:0}))')
sub('nu.set(".wheel_stonesCon2",{y:1500,opacity:0}),nu.set(this.finalValue2,{opacity:0}),nu.to(".wheel_stonesCon2",{y:0,opacity:1,duration:1,ease:"bounce.out",delay:.5})',
    'window.__w2?(nu.set(".wheel_stonesCon2",{y:1500,opacity:0}),nu.set(this.finalValue2,{opacity:0}),nu.to(".wheel_stonesCon2",{y:0,opacity:1,duration:1,ease:"bounce.out",delay:.5})):(window.__w2=1,nu.set(this.finalValue2,{opacity:0}))')
open(js, 'w', encoding='utf-8').write(code)

# gems sit on the wheel: stronger contact shadow
ix = f'{OUT}/index.html'
html = open(ix).read()
old = 'filter:drop-shadow(0 4px 5px rgba(0,0,0,.6))'
assert html.count(old) == 1
html = html.replace(old, 'filter:drop-shadow(0 6px 3px rgba(0,0,0,.7)) drop-shadow(0 0 5px rgba(0,0,0,.45))')
open(ix, 'w').write(html)
# v5 sprites are centred in their box, so the gem centre goes on the middle of the free track:
# inner outline ends ~291, outer outline starts ~469 -> R=380 (v4 used 391.5 for its off-centre sprites)
import math
W_GEM, R_GEM = (150, 380.0) if N == 20 else (130, 390.0)   # N=25: largest width that keeps >=4 px between neighbours (out/fit25.py)
gh = W_GEM * 342 / 450
html = open(ix).read()
extra = []
for n in range(1, N + 1):
    t = math.radians((n - 2) * STEP)
    l = 500 + R_GEM * math.cos(t) - W_GEM / 2; tp = 500 + R_GEM * math.sin(t) - gh / 2
    new = f'.stonesCon img.s{n}{{left:{l:.1f}px;top:{tp:.1f}px;transform:rotate({(n - 2) * STEP:.2f}deg)}}'
    html, k = re.subn(r'\.stonesCon img\.s%d\{[^}]*\}' % n, lambda m, new=new: new, html)
    if k == 0: extra.append(new)        # positions 21..25 have no rule in the 20-position game
    assert k <= 1, (n, k)
if extra: html = html.replace('</head>', '<style>' + ''.join(extra) + '</style></head>')
if N != 20:
    html = html.replace('width:150px!important', f'width:{W_GEM}px!important')
    # 20 -> N positions: same four hard-coded spots in main.js as tools/build_n.py, and the original 25-position replay
    half = int(STEP // 2)
    rv = [(0, half, 2)] + [(math.floor(j * STEP - STEP / 2) + 1, math.floor(j * STEP + STEP / 2), (N + 2 - j - 1) % N + 1) for j in range(1, N)] + [(math.floor(360 - STEP / 2) + 1, 360, 2)]
    lit = 'rotationValues=[' + ','.join('{minDegree:%d,maxDegree:%d,value:%d}' % r for r in rv) + ']'
    code = open(js, encoding='utf-8').read()
    code, a = re.subn(r'rotationValues=\[\{minDegree:0,maxDegree:\d+,value:2\}.*?\{minDegree:\d+,maxDegree:360,value:2\}\]', lambda m: lit, code)
    code, b = re.subn(r'this\.data=\[[0-9.,]+\]', lambda m: 'this.data=[' + ','.join(['%g' % STEP] * N) + ']', code)
    code, c = re.subn(r'maxDegree\)-\d+', lambda m: 'maxDegree)-%d' % half, code)
    code, d = re.subn(r'\(r\+5\)%\d+', lambda m: '(r+5)%%%d' % N, code)
    assert (a, b, c, d) == (2, 2, 2, 2), (a, b, c, d)
    open(js, 'w', encoding='utf-8').write(code)
    assert N == 25, 'replay.js comes from the original 25-position game'
    orig = open('out/game_pub_fig/replay.js', encoding='utf-8').read()
    pat = r'var VISUAL = .*;\n  var ROUNDS = .*;\n'
    rp = f'{OUT}/replay.js'; cur = open(rp, encoding='utf-8').read()
    assert len(re.findall(pat, orig)) == 1 and len(re.findall(pat, cur)) == 1
    keep = re.search(pat, orig).group(0)
    open(rp, 'w', encoding='utf-8').write(re.sub(pat, lambda m: keep, cur))
open(ix, 'w').write(html)
print('ok')
