import re
css = open("out/game/static/css/main.be085d95.css", encoding="utf-8").read()
print("css bytes:", len(css))
rules = re.findall(r"([^{}]+)\{([^{}]*)\}", css)
keys = ("stonesCon", "wheel-background", "wheel_stonesCon", "wheel-container", ".filter", "con-doubleWheel", "arrow-container")
shown = 0
for sel, body in rules:
    if any(k in sel for k in keys) and not re.search(r"\.s\d+", sel):
        print(sel.strip()[:120], "{", body.strip()[:400], "}")
        shown += 1
print("shown", shown)
s_rules = [(sel.strip(), body.strip()) for sel, body in rules if re.search(r"\.s1\b|\.s2\b|\.s5\b", sel)]
for sel, body in s_rules[:12]:
    print("S:", sel[:100], "{", body[:300], "}")
print("gold/wild rules:", [(s.strip()[:80], b.strip()[:160]) for s, b in rules if re.search(r"\.(gold|wild|green)\b", s)][:8])
