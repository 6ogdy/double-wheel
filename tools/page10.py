p = open("out/demo.html", encoding="utf-8").read()
css = """.game-frame { position: relative; width: 100%; aspect-ratio: 16 / 9; background: #000; border-radius: var(--radius); overflow: hidden; }
.game-frame iframe { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; border: 0; transform-origin: 0 0; }
.game-link { margin-top: 16px; }
.game-link a { color: var(--accent); font-weight: 500; }
"""
p = p.replace("figure { margin: 0;", css + "figure { margin: 0;", 1)
section = """  <section aria-labelledby="game-h">
    <div class="section-head">
      <h2 id="game-h">Jocul, cu pietrele noi</h2>
      <p>Jocul real, cu pietrele de la nivelul 6. Rundele sunt redate din înregistrări ale serverului, fără conexiune live. WILD rămâne cel original până alege clientul.</p>
    </div>
    <div class="game-frame" id="game-frame"><iframe id="game-iframe" src="game/index.html" title="Double Wheel" allow="autoplay"></iframe></div>
    <p class="game-link"><a href="game/index.html" target="_blank" rel="noopener">Deschide jocul pe tot ecranul</a></p>
  </section>

"""
anchor = '  <section aria-labelledby="gems-h">'
assert p.count(anchor) == 1
p = p.replace(anchor, section + anchor, 1)
script = """<script>
(function () {
  var box = document.getElementById("game-frame"), fr = document.getElementById("game-iframe");
  function fit() { fr.style.transform = "scale(" + (box.clientWidth / 1920) + ")"; }
  fit(); window.addEventListener("resize", fit);
})();
</script>
"""
p = p.rstrip() + "\n" + script
open("out/demo.html", "w", encoding="utf-8").write(p); print("ok")
