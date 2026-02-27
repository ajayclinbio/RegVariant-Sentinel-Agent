
import os
from transformers import logging as hf_logging
from src.ingest.pubmed import harvest
from src.classify.zero_shot import build_classifier, classify_record
from src.extract.regex_extract import extract_entities
from src.score.evidence_score import score_record
from src.utils.io import ensure_dir, write_jsonl

OUT_DIR = os.getenv("OUT_DIR", "outputs")
ensure_dir(OUT_DIR)

def main():
    hf_logging.set_verbosity_error()
    records = harvest(days_back=30, retmax=200)
    zshot = build_classifier()
    for r in records:
        classify_record(r, zshot, threshold=0.70)
        text = (r.get("title","") + " " + r.get("abstract",""))
        r["extracted"] = extract_entities(text)
        score_record(r, min_threshold=4)
    write_jsonl(os.path.join(OUT_DIR, "results.jsonl"), records)
    print(f"Saved {len(records)} records → {os.path.join(OUT_DIR, 'results.jsonl')}")

if __name__ == "__main__":
    main()
