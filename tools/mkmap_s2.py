import json, os
D = "out/game_pub_s2"; m = {}; tot = 0
for r, _, fs in os.walk(D):
    for f in fs:
        p = os.path.join(r, f); rel = os.path.relpath(p, D).replace("\\", "/")
        m["game/" + rel] = "game_pub_s2/" + rel; tot += os.path.getsize(p)
json.dump(m, open("out/game_s2_files.json", "w"), separators=(",", ":"))
print(len(m), "files", round(tot / 1e6, 1), "MB; biggest", max(os.path.getsize(os.path.join(D, k[5:])) for k in m) // 1000, "KB")
print(json.dumps(m, separators=(",", ":")))
