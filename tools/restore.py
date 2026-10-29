from PIL import Image
for i in range(5):
    Image.open(f"out/edit/m{i}.png").save(f"out/new/gold_t{i+1}.webp", "WEBP", quality=92, method=6)
    Image.open(f"out/edit2/m{i}.png").save(f"out/new/gold_s{i+1}.webp", "WEBP", quality=92, method=6)
p = open("out/demo.html", encoding="utf-8").read()
anchor = 'Nivel 6</figcaption></figure>\n    </div>\n  </section>'
assert p.count(anchor) == 1
def row(label, files, caps):
    return (f'    <p class="row-label new" style="margin-top:32px">{label}</p>\n    <div class="gems">\n'
      + "".join(f'      <figure><div class="slot"><img src="new/{f}.webp" alt="{c}"></div><figcaption>{c}</figcaption></figure>\n' for f, c in zip(files, caps))
      + '    </div>\n')
add = ('Nivel 6</figcaption></figure>\n    </div>\n'
  + row("Variante anterioare, doar textura", [f"gold_t{i}" for i in range(1, 6)], [f"Textura {i}" for i in range(1, 6)])
  + row("Variante anterioare, structuri noi", [f"gold_s{i}" for i in range(1, 6)], ["În trepte", "Radială", "Pernă cu romburi", "Stea cu raze", "Trei hexagoane"])
  + '  </section>')
p = p.replace(anchor, add)
open("out/demo.html", "w", encoding="utf-8").write(p); print("restored")
