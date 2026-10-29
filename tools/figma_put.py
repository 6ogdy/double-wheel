import os
os.chdir("out")   # run from the project root: py -I tools/figma_put.py (needs out/figma/{gold,green,blue,pink,violet}.png, transparent, 1140x1500, and out/game_pub_fig)
from PIL import Image
M = "game_pub_fig/static/media"
H = {"gold": "d53168443bfda397846e", "green": "f25c93dd911fde41af2f", "blue": "52c7c705f881c6ec951f",
     "pink": "8cfdeb4e09969b101163", "violet": "fe2430dc563bad88d219"}
for n, h in H.items():
    im = Image.open(f"figma/{n}.png").convert("RGBA").rotate(-90, expand=True)   # clockwise, like WILD reads left to right
    assert im.size == (1500, 1140), im.size
    im.save(f"{M}/{n}.{h}.webp", "WEBP", quality=92, method=6)
    print(n, im.size)
