import os
import time
import asyncio
from fastapi.testclient import TestClient
from project1.app import create_app


def test_ws_echo_mock_generation():
    # ensure no token required for test by clearing env
    if 'PROJECT1_API_TOKEN' in os.environ:
        del os.environ['PROJECT1_API_TOKEN']

    app = create_app()
    client = TestClient(app)

    with client.websocket_connect('/ws') as ws:
        ws.send_text('Hello websocket')
        data = ws.receive_text()
        assert data is not None
        assert 'mock' in data or 'generated' in data
