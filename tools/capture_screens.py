"""capture two rounds of the 25-position game at 1920x1080, every 0.5 s, princess layer hidden (it is added later from the HQ poses).
run from repo root: py out/cap/run.py"""
import time, os, glob
from playwright.sync_api import sync_playwright

URL = 'http://localhost:8765/assets/wheel-v6moss-25/game-published/index.html'
OUT = 'out/cap/run'
os.makedirs(OUT, exist_ok=True)
for f in glob.glob(f'{OUT}/*.png'): os.remove(f)
ARGS = ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist']
with sync_playwright() as pw:
    b = pw.chromium.launch(args=ARGS)
    p = b.new_page(viewport={'width': 1920, 'height': 1080}, device_scale_factor=1)
    # rounds: ROUNDS[floor(r * 11)]; first r=.05 -> index 0, then .85 -> index 9 (the WILD round)
    p.add_init_script('(() => { const s = [0.05, 0.85, 0.5]; let i = 0; Math.random = () => s[Math.min(i++, s.length - 1)]; })();')
    p.add_style_tag(content='.con-amazonPrincess{visibility:hidden!important}')
    p.goto(URL)
    p.wait_for_function("document.body.innerText.includes('RUND')", timeout=60000)
    p.add_style_tag(content='.con-amazonPrincess{visibility:hidden!important}')
    t1 = time.time()
    for i in range(70):
        p.screenshot(path=f'{OUT}/f_{i:03d}.png')
        print(i, round(time.time() - t1, 1), flush=True)
        time.sleep(max(0, 0.5 * (i + 1) - (time.time() - t1)))
    b.close()
