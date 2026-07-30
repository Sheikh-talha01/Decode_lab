# Project 1 — Custom AI Chatbot with Memory

This folder implements a minimal stateful chatbot demo with per-session memory stored in SQLite, a FastAPI HTTP API, and a small Streamlit UI. It is intentionally lightweight so you can run it locally without extra infra.

Quickstart

1. Copy `.env.example` and set `OPENAI_API_KEY` (optional; without a key the server runs in mock mode):

```powershell
copy .env.example .env
# edit .env and set OPENAI_API_KEY
```

2. Install dependencies and run the API:

```bash
python -m pip install -r requirements.txt
python run.py   # starts FastAPI on port 8001
```

3. Start the Streamlit UI (optional):

```bash
streamlit run ui_streamlit.py
```

Files of interest
- `src/project1/app.py` — FastAPI app with `/session`, `/chat`, `/health`.
- `src/project1/memory.py` — SQLite-backed memory store and rolling-window pruning.
- `src/project1/llm.py` — OpenAI adapter (mock when no key).
- `ui_streamlit.py` — minimal Streamlit front-end.
# Project 1 (placeholder)

This folder is reserved for the next project (`project1`). Add your new project files here.

Instructions:
- Create a top-level README describing the project in `project1/README.md`.
- Add source files under `project1/src/` and tests under `project1/tests/`.
