"""Halve the three character sprite sheets (frames 850 -> 425 px) so each file is small enough to be reviewed and shared."""
import os
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
SRC, OUT = "out/game/static/media", "out/game_small"
os.makedirs(OUT, exist_ok=True)
for name in ("idle.8ea07a61d9d150621e57", "pending.b4f905d3bde8f7f7d722", "winning.0ebfac7e244ab37c9a79"):
    im = Image.open(f"{SRC}/{name}.webp").convert("RGBA")
    half = im.resize((im.width // 2, im.height // 2), Image.LANCZOS)
    p = f"{OUT}/{name}_half.webp"
    half.save(p, "WEBP", quality=80, method=4)
    print(name, im.size, "->", half.size, round(os.path.getsize(p) / 1e6, 2), "MB")
