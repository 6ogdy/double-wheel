# Double Wheel: plan de continuare

Document de predare pentru o sesiune nouă, rulată de pe calculatorul tău.

## Scop
Pentru client: jocul Double Wheel refăcut, elementele regenerate, Figma aranjat cu componente și un artifact demo cu schimbările cerute.

## Surse
- Demo live (wrapper de scalare): https://www.cfvbfbtlotto.com/retail/client_api_3/update_page/files_double_wheel/scaling.html
- Jocul real: https://www.cfvbfbtlotto.com/retail/client_api_3/update_page/files_double_wheel/ (build create-react-app, PixiJS + GSAP + Redux, minificat, fără source map)
- Figma: https://www.figma.com/design/AOF1TrOfT05yBhSCclowOc/Double-Wheel-V2 (pagina `drafts`: Wheel - 1/2, Slice, BoxWin, Diamonds, Medals v1/v2, Arrows, Timer, LOGO, secțiunea SIMULARE)
- Repo: https://github.com/6ogdy/double-wheel, branch `claude/loving-meitner-cctcdf`

## Ce știm despre demo
- `scaling.html` doar pune jocul într-un iframe de 1920x1080 și aplică `transform: scale(window.innerWidth/1920)`, la fiecare 100 ms.
- Culori: `--col_1 #f7c328`, `--col_2 #3ff419`, `--col_3 #00edff`, `--col_4 #ff22d6`, `--col_5 #cc74ff`, plus gradiente `--grd_1..6`.
- Fonturi: Rubik (Regular, Medium, Light, Bold, ExtraBold).
- Asset-uri în `static/media/`: pietre `gold/green/blue/pink/violet/wild/wildFlipped.webp` (500x380), `background.webp`, `bkg_video.mp4`, `frame.webp`, `winnerBox.webp`, `titleFrame.webp`, `logoGame.webp`, `flowers.webp`, `flower_right.webp`, `toastB.png`, `blw/brw.webp`, plus trei sprite sheet-uri mari (`idle`, `pending`, `winning`, câte 10-25 MB) pentru personaj.
- Descărcarea se poate relua cu `curl` pe `.../files_double_wheel/static/media/<fișier>`; numele cu hash sunt în `static/css/main.be085d95.css` și `static/js/main.d348ebcc.js`.

## Schimbări cerute până acum
1. Pietre mai pronunțate și mai curate, cât mai puține umbre închise.
2. WILD mai bold.
3. Idee nouă: generezi o singură culoare pentru piatră și pentru WILD, apoi schimbi nuanța din cod sau din Figma, în loc să generezi fiecare culoare.
4. Lista completă de schimbări (aspect, mecanică, texte) urmează de la tine.

## Ce e făcut în repo
- `assets/gems/*.png`: prima variantă a pietrelor și WILD, procesată din cod (umbre ridicate, saturație mai mare, WILD cu contur).
- `tools/process_gems.py`: scriptul care le generează din `assets/orig/` (ignorat de git, descarcă-l din demo).
- Decizie luată: jocul se rescrie în HTML/CSS/JS simplu, fără build.

## Generare imagini (stare)
- Model: `gpt_image_2_5` din Higgsfield, 1k, calitate high, fundal transparent, 4:3.
- Cost măsurat pe imagine: 1k high 1,5 credite; 2k high 2,75 credite.
- **Au fost trimise 10 joburi** (≈15 credite) chiar înainte să întrerupi: 5 variante de piatră aurie (indexurile 0-4) și 5 variante de WILD (5-9). Nu le-am vizualizat. Le găsești în istoricul Higgsfield sau cu aceste ID-uri:
  - 0 `5e3cb3a2-a8ce-46c1-8d39-c377df4849a3`
  - 1 `a1e17193-1f9c-4d46-a8cf-b6fc313c849a`
  - 2 `a6f8e7ec-3de7-4b38-a8ae-f171bf39faf7`
  - 3 `929985bc-13e4-4986-894f-f6a88acd23ef`
  - 4 `1aec4a10-c086-4fa4-9f16-44630f08bbc2`
  - 5 `2aa8fb5a-38c9-4544-bd40-c880dfb90129`
  - 6 `da6f3f66-af30-45b6-aa2b-0b3eafd39171`
  - 7 `bf4b80d1-aa0a-4a1f-9719-3d56aa9518e3`
  - 8 `c057758d-17d6-4d22-824f-1bc3eb8640f8`
  - 9 `ed86f98d-d06a-447d-85cc-5acf7dfc1dc1`
- Referințele PNG (pietrele originale) nu au fost încărcate; nu s-a generat nimic cu ele.

## Pași de făcut
1. Alege din cele 10 imagini piatra și WILD preferate (sau regenerează).
2. Fă schimbarea de nuanță din cod (Python/Pillow, rotire de hue) pentru culorile `#f7c328`, `#3ff419`, `#00edff`, `#ff22d6`, `#cc74ff`; fă o imagine cu 5 culori x variantele alese plus WILD.
3. Citește Figma (`get_design_context`, `get_screenshot`) pentru roți, Slice, BoxWin, Diamonds, Medals, Arrows, Timer, LOGO.
4. Rescrie jocul: cadru 1920x1080 scalat uniform, două roți cu pietre și WILD, multiplicator în centru, diamant central, timer, BoxWin, medalii. Confirmă regulile exacte de câștig cu cine știe mecanica.
5. Figma curat: pagină nouă cu secțiuni (Logo, Roți, Pietre, UI, Ecrane), componente cu variante (piatră pe culoare, roată 1/2, buton, timer, BoxWin), stiluri de culoare și text, auto layout.
6. Artifact demo cu schimbările cerute, apoi livrabile: link Figma, link artifact, README.

## Note pentru sesiunea de pe calculator
- Rulată local, sesiunea nu mai are restricțiile de rețea ale containerului cloud (domeniile `cfvbfbtlotto.com`, `upload.higgsfield.ai` și `d2ol7oe51mr4n9.cloudfront.net` au fost blocate până să le permiți).
- Conectează serverele MCP Figma și Higgsfield și în sesiunea locală.
- Nu comite `assets/orig/` (60 MB, 3 fișiere de câte 25 MB).
