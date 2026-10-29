import re
s = open("out/game/static/js/main.d348ebcc.js", encoding="utf-8").read()
for key in ("SERVER_TIMEZONE", "serverTimezone"):
    for m in list(re.finditer(key, s))[:6]:
        print(key, m.start(), "::", s[max(0, m.start() - 250): m.end() + 350].replace("\n", " "))
        print("-----")
