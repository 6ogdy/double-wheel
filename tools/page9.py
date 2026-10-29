p = open("out/demo.html", encoding="utf-8").read()
anchor = '  </section>\n\n  <section aria-labelledby="spec-h">'
assert p.count(anchor) == 1
def fig(f, c):
    return f'      <figure><p class="row-label new">{c}</p><div class="slot"><img src="{f}" alt="WILD, {c}"></div></figure>\n'
row = ('    <p class="row-label" style="margin-top:32px">Încă mai bold, auriu</p>\n    <div class="wild-trio">\n'
  + fig("new/wild_b1.webp", "Fațete, +50%") + fig("new/wild_b2.webp", "Cristal, +60%") + fig("new/wild_b3.webp", "Metal lustruit, +60%") + '    </div>\n')
p = p.replace(anchor, row + anchor)
open("out/demo.html", "w", encoding="utf-8").write(p); print("ok")
