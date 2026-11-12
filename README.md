# Systems From Scratch Lab

A hands-on exploration of fundamental computer science concepts by implementing minimal, working versions of core systems from scratch in Python—using only the standard library.

---

## Implementations

| System | Directory | Core Concepts |
|---|---|---|
| **Mini-Git** | `01-mini-git/` | Content-addressed storage, SHA-1 hashing, blobs, trees, commit objects, refs, log traversal |
| **Mini-Redis** | `02-mini-redis/` | In-memory key-value store, TCP socket server, RESP protocol parser, TTL expiration |
| **Mini-HTTP-Server** | `03-mini-http-server/` | Raw socket HTTP/1.1 server, request parsing, routing, MIME types, static file serving |
| **Mini-Blockchain** | `04-mini-blockchain/` | Cryptographic ledger, SHA-256 proof-of-work mining, block verification, tampering check |
| **Mini-Neural-Net** | `05-mini-neural-net/` | 2-layer feedforward network, matrix operations, sigmoid activation, backpropagation |

---

## Running the Tests

Each system includes a standalone test script demonstrating functionality:

```bash
# Test Git implementation (init, hash-object, cat-file, write-tree, commit, log)
python 01-mini-git/test_minigit.py

# Test Redis implementation (SET, GET, DEL, EXISTS, EXPIRE, PING)
python 02-mini-redis/test_miniredis.py

# Test HTTP Server (GET routing, 404 handling, static files)
python 03-mini-http-server/test_miniserver.py

# Test Blockchain (Block mining, proof-of-work validation, chain tampering detection)
python 04-mini-blockchain/test_blockchain.py

# Test Neural Network (XOR problem learning and accuracy evaluation)
python 05-mini-neural-net/test_neural_net.py
```

---

## Design Goals

- **Zero External Dependencies:** Built entirely with Python standard library (`socket`, `hashlib`, `zlib`, `struct`, `math`).
- **Readable Implementations:** Prioritizes clean code structure over micro-optimizations to make the underlying protocol/algorithm clear.
