# Project1 — Custom AI Chatbot with Memory

Minimal stateful chatbot with per-session memory (SQLite), an HTTP API (FastAPI), and an optional Streamlit UI.

Quick start (use a virtual environment):

1. Create and activate a venv (Windows):

	python -m venv .venv
	.\.venv\Scripts\activate

2. Install core server deps:

	pip install -r requirements.txt

3a. Run the automated demo (no network, mock LLM):

	py -3 project1/manual_test.py

3b. Run the FastAPI server (in the venv):

	.\.venv\Scripts\python.exe project1/start_server.py

4. (Optional) Install the UI deps and run Streamlit UI:

	pip install -r requirements-ui.txt
	streamlit run project1/ui_streamlit.py

Notes
- `manual_test.py` runs a complete memory + mock LLM demo without starting the HTTP server — useful if installing heavy UI deps (numpy/Streamlit) is problematic on Windows.
- `requirements.txt` contains only runtime server deps; `requirements-ui.txt` contains the optional Streamlit UI deps.
- Docker: `project1/Dockerfile` and `project1/docker-compose.yml` are provided for containerized runs (requires Docker daemon).

Files of interest
- `project1/src/project1/app.py` — FastAPI app with `/session`, `/chat`, `/health`.
- `project1/src/project1/memory.py` — SQLite-backed memory store and pruning.
- `project1/src/project1/llm.py` — OpenAI adapter (mockable when `OPENAI_API_KEY` is not set).
- `project1/ui_streamlit.py` — optional Streamlit UI.

If you want, I can start the server in a container and run the demo there, or open the PR for final review and merge.
