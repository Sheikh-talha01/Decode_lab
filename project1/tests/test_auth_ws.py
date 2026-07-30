import os
from project1.auth import require_token
from project1.llm import OpenAIAdapter


def test_require_token_behavior():
    # no token configured -> allow all
    if 'PROJECT1_API_TOKEN' in os.environ:
        del os.environ['PROJECT1_API_TOKEN']
    assert require_token(None) is True

    # set token and test
    os.environ['PROJECT1_API_TOKEN'] = 'x123'
    assert require_token('Bearer x123') is True
    assert require_token('bearer x123') is True
    assert require_token('Bearer wrong') is False
    assert require_token(None) is False
    del os.environ['PROJECT1_API_TOKEN']


def test_mock_llm_adapter():
    adapter = OpenAIAdapter(api_key=None)
    raw = adapter.generate('test prompt')
    # adapter returns a coroutine normally; ensure str/raw is available
    import asyncio
    res = asyncio.get_event_loop().run_until_complete(raw)
    assert '{"generated"' in res
