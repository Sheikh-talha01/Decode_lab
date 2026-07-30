import pytest


fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient

from src.decode_lab.api import app


def test_health():
    client = TestClient(app)
    r = client.get('/health')
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
