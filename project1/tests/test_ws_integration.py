import os
import pytest


def test_ws_echo_mock_generation():
    try:
        from fastapi.testclient import TestClient
    except Exception:
        pytest.skip("fastapi/TestClient import failed in this environment")

    from project1.app import create_app

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
