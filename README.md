# 🛠️ Systems From Scratch Lab

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white" alt="Python Version" />
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License" />
  <img src="https://img.shields.io/badge/Architecture-Zero%20Dependency-orange" alt="Architecture" />
  <img src="https://img.shields.io/badge/Coverage-100%25%20Verified-brightgreen" alt="Tests" />
</p>

An original, modular collection of foundational computer science systems built from the ground up in pure Python without external frameworks or third-party wrappers.

> *"What I cannot create, I do not understand."* — **Richard Feynman**

---

## 📌 Included Systems

| # | System | Core Architecture | Key Components |
|---|---|---|---|
| **01** | **[Mini-Git](./01-mini-git)** | Content-addressed storage DAG | SHA-1 hashing, zlib compression, blob/tree/commit objects, immutable commit logs |
| **02** | **[Mini-Redis](./02-mini-redis)** | In-memory key-value database | Raw TCP socket listener, RESP protocol, atomic `INCR`, background thread TTL cleaner |
| **03** | **[Mini-HTTP-Server](./03-mini-http-server)** | Raw socket HTTP/1.1 web server | Protocol parser (method/URI/headers/body), static file server with MIME detection, REST endpoints |
| **04** | **[Mini-Blockchain](./04-mini-blockchain)** | Proof-of-Work distributed ledger | SHA-256 block mining with difficulty targeting, reward transactions, tamper detection |
| **05** | **[Mini-Neural-Net](./05-mini-neural-net)** | Multi-layer perceptron (MLP) | Forward pass, sigmoid activation, backpropagation with calculus chain-rule gradient descent |

---

## 🚀 Quickstart & Testing

Run all unit verification test suites across all 5 engines:

```bash
# 01. Test Mini-Git
python 01-mini-git/test_minigit.py

# 02. Test Mini-Redis (In-Memory Store)
python 02-mini-redis/test_miniredis.py

# 03. Test Mini-HTTP-Server
python 03-mini-http-server/test_miniserver.py

# 04. Test Mini-Blockchain
python 04-mini-blockchain/test_blockchain.py

# 05. Test Mini-Neural-Net
python 05-mini-neural-net/test_neural_net.py
```

---

## 👤 Author

Architected & built by **Shiva Tiwari** ([@SHIVA-TIWARI2403](https://github.com/SHIVA-TIWARI2403)).
