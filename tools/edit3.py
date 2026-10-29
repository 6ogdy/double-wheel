from PIL import Image, ImageChops
ref = Image.open("out/ref/gold_ref.png").convert("RGBA")
ra = ref.getchannel("A").point(lambda a: 255 if a > 127 else 0)
e = Image.open("out/edit3/e0.png").convert("RGBA"); e1 = e.resize(ref.size, Image.LANCZOS)
ea = e1.getchannel("A").point(lambda a: 255 if a > 127 else 0)
i = sum(ImageChops.multiply(ra, ea).point(lambda a: 1 if a > 127 else 0).getdata())
u = sum(ImageChops.lighter(ra, ea).point(lambda a: 1 if a > 127 else 0).getdata())
print(e.size, "IoU", round(i/u, 3))
out = e1.copy(); out.putalpha(ref.getchannel("A")); out.save("out/edit3/m0.png")
