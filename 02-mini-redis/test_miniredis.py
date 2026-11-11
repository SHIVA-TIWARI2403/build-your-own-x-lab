import socket
import time
import unittest
from miniredis import MiniRedisServer

class TestMiniRedis(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.port = 6388
        cls.server = MiniRedisServer(port=cls.port)
        cls.server.start(block=False)
        time.sleep(0.15) # Wait for socket to bind

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()

    def _send_cmd(self, cmd_str):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("127.0.0.1", self.port))
            s.sendall(f"{cmd_str}\r\n".encode("utf-8"))
            resp = s.recv(1024).decode("utf-8")
        return resp

    def test_ping(self):
        resp = self._send_cmd("PING")
        self.assertEqual(resp, "+PONG\r\n")

    def test_set_and_get(self):
        self._send_cmd("SET user:101 Shiva")
        resp = self._send_cmd("GET user:101")
        self.assertEqual(resp, "$5\r\nShiva\r\n")

    def test_incr(self):
        self._send_cmd("SET views 10")
        resp = self._send_cmd("INCR views")
        self.assertEqual(resp, ":11\r\n")

    def test_ttl_expiry(self):
        self._send_cmd("SET temp_token secret123 EX 1")
        resp1 = self._send_cmd("GET temp_token")
        self.assertIn("secret123", resp1)
        time.sleep(1.2)
        resp2 = self._send_cmd("GET temp_token")
        self.assertEqual(resp2, "$-1\r\n") # Expired

    def test_del_and_exists(self):
        self._send_cmd("SET session_id abc999")
        resp_exists = self._send_cmd("EXISTS session_id")
        self.assertEqual(resp_exists, ":1\r\n")

        self._send_cmd("DEL session_id")
        resp_not_exists = self._send_cmd("EXISTS session_id")
        self.assertEqual(resp_not_exists, ":0\r\n")

if __name__ == "__main__":
    unittest.main()
