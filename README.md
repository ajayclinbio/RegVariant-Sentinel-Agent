!Open In Colab

# RegulatoryVariant-Sentinel-AI-Agent

AI based research agent whose purpose is to scan biomedical literature to look for reported variants in the regulatory, non‑coding regions of the genome which are pathogenic and causative

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
To run this project in google colab use following:

git clone https://github.com/ajayclinbio/RegVariant-Sentinel-Agent.git
%cd RegVariant-Sentinel-Agent
!pip install -r requirements.txt
python -m src.orchestrate.run_pipeline
