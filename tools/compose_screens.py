"""5 game screens: captured frames (princess layer hidden) + the HQ princess pose at the game's position. run from repo root"""
import os
from PIL import Image

OUT = 'out/screens'
os.makedirs(OUT, exist_ok=True)
POS = (-210, 230)          # game rect is x -210, y 139; lowered so her cut-off bottom sits on the screen edge (the game hides it under the bottom bar)
SCREENS = [
    ('1_asteptare', 5, '01_idle_front_smile'),
    ('2_start_rotire', 9, '04_pending_looking_at_wheel'),
    ('3_rotire_rapida', 11, '05_pending_hair_in_wind'),
    ('4_wild_pe_roata', 48, '07_winning_smile'),
    ('5_rezultat', 30, '08_winning_front_smile'),
]
for name, i, pose in SCREENS:
    bg = Image.open(f'out/cap/run/f_{i:03d}.png').convert('RGBA')
    pr = Image.open(f'out/princess/{pose}.png').convert('RGBA')
    bg.alpha_composite(pr, POS) if POS[0] >= 0 else None
    if POS[0] < 0:                                     # alpha_composite does not take negative offsets: crop the part that is on screen
        crop = pr.crop((-POS[0], 0, pr.width, pr.height))
        bg.alpha_composite(crop, (0, POS[1]))
    bg.convert('RGB').save(f'{OUT}/screen_{name}.png')
    print(name, os.path.getsize(f'{OUT}/screen_{name}.png') // 1024, 'KB')
