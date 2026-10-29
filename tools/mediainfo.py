import os, struct, wave
from PIL import Image

G = "out/game_pub"
p = f"{G}/audio/notify.wav"
h = open(p, "rb").read(64)
print("notify.wav header:", h[:4], h[8:12], "fmt tag:", struct.unpack("<H", h[20:22])[0], "channels:", struct.unpack("<H", h[22:24])[0],
      "rate:", struct.unpack("<I", h[24:28])[0], "bits:", struct.unpack("<H", h[34:36])[0])
try:
    w = wave.open(p); print("  stdlib wave opens it:", w.getparams())
except Exception as e:
    print("  stdlib wave FAILS:", e)
for rel in ("img/wheel-spin.gif", "img/lucky.gif"):
    im = Image.open(f"{G}/{rel}"); print(rel, im.size, im.mode, "frames", getattr(im, "n_frames", 1))
for rel in ("static/media/toastB.0a3cec266608dc8d7f9d.png", "favicon.png", "img/mute.png", "img/sound.png"):
    im = Image.open(f"{G}/{rel}"); print(rel, im.size, im.mode, im.info.get("interlace"), os.path.getsize(f"{G}/{rel}"))
for dp, _, fs in os.walk(G):
    for f in fs:
        if f.endswith(".webp"):
            q = os.path.join(dp, f); im = Image.open(q)
            print(q.replace(chr(92), "/").replace(G + "/", ""), im.size, im.mode, "lossless?" if b"VP8L" in open(q, "rb").read(40) else "lossy/ext")
