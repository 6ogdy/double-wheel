
(function () {
  var VISUAL = {"0": "visual", "1": {"state": "ENDED", "id": 70716, "elapsed": 12303, "created": "2026-10-29T20:06:02.100Z", "crash": "6,1", "commCrash": "9,19", "elem_time": 8000, "start_time": 5000, "history": [{"crash": "6,1"}, {"crash": "2,5"}, {"crash": "6,2"}, {"crash": "1,3"}, {"crash": "2,6"}, {"crash": "2,2"}, {"crash": "3,6"}, {"crash": "2,2"}, {"crash": "1,1"}, {"crash": "5,6"}, {"crash": "1,6"}, {"crash": "1,3"}, {"crash": "1,1"}, {"crash": "6,6,2,3"}, {"crash": "2,6"}, {"crash": "4,6"}, {"crash": "6,2"}, {"crash": "2,2"}, {"crash": "2,1"}, {"crash": "6,6,2,1"}, {"crash": "1,3"}, {"crash": "1,2"}, {"crash": "2,1"}, {"crash": "1,3"}, {"crash": "6,1"}, {"crash": "6,2"}, {"crash": "2,4"}, {"crash": "6,3"}, {"crash": "2,2"}, {"crash": "2,2"}, {"crash": "3,5"}, {"crash": "6,2"}, {"crash": "2,2"}, {"crash": "1,2"}, {"crash": "6,1"}, {"crash": "4,1"}, {"crash": "3,4"}, {"crash": "6,2"}, {"crash": "6,6,6,4"}, {"crash": "1,1"}, {"crash": "1,4"}, {"crash": "4,1"}, {"crash": "1,2"}, {"crash": "2,1"}, {"crash": "6,1"}, {"crash": "4,6"}, {"crash": "6,1"}, {"crash": "2,2"}, {"crash": "6,6,6,1"}, {"crash": "6,2"}, {"crash": "1,1"}, {"crash": "3,6"}, {"crash": "4,1"}, {"crash": "1,1"}, {"crash": "2,4"}, {"crash": "2,1"}, {"crash": "6,6,6,1"}, {"crash": "2,2"}, {"crash": "2,1"}, {"crash": "2,1"}, {"crash": "6,1"}, {"crash": "1,3"}, {"crash": "2,2"}, {"crash": "2,6"}, {"crash": "3,1"}, {"crash": "5,1"}, {"crash": "5,2"}, {"crash": "6,3"}, {"crash": "4,6"}, {"crash": "2,6"}, {"crash": "2,3"}, {"crash": "3,1"}, {"crash": "6,5"}, {"crash": "1,6"}, {"crash": "6,2"}], "coef": {"0": 2, "1": 4, "2": 6, "3": 13, "4": 24, "5": 60, "count": 6, "len": 2}, "seq": [1, 2, 3, 6, 4, 1, 2, 6, 1, 2, 3, 6, 1, 4, 6, 1, 2, 3, 5, 2], "status": "success", "top": {"1": [{"userId": 39925281, "moneyIn": 38095, "moneyOut": 495235, "odds": 1300, "roundId": 68655, "pick": 3, "ticketTime": "2026-10-29 11:24:33", "username": "Test shop 902"}, {"userId": 39925208, "moneyIn": 6350, "moneyOut": 152400, "odds": 2400, "roundId": 68506, "pick": 4, "ticketTime": "2026-10-29 10:38:30", "username": "Test shop 902"}, {"userId": 39925232, "moneyIn": 6350, "moneyOut": 82550, "odds": 1300, "roundId": 68510, "pick": 3, "ticketTime": "2026-10-29 10:39:42", "username": "Test shop 902"}], "7": [{"userId": 39925281, "moneyIn": 38095, "moneyOut": 495235, "odds": 1300, "roundId": 68655, "pick": 3, "ticketTime": "2026-10-29 11:24:33", "username": "Test shop 902"}, {"userId": 39925208, "moneyIn": 6350, "moneyOut": 152400, "odds": 2400, "roundId": 68506, "pick": 4, "ticketTime": "2026-10-29 10:38:30", "username": "Test shop 902"}, {"userId": 39925232, "moneyIn": 6350, "moneyOut": 82550, "odds": 1300, "roundId": 68510, "pick": 3, "ticketTime": "2026-10-29 10:39:42", "username": "Test shop 902"}], "30": [{"userId": 39925281, "moneyIn": 38095, "moneyOut": 495235, "odds": 1300, "roundId": 68655, "pick": 3, "ticketTime": "2026-10-29 11:24:33", "username": "Test shop 902"}, {"userId": 39925208, "moneyIn": 6350, "moneyOut": 152400, "odds": 2400, "roundId": 68506, "pick": 4, "ticketTime": "2026-10-29 10:38:30", "username": "Test shop 902"}, {"userId": 39925232, "moneyIn": 6350, "moneyOut": 82550, "odds": 1300, "roundId": 68510, "pick": 3, "ticketTime": "2026-10-29 10:39:42", "username": "Test shop 902"}]}, "currency": "RON"}};
  var ROUNDS = [["2,6", "2,8"], ["1,1", "13,1"], ["2,2", "10,2"], ["1,2", "1,17"], ["4,1", "5,1"], ["3,4", "11,5"], ["1,3", "13,3"], ["3,3", "11,11"], ["2,1", "2,13"], ["6,6,1,2", "4,12,16,2"], ["6,6,1,3", "4,4,6,3"]];
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
