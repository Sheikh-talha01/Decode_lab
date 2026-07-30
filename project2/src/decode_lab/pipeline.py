import asyncio
import random
import time
import httpx


class AsyncPipeline:
    def __init__(self, adapter, max_concurrency: int = 5, max_retries: int = 4):
        self.adapter = adapter
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.max_retries = max_retries

    async def _call_with_retries(self, prompt: str, temperature: float = 0.7) -> str:
        attempt = 0
        while True:
            try:
                return await self.adapter.generate(prompt, temperature=temperature)
            except (httpx.HTTPError, TimeoutError) as exc:
                attempt += 1
                if attempt >= self.max_retries:
                    raise
                # exponential backoff with jitter
                delay = min(2 ** attempt, 10) * (0.5 + random.random() * 0.5)
                await asyncio.sleep(delay)

    async def generate(self, prompt: str, temperature: float = 0.7) -> str:
        async with self.semaphore:
            return await self._call_with_retries(prompt, temperature=temperature)
