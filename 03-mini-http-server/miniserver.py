import socket
import threading
import os
import json
import time
import sys

MIME_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".txt": "text/plain; charset=utf-8",
    ".png": "image/png",
    ".jpg": "image/jpeg"
}

class MiniHTTPServer:
    def __init__(self, host="127.0.0.1", port=8080, public_dir="public"):
        self.host = host
        self.port = port
        self.public_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), public_dir))
        self.running = False
        self.sock = None

    def build_response(self, status_code: int, status_text: str, content: bytes, content_type: str = "text/plain") -> bytes:
        headers = [
            f"HTTP/1.1 {status_code} {status_text}",
            f"Content-Type: {content_type}",
            f"Content-Length: {len(content)}",
            "Server: MiniServer/1.0 (Raw-Socket)",
            "Connection: close",
            f"Date: {time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime())}",
            "",
            ""
        ]
        return "\r\n".join(headers).encode("utf-8") + content

    def handle_request(self, raw_request: str) -> bytes:
        lines = raw_request.split("\r\n")
        if not lines or not lines[0]:
            return self.build_response(400, "Bad Request", b"Malformed HTTP Request")

        request_line = lines[0].split()
        if len(request_line) < 3:
            return self.build_response(400, "Bad Request", b"Malformed Request Line")

        method, path, _ = request_line
        
        # Parse query params
        query_params = {}
        if "?" in path:
            path, query_str = path.split("?", 1)
            for pair in query_str.split("&"):
                if "=" in pair:
                    k, v = pair.split("=", 1)
                    query_params[k] = v

        # Read body if present
        body = ""
        if "\r\n\r\n" in raw_request:
            body = raw_request.split("\r\n\r\n", 1)[1]

        # Built-in REST Endpoints
        if path == "/api/health":
            payload = json.dumps({"status": "ok", "timestamp": int(time.time()), "engine": "MiniHTTPServer"}).encode("utf-8")
            return self.build_response(200, "OK", payload, "application/json")

        elif path == "/api/echo" and method == "POST":
            payload = json.dumps({"received_body": body, "length": len(body)}).encode("utf-8")
            return self.build_response(200, "OK", payload, "application/json")

        elif path == "/api/info":
            payload = json.dumps({"server": "MiniHTTPServer", "author": "Shiva Tiwari", "architecture": "pure socket"}).encode("utf-8")
            return self.build_response(200, "OK", payload, "application/json")

        # Static file handling
        rel_path = "index.html" if path == "/" else path.lstrip("/")
        safe_path = os.path.normpath(os.path.join(self.public_dir, rel_path))

        # Directory traversal prevention
        if not safe_path.startswith(self.public_dir):
            return self.build_response(403, "Forbidden", b"Access Denied")

        if os.path.exists(safe_path) and os.path.isfile(safe_path):
            _, ext = os.path.splitext(safe_path)
            content_type = MIME_TYPES.get(ext.lower(), "application/octet-stream")
            with open(safe_path, "rb") as f:
                content = f.read()
            return self.build_response(200, "OK", content, content_type)

        return self.build_response(404, "Not Found", b"<h1>404 Not Found</h1><p>Resource does not exist.</p>", "text/html")

    def _client_worker(self, client_sock):
        with client_sock:
            try:
                data = b""
                while True:
                    chunk = client_sock.recv(4096)
                    data += chunk
                    if len(chunk) < 4096 or b"\r\n\r\n" in data:
                        break
                if data:
                    raw_req = data.decode("utf-8", errors="ignore")
                    response = self.handle_request(raw_req)
                    client_sock.sendall(response)
            except Exception:
                pass

    def start(self, block=True):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(20)
        self.running = True

        print(f"[MiniHTTP] Server running on http://{self.host}:{self.port}")

        def accept_loop():
            while self.running:
                try:
                    client_sock, _ = self.sock.accept()
                    t = threading.Thread(target=self._client_worker, args=(client_sock,), daemon=True)
                    t.start()
                except OSError:
                    break

        if block:
            accept_loop()
        else:
            t = threading.Thread(target=accept_loop, daemon=True)
            t.start()

    def stop(self):
        self.running = False
        if self.sock:
            try:
                self.sock.close()
            except Exception:
                pass

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    srv = MiniHTTPServer(port=port)
    try:
        srv.start(block=True)
    except KeyboardInterrupt:
        print("\nShutting down MiniServer...")
        srv.stop()
