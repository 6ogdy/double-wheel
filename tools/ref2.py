from PIL import Image
Image.open("out/new/gold_clean.webp").convert("RGBA").save("out/ref/clean_ref.png")
