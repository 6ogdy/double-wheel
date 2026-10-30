# Double Wheel: predare (2026-10-30)

Înlocuiește partea de stare din `PLAN.md`. Citește asta întâi după clear.

## Linkuri
- Artifact client (public, versiunea 10): https://claude.ai/artifact/SL1AvvkppMENDsBk6XQZd3. Orice publicare e vizibilă imediat.
- Figma: https://www.figma.com/design/AOF1TrOfT05yBhSCclowOc/Double-Wheel-V2, pagina `drafts`, secțiunea `Aztec wheel v2 (editable)` (straturi, componente `Stone` și `Wild`, `Wheel / Left`, `Wheel / Right`, `Scene 1920x1080`).
- Repo: https://github.com/6ogdy/double-wheel, branch `claude/loving-meitner-cctcdf`.

## Ce e făcut (în artifact)
- Roți aztec bronz, 20 de segmente, centrate exact (`tools/build_wheel.py`: remapare polară, medalion strat separat sub inel, centroid 500,500). Medalion 624 px: violet stânga, verde dreapta, închise la culoare.
- Pietre fără fundal, 150 px lățime, pe raza 393 (mijlocul benzii dintre buza interioară și bordura greca), cu umbră CSS. WILD = placă de bronz sculptată (varianta neagră a fost scoasă, selectorul de jos și el).
- Cota: Alfa Slab One (subset `alfa-sub.woff`), gradient auriu, centrată pe medalion (`top: calc(572px - 0.461em)`); `WILD` la 128 px, majuscule.
- Masă de piatră (`altar.webp`) și câte un picior de bronz (`foot.webp`) sub fiecare roată, prin `.con-doubleWheel::before`.
- Roțile cad de sus la începutul rundei, stânga apoi dreapta cu 0,5 s (patch în `main.d348ebcc.js`, ramura `STARTING`; dreapta folosește `y` pozitiv pentru că `.wheel-container2` e rotit cu 180°).
- Optimizare: sprite-urile prințesei la 300 px/cadru (patch `frameWidth:300` în JS și `scale(2.8333)` în CSS), `toastB` în WebP, Rubik în woff2 subset, pietre la 450x342. Total de la ≈19 MB la ≈9 MB.

## Structura jocului (de știut)
- `game/index.html` e CRA minificat cu CSS și script injectate; `replay.js` simulează WebSocket-ul (runde la 15 s).
- Wheel container 1000x1072, centrul roții la y=572 în coordonatele containerului; stânga: `translate:138px -1px`, dreapta: `translate:205px 1px`, ambele `scale 1.058`.
- Imaginea roții se afișează 1000x1000; stonesCon: left/top din CSS (`s1..s20`, unghi `(n-2)*18`).
- Prințesa se încarcă prin Pixi (`ax.load`) înainte de joc; asta ține ecranul "Loading...".

## Neterminat / idei
1. Încărcarea: `main.js` 2,4 MB și sprite-urile (≈4,5 MB) blochează încă ecranul de încărcare. Idee: încarcă doar `pending` la început, restul în fundal (cere patch în `init()` și retry în `KT`).
2. Pietrele noi, mai mari și volumetrice ca în referință (acum sunt cele originale, doar fără fundal și mărite 4%).
3. Măștile blend din Figma sunt aproximative față de culoarea din joc (în joc e coacută în `medallion_*.png`).
4. Selectorul WILD: variantele negre sunt în `assets/wild/` dacă se cer înapoi.
5. Referința de stil e imaginea cu roata aztec, pietre mari, "x2" auriu.

## Fișiere
- `assets/wheel-v2/`: ring, medalioane, placă WILD, altar, picior, plus `game-published/` (copia jocului publicat, fără sprite-uri).
- `tools/build_wheel.py` (inel + medalion), `tools/remove_gem_bg.py` (fundal pietre), `tools/process_gems.py` (vechi).
- `assets/orig/` ignorat de git.
