"""v4: 20 gems on the v3b ring, recoloured towards the reference look.
usage: build_v4.py   (run from the repo root; needs pillow, numpy)
- track (grey stone) -> warm brown, medallions -> reference violet / green, WILD plaque -> bronze.
Reads assets/wheel-v3b/wheel_{left,right}.png and the game copy assets/wheel-v3c/game-published,
writes assets/wheel-v4/game-published."""
import os, shutil, numpy as np
from PIL import Image

SRC = 'assets/wheel-v3c/game-published'
OUT = 'assets/wheel-v4/game-published'
MED = 'static/media'
C = 500.0
RM = 285.0          # medallion radius in the 1000 px wheel image
TRACK_IN, TRACK_OUT = RM + 9, 471.0

def load(p): return np.asarray(Image.open(p).convert('RGBA')).astype(np.float32) / 255
def smooth(a, b, x): t = np.clip((x - a) / (b - a), 0, 1); return t * t * (3 - 2 * t)

def recolour(img, med_mul, track_mul):
    h, w = img.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    rho = np.hypot(xx + .5 - C, yy + .5 - C)
    out = img.copy()
    rgb = img[..., :3]
    lum = rgb.mean(2, keepdims=True)
    # track: luminance texture tinted brown, soft edges so the bronze rims stay untouched
    tm = (smooth(TRACK_IN - 2, TRACK_IN + 3, rho) * (1 - smooth(TRACK_OUT - 3, TRACK_OUT + 2, rho)))[..., None]
    track = np.clip((lum * 1.15 - .02) * np.array(track_mul, np.float32), 0, 1)
    out[..., :3] = rgb * (1 - tm) + track * tm
    # medallion: per-channel gain, keeps the carved pattern
    mm = (1 - smooth(RM - 15, RM - 10, rho))[..., None]
    med = np.clip(rgb * np.array(med_mul, np.float32), 0, 1)
    out[..., :3] = out[..., :3] * (1 - mm) + med * mm
    return out

def save_webp(a, p): Image.fromarray((np.clip(a, 0, 1) * 255 + .5).astype(np.uint8), 'RGBA').save(p, quality=92)

def bronze(path_in, path_out):
    im = Image.open(path_in).convert('RGBA'); a = im.getchannel('A')
    hsv = np.asarray(im.convert('RGB').convert('HSV')).astype(np.float32)
    hsv[..., 1] *= .62; hsv[..., 2] *= .80
    rgb = Image.fromarray(hsv.astype(np.uint8), 'HSV').convert('RGB'); rgb.putalpha(a)
    rgb.save(path_out, quality=92)

def gem(path_in, path_out, hue_to, sat=1.25, val=.95):
    """shift mean hue to hue_to (degrees), deepen saturation: reference gems are richer, less pastel"""
    im = Image.open(path_in).convert('RGBA'); a = im.getchannel('A')
    hsv = np.asarray(im.convert('RGB').convert('HSV')).astype(np.float32)
    m = np.asarray(a) > 200
    h = hsv[..., 0] * 360 / 255
    cur = np.degrees(np.angle(np.exp(1j * np.radians(h[m])).mean())) % 360
    d = ((hue_to - cur + 180) % 360) - 180
    hsv[..., 0] = ((h + d) % 360) * 255 / 360
    hsv[..., 1] = np.clip(hsv[..., 1] * sat, 0, 255)
    hsv[..., 2] = np.clip(hsv[..., 2] * val, 0, 255)
    rgb = Image.fromarray(hsv.astype(np.uint8), 'HSV').convert('RGB'); rgb.putalpha(a)
    rgb.save(path_out, quality=92)

if os.path.exists('assets/wheel-v4'): shutil.rmtree('assets/wheel-v4')
shutil.copytree(SRC, OUT)
left = load('assets/wheel-v3b/wheel_left.png'); right = load('assets/wheel-v3b/wheel_right.png')
TRACK = (1.31, .81, .46)                      # grey ~52 -> brown ~ (68, 42, 24)
save_webp(recolour(left, (1.30, .10, .68), TRACK), f'{OUT}/{MED}/blw.aca7b4f092b7011ac227.webp')
save_webp(recolour(right, (.08, 1.20, .12), TRACK), f'{OUT}/{MED}/brw.f635fb57c5c829d76274.webp')
for n in ('wild.a5499ba14606d75104e8.webp', 'wildFlipped.9b0176bdc4cb414babc6.webp'):
    bronze(f'{SRC}/{MED}/{n}', f'{OUT}/{MED}/{n}')
for n, hue in (('gold.d53168443bfda397846e', 28), ('green.f25c93dd911fde41af2f', 135),
               ('blue.52c7c705f881c6ec951f', 220), ('pink.8cfdeb4e09969b101163', 298),
               ('violet.fe2430dc563bad88d219', 272)):
    gem(f'{SRC}/{MED}/{n}.webp', f'{OUT}/{MED}/{n}.webp', hue)
# centre gems radially in the visible track ; measured from rendered crops: R=405 left a gap only on the inner side, R=378 only on the outer side, so the optical centre is the midpoint (the sprite is not centred in its box)
import math, re
W_GEM, R_GEM = 150, 391.5
h = W_GEM * 342 / 450
def stone(n):
    t = math.radians((n - 2) * 18)
    l = 500 + R_GEM * math.cos(t) - W_GEM / 2; tp = 500 + R_GEM * math.sin(t) - h / 2
    return f'.stonesCon img.s{n}{{left:{l:.1f}px;top:{tp:.1f}px;transform:rotate({(n - 2) * 18:.2f}deg)}}'
ix = f'{OUT}/index.html'
html = open(ix).read()
for n in range(1, 21):
    html, k = re.subn(r'\.stonesCon img\.s%d\{[^}]*\}' % n, lambda m, n=n: stone(n), html)
    assert k == 1, (n, k)
open(ix, 'w').write(html)
print('ok')
