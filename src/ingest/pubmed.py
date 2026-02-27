
import time, requests
from lxml import etree

QUERY = r"""(
  (noncoding[tiab] OR non-coding[tiab] OR regulatory[tiab] OR promoter[tiab] OR enhancer[tiab]
   OR "cis-regulatory"[tiab] OR UTR[tiab] OR "5' UTR"[tiab] OR "3' UTR"[tiab]
   OR "polyA signal"[tiab] OR "polyadenylation signal"[tiab] OR TFBS[tiab])
  AND
  (variant[tiab] OR mutation[tiab] OR SNV[tiab] OR indel[tiab])
  AND
  (pathogenic[tiab] OR "disease-causing"[tiab] OR causal[tiab] OR mechanism[tiab])
)
NOT (splice[tiab] OR splicing[tiab] OR "cryptic splice"[tiab] OR branchpoint[tiab]) AND Humans[mesh]
"""

def esearch_ids(days_back=30, retmax=200):
    term = f"({QUERY}) AND ({days_back}[DP])"
    params = {"db":"pubmed","retmode":"json","retmax":str(retmax),"term":term}
    r = requests.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi", params=params, timeout=60)
    r.raise_for_status()
    return r.json()["esearchresult"]["idlist"]

def efetch_xml(id_batch):
    EFETCH = {"db":"pubmed","retmode":"xml","id":",".join(id_batch)}
    r = requests.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi", params=EFETCH, timeout=120)
    r.raise_for_status()
    return r.text

def parse_pubmed_xml(xml_text):
    root = etree.fromstring(xml_text.encode())
    out = []
    for art in root.findall(".//PubmedArticle"):
        pmid = art.findtext(".//PMID") or ""
        title = art.findtext(".//ArticleTitle") or ""
        abstract = " ".join([t.text for t in art.findall(".//Abstract/AbstractText") if t is not None and t.text]) or ""
        year = art.findtext(".//PubDate/Year") or ""
        journal = art.findtext(".//Journal/Title") or ""
        out.append({"pmid": pmid, "title": title, "abstract": abstract, "year": year, "journal": journal})
    return out

def harvest(days_back=30, retmax=200):
    ids = esearch_ids(days_back=days_back, retmax=retmax)
    records = []
    for i in range(0, len(ids), 200):
        xml = efetch_xml(ids[i:i+200])
        records.extend(parse_pubmed_xml(xml))
        time.sleep(0.34)
    return records
