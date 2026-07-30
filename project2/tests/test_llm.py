import asyncio
import json

import httpx

from src.decode_lab.llm import OpenAIAdapter


class DummyResponse:
    def __init__(self, data):
        self._data = data

    def raise_for_status(self):
        return None

    def json(self):
        return self._data


class DummyAsyncClient:
    def __init__(self, data):
        self._data = data

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def post(self, url, headers=None, json=None):
        return DummyResponse(self._data)


def test_parse_chat_style(monkeypatch):
    data = {"choices": [{"message": {"content": "Hello chat"}}]}
    monkeypatch.setattr(httpx, "AsyncClient", lambda timeout=30.0: DummyAsyncClient(data))
    adapter = OpenAIAdapter(api_key="sk-test")
    out = asyncio.get_event_loop().run_until_complete(adapter.generate("prompt"))
    obj = json.loads(out)
    assert obj["generated"] == "Hello chat"


def test_parse_legacy_style(monkeypatch):
    data = {"choices": [{"text": "Hello legacy"}]}
    monkeypatch.setattr(httpx, "AsyncClient", lambda timeout=30.0: DummyAsyncClient(data))
    adapter = OpenAIAdapter(api_key="sk-test")
    out = asyncio.get_event_loop().run_until_complete(adapter.generate("prompt"))
    obj = json.loads(out)
    assert obj["generated"] == "Hello legacy"
