"""Static server for out/game plus POST /__rec, which appends recorded websocket frames to out/rec.jsonl."""
import http.server, os, sys, time

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out", "game")
REC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out", "rec.jsonl")


class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(n).decode("utf-8")
        with open(REC, "a", encoding="utf-8") as f:
            f.write(body.replace("\n", " ")[:-1] + ',"ts":' + repr(time.time()) + "}\n")
        self.send_response(204)
        self.end_headers()

    def log_message(self, *a):
        pass


http.server.ThreadingHTTPServer(("127.0.0.1", int(sys.argv[1])), H).serve_forever()
