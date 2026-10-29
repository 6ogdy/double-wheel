"""Find every media/file path the game's html, css and js mention, and report the ones missing from the published folder."""
import os, re

G = "out/game_pub"
texts = {}
for rel in ("index.html", "static/css/main.be085d95.css", "static/js/main.d348ebcc.js", "replay.js"):
    texts[rel] = open(os.path.join(G, rel), encoding="utf-8").read()
exts = r"(?:png|jpe?g|gif|webp|svg|avif|mp4|webm|mp3|wav|ogg|m4a|ttf|woff2?|otf|json|ico|mov)"
pat = re.compile(r"""["'(]([A-Za-z0-9_./~\-]*\.%s)(?:\?[^"')]*)?["')]""" % exts)
seen = {}
for rel, t in texts.items():
    for m in pat.finditer(t):
        seen.setdefault(m.group(1), set()).add(rel)
missing = []
for ref, where in sorted(seen.items()):
    cands = [os.path.normpath(os.path.join(G, ref.lstrip("./"))),
             os.path.normpath(os.path.join(G, "static", ref.lstrip("./"))),
             os.path.normpath(os.path.join(G, "static/media", os.path.basename(ref)))]
    ok = any(os.path.exists(c) for c in cands)
    if not ok:
        missing.append((ref, sorted(where)))
print("refs found:", len(seen), "| missing:", len(missing))
for m in missing:
    print("MISSING", m)
