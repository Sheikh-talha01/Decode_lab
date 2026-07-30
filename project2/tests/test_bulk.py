import os
import json
import asyncio
from pathlib import Path

from src.decode_lab.bulk import run_bulk


class DummyPipeline:
    def __init__(self, response_template='{"generated": "ok"}'):
        self.response_template = response_template

    async def generate(self, prompt: str):
        # return the same JSON string for all prompts
        await asyncio.sleep(0)
        return self.response_template


def test_run_bulk(tmp_path: Path):
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text("id,product,name,tone,platform\n1,Shoe,Acme,witty,linkedin\n2,Bag,Pro,professional,linkedin\n")

    out_path = tmp_path / "out.jsonl"
    pipeline = DummyPipeline()

    asyncio.get_event_loop().run_until_complete(run_bulk(str(csv_path), pipeline, template=type('T', (), { 'compile': staticmethod(lambda v: 'prompt')})(), out_path=str(out_path)))

    assert out_path.exists()
    lines = out_path.read_text(encoding='utf8').strip().splitlines()
    assert len(lines) == 2
    obj = json.loads(lines[0])
    assert 'generated' in obj
