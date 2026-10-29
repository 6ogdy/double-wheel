from PIL import Image, ImageChops
ref = Image.open("out/ref/gold_ref.png").convert("RGBA")
ra = ref.getchannel("A").point(lambda a: 255 if a > 127 else 0)
def dark_share(im):
    # share of opaque pixels with brightness (V) under 35% -> the "dark shadow" measure
    v = im.convert("RGB").convert("HSV").getchannel("V"); a = im.getchannel("A")
    px = [x for x, al in zip(v.getdata(), a.getdata()) if al > 200]
    return sum(1 for x in px if x < 90) / len(px)
print("original dark share", round(dark_share(ref), 3))
for i in range(5):
    e = Image.open(f"out/edit2/e{i}.png").convert("RGBA")
    e1 = e.resize(ref.size, Image.LANCZOS)
    ea = e1.getchannel("A").point(lambda a: 255 if a > 127 else 0)
    inter = sum(ImageChops.multiply(ra, ea).point(lambda a: 1 if a > 127 else 0).getdata())
    union = sum(ImageChops.lighter(ra, ea).point(lambda a: 1 if a > 127 else 0).getdata())
    out = e1.copy(); out.putalpha(ref.getchannel("A")); out.save(f"out/edit2/m{i}.png")
    print(i, e.size, "IoU", round(inter/union, 3), "dark share", round(dark_share(out), 3))
