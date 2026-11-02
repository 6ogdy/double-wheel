"""Put the real princess sprite sheets (half size, 425 px frames) into the 25-position games.
The published copies carried blank 4200x4200 placeholders (identical md5, no visible pixels), so the princess never showed.
usage (repo root): py tools/restore_princess.py   -- needs out/game_small/*_half.webp (made by the sheet recompression step)"""
import shutil

SHEETS = ['idle.8ea07a61d9d150621e57', 'pending.b4f905d3bde8f7f7d722', 'winning.0ebfac7e244ab37c9a79']
for kind in ('moss', 'clean'):
    G = f'assets/wheel-v6{kind}-25/game-published'
    for n in SHEETS:
        shutil.copyfile(f'out/game_small/{n}_half.webp', f'{G}/static/media/{n}.webp')
    js = f'{G}/static/js/main.d348ebcc.js'
    code = open(js, encoding='utf-8').read()
    a, b = 'frameWidth:300,frameHeight:300', 'frameWidth:425,frameHeight:425'
    if code.count(a) == 1: code = code.replace(a, b)
    assert code.count(b) == 1, 'frame size patch'
    open(js, 'w', encoding='utf-8').write(code)
    ix = f'{G}/index.html'
    html = open(ix, encoding='utf-8').read()
    a, b = '.con-amazonPrincess>div{transform:scale(2.8333);transform-origin:0 0}', '.con-amazonPrincess>div{transform:scale(2);transform-origin:0 0}'   # 425 px frame x 2 = the same 850 px footprint
    if html.count(a) == 1: html = html.replace(a, b)
    assert html.count(b) == 1, 'scale patch'
    a, b = '.con-amazonPrincess{translate:-50px 0}', '.con-amazonPrincess{translate:-50px 91px}'   # the game hides her cut-off feet under the bottom bar (bottom:91px); the demo has no bar, so she goes down to the screen edge
    if html.count(a) == 1: html = html.replace(a, b)
    assert html.count(b) == 1, 'translate patch'
    open(ix, 'w', encoding='utf-8').write(html)
    print(kind, 'ok')
