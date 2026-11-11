# 🔗 04 - Mini-Blockchain

A cryptographic Proof-of-Work distributed ledger built from scratch in Python, implementing SHA-256 block hashing, difficulty targeting, and immutable tamper detection.

---

## 🚀 Key Features

* **Cryptographic Block Hashing:** Every block computes an immutable SHA-256 hash across its index, timestamp, transactions, nonce, and the previous block's hash.
* **Proof-of-Work (PoW) Mining:** Implements cryptographic difficulty targeting where a miner must compute nonces until the block hash begins with $N$ leading zeros.
* **Tamper Proof Ledger:** If any past transaction is modified by even 1 bit, every subsequent hash in the chain breaks, immediately failing validity verification.
* **Mining Incentives:** Automatically generates and credits network mining reward transactions upon block discovery.

---

## 🏃 Quick Usage

```bash
python blockchain.py
```

---

## 🧪 Testing

```bash
python test_blockchain.py
```
