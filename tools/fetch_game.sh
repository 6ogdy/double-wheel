#!/usr/bin/env bash
# Re-download the client's game build into out/game (not stored in the repo). Run from the project root.
set -e
B=https://www.cfvbfbtlotto.com/retail/client_api_3/update_page/files_double_wheel
mkdir -p out/game/static/js out/game/static/css out/game/static/media out/game/img out/game/audio
cd out/game
curl -sS "$B/" -o index.html
curl -sS "$B/static/js/main.d348ebcc.js" -o static/js/main.d348ebcc.js
curl -sS "$B/static/css/main.be085d95.css" -o static/css/main.be085d95.css
for f in $(grep -oE 'static/media/[A-Za-z0-9_.-]+' static/js/main.d348ebcc.js static/css/main.be085d95.css | sed 's/^[^:]*://' | sort -u) \
         img/centerGems.webp img/leftArrow.webp img/rightArrow.webp img/mute.png img/sound.png img/ic1_sub.webp img/ic2_sub.webp img/ic3_sub.webp \
         img/blue.webp img/pink.webp img/wheel-spin.gif img/lucky.gif \
         audio/notify.wav audio/magic.mp3 audio/mystic-ambience.mp3 audio/spin.mp3 audio/wild.mp3 favicon.png manifest.json logo192.png; do
  curl -sS "$B/$f" -o "$f" -w "%{http_code} %{size_download} $f\n"
done
# the original stones and WILD for comparison
mkdir -p ../orig
for n in gold.d53168443bfda397846e green.f25c93dd911fde41af2f blue.52c7c705f881c6ec951f pink.8cfdeb4e09969b101163 violet.fe2430dc563bad88d219 wild.a5499ba14606d75104e8 wildFlipped.9b0176bdc4cb414babc6; do
  curl -sS "$B/static/media/$n.webp" -o "../orig/${n%%.*}.webp"
done
