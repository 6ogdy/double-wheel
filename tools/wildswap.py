"""Put the chosen WILD (obsidian, bolder) into the game: wild.webp as is, wildFlipped.webp mirrored and placed 4 px (x3 = 12 px) higher like the original."""
from PIL import Image, ImageOps

S = 3
G = "out/game_pub/static/media"
src = Image.open("out/new/wild_n2.webp").convert("RGBA")
word = src.crop((0, 104 * S, 500 * S, 280 * S))           # the 500x176 footprint
src.save(f"{G}/wild.a5499ba14606d75104e8.webp", "WEBP", quality=92, method=6)
flipped = Image.new("RGBA", src.size, (0, 0, 0, 0))
flipped.paste(ImageOps.mirror(word), (0, 100 * S))        # original wildFlipped sits at y=100
flipped.save(f"{G}/wildFlipped.9b0176bdc4cb414babc6.webp", "WEBP", quality=92, method=6)
print("wild swapped", src.size)
