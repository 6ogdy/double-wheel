from PIL import Image
im = Image.open("out/orig/gold.webp").convert("RGBA")
im.resize((1500, 1140), Image.LANCZOS).save("out/ref/gold_ref.png")
print(im.getchannel("A").getextrema())
