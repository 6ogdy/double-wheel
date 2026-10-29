from PIL import Image
im = Image.open("out/orig/wild.webp").convert("RGBA")
bb = im.getchannel("A").point(lambda a: 255 if a > 20 else 0).getbbox()
im.crop(bb).resize((1500, 528), Image.LANCZOS).save("out/ref/wild_ref.png"); print(bb)
