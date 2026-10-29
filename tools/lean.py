"""Lean demo: no background video, silent WAV audio, no manifest. Fewer media files for the public-sharing review."""
import json, os, re, wave

G = "out/game_pub"
for rel in ("static/media/bkg_video.c69c5b1de9e640b73d26.mp4", "manifest.json", "logo192.png",
            "audio/magic.mp3", "audio/mystic-ambience.mp3", "audio/spin.mp3", "audio/wild.mp3"):
    if os.path.exists(f"{G}/{rel}"):
        os.remove(f"{G}/{rel}")
for name in ("magic", "mystic-ambience", "spin", "wild"):
    with wave.open(f"{G}/audio/{name}.wav", "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(8000)
        w.writeframes(b"\x00\x00" * 8000)          # one second of silence

js_path = f"{G}/static/js/main.d348ebcc.js"
js = open(js_path, encoding="utf-8").read()
for name in ("magic", "mystic-ambience", "spin", "wild"):
    old = f'"audio/{name}.mp3"'
    assert js.count(old) == 1, old
    js = js.replace(old, f'"audio/{name}.wav"')
# Pixi probes AVIF and WebM support with tiny embedded data URIs; AVIF is not a reviewable image type, so the share review rejects the file.
# Neither format is used by the game, so the probes just fail ("data:," cannot load) and Pixi treats them as unsupported.
js, n_avif = re.subn(r"data:image/avif;base64,[A-Za-z0-9+/=]+", "data:,", js)
js, n_webm = re.subn(r"data:video/webm;base64,[A-Za-z0-9+/=]+", "data:,", js)
assert (n_avif, n_webm) == (1, 1), (n_avif, n_webm)
open(js_path, "w", encoding="utf-8").write(js)

html_path = f"{G}/index.html"
html = open(html_path, encoding="utf-8").read()
html = re.sub(r'<link rel="apple-touch-icon"[^>]*/>', "", html)
html = re.sub(r'<link rel="manifest"[^>]*/>', "", html)
open(html_path, "w", encoding="utf-8").write(html)

files, total = {}, 0
for dp, _, fs in os.walk(G):
    for f in fs:
        p = os.path.join(dp, f); rel = os.path.relpath(p, G).replace("\\", "/")
        files[f"game/{rel}"] = f"game_pub/{rel}"; total += os.path.getsize(p)
json.dump(files, open("out/game_lean_files.json", "w"))
print(len(files), "files,", round(total / 1e6, 1), "MB")
print("left:", sorted(set(k.rsplit(".", 1)[-1] for k in files)))
