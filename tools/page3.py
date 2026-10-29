import re
from PIL import Image, ImageChops
ref = Image.open("out/ref/gold_ref.png").convert("RGBA")
m = Image.open("out/edit3/m0.png").convert("RGBA")
e = Image.open("out/edit3/e0.png").convert("RGBA").resize(ref.size, Image.LANCZOS)
# keep only pixels opaque in BOTH the original silhouette and the generated art, so no colour fringe shows at the edge
a = ImageChops.darker(ref.getchannel("A"), e.getchannel("A"))
a = a.point(lambda v: 0 if v < 200 else v)
out = e.copy(); out.putalpha(a); out.save("out/new/gold_clean.webp", "WEBP", quality=92, method=6)
p = open("out/demo.html", encoding="utf-8").read()
p = re.sub(r'<p class="row-label new">Variante noi, auriu</p>.*?</div>\n  </section>',
 '<p class="row-label new">Nou, auriu</p>\n    <div class="gems">\n      <div class="slot"><img src="new/gold_clean.webp" alt="Piatră aurie, nouă, curată"></div>\n    </div>\n  </section>', p, count=1, flags=re.S)
p = p.replace("<h2 id=\"gems-h\">Pietrele, structură nouă</h2>", "<h2 id=\"gems-h\">Piatra, curată și simplă</h2>")
p = re.sub(r'(<h2 id="gems-h">.*?</h2>\s*<p>).*?(</p>)', r'\1Aceeași formă trapezoidală și aceeași dimensiune. Fațete puține și mari, culori plate, o singură sclipire, fără umbre închise. Celelalte patru culori se obțin din această piatră după aprobare.\2', p, count=1, flags=re.S)
open("out/demo.html", "w", encoding="utf-8").write(p)
print("gems blocks:", p.count('class="gems"'), "| v-refs left:", p.count("gold_v"))
