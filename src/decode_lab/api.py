from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from .template import MasterTemplate
from .llm import OpenAIAdapter
from .pipeline import AsyncPipeline
from .models import TextOutput
from .validation import apply_platform_filters, check_and_sanitize_profanity

app = FastAPI(title="DecodeLab Copy Generator")


class GenerateRequest(BaseModel):
    product: str
    name: str
    tone: str
    platform: str
    temperature: Optional[float] = 0.7


@app.post("/generate", response_model=TextOutput)
async def generate(req: GenerateRequest):
    api_key = None
    try:
        adapter = OpenAIAdapter(api_key=api_key)
    except RuntimeError:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not configured on server")

    pipeline = AsyncPipeline(adapter=adapter, max_concurrency=3)
    master = MasterTemplate()
    prompt = master.compile(req.dict())
    raw = await pipeline.generate(prompt, temperature=req.temperature)

    # parse raw JSON
    import json

    try:
        data = json.loads(raw)
    except Exception:
        data = {"generated": str(raw)}

    processed, truncated, reason = apply_platform_filters(req.platform, data.get("generated", ""))
    sanitized, unsafe = check_and_sanitize_profanity(processed)

    out = TextOutput(
        id=None,
        product=req.product,
        name=req.name,
        tone=req.tone,
        platform=req.platform,
        generated=data.get("generated", ""),
        processed=sanitized,
        truncated=truncated,
        filter_reason=reason,
        unsafe=unsafe,
    )
    return out


@app.get("/health")
async def health():
    return {"status": "ok"}
