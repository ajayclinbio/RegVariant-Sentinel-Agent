
import os, json

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def write_jsonl(path: str, records):
    with open(path, "w") as f:
        for r in records:
            f.write(json.dumps(r) + "
")

def read_jsonl(path: str):
    out = []
    with open(path, "r") as f:
        for line in f:
            out.append(json.loads(line))
    return out
