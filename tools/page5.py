p = open("out/demo.html", encoding="utf-8").read()
anchor = 'Nivel 3</figcaption></figure>\n    </div>\n  </section>'
add = ('Nivel 3</figcaption></figure>\n    </div>\n    <p class="row-label new" style="margin-top:32px">Mai realist, sticlă lustruită</p>\n    <div class="gems">\n'
 + "".join(f'      <figure><div class="slot"><img src="new/{f}.webp" alt="{c}"></div><figcaption>{c}</figcaption></figure>\n'
   for f, c in [("gold_r1", "Nivel 4"), ("gold_r2", "Nivel 5"), ("gold_r3", "Nivel 6")])
 + '    </div>\n  </section>')
assert p.count(anchor) == 1
p = p.replace(anchor, add)
p = p.replace("Piatra, trei niveluri de detaliu", "Piatra, șase niveluri de detaliu")
p = p.replace("apoi razele de lumină. Fără umbre închise.", "apoi razele de lumină. Nivelurile 4-6 păstrează aceeași structură, dar redau piatra ca sticlă lustruită, cu tot mai multe fațete. Fără umbre închise.")
open("out/demo.html", "w", encoding="utf-8").write(p); print("ok")
