from PIL import Image
S = 3
for i in range(3):
    e = Image.open(f"out/wild/b{i}.png").convert("RGBA")
    bb = e.getchannel("A").point(lambda a: 255 if a > 127 else 0).getbbox()
    w, h = bb[2]-bb[0], bb[3]-bb[1]
    word = e.crop(bb).resize((500*S, 176*S), Image.LANCZOS)   # same 500:176 footprint as the original wild.webp
    canvas = Image.new("RGBA", (500*S, 380*S), (0, 0, 0, 0)); canvas.paste(word, (0, 104*S), word)
    canvas.save(f"out/new/wild_b{i+1}.webp", "WEBP", quality=92, method=6)
    print(i+1, "generated word ratio", round(w/h, 3), "-> stretch vertical x", round((500/176)/(w/h), 3))
