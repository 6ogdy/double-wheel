from PIL import Image
for src, dst in (("wild_k2", "kref_a"), ("wild_k3", "kref_b")):
    im = Image.open(f"out/new/{src}.webp").convert("RGBA").crop((0, 312, 1500, 840))
    im.save(f"out/ref/{dst}.png"); print(dst, im.size)
