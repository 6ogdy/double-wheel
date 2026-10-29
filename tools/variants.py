from PIL import Image
for i in range(5):
    Image.open(f"out/edit/m{i}.png").save(f"out/new/gold_v{i+1}.webp", "WEBP", quality=92, method=6)
