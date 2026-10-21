import json
import os
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse


class Handler(BaseHTTPRequestHandler):
    server_version = "SandboxTarget/0.1"

    def send_json(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        request = urlparse(self.path)
        if request.path == "/healthz":
            self.send_json(200, {"status": "ok"})
            return

        if request.path != "/run":
            self.send_json(404, {"error": "not found"})
            return

        command = parse_qs(request.query).get("command", [""])[0]
        if not command:
            self.send_json(400, {"error": "missing command"})
            return

        # Deliberately vulnerable: this is the behavior under test.
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd="/tmp",
                capture_output=True,
                text=True,
                timeout=2,
                check=False,
            )
        except subprocess.TimeoutExpired:
            self.send_json(408, {"error": "command timed out"})
            return

        self.send_json(
            200,
            {
                "returncode": result.returncode,
                "stdout": result.stdout[-4096:],
                "stderr": result.stderr[-4096:],
                "sandbox": {
                    "uid": os.getuid(),
                    "cwd": os.getcwd(),
                },
            },
        )

    def log_message(self, format_string, *args):
        return


HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
