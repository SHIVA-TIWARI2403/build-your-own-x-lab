import os
import sys
import zlib
import hashlib
import time

MINIGIT_DIR = ".minigit"

def get_repo_root():
    current = os.getcwd()
    while current:
        if os.path.exists(os.path.join(current, MINIGIT_DIR)):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent
    return None

def init():
    if os.path.exists(MINIGIT_DIR):
        print(f"Repository already initialized in {os.path.abspath(MINIGIT_DIR)}")
        return
    os.makedirs(os.path.join(MINIGIT_DIR, "objects"), exist_ok=True)
    os.makedirs(os.path.join(MINIGIT_DIR, "refs", "heads"), exist_ok=True)
    with open(os.path.join(MINIGIT_DIR, "HEAD"), "w", encoding="utf-8") as f:
        f.write("ref: refs/heads/main\n")
    print(f"Initialized empty MiniGit repository in {os.path.abspath(MINIGIT_DIR)}")

def hash_object(data: bytes, obj_type: str = "blob", write: bool = True) -> str:
    header = f"{obj_type} {len(data)}\0".encode("utf-8")
    full_content = header + data
    obj_hash = hashlib.sha1(full_content).hexdigest()

    if write:
        root = get_repo_root() or os.getcwd()
        obj_dir = os.path.join(root, MINIGIT_DIR, "objects", obj_hash[:2])
        obj_file = os.path.join(obj_dir, obj_hash[2:])
        os.makedirs(obj_dir, exist_ok=True)
        if not os.path.exists(obj_file):
            with open(obj_file, "wb") as f:
                f.write(zlib.compress(full_content))
    return obj_hash

def cat_file(obj_hash: str):
    root = get_repo_root()
    if not root:
        print("Fatal: not a minigit repository")
        return None, None
    obj_path = os.path.join(root, MINIGIT_DIR, "objects", obj_hash[:2], obj_hash[2:])
    if not os.path.exists(obj_path):
        raise FileNotFoundError(f"Object {obj_hash} not found")
    with open(obj_path, "rb") as f:
        decompressed = zlib.decompress(f.read())
    null_idx = decompressed.index(b"\0")
    header = decompressed[:null_idx].decode("utf-8")
    obj_type, _ = header.split(" ")
    content = decompressed[null_idx + 1:]
    return obj_type, content

def write_tree(dir_path: str = ".") -> str:
    root = get_repo_root() or os.getcwd()
    entries = []
    
    for item in sorted(os.listdir(dir_path)):
        if item in [MINIGIT_DIR, ".git", "__pycache__"]:
            continue
        full_path = os.path.join(dir_path, item)
        if os.path.isfile(full_path):
            with open(full_path, "rb") as f:
                content = f.read()
            blob_hash = hash_object(content, "blob", write=True)
            mode = "100644"
            entries.append((mode, item, bytes.fromhex(blob_hash)))
        elif os.path.isdir(full_path):
            sub_tree_hash = write_tree(full_path)
            mode = "040000"
            entries.append((mode, item, bytes.fromhex(sub_tree_hash)))

    tree_content = b"".join(f"{mode} {name}\0".encode("utf-8") + sha for mode, name, sha in entries)
    return hash_object(tree_content, "tree", write=True)

def get_current_head_ref():
    root = get_repo_root()
    head_path = os.path.join(root, MINIGIT_DIR, "HEAD")
    with open(head_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
    if content.startswith("ref: "):
        ref_rel = content.split("ref: ")[1]
        return os.path.join(root, MINIGIT_DIR, ref_rel)
    return None

def get_parent_commit():
    ref_path = get_current_head_ref()
    if ref_path and os.path.exists(ref_path):
        with open(ref_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None

def commit(message: str, author: str = "Shiva Tiwari <shiva@example.com>") -> str:
    root = get_repo_root()
    if not root:
        print("Fatal: not a minigit repository")
        return ""

    tree_hash = write_tree(root)
    parent_commit = get_parent_commit()
    timestamp = int(time.time())

    lines = [f"tree {tree_hash}"]
    if parent_commit:
        lines.append(f"parent {parent_commit}")
    lines.append(f"author {author} {timestamp} +0000")
    lines.append(f"committer {author} {timestamp} +0000")
    lines.append("")
    lines.append(message)
    lines.append("")

    commit_payload = "\n".join(lines).encode("utf-8")
    commit_hash = hash_object(commit_payload, "commit", write=True)

    ref_path = get_current_head_ref()
    os.makedirs(os.path.dirname(ref_path), exist_ok=True)
    with open(ref_path, "w", encoding="utf-8") as f:
        f.write(commit_hash + "\n")

    print(f"[{commit_hash[:7]}] {message}")
    return commit_hash

def log():
    commit_hash = get_parent_commit()
    if not commit_hash:
        print("No commits yet.")
        return

    while commit_hash:
        _, content = cat_file(commit_hash)
        lines = content.decode("utf-8").split("\n")
        parent = None
        author = ""
        msg_lines = []
        is_msg = False

        for line in lines:
            if is_msg:
                msg_lines.append(line)
            elif line.startswith("parent "):
                parent = line.split(" ")[1]
            elif line.startswith("author "):
                author = line[7:]
            elif line == "":
                is_msg = True

        print(f"\033[33mcommit {commit_hash}\033[0m")
        print(f"Author: {author}")
        print(f"\n    {(' '.join(msg_lines)).strip()}\n")
        commit_hash = parent

def main():
    if len(sys.argv) < 2:
        print("Usage: minigit [init | hash-object <file> | write-tree | commit -m <msg> | log]")
        return

    cmd = sys.argv[1]
    if cmd == "init":
        init()
    elif cmd == "hash-object" and len(sys.argv) > 2:
        with open(sys.argv[2], "rb") as f:
            h = hash_object(f.read(), write=True)
        print(h)
    elif cmd == "write-tree":
        t = write_tree(".")
        print(t)
    elif cmd == "commit":
        if "-m" in sys.argv:
            idx = sys.argv.index("-m")
            if idx + 1 < len(sys.argv):
                commit(sys.argv[idx + 1])
            else:
                print("Error: commit message required")
        else:
            print("Error: use -m <message>")
    elif cmd == "log":
        log()
    else:
        print(f"Unknown command: {cmd}")

if __name__ == "__main__":
    main()
