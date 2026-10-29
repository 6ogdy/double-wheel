from PIL import Image, ImageChops
ref = Image.open("out/ref/gold_ref.png").convert("RGBA")
ra = ref.getchannel("A").point(lambda a: 255 if a > 127 else 0)
for i in range(5):
    e = Image.open(f"out/edit/e{i}.png").convert("RGBA")
    e1 = e.resize(ref.size, Image.LANCZOS)
    ea = e1.getchannel("A").point(lambda a: 255 if a > 127 else 0)
    inter = sum(ImageChops.multiply(ra, ea).point(lambda a: 1 if a > 127 else 0).getdata())
    union = sum(ImageChops.lighter(ra, ea).point(lambda a: 1 if a > 127 else 0).getdata())
    bb = e.getchannel("A").point(lambda a: 255 if a > 20 else 0).getbbox()
    out = e1.copy(); out.putalpha(ref.getchannel("A"))   # silhouette locked to the original
    out.save(f"out/edit/m{i}.png")
    print(i, e.size, "bbox", bb, "silhouette IoU", round(inter/union, 3))
