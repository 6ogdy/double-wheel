"""Patch the 25-position games for 425 px princess frames. Run it after build_v6.py (which recreates the game folders),
then run build_princess_sheets.py to put the real sheets in. The published copies once carried blank 4200x4200 placeholders
(identical md5, no visible pixels), so the princess never showed.
Patches: frameWidth 300 -> 425 in main.js, canvas scale 2.8333 -> 2 and a 91 px downward translate in index.html.
usage (repo root): py tools/restore_princess.py"""
for kind in ('moss', 'clean'):
    G = f'assets/wheel-v6{kind}-25/game-published'
    js =f'{G}/static/js/main.d348ebcc.js'
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
