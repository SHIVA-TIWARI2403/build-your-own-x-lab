import socket
import time
import unittest
import json
from miniserver import MiniHTTPServer

class TestMiniHTTPServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.port = 8899
        cls.server = MiniHTTPServer(port=cls.port)
        cls.server.start(block=False)
        time.sleep(0.15)

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()

    def _http_request(self, method, path, body="", headers=None):
        headers = headers or {}
        req_lines = [f"{method} {path} HTTP/1.1", f"Host: 127.0.0.1:{self.port}"]
        for k, v in headers.items():
            req_lines.append(f"{k}: {v}")
        if body:
            req_lines.append(f"Content-Length: {len(body)}")
        req_lines.append("\r\n")
        req_payload = "\r\n".join(req_lines) + body

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("127.0.0.1", self.port))
            s.sendall(req_payload.encode("utf-8"))
            response_data = b""
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                response_data += chunk
        return response_data.decode("utf-8", errors="ignore")

    def test_get_static_html(self):
        resp = self._http_request("GET", "/")
        self.assertTrue(resp.startswith("HTTP/1.1 200 OK"))
        self.assertIn("Content-Type: text/html", resp)
        self.assertIn("Mini-HTTP-Server", resp)

    def test_get_api_health(self):
        resp = self._http_request("GET", "/api/health")
        self.assertTrue(resp.startswith("HTTP/1.1 200 OK"))
        self.assertIn("application/json", resp)
        body = resp.split("\r\n\r\n")[1]
        data = json.loads(body)
        self.assertEqual(data["status"], "ok")

    def test_post_api_echo(self):
        body_content = "Hello MiniServer World"
        resp = self._http_request("POST", "/api/echo", body=body_content)
        self.assertTrue(resp.startswith("HTTP/1.1 200 OK"))
        body = resp.split("\r\n\r\n")[1]
        data = json.loads(body)
        self.assertEqual(data["received_body"], body_content)

    def test_404_not_found(self):
        resp = self._http_request("GET", "/non_existent_page_1234")
        self.assertTrue(resp.startswith("HTTP/1.1 404 Not Found"))

if __name__ == "__main__":
    unittest.main()
