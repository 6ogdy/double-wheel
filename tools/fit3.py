from PIL import Image, ImageChops
ref = Image.open("out/ref/gold_ref.png").convert("RGBA")
e = Image.open("out/edit3/e0.png").convert("RGBA")
bb = e.getchannel("A").point(lambda a: 255 if a > 127 else 0).getbbox()
e = e.crop(bb).resize(ref.size, Image.LANCZOS)   # generated art stretched to the full frame, as the originals fill theirs
ra = ref.getchannel("A").point(lambda a: 255 if a > 127 else 0)
ea = e.getchannel("A").point(lambda a: 255 if a > 127 else 0)
i = sum(ImageChops.multiply(ra, ea).point(lambda a: 1 if a > 127 else 0).getdata())
u = sum(ImageChops.lighter(ra, ea).point(lambda a: 1 if a > 127 else 0).getdata())
print("crop bbox", bb, "IoU after fit", round(i/u, 3))
a = ImageChops.darker(ref.getchannel("A"), e.getchannel("A")).point(lambda v: 0 if v < 200 else v)
out = e.copy(); out.putalpha(a); out.save("out/new/gold_clean.webp", "WEBP", quality=92, method=6)
