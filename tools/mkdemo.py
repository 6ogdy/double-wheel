p = open("out/game/index.html", encoding="utf-8").read()
t = '<script defer="defer" src="./static/js/main.d348ebcc.js">'
assert p.count(t) == 1
open("out/game/demo.html", "w", encoding="utf-8").write(p.replace(t, '<script src="./replay.js"></script>' + t))
print("demo.html ok")
