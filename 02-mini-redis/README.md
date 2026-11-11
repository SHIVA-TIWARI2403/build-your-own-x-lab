# ⚡ 02 - Mini-Redis

An in-memory key-value database engine implemented using raw TCP sockets in Python, supporting Redis-compatible RESP response formats, thread concurrency, and automated background TTL expiration.

---

## 🚀 Key Features

* **TCP Socket Listener:** Accepts multi-client network connections concurrently using threading.
* **Core Commands:**
  * `PING` &rarr; `+PONG`
  * `SET <key> <value> [EX seconds]` &rarr; Stores key-value with optional expiration.
  * `GET <key>` &rarr; Retrieves value or returns `$-1` if expired / not found.
  * `DEL <key...>` &rarr; Removes keys and returns deleted count.
  * `INCR <key>` &rarr; Atomically increments integer counter.
  * `EXISTS <key>` &rarr; Checks existence.
  * `KEYS [pattern]` &rarr; Lists matching keys.
  * `INFO` &rarr; Returns engine statistics.
* **Passive & Active Expiration:** Key expirations are checked both lazily on retrieval and actively via a background sweeper thread.

---

## 🏃 Running the Server

```bash
# Start server on default port 6380
python miniredis.py 6380
```

In another terminal or via telnet / netcat:
```bash
telnet 127.0.0.1 6380
SET hero "Shiva"
GET hero
INCR counter
```

---

## 🧪 Testing

```bash
python test_miniredis.py
```
