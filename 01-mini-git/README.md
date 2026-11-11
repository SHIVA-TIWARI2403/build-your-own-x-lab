# 📦 01 - Mini-Git

A functional, content-addressed version control engine built from scratch in Python, implementing Git's core internal object storage model.

---

## 💡 How Git Works Internally

Git is essentially a directed acyclic graph (DAG) of cryptographically hashed objects stored inside `.minigit/objects/`:
1. **Blob:** Stores raw file data without file names or permissions.
2. **Tree:** Represents directories. Maps file names and permissions (`mode`) to SHA-1 hashes of blobs or sub-trees.
3. **Commit:** A snapshot containing a tree hash, parent commit hash, author info, timestamp, and commit message.

```
Commit Object -> Points to Tree Object -> Points to Blob (File Data)
      |
   (parent)
      v
Previous Commit Object -> Points to Tree Object
```

---

## 🛠️ Commands Supported

* `python minigit.py init` — Initializes `.minigit/` directory structure.
* `python minigit.py hash-object <file>` — Computes SHA-1 hash and writes compressed object.
* `python minigit.py write-tree` — Recursively walks directory tree and computes tree hashes.
* `python minigit.py commit -m "<message>"` — Records a permanent immutable commit snapshot.
* `python minigit.py log` — Displays the full history log along with commit hashes and authors.

---

## 🧪 Testing

```bash
python test_minigit.py
```
