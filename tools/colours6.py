import math
from PIL import Image
def mean_hue(im):
    hs, ss, vs = im.convert("RGB").convert("HSV").split(); a = im.getchannel("A")
    sx = sy = 0
    for h, s, v, al in zip(hs.getdata(), ss.getdata(), vs.getdata(), a.getdata()):
        if al > 200 and s > 140 and v > 140:
            t = h/255*2*math.pi; sx += math.cos(t); sy += math.sin(t)
    return (math.atan2(sy, sx)/(2*math.pi)) % 1.0
def rotate(im, shift):
    h, s, v = im.convert("RGB").convert("HSV").split(); k = round(shift*255)
    out = Image.merge("HSV", (h.point(lambda x: (x + k) % 256), s, v)).convert("RGB").convert("RGBA")
    out.putalpha(im.getchannel("A")); return out
base = Image.open("out/new/gold_r3.webp").convert("RGBA")
bh = mean_hue(base); print("level 6 hue", round(bh*360))
for name in ["gold", "green", "blue", "pink", "violet"]:
    th = mean_hue(Image.open(f"out/orig/{name}.webp").convert("RGBA"))
    rotate(base, th - bh).save(f"out/new/n6_{name}.webp", "WEBP", quality=92, method=6)
    print(name, round(th*360))
