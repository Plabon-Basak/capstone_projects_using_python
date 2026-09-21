import argparse
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from store import TaskStore


STORE = TaskStore()
STATIC = Path(__file__).parent / "static"


class AppHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC), **kwargs)

    def send_json(self, status, data):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_json(self):
        length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(length) or b"{}")

    def do_GET(self):
        if self.path == "/api/tasks":
            return self.send_json(200, {"tasks": STORE.list()})
        return super().do_GET()

    def do_POST(self):
        try:
            if self.path == "/api/tasks":
                data = self.read_json()
                return self.send_json(201, STORE.create(data.get("title", "")))
            self.send_json(404, {"error": "Endpoint not found"})
        except json.JSONDecodeError:
            self.send_json(400, {"error": "Malformed JSON request body"})
        except ValueError as error:
            self.send_json(400, {"error": str(error)})

    def do_PATCH(self):
        try:
            if not self.path.startswith("/api/tasks/"):
                self.send_json(404, {"error": "Endpoint not found"})
                return
            try:
                task_id = int(self.path.rsplit("/", 1)[-1])
            except ValueError:
                self.send_json(400, {"error": "Invalid task id"})
                return
            self.send_json(200, STORE.toggle(task_id))
        except LookupError as error:
            self.send_json(404, {"error": str(error)})


def check():
    created = STORE.create("Verify frontend and backend integration")
    toggled = STORE.toggle(created["id"])
    result = {
        "status": "ok",
        "task_count": len(STORE.list()),
        "created_and_toggled": toggled,
    }
    print(json.dumps(result, indent=2))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    if args.check:
        return check()

    print(f"Day 100 app running at http://localhost:{args.port}")
    server = ThreadingHTTPServer(("localhost", args.port), AppHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
