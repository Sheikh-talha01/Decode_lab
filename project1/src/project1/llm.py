import os
import json
import asyncio
from typing import Optional

import httpx


class OpenAIAdapter:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

    async def generate(self, prompt: str, temperature: float = 0.7) -> str:
        # If no API key, mock response
        if not self.api_key:
            await asyncio.sleep(0)
            return json.dumps({"generated": "(mock) " + prompt[:140]})

        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {"model": "gpt-4o-mini", "messages": [{"role": "user", "content": prompt}], "temperature": temperature}

        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.post(url, headers=headers, json=payload)
            r.raise_for_status()
            data = r.json()

        if isinstance(data, dict) and "choices" in data and data["choices"]:
            choice = data["choices"][0]
            if isinstance(choice, dict) and "message" in choice and "content" in choice["message"]:
                text = choice["message"]["content"]
            elif "text" in choice:
                text = choice["text"]
            else:
                text = json.dumps(data)
        else:
            text = json.dumps(data)

        return json.dumps({"generated": text})
