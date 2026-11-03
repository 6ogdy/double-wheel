"""Multicolor (holographic) gem: same 500x380 emerald cut as the other gems.
usage (repo root; needs pillow, numpy, scipy): make_multicolor_gem.py
- lights, edges and facet shading come from assets/gems/blue.png (structure and size match the set); only colour is rebuilt
- base colour: bilinear blend of four corner hues (gold, pink, teal, violet) with green along the top, so no hard seams
- iridescence: hue shifts with the local facet shade, so every facet and light streak gets its own hue
- pale light bands go pearly (low saturation), the outer rim goes gold
- writes assets/gems/multicolor.png and a 150 px comparison strip in the scratchpad"""
import colorsys
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter, distance_transform_edt

src = np.asarray(Image.open('assets/gems/blue.png').convert('RGBA')).astype(np.float32) / 255
H, W = src.shape[:2]
rgb, a = src[..., :3], src[..., 3]
mx, mn = rgb.max(2), rgb.min(2)
lum = rgb @ np.array([.3, .59, .11], np.float32)
sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)

def hue_rgb(deg): return np.array(colorsys.hsv_to_rgb(deg / 360, 1, 1), np.float32)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
u, w = (xx + .5) / W, (yy + .5) / H
# corner colours blended in RGB (a hue interpolation would pass through the wrong middle hue)
TL, TR, BL, BR = hue_rgb(48), hue_rgb(318), hue_rgb(185), hue_rgb(268)
TM = hue_rgb(115)
top = np.where((u < .5)[..., None], TL * (1 - 2 * u)[..., None] + TM * (2 * u)[..., None], TM * (2 - 2 * u)[..., None] + TR * (2 * u - 1)[..., None])
bot = BL * (1 - u)[..., None] + BR * u[..., None]
base = top * (1 - w)[..., None] + bot * w[..., None]
mxb = base.max(2, keepdims=True); base = base / np.maximum(mxb, 1e-6)       # back to full value; shading is added later

# iridescence: shift hue by the local facet shade (high-pass of luminance)
shade = lum - gaussian_filter(lum, 14)
shade = shade / (np.abs(shade).max() + 1e-6)
hsv = np.array([colorsys.rgb_to_hsv(*p) for p in base.reshape(-1, 3)], np.float32).reshape(H, W, 3)
h = (hsv[..., 0] + .22 * shade + .08 * np.sin(8 * np.pi * (u * .6 + w * .4))) % 1.0
s = np.clip(hsv[..., 1] * (.7 + .5 * sat), 0, 1)
# pale bands go pearly: the lighter the source, the less saturated, tinted by the local hue
pearl = np.clip((lum - .66) / .26, 0, 1)
s = s * (1 - .7 * pearl)
v = np.clip(.12 + 1.0 * lum + .12 * pearl, 0, 1)

def hsv2rgb(h, s, v):
    i = np.floor(h * 6).astype(int) % 6; f = h * 6 - np.floor(h * 6)
    p, q, t = v * (1 - s), v * (1 - s * f), v * (1 - s * (1 - f))
    out = np.zeros(h.shape + (3,), np.float32)
    for k, (r, g, b) in enumerate([(v, t, p), (q, v, p), (p, v, t), (p, q, v), (t, p, v), (v, p, q)]):
        m = i == k; out[m, 0], out[m, 1], out[m, 2] = r[m], g[m], b[m]
    return out
res = hsv2rgb(h, s, v)

# gold rim on the outermost ~8 px of the silhouette
d = distance_transform_edt(a > .5)
rim = np.clip((8 - d) / 3, 0, 1)[..., None]
gold = np.stack([1.0 * (.5 + .55 * lum), .72 * (.5 + .6 * lum), .16 * (.5 + .6 * lum)], -1)
res = res * (1 - rim) + np.clip(gold, 0, 1) * rim

Image.fromarray((np.clip(np.dstack([res, a]), 0, 1) * 255 + .5).astype(np.uint8), 'RGBA').save('assets/gems/multicolor.png')

names = ['gold', 'green', 'blue', 'pink', 'violet', 'multicolor']
strip = Image.new('RGBA', (160 * len(names), 130), (24, 24, 24, 255))
for i, n in enumerate(names):
    g = Image.open(f'assets/gems/{n}.png').convert('RGBA').resize((150, 114), Image.LANCZOS)
    strip.alpha_composite(g, (160 * i + 5, 8))
strip.save('/private/tmp/claude-501/gem_strip.png')
