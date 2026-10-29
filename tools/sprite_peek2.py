import re
s = open("out/game/static/js/main.d348ebcc.js", encoding="utf-8").read()
i = s.find("frameWidth:850")
seg = s[i - 2600: i]
print(seg[-2600:].replace("\n", " "))
print("=====QT component=====")
j = s.find("QT=")
print(s[j: j + 2200].replace("\n", " "))
