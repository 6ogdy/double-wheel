import re
p = open("out/demo.html", encoding="utf-8").read()
new = ('<p class="row-label new">Nou, auriu, de la simplu la mai detaliat</p>\n    <div class="gems">\n'
 + "".join(f'      <figure><div class="slot"><img src="new/{f}.webp" alt="{c}"></div><figcaption>{c}</figcaption></figure>\n'
   for f, c in [("gold_clean", "Baza, curată"), ("gold_c1", "Nivel 1"), ("gold_c2", "Nivel 2"), ("gold_c3", "Nivel 3")])
 + '    </div>\n  </section>')
p, n = re.subn(r'<p class="row-label new">Nou, auriu</p>.*?</div>\n  </section>', new, p, count=1, flags=re.S)
p = re.sub(r'(<h2 id="gems-h">).*?(</h2>\s*<p>).*?(</p>)', r'\1Piatra, trei niveluri de detaliu\2Aceeași formă trapezoidală și aceeași dimensiune. Fiecare nivel adaugă puțin față de cel dinainte: mai întâi diagonalele, apoi un diamant central cu ramă interioară, apoi razele de lumină. Fără umbre închise.\3', p, count=1, flags=re.S)
open("out/demo.html", "w", encoding="utf-8").write(p); print("replaced", n)
