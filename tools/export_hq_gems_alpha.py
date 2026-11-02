"""cut the flat (30,30,30) background from the 1500x1140 gems, same method as tools/remove_gem_bg.py with the soft edge scaled for 3.3x. run from repo root"""
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

BG = np.array([30, 30, 30], float)
RAMP = 2.0 * 1500 / 450        # the game sprite ramp (2 px at 450) at this size


def remove(path):
    a = np.asarray(Image.open(path).convert('RGB')).astype(float)
    cand = np.abs(a - BG).max(axis=2) < 14
    lab, n = ndi.label(cand)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bg = np.isin(lab, list(border))
    dist = ndi.distance_transform_edt(~bg)
    alpha = np.clip((dist - 0.5 * 3.3) / RAMP, 0, 1); alpha[bg] = 0
    al = np.maximum(alpha, 1e-3)[..., None]
    edge = (alpha > 0) & (alpha < 1)
    rgb = a.copy(); rgb[edge] = np.clip((a[edge] - (1 - al[edge]) * BG) / al[edge], 0, 255)
    Image.fromarray(np.dstack([rgb, alpha * 255]).astype(np.uint8), 'RGBA').save(path)
    return bg.mean()


for k in ('gold', 'green', 'blue', 'pink', 'violet'):
    print(k, 'background share', round(remove(f'out/hq/gem_{k}.png'), 3))
