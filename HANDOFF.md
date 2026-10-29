# Double Wheel: predare (29 oct 2026)

Document pentru o sesiune nouă. Înlocuiește `PLAN.md`, care e vechi (a fost scris înainte să existe demo-ul).
Citește mai întâi secțiunea **Ce a cerut Bogdan ca următor pas**, apoi restul.

## 1. Scop

Clientul vrea jocul Double Wheel (PixiJS + GSAP + Redux, build create-react-app) cu elemente noi, mai curate.
Jocul real **nu se rescrie**. Se schimbă doar imagini și puțin CSS, în aceleași dimensiuni și cu același raport.
Pentru client: un demo public cu jocul și un artifact separat cu elementele.

Reguli ale lui Bogdan (din `~/.claude/CLAUDE.md`): verifică înainte să afirmi, explică simplu cu exemple reale,
răspunde în română, fără cratime lungi în textul vizibil, fișierele doar în folderul proiectului,
orice comandă Python cu `</dev/null` (altfel pornește REPL-ul și umple discul).

## 2. Linkuri

| Ce | Link | Stare |
|---|---|---|
| Joc, public | https://claude.ai/artifact/8Gr8mdYoUgjrU7cGov3ii8 | partajat cu oricine are linkul; are **încă discul vechi** pe roată. Orice republicare se vede imediat la client |
| Joc, roți aerisite | https://claude.ai/artifact/JGSWa44fY1tKZiF84SwhQo | privat; Bogdan a spus că **nu-i place** (vezi secțiunea 3) |
| Elemente (pietre, WILD, variante) | https://claude.ai/artifact/CyK4wvMPH6ucjDXxASw4Tc | versiunea 15, doar imagini, fără joc |
| 5 artifact-uri de test | `Lccpt2KYbQsY6EidbMELUV`, `L9N6LwSA7f2DrueutxEssQ`, `UuyhwZ8fNsN4HnwFiMPZy1`, `YMmDv3qo5DUzoozRSBytjF`, `22Pb3ZY4jE3nC9mbY7s2i1` | de șters, dar doar dacă Bogdan cere |
| Figma | https://www.figma.com/design/AOF1TrOfT05yBhSCclowOc/Double-Wheel-V2 | **neatins** (doar `whoami`). Pasul "Figma curat cu componente" nu e făcut |
| Demo original (client) | https://www.cfvbfbtlotto.com/retail/client_api_3/update_page/files_double_wheel/ | neschimbat |

## 3. Ce a cerut Bogdan ca următor pas

Mesajul lui, în ordine, după ce a văzut varianta aerisită:

1. **Elementele colorate nu sunt ok.** Rotirea de nuanță dintr-o singură piatră aurie dă culori care nu-i plac (cyan prea deschis, violet prea închis).
   Trebuie altă soluție de recolorare. Idei: (a) harta de gradient pe luminanță, cu culorile exacte din joc (`--col_1..5`: `#f7c328 #3ff419 #00edff #ff22d6 #cc74ff`);
   (b) generare per culoare cu editare Higgsfield pornind de la piatra nivel 6 ("păstrează forma și structura, schimbă doar culoarea în ...");
   (c) componente cu variante de culoare în Figma.
2. **"Ai scos toată roata, nu doar cea externă."** Trebuie scos doar discul exterior. Au rămas de păstrat: discul interior cu modelul și cercurile aurii interioare.
   Acum `.wheel-background` (imaginea `blw.webp` / `brw.webp`, 298x300) conține și discul exterior și cel interior, iar `<canvas>` desenează cercurile aurii și separatoarele.
   Soluția probabilă: editez `blw`/`brw` (taie inelul exterior, lasă cercul interior) și ascund doar ce desenează canvas-ul în exterior.
3. **Mai puține elemente pe roată, ca să se poată mări.** Acum sunt 25 de poziții pe inel (`s1..s25`), pietrele se ating deja. Mărirea cere mai puține poziții.
   Poziția fiecărei pietre e în CSS (`.stonesCon img.sN{left;top;transform:rotate()}`), dar numărul de poziții și mapările rezultatelor sunt în JS (secvența `seq` din serverul real, 25 de valori).
   De investigat în `static/js/main.*.js` înainte să se promită ceva. Nu se poate decide singur: întrebați-l pe Bogdan câte poziții vrea.
4. **WILD să aibă aceeași dimensiune ca diamantele.** Acum `.stonesCon img.wild{width:200px}` față de 126 px la pietre. Se aduce la aceeași lățime a cadrului (aceeași cutie 500x380 ca piatra).

**Mai întâi, în ordinea cerută de el: `push main` și predarea (acest document).** Restul de mai sus vine după.

## 4. Alegerile făcute până acum

| Subiect | Alegere | Fișier |
|---|---|---|
| Piatra | **Nivelul 6** (sticlă lustruită, aceeași structură ca nivelul 3) | `assets/stones/level6/*.webp` |
| WILD | **Obsidian, mai bold** (negru cu contur auriu) | `assets/wild/wild_n2.webp` |
| Alte WILD păstrate | aurii (v1..v4, b1..b3), negre (k1..k3, n1, n3) | `assets/wild/` |
| Variante vechi de piatră | păstrate, Bogdan a zis "posibil să revenim" | `assets/stones/variants/` |

Toate fișierele noi sunt la **3x**: 1500x1140 pentru piatră, 1500x528 pentru partea vizibilă a WILD-ului.
Raportul e identic cu originalele din joc (piatră 500x380 = 1,316; WILD vizibil 500x176 = 2,841, la 104 px de sus în cadru, 312 px la 3x).
Fișierul `wildFlipped` din joc e oglindit și la 100 px de sus (300 la 3x). `tools/wildswap.py` îl produce.

Silueta originală a pietrei (trapez) se păstrează aplicând masca alfa a originalului. Pietrele s-au generat cu Higgsfield `gpt_image_2_5` (2k, calitate high, fundal transparent),
prin **editare pe o imagine de referință**, nu din text.

## 5. Higgsfield

- Model: `gpt_image_2_5`, 2k high = 2,75 credite/imagine. Credite la ultima verificare: 5257 (plan max).
- Referințe încărcate (media_id): piatra originală aurie `75ac129b-8108-42d1-8e7b-98b535313f6c`, piatra curată `c10a88d2-3a2b-4deb-a554-1033d561d73d`,
  nivel 3 `863d3cb9-231d-4b09-83dc-0c5ee6143a07`, WILD original `206178ca-2bfe-4981-9d63-d8d5aac2a573`,
  WILD negre `13f52e95-fb15-4b3a-a22e-2d1f64502fe2` (lucios) și `16d3bbe0-da1f-4fad-b0ad-bd9adcebdadc` (obsidian). Expiră, dar sunt în istoricul Higgsfield.
- Lecție: generat din text, modelul nu respectă raportul. Funcționează: editare pe referință + decupare la caseta vizibilă + scalare la cadrul original + mască alfa.

## 6. Demo-ul: cum e făcut

Jocul se leagă la `wss://csubretail.com:3913` (server real). Un artifact nu are voie la WebSocket extern, deci demo-ul **redă rundele înregistrate**.

- Protocol (JSON): `{"0":"visual"}` trimis de joc, răspuns `visual` cu `state, id, elapsed, created, crash, commCrash, elem_time:8000, start_time:5000, coef, seq, history, status, top, currency`;
  apoi ciclu de 18 s: `starting{id}` -> +4 s `blocking` -> +1 s `started{crash,commCrash}` -> +8 s `crash{crash}` -> +5 s următorul `starting`.
- `tools/mkreplay.py` construiește `replay.js` (un `WebSocket` fals) din `demo/rec_try1.jsonl` și `demo/rec.jsonl` (11 runde reale). În demo ciclul e scurtat la 15 s (nu mai există ecran de pariuri).
- Înregistrare: `tools/rec_server.py` + `tools/rec.js` (server local care salvează cadrele).
- `index.html` primește `replay.js` înaintea `main.*.js`. Pagina "shell" (`demo/demo_game.html`) pune jocul într-un iframe de 1920x1080 scalat.

### CSS-ul demo-ului (`tools/demo_css.py`)

- Ascunde interfața cu `opacity:0`, **nu** cu `display:none`: jocul așteaptă evenimente de la bara de timp, iar cu `display:none` roțile nu mai pornesc.
- `.background_video` ascuns, fundalul e `background.webp` (aceeași junglă).
- Personajul: sprite-urile sunt la jumătate de rezoluție (cadre de 425 px), `main.js` e modificat (`frameWidth:850` -> `425`) și canvasul e scalat 2x din CSS.
- Roțile (varianta aerisită): `.wheel-container{scale:1.2}`, pietre 126 px, WILD 200 px, margini negative ca centrele să rămână pe loc.

## 7. Capcane (toate verificate)

| Problemă | Cauza reală | Ce am făcut |
|---|---|---|
| Partajarea publică respinsă: "couldn't be reviewed" | `main.js` conținea **două imagini încorporate**: `data:image/avif;base64,...` (AVIF nu e tip permis) și `data:video/webm;base64,...`. Sunt teste Pixi pentru suport de format | înlocuite cu `data:,` în `tools/lean.py`. Găsit prin 5 artifact-uri de test (sprite-urile, fonturile, sunetele, gif-urile și webp-urile treceau) |
| Fișiere uriașe | sprite-urile personajului: 11050x11050 px, 25 MB (limita artifact: 15 MB/fișier) | reduse la jumătate (`tools/sprites_half.py`), 2 până la 5 MB |
| Browserul din aplicație arată data 01/01/1970 | în panoul de browser `Date.now()` returnează 0 (am verificat) | nu e o eroare a jocului; la utilizator ceasul merge |
| Demo fără sunet și fără video de fundal | mp3-urile și mp4-ul nu au fost cauza respingerii, dar le-am scos ca să reduc riscul | `lean.py` pune WAV-uri goale; sunetele reale se pot readuce (neîncercat dacă trec) |
| Artifact public și republicare | modificările se văd imediat la oricine are linkul | variantele noi se publică **într-un artifact nou**, apoi se înlocuiește cel public doar la cererea lui Bogdan |
| `gh` activ e `design-mkt-1` (doar citire pe repo) | repo-ul e al lui `6ogdy` | `GH_TOKEN="$(gh auth token --user 6ogdy)"` pe comandă, fără să schimbi contul activ |

## 8. Cum reiei lucrul

Structura de lucru așteptată de scripturi (rulează din rădăcina proiectului, cu `out/` lângă `tools/`):

```bash
# 1. jocul original (NU e în repo, aparține clientului)
bash tools/fetch_game.sh            # creează out/game cu build-ul

# 2. reconstruiește folderul de publicat
py -I tools/mkreplay.py </dev/null
py -I tools/pub.py </dev/null       # copiază în out/game_pub, sprite-uri la jumătate, patch main.js
py -I tools/demo_css.py </dev/null  # CSS-ul demo-ului
py -I tools/lean.py </dev/null      # fără video/mp3, patch AVIF/WebM
py -I tools/wildswap.py </dev/null  # WILD obsidian în joc

# 3. test local
py -I -m http.server 8767 --directory out/game_pub --bind 127.0.0.1 </dev/null
# deschide http://127.0.0.1:8767/index.html?v=N la 1920x1080; prima rotire apare după ~25 s
```

Publicarea se face cu uneltele Artifact: `file_path` = pagina shell, `root` = `out`, `files` = harta din `out/game_lean_files.json`.
Scripturile `tools/*.py` au fost scrise pe parcurs; cele care contează sunt `pub.py`, `demo_css.py`, `lean.py`, `mkreplay.py`, `wildswap.py`, `sprites_half.py`, `colours6.py`, `wildfit*.py`, `measure.py`, `sheet.py`.
Restul sunt unelte de inspecție (`*_peek.py`, `typecheck.py`, `datauri.py`, `refcheck.py`).

## 9. Ce NU e în repo (și de ce)

- `out/game` și `out/game_pub`: build-ul clientului, ~70 MB. Se re-descarcă cu `tools/fetch_game.sh`.
- `assets/orig/`: pietrele și WILD originale (din demo). Se re-descarcă la fel.
- Orice token. Contul `6ogdy` e deja autentificat pe calculatorul lui Bogdan.

## 10. Ce n-am verificat

- Jocul din artifact nu l-am deschis eu în mediul artifact-ului (e privat); Bogdan l-a văzut și a confirmat că merge.
- Dacă sunetele și videoul de fundal trec de verificare la partajare (nu le-am retestat după ce am găsit cauza reală).
- Figma: nimic.
