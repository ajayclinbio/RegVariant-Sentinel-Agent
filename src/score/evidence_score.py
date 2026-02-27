
import re

def evidence_from_text(text: str):
    feats = set()
    if re.search(r"luciferase|reporter assay|MPRA", text, re.I): feats.add("functional")
    if re.search(r"EMSA|allele-specific binding|ChIP", text, re.I): feats.add("tf_binding")
    if re.search(r"CRISPRi|CRISPRa|CRISPR knockout|deletion", text, re.I): feats.add("enhancer_gene_link")
    if re.search(r"segregation|LOD|de novo", text, re.I): feats.add("segregation_or_de_novo")
    if re.search(r"ClinVar|pathogenic|likely pathogenic", text, re.I): feats.add("clinvar_assertion")
    if re.search(r"replicate|independent cohort", text, re.I): feats.add("replication")
    return feats

def score_record(rec, min_threshold=4):
    text = (rec.get("title","") + " " + rec.get("abstract",""))
    feats = evidence_from_text(text)
    score = 0
    score += 2 if "functional" in feats else 0
    score += 1 if "tf_binding" in feats else 0
    score += 2 if "enhancer_gene_link" in feats else 0
    score += 2 if "segregation_or_de_novo" in feats else 0
    score += 1 if "clinvar_assertion" in feats else 0
    score += 1 if "replication" in feats else 0
    if rec.get("cls",{}).get("label") == "association only":
        score -= 2
    rec["evidence"] = list(feats)
    rec["evidence_score"] = score
    rec["above_threshold"] = (rec.get("keep") and score >= min_threshold)
    return rec
