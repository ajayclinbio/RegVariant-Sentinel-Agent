
import re
from transformers import pipeline

_ban = re.compile(r"(splice|splicing|branchpoint|spliceosome)", re.I)

def build_classifier(model_name="facebook/bart-large-mnli"):
    return pipeline("zero-shot-classification", model=model_name)

def classify_record(rec, zshot, threshold=0.70):
    text = (rec.get("title","") + " " + rec.get("abstract",""))
    if _ban.search(text):
        rec["keep"] = False
        rec["cls"] = {"label":"exclude_splicing","score":1.0}
        return rec
    labels = ["causal noncoding variant study", "association only", "not relevant"]
    out = zshot(text, labels, hypothesis_template="This paper presents a {}.", multi_label=False)
    best_label, best_score = out["labels"][0], float(out["scores"][0])
    rec["cls"] = {"label": best_label, "score": best_score}
    rec["keep"] = (best_label == "causal noncoding variant study" and best_score >= threshold)
    return rec
