import sys, glob
from PIL import Image
files = sys.argv[2:]
tw, th = 400, 304
cols = 5
rows = (len(files)+cols-1)//cols
sheet = Image.new("RGB", (cols*tw, rows*th), (40, 44, 60))
for i, p in enumerate(files):
    im = Image.open(p).convert("RGBA"); im.thumbnail((tw-8, th-8))
    sheet.paste(im, ((i%cols)*tw+4, (i//cols)*th+4), im)
sheet.save(sys.argv[1])
