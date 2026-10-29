from PIL import Image, ImageChops
ref = Image.open("out/ref/gold_ref.png").convert("RGBA")   # original silhouette
ra = ref.getchannel("A").point(lambda a: 255 if a > 127 else 0)
for i in range(3):
    e = Image.open(f"out/edit5/e{i}.png").convert("RGBA")
    bb = e.getchannel("A").point(lambda a: 255 if a > 127 else 0).getbbox()
    e = e.crop(bb).resize(ref.size, Image.LANCZOS)
    ea = e.getchannel("A").point(lambda a: 255 if a > 127 else 0)
    inter = sum(ImageChops.multiply(ra, ea).point(lambda a: 1 if a > 127 else 0).getdata())
    union = sum(ImageChops.lighter(ra, ea).point(lambda a: 1 if a > 127 else 0).getdata())
    a = ImageChops.darker(ref.getchannel("A"), e.getchannel("A")).point(lambda v: 0 if v < 200 else v)
    out = e.copy(); out.putalpha(a); out.save(f"out/new/gold_r{i+1}.webp", "WEBP", quality=92, method=6)
    print(i+1, "IoU", round(inter/union, 3))
