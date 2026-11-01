"""v5: reference look, flat wheel + new rounded gems.
usage: build_v5.py   (run from the repo root; needs pillow, numpy, scipy; run build_v4.py first)
- ring: thick rims removed, flat track with a thin bronze outline, flatter medallion
- gems: new rounded faceted sprites, no pale frame, stronger drop shadow so they sit on the wheel
Reads assets/wheel-v4/game-published, writes assets/wheel-v5/game-published."""
import os, re, shutil, numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy.ndimage import map_coordinates

SRC = 'assets/wheel-v4/game-published'
OUT = 'assets/wheel-v5/game-published'
MED = 'static/media'
C = 500.0

def smooth(a, b, x): t = np.clip((x - a) / (b - a), 0, 1); return t * t * (3 - 2 * t)
def load(p): return np.asarray(Image.open(p).convert('RGBA')).astype(np.float32) / 255
def save_webp(a, p): Image.fromarray((np.clip(a, 0, 1) * 255 + .5).astype(np.uint8), 'RGBA').save(p, quality=92)

# ---------------------------------------------------------------- ring
def flat_ring(img, flat):
    h, w = img.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    dx, dy = xx + .5 - C, yy + .5 - C
    rho = np.hypot(dx, dy); ang = np.arctan2(dy, dx)
    # track colour + texture sampled from the middle of the track, same angle
    sx, sy = C + 380 * np.cos(ang), C + 380 * np.sin(ang)
    track = np.stack([map_coordinates(img[..., c], [sy - .5, sx - .5], order=1) for c in range(3)], -1)
    out = img.copy()
    rgb = img[..., :3]
    # medallion: flatter, calendar pattern only faintly visible, soft darkening towards the edge
    flat = np.array(flat, np.float32)
    med = rgb * .45 + flat * .55
    med = med * (1 - .35 * smooth(215, 266, rho))[..., None]
    mm = (1 - smooth(260, 268, rho))[..., None]
    base = med * mm
    # track zone (everything between the medallion and the outer edge)
    tz = (smooth(260, 268, rho) * (1 - smooth(478, 481, rho)))[..., None]
    # sampled texture only where the old rims were; the real track keeps its own texture (no radial streaks)
    wz = (smooth(262, 270, rho) * (1 - smooth(296, 304, rho)) + smooth(456, 464, rho))[..., None]
    wz = np.clip(wz, 0, 1)
    col = base * (1 - tz) + (rgb * (1 - wz) + track * wz) * tz
    # no highlighted outlines (reference has none): only a soft shade where the track meets the medallion and the outer edge
    shade = 1 - .22 * (1 - smooth(266, 290, rho)) * smooth(262, 270, rho) - .28 * smooth(458, 480, rho)
    col = col * shade[..., None]
    out[..., :3] = col
    out[..., 3] = 1 - smooth(480, 482.5, rho)
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

if os.path.exists('assets/wheel-v5'): shutil.rmtree('assets/wheel-v5')
shutil.copytree(SRC, OUT)
for n, flat in (('blw.aca7b4f092b7011ac227.webp', (.20, .035, .13)), ('brw.f635fb57c5c829d76274.webp', (.03, .15, .05))):
    save_webp(flat_ring(load(f'{SRC}/{MED}/{n}'), flat), f'{OUT}/{MED}/{n}')
# gems: the owner chose the original sprites (v2/v3a) over the generated ones (gem_sprite above, kept for reference)
ORIG = 'assets/wheel-v3a/game-published'
for n in GEMS:
    shutil.copyfile(f'{ORIG}/{MED}/{n}.webp', f'{OUT}/{MED}/{n}.webp')

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
W_GEM, R_GEM = 150, 380.0
gh = W_GEM * 342 / 450
html = open(ix).read()
for n in range(1, 21):
    t = math.radians((n - 2) * 18)
    l = 500 + R_GEM * math.cos(t) - W_GEM / 2; tp = 500 + R_GEM * math.sin(t) - gh / 2
    new = f'.stonesCon img.s{n}{{left:{l:.1f}px;top:{tp:.1f}px;transform:rotate({(n - 2) * 18:.2f}deg)}}'
    html, k = re.subn(r'\.stonesCon img\.s%d\{[^}]*\}' % n, lambda m, new=new: new, html)
    assert k == 1, (n, k)
open(ix, 'w').write(html)
print('ok')
