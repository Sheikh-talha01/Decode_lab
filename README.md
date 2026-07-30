
Generative AI: Automated Copywriting & Tone Transformer

Overview
-
This repository implements a Python CLI that compiles a master instruction template, calls an LLM to generate marketing copy, and applies platform-specific filters and profanity sanitization. It supports single-item runs and CSV bulk processing.

Quickstart

1. Create a virtual environment and install dependencies:

```bash
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
```

2. Set your OpenAI API key (do NOT commit your key):

Windows cmd:

```bash
setx OPENAI_API_KEY "your_api_key_here"
```

3. Single-item example:

```bash
python run.py --product Shoe --name "Acme Runner" --tone witty --platform linkedin
```

4. Bulk CSV example (writes `outputs.jsonl` by default):

```bash
python run.py --csv examples/sample.csv --csv-out outputs.jsonl
```

Outputs
-
- Single-run prints a structured JSON `TextOutput` object with fields like `generated`, `processed`, `truncated`, and `unsafe`.
- Bulk runs write one JSON object per line to the specified output file. Each record contains the original CSV fields plus `generated`, `processed`, `truncated`, `filter_reason`, and `unsafe`.

Notes & Safety
-
- The project includes a small built-in profanity sanitizer (`src/decode_lab/validation.py`) for demonstration. Replace or extend it with a production-grade filter if needed.
- Keep your API keys out of source control. The CLI checks `OPENAI_API_KEY` from the environment.

Docker
-
Build and run the CLI in Docker (example):

```bash
docker build -t decode_lab:latest .
docker run --rm -e OPENAI_API_KEY="$OPENAI_API_KEY" decode_lab:latest --product Shoe --name "Acme Runner" --tone witty --platform linkedin
```

Development & Tests
-
Run the test suite:

```bash
python -m pytest -q
```

Files of interest
- `src/decode_lab/cli.py` — CLI entry and orchestration
- `src/decode_lab/template.py` — master template compiler
- `src/decode_lab/llm.py` — OpenAI adapter
- `src/decode_lab/pipeline.py` — async pipeline with concurrency
- `src/decode_lab/bulk.py` — CSV bulk runner
- `src/decode_lab/validation.py` — platform limits and profanity sanitizer
- `src/decode_lab/models.py` — Pydantic output schemas

"# Decode_lab_task_2 " 
