PY=python
PIP=pip

.PHONY: install test run docker-build compose-up

install:
	$(PIP) install -r requirements.txt

test:
	$(PY) -m pytest -q

run:
	$(PY) run.py

docker-build:
	docker build -t decode_lab:latest .

compose-up:
	docker compose up --build
