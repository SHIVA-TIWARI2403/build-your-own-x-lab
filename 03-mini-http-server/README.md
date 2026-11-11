# 🌐 03 - Mini-HTTP-Server

A raw TCP socket HTTP/1.1 server built entirely from scratch in Python with zero third-party dependencies.

---

## 🚀 Key Features

* **Pure TCP Sockets:** Uses Python's native `socket` library to handle network transport layer connections.
* **HTTP/1.1 Protocol Parser:** Parses request lines (Method, URI, Query Params, HTTP version), headers, and message bodies.
* **REST Routing Engine:** Built-in JSON endpoints (`/api/health`, `/api/echo`, `/api/info`).
* **Static File Server:** Serves HTML, CSS, JavaScript, and images from the `public/` directory with correct MIME types and path traversal guards.
* **Multi-threaded Workers:** Spawns concurrent connection handlers to serve multiple clients simultaneously.

---

## 🏃 Running the Server

```bash
# Starts server on default port 8080
python miniserver.py 8080
```

Open in any browser:
* `http://localhost:8080/` &rarr; Renders the static HTML page.
* `http://localhost:8080/api/health` &rarr; Returns JSON status payload.

---

## 🧪 Testing

```bash
python test_miniserver.py
```
