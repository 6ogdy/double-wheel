import re
css = open("out/game_pub/static/css/main.be085d95.css", encoding="utf-8").read()
urls = sorted(set(re.findall(r"url\(([^)]*)\)", css)))
print("CSS url() refs:", len(urls))
for u in urls:
    print("  ", u[:140])
js = open("out/game_pub/static/js/main.d348ebcc.js", encoding="utf-8").read()
ext = sorted(set(re.findall(r"https?://[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=%-]+", js)))
print("JS absolute URLs:", len(ext))
for u in ext:
    print("  ", u[:140])
print("JS data: URIs:", len(re.findall(r"data:(?:image|audio|video)/[a-z0-9.+-]+;base64", js)))
print("JS size MB:", round(len(js) / 1e6, 2), "| longest line chars:", max(len(l) for l in js.split("\n")))
