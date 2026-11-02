"""Export the 25-position rings (moss) as PNG and compose a preview of each wheel with its 25 gems.
run from the repo root: py out/figma25.py"""
import math, os, re
from PIL import Image

G = 'assets/wheel-v6moss-25/game-published'
M = f'{G}/static/media'
OUT = 'out/figma25'
os.makedirs(OUT, exist_ok=True)
html = open(f'{G}/index.html', encoding='utf-8').read()
rp = open(f'{G}/replay.js', encoding='utf-8').read()
seq = re.search(r'var VISUAL = (.*);\n', rp).group(1)
import json
seq = json.loads(seq)['1']['seq']
assert len(seq) == 25
KIND = {1: 'gold', 2: 'green', 3: 'blue', 4: 'pink', 5: 'violet', 6: 'wild'}
W = int(re.search(r'\.stonesCon img\{width:(\d+)px', html).group(1))
files = {f.split('.')[0]: f for f in os.listdir(M) if f.endswith('.webp')}
step = 360 / 25
m2 = re.search(r'\.stonesCon img\.s2\{left:([\d.]+)px', html)
R = float(m2.group(1)) + W / 2 - 500             # position 2 sits at 0 deg: its centre x minus the wheel centre is the radius the game uses
print('R from the game css:', R)
for side, ring, wild in (('left', 'blw', 'wild'), ('right', 'brw', 'wildFlipped')):
    r = Image.open(f'{M}/{files[ring]}').convert('RGBA')
    assert r.size == (1000, 1000), r.size
    r.save(f'{OUT}/wheel_{side}_stone_moss_25.png')
    canvas = r.copy()
    for n, v in enumerate(seq, 1):
        name = wild if v == 6 else KIND[v]
        g = Image.open(f'{M}/{files[name]}').convert('RGBA')
        g = g.resize((W, round(W * g.height / g.width)), Image.LANCZOS)
        ang = (n - 2) * step
        g = g.rotate(-ang, expand=True, resample=Image.BICUBIC)
        t = math.radians(ang)
        cx, cy = 500 + R * math.cos(t), 500 + R * math.sin(t)
        canvas.alpha_composite(g, (round(cx - g.width / 2), round(cy - g.height / 2)))
    canvas.save(f'{OUT}/preview_{side}_25_gems.png')
print('ok', W, os.listdir(OUT))
