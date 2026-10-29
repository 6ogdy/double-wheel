from PIL import Image, ImageOps
S = 3
src = Image.open("out/gen/v3.png").convert("RGBA")
bb = src.getchannel("A").point(lambda a: 255 if a > 20 else 0).getbbox()
word = src.crop(bb).resize((500*S, 176*S), Image.LANCZOS)  # same 500:176 footprint as the original wild.webp
for name, img, top in [("wild", word, 104), ("wildFlipped", ImageOps.mirror(word), 100)]:
    canvas = Image.new("RGBA", (500*S, 380*S), (0, 0, 0, 0))
    canvas.paste(img, (0, top*S), img)
    canvas.save(f"out/new/{name}.webp", "WEBP", quality=92, method=6)
