import re
s = open("out/game/static/js/main.d348ebcc.js", encoding="utf-8").read()
for key in ("amazonPrincess",):
    for m in list(re.finditer(key, s))[:4]:
        print(m.start(), "::", s[max(0, m.start() - 700): m.end() + 1400].replace("\n", " "))
        print("--------")
