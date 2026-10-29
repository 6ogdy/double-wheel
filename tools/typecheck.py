"""List every published file with its extension, detected format (magic bytes) and size, flagging mismatches."""
import os, struct

def detect(p):
    with open(p, "rb") as f:
        h = f.read(64)
    if h[:8] == b"\x89PNG\r\n\x1a\n": return "png"
    if h[:3] == b"GIF": return "gif"
    if h[:3] == b"\xff\xd8\xff": return "jpeg"
    if h[:4] == b"RIFF" and h[8:12] == b"WEBP":
        with open(p, "rb") as f:
            blob = f.read(4096)
        return "webp(animated)" if b"ANIM" in blob else "webp"
    if h[:4] == b"RIFF" and h[8:12] == b"WAVE": return "wav"
    if h[:3] == b"ID3" or (h[0] == 0xFF and (h[1] & 0xE0) == 0xE0): return "mp3"
    if h[4:8] == b"ftyp": return "mp4:" + h[8:12].decode("latin1")
    if h[:4] in (b"\x00\x01\x00\x00", b"true", b"OTTO"): return "ttf"
    try:
        h.decode("utf-8"); return "text"
    except Exception:
        return "unknown"

OK = {"png": {"png"}, "gif": {"gif"}, "webp": {"webp"}, "jpg": {"jpeg"}, "jpeg": {"jpeg"}, "wav": {"wav"}, "mp3": {"mp3"}}
for root in ("out/game_pub", "out/new", "out/orig"):
    for dp, _, fs in os.walk(root):
        for f in sorted(fs):
            p = os.path.join(dp, f); ext = f.rsplit(".", 1)[-1].lower(); d = detect(p)
            flag = ""
            if ext in OK and d not in OK[ext]: flag = "  <-- MISMATCH"
            if ext == "mp4" and not d.startswith("mp4"): flag = "  <-- MISMATCH"
            if "animated" in d: flag += "  <-- animated webp"
            if flag or os.path.getsize(p) > 3_000_000 or ext in ("ttf", "json", "js", "css"):
                print(f"{p.replace(chr(92), '/'):70s} .{ext:5s} {d:14s} {os.path.getsize(p)/1e6:7.2f} MB{flag}")
