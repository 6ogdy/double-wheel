"""files map for the Artifact tool: game-v4 = moss 25, game-v5 = clean 25. run from repo root"""
import os, json
m = {}
for v, k in (('v4', 'moss'), ('v5', 'clean')):
    r = f'assets/wheel-v6{k}-25/game-published'
    for d, _, fs in os.walk(r):
        for f in fs:
            p = os.path.join(d, f).replace('\\', '/')
            m[f'game-{v}/' + os.path.relpath(p, r).replace('\\', '/')] = p
    m[f'game-{v}/static/js/main.nanim.js'] = None        # old name; the new build ships main.d348ebcc.js
print(len(m), 'entries', file=__import__('sys').stderr)
print(json.dumps(m, separators=(',', ':')))
