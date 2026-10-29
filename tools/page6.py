import re
p = open("out/demo.html", encoding="utf-8").read()
p = p.replace(".wild-pair .slot { background", ".wild-one { max-width: 560px; margin-bottom: 32px; }\n.wild-pair .slot, .wild-one .slot { background", 1)
def fig(f, c, new=True):
    cls = "row-label new" if new else "row-label"
    return f'      <figure><p class="{cls}">{c}</p><div class="slot"><img src="{f}" alt="WILD, {c}"></div></figure>\n'
block = ('<div class="wild-one">\n' + fig("orig/wild.webp", "Original", False).replace("      ", "    ", 1) + '    </div>\n    <div class="wild-pair">\n'
  + fig("new/wild_v1.webp", "1. Aceeași formă, mai curat")
  + fig("new/wild_v2.webp", "2. Mai bold, fațete")
  + fig("new/wild_v3.webp", "3. Mai bold, cristal")
  + fig("new/wild_v4.webp", "4. Mai bold, metal lustruit")
  + fig("new/wild.webp", "Varianta anterioară, lucioasă")
  + '    </div>\n  </section>')
p, n = re.subn(r'<div class="wild-pair">.*?</div>\n  </section>', lambda m: block, p, count=1, flags=re.S)
p = p.replace("<h2 id=\"wild-h\">WILD mai bold</h2>", "<h2 id=\"wild-h\">WILD, variante</h2>")
p = re.sub(r'(<h2 id="wild-h">.*?</h2>\s*<p>).*?(</p>)', r'\1Același cadru și aceleași proporții ca fișierul din joc. Variantele pornesc de la literele originale: de la aceeași formă cu fațete mai curate, până la litere mai groase.\2', p, count=1, flags=re.S)
open("out/demo.html", "w", encoding="utf-8").write(p); print("replaced", n)
