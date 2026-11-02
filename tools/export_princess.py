"""princess frames from the original 850 px sprite sheets: contact sheets (mode 'sheet') and chosen exports (mode 'export')
run from repo root: py out/princess.py sheet | export"""
import sys, os
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
M = 'out/game/static/media'
FW = 850
SHEETS = {'idle': 'idle.8ea07a61d9d150621e57.webp', 'pending': 'pending.b4f905d3bde8f7f7d722.webp', 'winning': 'winning.0ebfac7e244ab37c9a79.webp'}
mode = sys.argv[1]
os.makedirs('out/princess', exist_ok=True)


def frame(im, i):
    n = im.width // FW
    return im.crop(((i % n) * FW, (i // n) * FW, (i % n) * FW + FW, (i // n) * FW + FW))


for name, f in SHEETS.items():
    im = Image.open(f'{M}/{f}')
    n = im.width // FW
    total = n * n
    # last non-empty frame (the sheet is padded with empty cells)
    last = 0
    for i in range(total - 1, -1, -1):
        if frame(im, i).getchannel('A').getbbox(): last = i; break
    print(name, 'grid', n, 'x', n, 'frames with content:', last + 1)
    if mode == 'sheet':
        k = 12
        idx = [round(j * last / (k - 1)) for j in range(k)]
        W = 4
        sheet = Image.new('RGBA', (W * 300, ((k + W - 1) // W) * 300), (60, 60, 60, 255))
        for j, i in enumerate(idx):
            fr = frame(im, i).resize((300, 300), Image.LANCZOS)
            sheet.alpha_composite(fr, ((j % W) * 300, (j // W) * 300))
        sheet.convert('RGB').save(f'out/princess/contact_{name}.png')
        print(' frames', idx)

if mode == 'export':
    POSES = [('01_idle_front_smile', 'idle', 0), ('02_idle_turned', 'idle', 27), ('03_idle_profile', 'idle', 59),
             ('04_pending_looking_at_wheel', 'pending', 0), ('05_pending_hair_in_wind', 'pending', 87),
             ('06_winning_eyes_closed', 'winning', 51), ('07_winning_smile', 'winning', 76), ('08_winning_front_smile', 'winning', 114)]
    ims = {k: Image.open(f'{M}/{v}') for k, v in SHEETS.items()}
    for name, sheet, i in POSES:
        fr = frame(ims[sheet], i)
        assert fr.getchannel('A').getbbox(), name
        fr.save(f'out/princess/{name}.png')
        print(name, os.path.getsize(f'out/princess/{name}.png') // 1024, 'KB')
