"""Put the multicolor gem on both wheels of a built game folder.
usage (repo root; needs pillow): add_multicolor.py assets/wheel-v6clean/game-published [...]
- copies assets/gems/multicolor.png as img/multicolor.webp (450x342, like the other gems)
- patches both wheel renders so 2-3 random stones per wheel and per round show the multicolor gem instead of their colour
- picks keep every colour on the wheel at least once, never touch WILD, and keep neighbours at least 3 slots apart
- the stone keeps its colour class, so the winning effect and the payout logic are unchanged (the gem is visual only)"""
import sys, re
from PIL import Image

JS = 'static/js/main.d348ebcc.js'
OLD = 'src:this.getImg(t),alt:t},e))'
NEW = 'src:window.__mc?window.__mc(e,this.props.diamondsValues,this.getImg(t),"%s"):this.getImg(t),alt:t},e))'
HELPER = '''
  // multicolor gems: 2-3 per wheel and round, replacing random stones; every colour stays on the wheel, WILD (6) is never replaced
  window.__mc = (function () {
    var cache = {};
    function pick(v) {
      var n = v.length, cnt = {}, i, k;
      v.forEach(function (x) { cnt[x] = (cnt[x] || 0) + 1; });
      var want = 2 + Math.floor(Math.random() * 2), out = [], tries = 0;
      while (out.length < want && tries++ < 200) {
        i = Math.floor(Math.random() * n);
        if (v[i] === 6 || cnt[v[i]] < 2 || out.some(function (j) { var d = Math.abs(i - j); return Math.min(d, n - d) < 3; })) continue;
        cnt[v[i]]--; out.push(i);
      }
      return out;
    }
    return function (i, v, def, side) {
      if (!v || !v.length) return def;
      var key = side + v.join(','), hit = cache[key];
      if (!hit) { cache = {}; hit = cache[key] = pick(v); }
      return hit.indexOf(i) >= 0 ? './img/multicolor.webp' : def;
    };
  })();
'''
for d in sys.argv[1:]:
    Image.open('assets/gems/multicolor.png').convert('RGBA').resize((450, 342), Image.LANCZOS).save(f'{d}/img/multicolor.webp', quality=92)
    js = open(f'{d}/{JS}', encoding='utf8').read()
    if '__mc' in js: print(d, 'already patched'); continue
    assert js.count(OLD) == 2, (d, js.count(OLD))
    js = js.replace(OLD, NEW % 'L', 1).replace(OLD, NEW % 'R', 1)
    open(f'{d}/{JS}', 'w', encoding='utf8').write(js)
    rp = open(f'{d}/replay.js', encoding='utf8').read()
    rp = rp.replace('(function () {\n', '(function () {' + HELPER, 1)
    open(f'{d}/replay.js', 'w', encoding='utf8').write(rp)
    print(d, 'ok')
