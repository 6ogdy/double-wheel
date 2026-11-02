"""v6: wheel ring and foot restyled in the stone of the altar under them (carved grey stone).
usage: build_v6.py moss|clean   (run from the repo root; needs pillow, numpy, scipy; run build_v5.py full first)
- reads assets/wheel-v5full/game-published, writes assets/wheel-v6<moss|clean>/game-published
- ring: the v5full ring keeps its carving (key bands, separators); colour and grain come from the altar stone
- foot: same stone, same grain
- 'moss' adds moss on the stone (outer rim, grooves, top of the foot) in the colour measured on the altar; 'clean' has none
The medallions, gems and WILD plaques are not touched."""
import os, sys, shutil, numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter, zoom

KIND = next((a for a in sys.argv[1:] if a in ('moss', 'clean')), None)
assert KIND, 'usage: build_v6.py moss|clean'
MOSS = KIND == 'moss'
SFX = '' if os.environ.get('N', '20') == '20' else '-' + os.environ['N']   # N=25: reads wheel-v5full-25, writes wheel-v6<kind>-25
SRC = f'assets/wheel-v5full{SFX}/game-published'
OUT = f'assets/wheel-v6{KIND}{SFX}/game-published'
MED = 'static/media'
C = 500.0
SH = 0 if os.environ.get('N', '20') == '20' else 14      # medallion growth, same as build_v5.py
rng = np.random.default_rng(7)

def smooth(a, b, x): t = np.clip((x - a) / (b - a), 0, 1); return t * t * (3 - 2 * t)
def load(p): return np.asarray(Image.open(p).convert('RGBA')).astype(np.float32) / 255
def save_webp(a, p): Image.fromarray((np.clip(a, 0, 1) * 255 + .5).astype(np.uint8), 'RGBA').save(p, quality=92)

# ---------------------------------------------------------------- stone grain from the altar
altar = load(f'{SRC}/{MED}/altar.webp')
lum = altar[..., :3].mean(2)
band = lum[40:72, 100:1300]                       # flat part of the front face, above the carving
grain = band - gaussian_filter(band, 5)           # high-pass: pits, chips, fine speckle
grain = grain / grain.std()

def tile_grain(h, w):
    """mirrored tiling of the altar grain (no seams), scaled 1:1"""
    gh, gw = grain.shape
    big = np.tile(np.block([[grain, grain[:, ::-1]], [grain[::-1], grain[::-1, ::-1]]]), (h // (2 * gh) + 1, w // (2 * gw) + 1))
    return big[:h, :w]

def fbm(h, w, scales=(180, 70, 28, 11), seed=0):
    r = np.random.default_rng(seed); out = np.zeros((h, w), np.float32); amp = 1.0; tot = 0
    for s in scales:
        n = r.standard_normal((h // s + 3, w // s + 3)).astype(np.float32)
        z = zoom(n, s, order=3)[:h, :w]
        out += amp * z; tot += amp; amp *= .55
    return out / out.std()

STONE = np.array([.262, .236, .176], np.float32)  # altar front face, moss excluded
STONE_DARK = np.array([.16, .145, .105], np.float32)
MOSS_DARK = np.array([.07, .095, .02], np.float32)   # measured on the altar moss
MOSS_LIGHT = np.array([.20, .27, .06], np.float32)

def stone_colour(shape, relief, grain_amp=.16, seed=1):
    """stone base * carving relief * grain, with large soft stains like the altar"""
    h, w = shape
    stain = fbm(h, w, (240, 90, 35), seed)
    base = STONE * (1 + .22 * stain[..., None])
    base = base * (1 + grain_amp * tile_grain(h, w)[..., None])
    return np.clip(base * relief[..., None], 0, 1)

def add_moss(col, mask, h, w, seed=3):
    n = fbm(h, w, (120, 45, 18, 7), seed)
    m = np.clip((mask + .55 * n - .15) * 2.2, 0, 1)
    m = smooth(.35, .75, m)[..., None]
    tone = MOSS_DARK + (MOSS_LIGHT - MOSS_DARK) * np.clip(.5 + .45 * fbm(h, w, (30, 9, 4), seed + 1), 0, 1)[..., None]
    tone = tone * (1 + .18 * tile_grain(h, w)[..., None])
    return col * (1 - m) + tone * m

# ---------------------------------------------------------------- ring
def stone_ring(img):
    h, w = img.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    dx, dy = xx + .5 - C, yy + .5 - C
    rho = np.hypot(dx, dy)
    rgb = img[..., :3]
    ring = (rho > 320) & (rho < 450)
    ref = rgb[ring].mean()                                        # flat track level; the carving is the deviation from it
    l = rgb.mean(2)
    relief = np.clip((l / ref) ** 1.15, .25, 2.2)
    col = stone_colour((h, w), relief)
    if MOSS:
        # moss grows on the outer rim and in the dark grooves, a little on the track
        outer = smooth(440, 494, rho)
        groove = np.clip((.85 - relief) * 2.5, 0, 1)
        col = add_moss(col, .55 * outer + .5 * groove - .2, h, w)
    out = img.copy()
    zone = smooth(262 + SH, 268 + SH, rho)[..., None]                 # medallion (rho < 262 + SH) stays as it is
    out[..., :3] = rgb * (1 - zone) + col * zone
    return out

# ---------------------------------------------------------------- foot
def stone_foot(img):
    h, w = img.shape[:2]
    a = img[..., 3]
    l = img[..., :3].mean(2)
    m = l[a > .9]
    relief = np.clip((l / m.mean()) ** 1.1, .3, 2.0)
    col = stone_colour((h, w), relief, grain_amp=.22, seed=11)
    if MOSS:
        yy = np.mgrid[0:h, 0:w][0].astype(np.float32) / h
        col = add_moss(col, 1.1 * (1 - smooth(0, .42, yy)) - .15 + .25 * np.clip(.9 - relief, 0, 1), h, w, seed=13)
    out = img.copy(); out[..., :3] = col
    return out

if os.path.exists(os.path.dirname(OUT)): shutil.rmtree(os.path.dirname(OUT))
shutil.copytree(SRC, OUT)
save_webp(stone_ring(load(f'{SRC}/{MED}/blw.aca7b4f092b7011ac227.webp')), f'{OUT}/{MED}/blw.aca7b4f092b7011ac227.webp')
save_webp(stone_ring(load(f'{SRC}/{MED}/brw.f635fb57c5c829d76274.webp')), f'{OUT}/{MED}/brw.f635fb57c5c829d76274.webp')
save_webp(stone_foot(load(f'{SRC}/{MED}/foot.webp')), f'{OUT}/{MED}/foot.webp')

# no entrance animation, ever: wheels, centre gem and arrows are already in place when a round starts
js = f'{OUT}/static/js/main.d348ebcc.js'
code = open(js, encoding='utf-8').read()
def sub(old, new):
    global code
    assert code.count(old) == 1, old
    code = code.replace(old, new)
sub('window.__w1?(nu.set(".wheel_stonesCon",{y:-1500,opacity:0}),nu.set(this.finalValue,{opacity:0}),nu.to(".wheel_stonesCon",{y:0,opacity:1,duration:1,ease:"bounce.out"})):(window.__w1=1,nu.set(this.finalValue,{opacity:0}))',
    'nu.set(this.finalValue,{opacity:0})')
sub('window.__w2?(nu.set(".wheel_stonesCon2",{y:1500,opacity:0}),nu.set(this.finalValue2,{opacity:0}),nu.to(".wheel_stonesCon2",{y:0,opacity:1,duration:1,ease:"bounce.out",delay:.5})):(window.__w2=1,nu.set(this.finalValue2,{opacity:0}))',
    'nu.set(this.finalValue2,{opacity:0})')
sub('nu.set(".arrow-container",{scale:0,opacity:0})', 'nu.set(".arrow-container",{scale:1,opacity:1})')
sub('this.rotateTimeline.to(".arrow-container",{scale:1,opacity:1,duration:1},0).to(".wheel_stonesCon",{y:0,opacity:1,duration:1,ease:"bounce.out"},0)',
    'this.rotateTimeline.set(".arrow-container",{scale:1,opacity:1},0).set(".wheel_stonesCon",{y:0,opacity:1},0)')
sub('this.rotateTimeline.to(".wheel_stonesCon2",{y:0,opacity:1,duration:1,ease:"bounce.out"},.5)',
    'this.rotateTimeline.set(".wheel_stonesCon2",{y:0,opacity:1},.5)')
open(js, 'w', encoding='utf-8').write(code)
print('ok', OUT)
