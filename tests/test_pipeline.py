import asyncio

from src.decode_lab.pipeline import AsyncPipeline


class DummyAdapter:
    def __init__(self, response):
        self.response = response

    async def generate(self, prompt: str, temperature: float = 0.7):
        return self.response


def test_pipeline_basic():
    adapter = DummyAdapter('{"generated": "hello"}')
    pipeline = AsyncPipeline(adapter=adapter, max_concurrency=2)

    res = asyncio.get_event_loop().run_until_complete(pipeline.generate("prompt"))
    assert 'generated' in res
