p = open("out/demo.html", encoding="utf-8").read()
p = p.replace(".wild-pair .slot, .wild-one .slot { background", ".wild-trio { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 24px; margin-top: 32px; }\n.wild-trio .slot, .wild-pair .slot, .wild-one .slot { background", 1)
p = p.replace("  .wild-pair, dl {", "  .wild-pair, .wild-trio, dl {", 1)
p = p.replace("@media (max-width: 900px) { .gems {", "@media (max-width: 900px) { .wild-trio { grid-template-columns: minmax(0, 1fr); } .gems {", 1)
def fig(f, c):
    return f'      <figure><p class="row-label new">{c}</p><div class="slot"><img src="{f}" alt="WILD, {c}"></div></figure>\n'
trio = ('    <div class="wild-trio">\n' + fig("new/wild_k1.webp", "Negru, contur auriu subțire") + fig("new/wild_k2.webp", "Negru lucios, contur gros")
  + fig("new/wild_k3.webp", "Obsidian, contur cristal") + '    </div>\n  </section>\n\n  <section aria-labelledby="spec-h">')
anchor = '  </section>\n\n  <section aria-labelledby="spec-h">'
assert p.count(anchor) == 1
p = p.replace(anchor, trio)
open("out/demo.html", "w", encoding="utf-8").write(p); print("ok", p.count("wild-trio"))
