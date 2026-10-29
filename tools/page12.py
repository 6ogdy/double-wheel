import json, re
p = open("out/demo.html", encoding="utf-8").read()
p, n1 = re.subn(r'  <section aria-labelledby="game-h">.*?</section>\n\n', "", p, count=1, flags=re.S)
i = p.rfind("<script>")
assert i > 0 and "game-frame" in p[i:]
p = p[:i].rstrip() + "\n"
open("out/demo.html", "w", encoding="utf-8").write(p)
print("removed section", n1, "| game refs left:", p.count("game/"), "| game-frame left:", p.count("game-frame"))
print(json.dumps({k: None for k in json.load(open("out/game_files.json"))}))
