(function () {
  var W = window.WebSocket;
  function post(o) {
    try { fetch("/__rec", { method: "POST", body: JSON.stringify(o), keepalive: true }); } catch (e) {}
  }
  window.WebSocket = function (u, p) {
    var ws = p ? new W(u, p) : new W(u);
    post({ t: Date.now(), dir: "open", d: u });
    ws.addEventListener("message", function (e) { post({ t: Date.now(), dir: "in", d: e.data }); });
    var os = ws.send.bind(ws);
    ws.send = function (d) { post({ t: Date.now(), dir: "out", d: d }); return os(d); };
    return ws;
  };
  window.WebSocket.prototype = W.prototype;
})();
