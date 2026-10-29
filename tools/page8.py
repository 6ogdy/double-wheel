p = open("out/demo.html", encoding="utf-8").read()
anchor = '    <p class="row-label new">Nou, auriu, de la simplu la mai detaliat</p>'
assert p.count(anchor) == 1
names = [("gold", "Auriu"), ("green", "Verde"), ("blue", "Cyan"), ("pink", "Roz"), ("violet", "Violet")]
row = ('    <p class="row-label new">Nivel 6, cele cinci culori</p>\n    <div class="gems">\n'
  + "".join(f'      <figure><div class="slot"><img src="new/n6_{f}.webp" alt="Nivel 6, {c}"></div><figcaption>{c}</figcaption></figure>\n' for f, c in names)
  + '    </div>\n    <p class="row-label" style="margin-top:32px">Toate variantele de lucru</p>\n')
p = p.replace(anchor, row + anchor, 1)
p = p.replace("Piatra, șase niveluri de detaliu", "Piatra, nivelul 6 în cinci culori")
open("out/demo.html", "w", encoding="utf-8").write(p); print("ok")
