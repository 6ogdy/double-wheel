"""Build out/game/replay.js: a fake WebSocket that replays the real server's protocol, recorded in out/rec*.jsonl.

Recorded cycle (18 s per round, measured from server timestamps):
  starting(id) -> +4 s blocking -> +1 s started(crash, commCrash) -> +8 s crash(crash) -> +5 s starting(id+1)
"""
import json

rows = []
for p in ("out/rec_try1.jsonl", "out/rec.jsonl"):
    rows += [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]

visual = None
pairs = []
for r in rows:
    if r["dir"] != "in":
        continue
    j = json.loads(r["d"])
    if j["0"] == "visual" and j["1"].get("state") == "ENDED":
        visual = j
    if j["0"] == "started":
        pairs.append([j["1"]["crash"], j["1"]["commCrash"]])
seen, uniq = set(), []
for p in pairs:
    if tuple(p) not in seen:
        seen.add(tuple(p)); uniq.append(p)
print("visual keys:", list(visual["1"].keys()), "| history len:", len(visual["1"].get("history", [])))
print("unique recorded rounds:", len(uniq))

shim = r"""
(function () {
  var VISUAL = __VISUAL__;
  var ROUNDS = __ROUNDS__;
  var id = VISUAL[1].id, n = 0;
  function FakeWS(url) {
    var ws = this; ws.url = url; ws.readyState = 0; ws.onopen = ws.onmessage = ws.onclose = ws.onerror = null;
    function emit(a) { if (ws.readyState === 1 && ws.onmessage) ws.onmessage({ data: JSON.stringify(a) }); }
    function round() {
      var r = ROUNDS[Math.floor(Math.random() * ROUNDS.length)];
      id += 1;
      emit({ 0: "starting", 1: { id: id } });
      // the real server waits 4 s for bets; the demo hides the bet UI, so the wait is shortened (spin stays 8 s)
      setTimeout(function () { emit({ 0: "blocking" }); }, 1500);
      setTimeout(function () { emit({ 0: "started", 1: { crash: r[0], commCrash: r[1] } }); }, 2500);
      setTimeout(function () { emit({ 0: "crash", 1: { crash: r[0] } }); }, 10500);
    }
    ws.send = function (d) {
      var m = JSON.parse(d);
      if (m[0] === "visual") {
        var now = Date.now();  // keeps the on-screen clock current (skipped if the browser clock is not real)
        if (now > 1e12) VISUAL[1].created = new Date(now - VISUAL[1].elapsed).toISOString();
        emit(VISUAL);
        setTimeout(function () { round(); ws._t = setInterval(round, 15000); }, 1500);
      }
    };
    ws.close = function () { clearInterval(ws._t); ws.readyState = 3; if (ws.onclose) ws.onclose({}); };
    ws.addEventListener = function () {}; ws.removeEventListener = function () {};
    setTimeout(function () { ws.readyState = 1; if (ws.onopen) ws.onopen({}); }, 50);
  }
  FakeWS.CONNECTING = 0; FakeWS.OPEN = 1; FakeWS.CLOSING = 2; FakeWS.CLOSED = 3;
  window.WebSocket = FakeWS;
})();
""".replace("__VISUAL__", json.dumps(visual, ensure_ascii=False)).replace("__ROUNDS__", json.dumps(uniq))
open("out/game/replay.js", "w", encoding="utf-8").write(shim)
print("replay.js bytes:", len(shim))
