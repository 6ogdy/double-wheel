import re
s = open("out/game/static/js/main.d348ebcc.js", encoding="utf-8").read()
for m in re.finditer(r"csubretail", s):
    print(s[max(0, m.start() - 900): m.end() + 1500].replace("\n", " "))
    print("=========")
print("WebSocket uses:", len(re.findall(r"new WebSocket", s)), "| io( uses:", len(re.findall(r"\bio\(", s)))
