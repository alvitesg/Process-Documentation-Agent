# Process Documentation Agent

A lightweight AI-agent scaffold for assessing business/process documentation and generating:

1. **Audit narrative**
2. **Process flow chart (Mermaid)**
3. **Risk & Control Self-Assessment (RCSA)**

This repository now includes both a CLI and a browser-based GUI.

## What this project does

Given process artifacts (SOPs, policies, narratives, walkthrough notes), the agent will:

- Parse and segment source content.
- Extract structured process facts (actors, systems, steps, controls, risks, evidence).
- Generate:
  - `audit_narrative.md`
  - `process_flowchart.mmd`
  - `rcsa.md`

## Quick start (GUI)

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run process_doc_agent/gui.py
```

Run the command from the repository root, then open the URL shown by Streamlit (usually `http://localhost:8501`) and upload `.txt` files.

## Quick start (CLI)

```bash
python -m process_doc_agent.cli run --input ./sample_input --output ./artifacts
```

## Repository structure

```text
process_doc_agent/
  cli.py                 # Command-line entrypoint
  gui.py                 # Streamlit GUI for file uploads
  models.py              # Data structures for process, risks, and controls
  pipeline.py            # End-to-end orchestration
  prompts.py             # Prompt templates by output type
  renderers.py           # Markdown and Mermaid renderers
sample_input/
  process_notes.txt      # Example source artifact
```

## Implementation notes

- The default LLM client is intentionally mocked to keep this repo dependency-light.
- Replace `MockLLMClient` with your provider client (OpenAI, Azure OpenAI, etc.).
- Add retrieval over larger corpora as needed (vector DB, document store).

## Suggested production upgrades

- Add document OCR/ingestion for PDFs and images.
- Add taxonomy alignment for risks/controls.
- Add scoring rubric for control design and operating effectiveness.
- Add human-in-the-loop review checkpoints.
- Add evidence traceability map from each generated statement to source excerpts.
