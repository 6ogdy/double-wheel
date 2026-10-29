import base64, re
js = open("out/game_pub/static/js/main.d348ebcc.js", encoding="utf-8").read()
for m in re.finditer(r"data:((?:image|audio|video)/[a-z0-9.+-]+);base64,([A-Za-z0-9+/=]*)", js):
    raw = base64.b64decode(m.group(2) + "=" * (-len(m.group(2)) % 4))
    print(m.start(), m.group(1), "b64 chars:", len(m.group(2)), "bytes:", len(raw), "head:", raw[:16])
    ctx = js[max(0, m.start() - 90): m.start()].replace("\n", " ")
    print("   context before:", ctx[-90:])
