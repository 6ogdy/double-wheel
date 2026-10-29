import sys, glob
from PIL import Image
for p in sorted(glob.glob(sys.argv[1])):
    im = Image.open(p).convert("RGBA")
    bb = im.getchannel("A").point(lambda a: 255 if a > 20 else 0).getbbox()
    w, h = bb[2]-bb[0], bb[3]-bb[1]
    print(p, im.size, "bbox", bb, "visible", (w, h), "ratio", round(w/h, 3))
