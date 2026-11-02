"""high-quality exports for the client Figma file. run from repo root: py out/hq_assets.py
- gems: the 1140x1500 Figma originals rotated 90 deg clockwise -> 1500x1140 (same orientation as the game sprites)
- altar: assets/wheel-v2/altar.png 2000x280
- foot (stone + moss): the v6 recipe (tools/build_v6.py stone_foot) run on the 816x441 foot, noise scales multiplied by K"""
import os, shutil, numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter, zoom

OUT = 'out/hq'
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- gems + altar
for k in ('gold', 'green', 'blue', 'pink', 'violet'):
    im = Image.open(f'out/figma/{k}.png').convert('RGBA').rotate(-90, expand=True)
    assert im.size == (1500, 1140), im.size
    im.save(f'{OUT}/gem_{k}.png')
shutil.copyfile('assets/wheel-v2/altar.png', f'{OUT}/altar_stone.png')

# ---------------------------------------------------------------- foot, v6 recipe at high resolution
foot = np.asarray(Image.open('assets/wheel-v2/foot.png').convert('RGBA')).astype(np.float32) / 255
K = foot.shape[1] / 260.0                         # the game foot is 260 px wide
altar = np.asarray(Image.open('assets/wheel-v2/altar.png').convert('RGBA')).astype(np.float32) / 255
AK = altar.shape[1] / 1400.0                      # the v6 grain was taken from the 1400 px game altar
lum = altar[..., :3].mean(2)
band = lum[round(40 * AK):round(72 * AK), round(100 * AK):round(1300 * AK)]
grain = band - gaussian_filter(band, 5 * AK)
grain = grain / grain.std()
grain = zoom(grain, K * 1.0 / AK, order=1)        # same grain size relative to the foot as in the game


def smooth(a, b, x): t = np.clip((x - a) / (b - a), 0, 1); return t * t * (3 - 2 * t)


def tile_grain(h, w):
    gh, gw = grain.shape
    big = np.tile(np.block([[grain, grain[:, ::-1]], [grain[::-1], grain[::-1, ::-1]]]), (h // (2 * gh) + 1, w // (2 * gw) + 1))
    return big[:h, :w]


def fbm(h, w, scales, seed=0):
    r = np.random.default_rng(seed); out = np.zeros((h, w), np.float32); amp = 1.0
    for s in scales:
        s = max(2, int(round(s * K)))
        n = r.standard_normal((h // s + 3, w // s + 3)).astype(np.float32)
        out += amp * zoom(n, s, order=3)[:h, :w]; amp *= .55
    return out / out.std()


STONE = np.array([.262, .236, .176], np.float32)
MOSS_DARK = np.array([.07, .095, .02], np.float32)
MOSS_LIGHT = np.array([.20, .27, .06], np.float32)
h, w = foot.shape[:2]
a = foot[..., 3]
l = foot[..., :3].mean(2)
relief = np.clip((l / l[a > .9].mean()) ** 1.1, .3, 2.0)
stain = fbm(h, w, (240, 90, 35), 11)
col = STONE * (1 + .22 * stain[..., None])
col = col * (1 + .22 * tile_grain(h, w)[..., None])
col = np.clip(col * relief[..., None], 0, 1)
yy = np.mgrid[0:h, 0:w][0].astype(np.float32) / h
mask = 1.1 * (1 - smooth(0, .42, yy)) - .15 + .25 * np.clip(.9 - relief, 0, 1)
n = fbm(h, w, (120, 45, 18, 7), 13)
m = smooth(.35, .75, np.clip((mask + .55 * n - .15) * 2.2, 0, 1))[..., None]
tone = MOSS_DARK + (MOSS_LIGHT - MOSS_DARK) * np.clip(.5 + .45 * fbm(h, w, (30, 9, 4), 14), 0, 1)[..., None]
tone = tone * (1 + .18 * tile_grain(h, w)[..., None])
col = col * (1 - m) + tone * m
out = foot.copy(); out[..., :3] = col
Image.fromarray((np.clip(out, 0, 1) * 255 + .5).astype(np.uint8), 'RGBA').save(f'{OUT}/foot_stone_moss.png')
print('ok', {f: Image.open(f'{OUT}/{f}').size for f in sorted(os.listdir(OUT))})
