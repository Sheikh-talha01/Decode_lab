Generative AI: Automated Copywriting & Tone Transformer

Overview
-
This repository implements a Python CLI that compiles a master instruction template, calls an LLM to generate marketing copy, and applies platform-specific filters and profanity sanitization. It supports single-item runs and CSV bulk processing.

Quickstart

1. Create a virtual environment and install dependencies:

```bash
python -m venv env
source env/bin/activate  # or env\Scripts\activate on Windows
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

Docker Compose
-
Use `docker-compose.yml` to build and run the FastAPI demo locally (exposes port 8000):

```powershell
copy .env.example .env
# then edit .env and set OPENAI_API_KEY
```

Start the service:

```bash
docker compose up --build
```

The FastAPI demo will be reachable at http://localhost:8000/ and the OpenAPI docs at http://localhost:8000/docs
