"""capture two rounds at 1920x1080 every 0.5 s AND record the DOM state of each frame (wheel rotation, multiplier text, positions), so the Figma screens can be built from layers. run from repo root"""
import time, os, glob, json
from playwright.sync_api import sync_playwright

URL = 'http://localhost:8765/assets/wheel-v6moss-25/game-published/index.html'
OUT = 'out/cap/run2'
os.makedirs(OUT, exist_ok=True)
for f in glob.glob(f'{OUT}/*'): os.remove(f)
JS = """() => {
  const q = s => document.querySelector(s);
  const M = el => el ? getComputedStyle(el).transform : null;
  const r = el => { if (!el) return null; const b = el.getBoundingClientRect(); return [b.x, b.y, b.width, b.height]; };
  const out = {};
  for (const [k, sel] of [['L', '.wheel_stonesCon'], ['R', '.wheel_stonesCon2']]) {
    const w = q(sel), ring = w.querySelector('.wheel-background'), st = w.querySelector('.stonesCon');
    out[k] = {wheel: M(w), wheelRect: r(w), ring: M(ring), ringRect: r(ring), stones: M(st), stonesRect: r(st)};
  }
  out.vals = [...document.querySelectorAll('#final-value,#final-valueSecond,.final-value')].map(e => ({id: e.id, txt: e.innerText, rect: r(e), op: getComputedStyle(e).opacity, fs: getComputedStyle(e).fontSize}));
  out.center = [...document.querySelectorAll('img')].filter(i => /centerGems|Arrow/i.test(i.src)).map(i => ({src: i.src.split('/').pop(), rect: r(i), tf: M(i), op: getComputedStyle(i).opacity}));
  return out;
}"""
ARGS = ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist']
with sync_playwright() as pw:
    b = pw.chromium.launch(args=ARGS)
    p = b.new_page(viewport={'width': 1920, 'height': 1080}, device_scale_factor=1)
    p.add_init_script('(() => { const s = [0.05, 0.85, 0.5]; let i = 0; Math.random = () => s[Math.min(i++, s.length - 1)]; })();')
    p.goto(URL)
    p.wait_for_function("document.body.innerText.includes('RUND')", timeout=60000)
    p.add_style_tag(content='.con-amazonPrincess{visibility:hidden!important}')
    t1 = time.time(); meta = []
    for i in range(70):
        p.screenshot(path=f'{OUT}/f_{i:03d}.png')
        meta.append(p.evaluate(JS))
        time.sleep(max(0, 0.5 * (i + 1) - (time.time() - t1)))
    json.dump(meta, open(f'{OUT}/meta.json', 'w'))
    b.close()
print('done', len(meta))
