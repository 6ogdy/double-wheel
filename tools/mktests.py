"""Three small test artifacts, each holding one slice of the game's media, to find which slice the share review rejects."""
import json, os

G = "out/game_pub"
def walk(sub, exts):
    out = []
    for dp, _, fs in os.walk(f"{G}/{sub}" if sub else G):
        for f in sorted(fs):
            if f.rsplit(".", 1)[-1].lower() in exts:
                out.append(os.path.relpath(os.path.join(dp, f), G).replace("\\", "/"))
    return out

sprites = [r for r in walk("static/media", {"webp"}) if os.path.basename(r).split(".")[0] in ("idle", "pending", "winning")]
other_media = walk("", {"ttf", "wav", "gif", "png"})
rest = [r for r in walk("", {"webp"}) if r not in sprites] + ["static/js/main.d348ebcc.js", "static/css/main.be085d95.css"]

def page(title, body):
    return (f"<title>{title}</title>\n<style>:root{{--bg:#0b0f0c;--fg:#e8efe9;color-scheme:dark}}"
            f"body{{background:var(--bg);color:var(--fg);font:16px/1.5 system-ui,sans-serif;padding:24px}}"
            f"img{{max-width:160px;margin:4px}}</style>\n<h1>{title}</h1>\n{body}\n")

t1 = page("Test sprites", "<p>Trei imagini mari.</p>\n" + "".join(f'<img src="s/{os.path.basename(r)}" alt="sprite">\n' for r in sprites))
t2 = page("Test fonturi sunete", "<p>Fonturi, sunete, gif și png.</p>\n"
          + "".join(f'<audio controls src="m/{os.path.basename(r)}"></audio>\n' for r in other_media if r.endswith(".wav"))
          + "".join(f'<img src="m/{os.path.basename(r)}" alt="">\n' for r in other_media if r.endswith((".gif", ".png")))
          + "".join(f'<a href="m/{os.path.basename(r)}">{os.path.basename(r)}</a><br>\n' for r in other_media if r.endswith(".ttf")))
t3 = page("Test webp js", "<p>Imaginile webp mici, codul js și css.</p>\n"
          + "".join(f'<img src="w/{os.path.basename(r)}" alt="">\n' for r in rest if r.endswith(".webp")))
for name, html in (("t1", t1), ("t2", t2), ("t3", t3)):
    open(f"out/{name}.html", "w", encoding="utf-8").write(html)
maps = {
    "t1": {f"s/{os.path.basename(r)}": f"game_pub/{r}" for r in sprites},
    "t2": {f"m/{os.path.basename(r)}": f"game_pub/{r}" for r in other_media},
    "t3": {f"w/{os.path.basename(r)}": f"game_pub/{r}" for r in rest},
}
for k, v in maps.items():
    print(k, len(v), "files")
    print(json.dumps(v))
