"""Split test 3: t4 = js + css only, t5 = the webp images only."""
import json, os
G = "out/game_pub"
webps = []
for dp, _, fs in os.walk(G):
    for f in sorted(fs):
        r = os.path.relpath(os.path.join(dp, f), G).replace("\\", "/")
        if f.endswith(".webp") and os.path.basename(r).split(".")[0] not in ("idle", "pending", "winning"):
            webps.append(r)
style = ("<style>:root{--bg:#0b0f0c;--fg:#e8efe9;color-scheme:dark}body{background:var(--bg);color:var(--fg);"
         "font:16px/1.5 system-ui,sans-serif;padding:24px}img{max-width:120px;margin:4px}</style>\n")
open("out/t4.html", "w", encoding="utf-8").write("<title>Test js css</title>\n" + style + "<h1>Test js css</h1>\n<p>Doar codul js și css al jocului.</p>\n"
                                                  '<a href="c/main.d348ebcc.js">main.js</a><br><a href="c/main.be085d95.css">main.css</a>\n')
open("out/t5.html", "w", encoding="utf-8").write("<title>Test webp mici</title>\n" + style + "<h1>Test webp mici</h1>\n"
                                                  + "".join(f'<img src="w/{os.path.basename(r)}" alt="">\n' for r in webps))
print("t4", json.dumps({"c/main.d348ebcc.js": "game_pub/static/js/main.d348ebcc.js", "c/main.be085d95.css": "game_pub/static/css/main.be085d95.css"}))
print("t5", len(webps), json.dumps({f"w/{os.path.basename(r)}": f"game_pub/{r}" for r in webps}))
