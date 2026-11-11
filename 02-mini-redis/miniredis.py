import socket
import threading
import time
import sys

class MiniRedisServer:
    def __init__(self, host="127.0.0.1", port=6380):
        self.host = host
        self.port = port
        self.store = {}          # key -> value
        self.expires = {}        # key -> expire_timestamp
        self.lock = threading.Lock()
        self.running = False
        self.server_sock = None

    def _purge_expired(self):
        while self.running:
            time.sleep(0.5)
            now = time.time()
            with self.lock:
                expired_keys = [k for k, exp in self.expires.items() if now >= exp]
                for k in expired_keys:
                    self.store.pop(k, None)
                    self.expires.pop(k, None)

    def _is_expired(self, key):
        if key in self.expires:
            if time.time() >= self.expires[key]:
                self.store.pop(key, None)
                self.expires.pop(key, None)
                return True
        return False

    def handle_command(self, cmd_line: str) -> str:
        parts = cmd_line.strip().split()
        if not parts:
            return "-ERR empty command\r\n"

        cmd = parts[0].upper()
        args = parts[1:]

        with self.lock:
            if cmd == "PING":
                msg = args[0] if args else "PONG"
                return f"+{msg}\r\n"

            elif cmd == "SET":
                if len(args) < 2:
                    return "-ERR wrong number of arguments for 'set'\r\n"
                key, val = args[0], args[1]
                ttl = None
                if len(args) >= 4 and args[2].upper() == "EX":
                    try:
                        ttl = float(args[3])
                    except ValueError:
                        return "-ERR value is not an integer or out of range\r\n"

                self.store[key] = val
                if ttl:
                    self.expires[key] = time.time() + ttl
                else:
                    self.expires.pop(key, None)
                return "+OK\r\n"

            elif cmd == "GET":
                if len(args) != 1:
                    return "-ERR wrong number of arguments for 'get'\r\n"
                key = args[0]
                if self._is_expired(key) or key not in self.store:
                    return "$-1\r\n"
                val = str(self.store[key])
                return f"${len(val)}\r\n{val}\r\n"

            elif cmd == "DEL":
                if not args:
                    return "-ERR wrong number of arguments for 'del'\r\n"
                deleted = 0
                for k in args:
                    if k in self.store and not self._is_expired(k):
                        self.store.pop(k, None)
                        self.expires.pop(k, None)
                        deleted += 1
                return f":{deleted}\r\n"

            elif cmd == "EXISTS":
                if len(args) != 1:
                    return "-ERR wrong number of arguments for 'exists'\r\n"
                key = args[0]
                exists = 1 if (key in self.store and not self._is_expired(key)) else 0
                return f":{exists}\r\n"

            elif cmd == "INCR":
                if len(args) != 1:
                    return "-ERR wrong number of arguments for 'incr'\r\n"
                key = args[0]
                if self._is_expired(key) or key not in self.store:
                    val = 0
                else:
                    try:
                        val = int(self.store[key])
                    except ValueError:
                        return "-ERR value is not an integer or out of range\r\n"
                val += 1
                self.store[key] = str(val)
                return f":{val}\r\n"

            elif cmd == "KEYS":
                pattern = args[0] if args else "*"
                active_keys = [k for k in self.store if not self._is_expired(k)]
                if pattern == "*":
                    matched = active_keys
                else:
                    matched = [k for k in active_keys if pattern in k]
                resp = f"*{len(matched)}\r\n"
                for k in matched:
                    resp += f"${len(k)}\r\n{k}\r\n"
                return resp

            elif cmd == "INFO":
                active_keys = len([k for k in self.store if not self._is_expired(k)])
                info_text = f"# MiniRedis\r\nversion:1.0.0\r\ntotal_keys:{active_keys}\r\nuptime_sec:ok"
                return f"${len(info_text)}\r\n{info_text}\r\n"

            else:
                return f"-ERR unknown command '{cmd}'\r\n"

    def _client_handler(self, client_sock):
        with client_sock:
            buffer = ""
            while self.running:
                try:
                    data = client_sock.recv(1024)
                    if not data:
                        break
                    buffer += data.decode("utf-8", errors="ignore")
                    while "\r\n" in buffer or "\n" in buffer:
                        delim = "\r\n" if "\r\n" in buffer else "\n"
                        line, buffer = buffer.split(delim, 1)
                        if line.strip():
                            response = self.handle_command(line)
                            client_sock.sendall(response.encode("utf-8"))
                except Exception:
                    break

    def start(self, block=True):
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock.bind((self.host, self.port))
        self.server_sock.listen(10)
        self.running = True

        cleaner = threading.Thread(target=self._purge_expired, daemon=True)
        cleaner.start()

        print(f"[MiniRedis] Server started on tcp://{self.host}:{self.port}")

        def accept_loop():
            while self.running:
                try:
                    sock, _ = self.server_sock.accept()
                    t = threading.Thread(target=self._client_handler, args=(sock,), daemon=True)
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
        if self.server_sock:
            try:
                self.server_sock.close()
            except Exception:
                pass

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 6380
    server = MiniRedisServer(port=port)
    try:
        server.start(block=True)
    except KeyboardInterrupt:
        print("\nShutting down MiniRedis...")
        server.stop()
