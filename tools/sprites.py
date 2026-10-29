import os
from PIL import Image

SRC = "out/game/static/media"
OUT = "out/game_small"
os.makedirs(OUT, exist_ok=True)
for name in ("idle.8ea07a61d9d150621e57", "pending.b4f905d3bde8f7f7d722", "winning.0ebfac7e244ab37c9a79"):
    im = Image.open(f"{SRC}/{name}.webp")
    print(name, im.size, im.mode, "frames:", getattr(im, "n_frames", 1), "src MB:", round(os.path.getsize(f"{SRC}/{name}.webp") / 1e6, 1))
    if getattr(im, "n_frames", 1) > 1:
        print("  animated, skipping recompress test")
        continue
    for q in (80, 70, 60):
        p = f"{OUT}/{name}_q{q}.webp"
        im.convert("RGBA").save(p, "WEBP", quality=q, method=4)
        print("  q", q, "->", round(os.path.getsize(p) / 1e6, 1), "MB")
