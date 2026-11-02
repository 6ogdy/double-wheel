"""Princess sprite sheets from the PNG sequences in assets/girl (850x850, transparent).
Frames are resized to 425 px and laid out row by row in the same grids the game already uses (idle 8x8, pending 13x13, winning 12x12),
so the game only needs the sheets replaced. Writes into both 25-position game folders. run from the repo root: py tools/build_princess_sheets.py"""
import glob, os
from PIL import Image

SEQ = {'idle.8ea07a61d9d150621e57': ('Idle/idle_final', 8), 'pending.b4f905d3bde8f7f7d722': ('Pending/pending 8 sec - 3', 13), 'winning.0ebfac7e244ab37c9a79': ('Winning/winning 7 sec - 3', 12)}
FW = 425
for name, (folder, n) in SEQ.items():
    fs = sorted(glob.glob(f'assets/girl/{folder}/*.png'))
    assert 0 < len(fs) <= n * n, (name, len(fs))
    sheet = Image.new('RGBA', (n * FW, n * FW), (0, 0, 0, 0))
    for i, f in enumerate(fs):
        im = Image.open(f).convert('RGBA')
        assert im.size == (850, 850), (f, im.size)
        sheet.paste(im.resize((FW, FW), Image.LANCZOS), ((i % n) * FW, (i // n) * FW))
    for kind in ('moss', 'clean'):
        out = f'assets/wheel-v6{kind}-25/game-published/static/media/{name}.webp'
        sheet.save(out, 'WEBP', quality=90, method=4)
    print(name, len(fs), 'frames,', sheet.size, round(os.path.getsize(out) / 1e6, 1), 'MB', flush=True)
