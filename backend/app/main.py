import os
import sys
import json
from pathlib import Path

# Ensure backend directory is in sys.path
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from app.config.settings import settings
from app.config.database import db
from app.rag.vector_store import vector_store
from app.utils.logger import logger
from app.api.router import route_request

class BankingAPIHandler(SimpleHTTPRequestHandler):
    def _set_cors_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Request-ID")
        self.send_header("Content-Type", "application/json")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_cors_headers(204)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query_params = {k: v[0] if len(v) == 1 else v for k, v in parse_qs(parsed.query).items()}
        headers = {k.lower(): v for k, v in self.headers.items()}

        if path in ("/", "/health"):
            self._set_cors_headers(200)
            self.wfile.write(json.dumps({
                "status": "healthy",
                "service": settings.PROJECT_NAME,
                "version": "1.0.0"
            }).encode("utf-8"))
            return

        res = route_request(
            method="GET",
            path=path,
            headers=headers,
            query_params=query_params
        )

        status_code = res.get("status_code", 200)
        self._set_cors_headers(status_code)
        self.wfile.write(json.dumps(res).encode("utf-8"))

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        headers = {k.lower(): v for k, v in self.headers.items()}

        content_length = int(self.headers.get("Content-Length", 0))
        body = {}
        if content_length > 0:
            raw_body = self.rfile.read(content_length).decode("utf-8")
            try:
                body = json.loads(raw_body)
            except Exception:
                body = {}

        res = route_request(
            method="POST",
            path=path,
            body=body,
            headers=headers
        )

        status_code = res.get("status_code", 200)
        self._set_cors_headers(status_code)
        self.wfile.write(json.dumps(res).encode("utf-8"))

    def do_DELETE(self):
        parsed = urlparse(self.path)
        path = parsed.path
        headers = {k.lower(): v for k, v in self.headers.items()}

        res = route_request(
            method="DELETE",
            path=path,
            headers=headers
        )

        status_code = res.get("status_code", 200)
        self._set_cors_headers(status_code)
        self.wfile.write(json.dumps(res).encode("utf-8"))

    def do_PUT(self):
        parsed = urlparse(self.path)
        path = parsed.path
        headers = {k.lower(): v for k, v in self.headers.items()}

        content_length = int(self.headers.get("Content-Length", 0))
        body = {}
        if content_length > 0:
            raw_body = self.rfile.read(content_length).decode("utf-8")
            try:
                body = json.loads(raw_body)
            except Exception:
                body = {}

        res = route_request(
            method="PUT",
            path=path,
            body=body,
            headers=headers
        )

        status_code = res.get("status_code", 200)
        self._set_cors_headers(status_code)
        self.wfile.write(json.dumps(res).encode("utf-8"))

    def log_message(self, format, *args):
        logger.info(f"{self.address_string()} - {format % args}")

def run_server(host: str = "0.0.0.0", port: int = 8000):
    server = HTTPServer((host, port), BankingAPIHandler)
    logger.info(f"=================================================")
    logger.info(f" Apex Bank Daily Banking Assistant API")
    logger.info(f" Listening on http://{host}:{port}")
    logger.info(f" Health check: http://127.0.0.1:{port}/health")
    logger.info(f"=================================================")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Server shutting down gracefully.")
        server.server_close()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    run_server(port=port)
