import math, colorsys
from PIL import Image
S = 3  # quality factor
W, H = 500*S, 380*S

def visible_bbox(im):
    return im.getchannel("A").point(lambda a: 255 if a > 20 else 0).getbbox()

def mean_hue(im):
    # circular mean of hue over vivid, bright pixels, as 0..1
    hsv = im.convert("RGB").convert("HSV"); a = im.getchannel("A")
    hs, ss, vs = hsv.split(); sx = sy = n = 0
    for h, s, v, al in zip(hs.getdata(), ss.getdata(), vs.getdata(), a.getdata()):
        if al > 200 and s > 140 and v > 140:
            t = h/255*2*math.pi; sx += math.cos(t); sy += math.sin(t); n += 1
    return (math.atan2(sy, sx)/(2*math.pi)) % 1.0

def rotate(im, shift):
    rgb = im.convert("RGB"); h, s, v = rgb.convert("HSV").split()
    k = round(shift*255)
    h = h.point(lambda x: (x + k) % 256)
    out = Image.merge("HSV", (h, s, v)).convert("RGB").convert("RGBA")
    out.putalpha(im.getchannel("A")); return out

src = Image.open("out/gen/0.png").convert("RGBA")
src = src.crop(visible_bbox(src))
base = src.resize((W, H), Image.LANCZOS)  # fills the same 500:380 frame as the originals
src_h = mean_hue(base)
print("source hue", round(src_h*360))
for name in ["gold", "green", "blue", "pink", "violet"]:
    orig = Image.open(f"out/orig/{name}.webp").convert("RGBA")
    th = mean_hue(orig)
    out = rotate(base, th - src_h)
    out.save(f"out/new/{name}.webp", "WEBP", quality=92, method=6)
    print(name, "orig hue", round(th*360), out.size)
