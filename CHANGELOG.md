# Changelog

All notable changes to this repository will be documented in this file.

## [v1.0.0] - 2026-07-31
- Added `project1`: stateful chatbot with SQLite memory, FastAPI API, Streamlit UI (optional), demo scripts, and tests.
- Added `project2`: automated copywriting & tone transformer (CLI, API, bulk runner).
- CI: project1 and project2 test workflows; optional Docker image publishing.
- Added top-level README and release tag `v1.0.0`.

## [v1.0.1] - 2026-07-31
- CI: enabled GHCR publishing on tag pushes; added DockerHub conditional publishing.
- Added WebSocket endpoint and token auth to `project1`, plus integration tests and demo client.
- Cleaned up gitignored local DB and improved README instructions.
