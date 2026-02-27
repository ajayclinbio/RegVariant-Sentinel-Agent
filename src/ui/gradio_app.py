
import os, json
import gradio as gr

DATA_PATH = os.getenv("DATA_PATH", "outputs/results.jsonl")

def _load():
    items = []
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            for line in f:
                items.append(json.loads(line))
    return items

def run_search(gene, min_score):
    recs = _load()
    rows = []
    for r in recs:
        if not r.get("above_threshold"):
            continue
        if gene and gene not in r.get("extracted",{}).get("genes",[]):
            continue
        if r.get("evidence_score",0) < int(min_score):
            continue
        rows.append([r["pmid"], r["title"], r["evidence_score"], r.get("cls",{}).get("label"), r.get("cls",{}).get("score")])
    return rows[:50]

def main():
    with gr.Blocks(title="Regulatory Variant Sentinel") as demo:
        gr.Markdown("# Noncoding Variant Causal Studies (Demo)")
        with gr.Row():
            gene = gr.Textbox(label="Filter by gene symbol (optional)", placeholder="e.g., TERT")
            min_score = gr.Slider(0, 10, value=4, step=1, label="Min evidence score")
        btn = gr.Button("Search")
        table = gr.Dataframe(headers=["PMID","Title","Evidence Score","Label","Cls Score"],
                             datatype=["number","str","number","str","number"], wrap=True)
        btn.click(run_search, inputs=[gene, min_score], outputs=table)
    demo.launch(server_name="0.0.0.0", share=False)

if __name__ == "__main__":
    main()
