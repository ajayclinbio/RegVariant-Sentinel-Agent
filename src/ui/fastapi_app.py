
import os, json
from fastapi import FastAPI
from typing import Optional

app = FastAPI(title="RegulatoryVariant Sentinel (Demo)")
DATA_PATH = os.getenv("DATA_PATH", "outputs/results.jsonl")

def load_records():
    recs = []
    if not os.path.exists(DATA_PATH):
        return recs
    with open(DATA_PATH, "r") as f:
        for line in f:
            recs.append(json.loads(line))
    return recs

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/search")
def search(gene: Optional[str] = None, min_score: int = 4, limit: int = 25):
    recs = load_records()
    res = []
    for r in recs:
        if not r.get("above_threshold"):
            continue
        if gene and gene not in r.get("extracted",{}).get("genes",[]):
            continue
        if r.get("evidence_score",0) < min_score:
            continue
        res.append({
            "pmid": r["pmid"],
            "title": r["title"],
            "evidence_score": r["evidence_score"],
            "label": r.get("cls",{}).get("label"),
            "score": r.get("cls",{}).get("score"),
            "extracted": r.get("extracted",{})
        })
    return res[:limit]
