"""Demo-only cut: keep the background, the character and the two wheels; hide the HUD, history, winners board, timer and toasts."""
p = open("out/game_pub/index.html", encoding="utf-8").read()
css = ("<style>"
       # opacity, not display:none, because the game waits on transition/animation events of some of these (the bet timer)
       ".background_video{display:none!important}"
       # airy wheels: no dark disc (wheel-background), no gold rings or dividers (canvas); bigger wheel (x1.2) and stones (126 px, WILD 200 px),
       # centres kept by negative margins, wheels and the centre diamond re-spaced so both fit between the character and the right edge
       ".wheel-background,.wheel_stonesCon canvas,.wheel_stonesCon2 canvas{opacity:0!important}"
       ".wheel-container{scale:1.2;translate:168px -5px}"
       ".wheel-container2{scale:1.2;translate:205px 5px}"
       ".con-amazonPrincess{translate:-50px 0}"
       ".stonesCon img{width:126px!important;margin-left:-3px;margin-top:-2.3px}"
       ".stonesCon img.wild{width:200px!important;margin-left:-35px;margin-top:-26.6px}"
       ".arrow-container{margin-left:186px}"
       ".App{background:#0b140d url(./static/media/background.c09b372e03a655d69d97.webp) center/cover no-repeat!important}"
       ".con-amazonPrincess{width:850px!important;height:850px!important}"
       ".con-amazonPrincess>div{transform:scale(2);transform-origin:0 0}"
       ".CrashVisualization,.CrashHistoryBar,.topTableCounter_container,.PlayerList,.App>section{opacity:0!important;pointer-events:none!important}"
       "</style>")
assert "</head>" in p
p = p.replace("</head>", css + "</head>", 1)
open("out/game_pub/index.html", "w", encoding="utf-8").write(p)
print("css added")
