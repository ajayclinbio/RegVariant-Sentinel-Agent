
# RegulatoryVariant-Sentinel-AI-Agent

**An AI-driven research agent that scans biomedical literature for reported pathogenic variants in the regulatory, non‑coding regions of the genome.**

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m src.orchestrate.run_pipeline
```

Outputs will be written to `outputs/results.jsonl`.

## Config
See `configs/pipeline.yaml` to change search scope, thresholds, and scoring.

## Colab
Clone this repo in Google Colab and run the same commands; mount Drive to persist outputs.
