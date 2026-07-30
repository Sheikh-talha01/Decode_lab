# Decode_lab

This repository contains two projects:

- `project1/` — Custom AI Chatbot with Memory
  - FastAPI server with per-session SQLite memory
  - Optional Streamlit UI (in `project1/ui_streamlit.py`)
  - Mock-capable OpenAI adapter for offline demos
  - Run quick demo: `py -3 project1/manual_test.py`

- `project2/` — Automated Copywriting & Tone Transformer
  - CLI-first generator, FastAPI endpoints, and bulk CSV runner
  - Async pipeline and robust OpenAI adapter

Quick actions

1. Run Project1 demo (no heavy deps):

    python -m venv .venv
    .\.venv\Scripts\activate
    pip install -r project1/requirements.txt
    py -3 project1/manual_test.py

2. Run Project2 tests:

    $env:PYTHONPATH="project2/src"; py -3 -m pytest project2/tests

Docker & CI

- CI workflow for `project1` is in `.github/workflows/project1-ci.yml`.
- Dockerfiles and `docker-compose.yml` exist in each project for containerized demos.

If you want, I can:
- Enable Docker image publishing in CI (requires DockerHub/GHCR secret),
- Add a GitHub Release and changelog entry, or
- Add auth and websockets to `project1`.
