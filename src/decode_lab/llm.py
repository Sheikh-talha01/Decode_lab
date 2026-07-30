import os
import json
from typing import Optional

import httpx


class OpenAIAdapter:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY not set")
        self.model = "gpt-4o-mini"

    async def generate(self, prompt: str, temperature: float = 0.7) -> str:
        """Call OpenAI's completion endpoint (mock compatibility).

        Returns the raw JSON string of the response choices[0].text or content field.
        """
        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": 200,
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.post(url, headers=headers, json=payload)
            # raise for non-2xx
            r.raise_for_status()
            data = r.json()

        # try to extract text -- support chat/completions and legacy
        # Prefer Chat-style message content
        if isinstance(data, dict) and "choices" in data and len(data["choices"]) > 0:
            choice = data["choices"][0]
            # chat completion
            if isinstance(choice, dict) and "message" in choice and isinstance(choice["message"], dict) and "content" in choice["message"]:
                text = choice["message"]["content"]
            # legacy completion
            elif "text" in choice:
                text = choice["text"]
            else:
                text = json.dumps(data)
        else:
            text = json.dumps(data)

        return json.dumps({"generated": text})
