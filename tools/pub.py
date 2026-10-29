"""Assemble out/game_pub: the game with the new stones, the offline replay shim, and sprite sheets recompressed under the 15 MB file limit."""
import json, os, shutil

SRC, DST = "out/game", "out/game_pub"
SKIP = {"rec.html", "rec.js", "demo.html", "scaling.html"}
shutil.rmtree(DST, ignore_errors=True)
for root, _, files in os.walk(SRC):
    for f in files:
        rel = os.path.relpath(os.path.join(root, f), SRC).replace("\\", "/")
        if rel in SKIP:
            continue
        os.makedirs(os.path.dirname(os.path.join(DST, rel)) or DST, exist_ok=True)
        shutil.copy2(os.path.join(root, f), os.path.join(DST, rel))
shutil.copy2(os.path.join(SRC, "demo.html"), os.path.join(DST, "index.html"))
for name in ("idle.8ea07a61d9d150621e57", "pending.b4f905d3bde8f7f7d722", "winning.0ebfac7e244ab37c9a79"):
    shutil.copy2(f"out/game_small/{name}_half.webp", f"{DST}/static/media/{name}.webp")
# sheets are half size now, so the game must cut 425 px frames; demo_css.py scales the canvas back up to 850 px
js_path = f"{DST}/static/js/main.d348ebcc.js"
js = open(js_path, encoding="utf-8").read()
assert js.count("frameWidth:850,frameHeight:850") == 1
open(js_path, "w", encoding="utf-8").write(js.replace("frameWidth:850,frameHeight:850", "frameWidth:425,frameHeight:425"))

files, total = {}, 0
for root, _, fs in os.walk(DST):
    for f in fs:
        p = os.path.join(root, f); rel = os.path.relpath(p, DST).replace("\\", "/")
        files[f"game/{rel}"] = f"game_pub/{rel}"; total += os.path.getsize(p)
print(len(files), "files,", round(total / 1e6, 1), "MB total; biggest:",
      sorted(((os.path.getsize(os.path.join(DST, k[5:])), k) for k in files), reverse=True)[:4])
json.dump(files, open("out/game_files.json", "w"))
