# Double Wheel: handoff, 25-position version (2026-11-03)

Read this first. It replaces the state sections of `HANDOFF.md` and `HANDOFF-aztec.md` (both in Romanian, kept as they were). From now on all documentation is in English.

## Links

| What | Where |
|---|---|
| Repo | https://github.com/6ogdy/double-wheel, branch `main` |
| Public artifact (the client sees it) | https://claude.ai/artifact/SL1AvvkppMENDsBk6XQZd3 (version 28). Change it only when the owner asks. |
| Client Figma file | https://www.figma.com/design/DOfDjqyqcqhnjtbjQuFd2g/ (file key `DOfDjqyqcqhnjtbjQuFd2g`, page `Page 1`) |
| Older Figma file, original game | https://www.figma.com/design/AOF1TrOfT05yBhSCclowOc/ (pages `drafts`, `V3 - Dev handoff`, `Backup 2026-11-01 (assets)`) |
| Live game used as the reference | https://www.cfvbfbtlotto.com/retail/client_api_3/update_page/files_double_wheel/scaling.html |

## What the game is now

- The aztec stone game, **25 gem positions per wheel** (the live game has 25: 8 gold, 6 green, 3 blue, 2 pink, 1 violet, 5 WILD). Checked in the live iframe: position sequence `1,2,3,1,6,4,1,2,6,1,2,3,1,6,2,1,4,6,1,2,3,1,5,2,6` (1 gold, 2 green, 3 blue, 4 pink, 5 violet, 6 WILD).
- Gem geometry in the 1000 px wheel box: width 130 px, centre radius 390 px, step 14.4 degrees, position `n` at `(n-2) * 14.4` degrees. No carved separators between the gems (they only exist at N=20). Gems are 5 colors of 1500x1140 art, shown from 450x342 sprites in the game.
- The medallion is 14 px larger than the 20-position version, so the free band is 15 px on both sides of the gems (measured on the exported image: gems cover radius 325 to 455, key bands end at about 310 and start at about 470).
- Two variants live in the repo: `assets/wheel-v6moss-25/game-published` (stone with moss, the one in the artifact) and `assets/wheel-v6clean-25/game-published` (no moss, not linked from the artifact page any more).
- The princess is the **v1 (dress) animation set** from `assets/girl/v1`. `assets/girl/v2` is a short-costume set that was tried and removed; it is not used anywhere.
- Scene at 1920x1080 (measured in the DOM): wheel centres `(730, 520.2)` and `(1530, 519.8)`, on-screen scale 0.7004 (the wheel shows at 700 px), altar at `(421, 885)` 1400x196, feet at `(628, 850)` and `(1428, 850)` 130x70, centre gem 104x141 at `(1078, 449)`, arrows 100x78 at `(1038, 481)` and `(1120, 481)`. The whole wheel (ring and gems) rotates together.

## Build order (run from the repo root, Python 3 with pillow, numpy, scipy)

```
N=25 py tools/build_v5.py full          # ring with key bands, gem positions, JS and replay for 25 positions
N=25 py tools/build_v6.py moss          # stone texture and moss (recreates the game folder)
N=25 py tools/build_v6.py clean
py tools/restore_princess.py            # 425 px frame patch in main.js, canvas scale 2, princess 91 px down
py tools/build_princess_sheets.py       # sprite sheets from assets/girl/v1 into both game folders
py tools/export_hq.py                   # HQ gems, altar, stone foot into out/hq (then tools/export_hq_gems_alpha.py cuts the gem background)
py tools/apply_hq_foot.py               # puts the 816 px foot into the moss game
```

Notes:
- `export_hq.py` needs the 1140x1500 gem exports in `out/figma/{gold,green,blue,pink,violet}.png` (also not in git) and `assets/wheel-v2/{altar,foot}.png`.
- `build_v5.py` reads the original 25-position `replay.js` from `out/game_pub_fig/replay.js`. `out/` is ignored by git, so on another machine that folder must be recreated first.
- On Windows, OneDrive can lock folders. If a build fails on `rmtree` with "Access is denied", remove the output folder with PowerShell `Remove-Item -Recurse -Force`, and stop any local server whose current folder is inside it.
- Python in a non-interactive shell must read stdin from nowhere: add `</dev/null` in bash. Heredoc Python is blocked by a local hook; write the script to a file first.

## Local test server and captures

```
py -m http.server 8765        # from the repo root
http://localhost:8765/assets/wheel-v6moss-25/game-published/index.html
```

`tools/capture_screens.py` shoots every 0.5 s at 1920x1080 with Playwright (Chromium needs `--use-angle=swiftshader --enable-unsafe-swiftshader` to render WebGL). `tools/capture_dom.py` does the same and also records each wheel's rotation, multiplier text and positions into `meta.json`. `tools/compose_screens.py` makes flat PNG screens.

## Princess

- Sequences: `assets/girl/v1/idle_final` (60 frames), `pending 8 sec - 3` (160), `winning 7 sec - 3` (140). All 850x850 transparent PNG. The folder is about 405 MB with v2 and is **not in git**.
- In the game the sheets are rebuilt at 425 px per frame, in grids 8x8 (idle), 13x13 (pending), 12x12 (winning): 2.7 + 6.4 + 6.5 MB. Frames at 850 px would give 25 MB per file, over the 15 MB artifact limit, and a 5525 px or larger texture on the GPU.
- Before 2026-11-03 the shipped sheets were blank placeholders (identical md5, 0 visible pixels): the princess never showed in the demo.

## Public artifact

- Page source: `demo/artifact_page.html` (a single iframe at 1920x1080, scaled to the window). The game lives in `game-v4/` (moss). `game-v5/` (clean) is still published but unlinked.
- To republish, use the Artifact tool with the URL above, `file_path` = the page, and a `files` map from `tools/artifact_files_map.py` (it prints the map; it also nulls the old `main.nanim.js`). Only changed files need to be sent.
- Limits: 15 MB per binary file, 64 MB per publish.

## Client Figma file

Everything in the file is in English.

| Section | Node | Content |
|---|---|---|
| Wheels, 25 positions | `26:2` | `23`, `24` layered wheels (1000x1000): a `Wheel / Left` or `Wheel / Right` frame with a `Wheel Empty` instance and 25 Gem and Wild instances |
| Game screens, 5 phases | `35:2` | frames `41` to `45` (1920x1080), built from layers |
| Girl (princess) | `30:2` | 8 poses, 850x850: `31` to `33` idle, `34`, `35` pending, `36` to `38` winning (`30:3` to `30:10`) |
| Components and source assets | `39:2` | `Gem` set `39:8` (Gold `39:3`, Green `39:4`, Blue `39:5`, Pink `39:6`, Violet `39:7`; 1500x1140, background cut out), `Wild` set `39:11` (Normal `39:9`, Flipped `39:10`; 450x342, not high quality, see open items), `Wheel Empty` set `39:14` (Left `39:12`, Right `39:13`; 1000x1000). These are also the source assets: the separate `Gems`, `WILD plaques` and empty-ring frames duplicated them and were deleted on 2026-11-03. |
| Foot and altar | `1:24` | foot 816x441, altar 2000x280 |
| Center gem and arrows | `1:30` | game originals |
| Background, decoration, frame, logo | `1:32` | game originals |

Screen layers, bottom to top: `Background`, `Altar`, `Shadow L`, `Shadow R`, `Foot L`, `Foot R`, `Wheel / Left`, `Wheel / Right`, `Arrow L`, `Arrow R`, `Center gem`, `Multiplier L` and `R` (Alfa Slab One, gold gradient, two shadows), `Princess`. The wheel frames are rotated with a transform matrix about their centre. The Gem instances carry the two CSS-like drop shadows as effects.

| Screen | Left wheel | Right wheel | Left text | Right text | Pose |
|---|---|---|---|---|---|
| 1 waiting | 0 deg | 0 deg | none | none | `31` |
| 2 spin start | 82.25 | 73.4 | x13 | x4 | `34` |
| 3 fast spin | 55.78 | -1.24 | x60 | x6 | `35` |
| 4 WILD on the wheel | -177.84 | -91.84 | WILD | x6 | `38` |
| 5 result | -144 | -58 | x2 | x2 | `37` |

The Figma plugin code that built these layers was run inline and is not saved in the repo. To rebuild, use the table above, the geometry section, and the node ids. Pitfalls met: a frame that received an uploaded image became an auto-layout frame once (`26:6`), so reset `layoutMode` to `NONE` after uploads; `upload_assets` with `nodeIds` replaces the fill of an existing node.

## GitHub and accounts

The active `gh` account is `design-mkt-1`, but the repo belongs to `6ogdy`. Push with that account's token:

```
TOK=$(gh auth token --user 6ogdy); git push "https://x-access-token:${TOK}@github.com/6ogdy/double-wheel.git" main
```

## Open items

1. **WILD plaques** are 450x342. The exact high-resolution source of the game version was not found (closest candidate, `assets/wheel-v2/wild_plaque.png` 1500x1107, differs by 37/255).
2. **Wheel rings** are 1000x1000. Their source is a 1024 px AI image (`assets/wheel-v3b/source_ring.png`). A real 2x ring needs the ring regenerated at 2048 px. On screen they are already sharp (shown at 700 px).
3. **Background** is 1471x777, stretched to 1920x1080 (about 1.3x), the softest area on screen. It needs the original from the client or an upscale.
4. The `clean` variant and `game-v5/` in the artifact are unused; remove them when the owner confirms.
5. The local test server on port 8765 may still be running.
6. `assets/girl/` is not in git. Decide whether to keep it only on disk or to add it (it would grow the repo a lot).
