
import re
import spacy

HGVS = re.compile(r"(?:NM|NC|NG|NR|ENST)_[0-9]+\.[0-9]+:[cnmg]\.[0-9\-\+\*]+[A-Z]>[A-Z]")
RSID = re.compile(r"rs[0-9]{3,}", re.I)

_nlp = None

def _get_nlp():
    global _nlp
    if _nlp is None:
        _nlp = spacy.load("en_core_sci_sm")
    return _nlp

def extract_entities(text: str):
    ents = {
        "hgvs": sorted(set(HGVS.findall(text))),
        "rsids": sorted(set(RSID.findall(text))),
        "genes": []
    }
    nlp = _get_nlp()
    doc = nlp(text)
    toks = {t.text for t in doc if t.is_alpha and 2 <= len(t.text) <= 7 and t.text.isupper()}
    ents["genes"] = sorted(toks)
    return ents
