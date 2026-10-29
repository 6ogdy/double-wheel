p = open("out/demo.html", encoding="utf-8").read()
anchor = '  </section>\n\n  <section aria-labelledby="spec-h">'
assert p.count(anchor) == 1
def fig(f, c):
    return f'      <figure><p class="row-label new">{c}</p><div class="slot"><img src="{f}" alt="WILD negru, {c}"></div></figure>\n'
row = ('    <p class="row-label" style="margin-top:32px">Negru, contur auriu, mai bold</p>\n    <div class="wild-trio">\n'
  + fig("new/wild_n1.webp", "Lucios, mai bold") + fig("new/wild_n3.webp", "Intermediar, bold") + fig("new/wild_n2.webp", "Obsidian, mai bold") + '    </div>\n')
p = p.replace(anchor, row + anchor)
old = "Jocul real, cu pietrele de la nivelul 6. Rundele sunt redate din înregistrări ale serverului, fără conexiune live. WILD rămâne cel original până alege clientul."
assert old in p
p = p.replace(old, "Doar roțile și personajul, cu pietrele de la nivelul 6. Rundele sunt redate din înregistrări ale serverului, fără conexiune live, iar prima rotire apare după câteva secunde. WILD rămâne cel original până alege clientul.")
open("out/demo.html", "w", encoding="utf-8").write(p); print("ok")
