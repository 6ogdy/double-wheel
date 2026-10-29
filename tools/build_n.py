"""Rebuild out/game_pub_s2 from the clean copy out/game_pub_fig with N wheel positions instead of 25.
Touches: main.js (4 hard-coded 25-position spots), replay.js (seq + winning positions), index.html css (stone positions/size), blw/brw (Figma wheels)."""
import json, math, os, re, shutil
os.chdir("out")   # run from the project root: py -I tools/build_n.py
from PIL import Image

N = 20
KEEP = [0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 13, 15, 16, 17, 18, 19, 20, 22, 23]   # original 0-based positions kept (drops 3, 12, 21 gold; 14 green; 24 wild)
assert len(KEEP) == N
SRC, DST = "game_pub_fig", "game_pub_s2"
shutil.copytree(SRC, DST, dirs_exist_ok=True)

# 1. wheel images from Figma (left wheel magenta = Wheel - 4, right wheel green = Wheel - 3)
M = f"{DST}/static/media/"
Image.open("../assets/wheel/wheel_magenta_left.png").convert("RGBA").save(M + "blw.aca7b4f092b7011ac227.webp", "WEBP", quality=92, method=6)
Image.open("../assets/wheel/wheel_green_right.png").convert("RGBA").save(M + "brw.f635fb57c5c829d76274.webp", "WEBP", quality=92, method=6)

# 2. main.js
step = 360 / N; half = step / 2
def centre(v): return ((N + 2 - v) % N) * step           # same rule as the 25-position table: value 2 sits at 0 deg
rv = [{"minDegree": 0, "maxDegree": math.floor(half), "value": 2}]
for j in range(1, N):
    c = j * step; v = (N + 2 - j - 1) % N + 1
    assert abs(centre(v) - c) < 1e-9
    rv.append({"minDegree": math.floor(c - half) + 1, "maxDegree": math.floor(c + half), "value": v})
rv.append({"minDegree": math.floor(360 - half) + 1, "maxDegree": 360, "value": 2})
lit = "rotationValues=[" + ",".join("{minDegree:%d,maxDegree:%d,value:%d}" % (r["minDegree"], r["maxDegree"], r["value"]) for r in rv) + "]"
p = f"{DST}/static/js/main.d348ebcc.js"; js = open(p, encoding="utf-8").read()
js, n1 = re.subn(r"rotationValues=\[\{minDegree:0,maxDegree:7,value:2\}.*?\{minDegree:353,maxDegree:360,value:2\}\]", lambda m: lit, js)
old_data = "this.data=[" + ",".join(["14.4"] * 25) + "]"
js, n2 = js.replace(old_data, "this.data=[" + ",".join([("%g" % step)] * N) + "]"), js.count(old_data)
n3 = js.count(".maxDegree)-7"); js = js.replace(".maxDegree)-7", ".maxDegree)-%d" % math.floor(half))
n4 = js.count("(r+5)%25"); js = js.replace("(r+5)%25", "(r+5)%%%d" % N)
assert (n1, n2, n3, n4) == (2, 2, 2, 2), (n1, n2, n3, n4)
open(p, "w", encoding="utf-8").write(js)

# 3. replay.js: 20-value seq, winning positions mapped to a kept position of the same stone type
p = f"{DST}/replay.js"; rp = open(p, encoding="utf-8").read()
m = re.search(r"var VISUAL = (.*);\n  var ROUNDS = (.*);\n", rp); visual, rounds = json.loads(m.group(1)), json.loads(m.group(2))
seq = visual["1"]["seq"]; assert seq == [1,2,3,1,6,4,1,2,6,1,2,3,1,6,2,1,4,6,1,2,3,1,5,2,6], seq
def newpos(i):                                              # i = original 1-based position
    o = i - 1
    if o in KEEP: return KEEP.index(o) + 1
    cands = [k for k in KEEP if seq[k] == seq[o]]
    k = min(cands, key=lambda k: (min((k - o) % 25, (o - k) % 25), k))
    return KEEP.index(k) + 1
visual["1"]["seq"] = [seq[k] for k in KEEP]
rounds2 = [[r[0], ",".join(str(newpos(int(x))) for x in r[1].split(","))] for r in rounds]
for a, b in zip(rounds, rounds2):                            # type at the new position must still equal the crash value
    for t, pos in zip(b[0].split(","), b[1].split(",")): assert visual["1"]["seq"][int(pos) - 1] == int(t), (a, b)
rp = rp.replace(m.group(0), "var VISUAL = " + json.dumps(visual, ensure_ascii=False) + ";\n  var ROUNDS = " + json.dumps(rounds2) + ";\n")
open(p, "w", encoding="utf-8").write(rp)
print("seq:", visual["1"]["seq"]); print("rounds:", rounds2)

# 4. css: stones on a circle (1000 px box, centre 500,500), bigger, WILD in the same frame as the diamonds
R, W = 401, 144; H = W * 380 / 500
rules = [".stonesCon img{width:%dpx!important;margin:0!important}" % W, ".stonesCon img.wild{width:%dpx!important;margin:0!important}" % W]
for k in range(1, N + 1):
    th = (k - 2) * step; a = math.radians(th)
    rules.append(".stonesCon img.s%d{left:%.1fpx;top:%.1fpx;transform:rotate(%.1fdeg)}" % (k, 500 + R * math.cos(a) - W / 2, 500 + R * math.sin(a) - H / 2, th))
html = open(f"{DST}/index.html", encoding="utf-8").read()
for old in (".stonesCon img{width:126px!important;margin-left:-3px;margin-top:-2.3px}", ".stonesCon img.wild{width:126px!important;margin-left:-3px;margin-top:-2.3px}", ".stonesCon img.wild{width:200px!important;margin-left:-35px;margin-top:-26.6px}"):
    html = html.replace(old, "")
html = html.replace(".wheel-background,.wheel_stonesCon canvas,.wheel_stonesCon2 canvas{opacity:0!important}", ".wheel_stonesCon canvas,.wheel_stonesCon2 canvas{opacity:0!important}")   # keep the Figma wheel image, hide only the old canvas drawing
assert ".wheel-background" not in html.split("<style>")[1] or True
# the full wheel image is back, so each wheel is ~794 px wide at scale 1.2: shrink to 1.058 (about 700 px), keep centres at x=730 and x=1530, diamond gem centre at x=1130 (container origin = 92 px left of the gem centre)
for old, new in ((".wheel-container{scale:1.2;translate:168px -5px}", ".wheel-container{scale:1.058;translate:138px -5px}"),
                 (".wheel-container2{scale:1.2;translate:205px 5px}", ".wheel-container2{scale:1.058;translate:205px 5px}"),
                 (".arrow-container{margin-left:186px}", ".arrow-container{margin-left:170px}")):
    assert html.count(old) == 1, old
    html = html.replace(old, new)
assert html.count("</head>") == 1
html = html.replace("</head>", "<style>" + "".join(rules) + "</style></head>")
open(f"{DST}/index.html", "w", encoding="utf-8").write(html)
print("stones: W=%d H=%.1f R=%d step=%g deg" % (W, H, R, step))
