import math, re
def table(N):
    step = 360 / N; half = step / 2
    rv = [(0, math.floor(half), 2)]
    for j in range(1, N):
        c = j * step; rv.append((math.floor(c - half) + 1, math.floor(c + half), (N + 2 - j - 1) % N + 1))
    rv.append((math.floor(360 - half) + 1, 360, 2)); return rv
js = open("out/game/static/js/main.d348ebcc.js", encoding="utf-8").read()   # untouched original from the client
orig = [tuple(map(int, m)) for m in re.findall(r"\{minDegree:(\d+),maxDegree:(\d+),value:(\d+)\}", re.search(r"rotationValues=\[(.*?)\],this\.rotationValues", js).group(1))]
print("original entries:", len(orig), "| my rule at N=25 matches original:", table(25) == orig)
t20 = table(20); print("N=20 entries:", len(t20), "| covers 0..360 without gaps:", all(t20[i][1] + 1 == t20[i + 1][0] for i in range(len(t20) - 1)))
