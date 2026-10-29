from PIL import Image
im = Image.open("out/game_pub/static/media/background.c09b372e03a655d69d97.webp").convert("RGB")
print(im.size); im.thumbnail((960, 540)); im.save("out/bg_peek.jpg")
