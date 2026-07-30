import argparse
import os
import asyncio

from .template import MasterTemplate
from .llm import OpenAIAdapter
from .pipeline import AsyncPipeline
from .models import OutputSchema


def build_parser():
    p = argparse.ArgumentParser(description="Automated Copywriting & Tone Transformer CLI")
    p.add_argument("--product", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--tone", required=True)
    p.add_argument("--platform", required=True, choices=["linkedin", "twitter", "instagram", "email"]) 
    p.add_argument("--temperature", type=float, default=0.7)
    p.add_argument("--csv", type=str, help="Path to CSV file for bulk processing")
    p.add_argument("--csv-out", type=str, default="outputs.jsonl", help="Path to write bulk JSONL outputs")
    return p


def format_input(args):
    return {
        "product": args.product,
        "name": args.name,
        "tone": args.tone,
        "platform": args.platform,
    }


def main():
    parser = build_parser()
    args = parser.parse_args()

    master = MasterTemplate()
    prompt = master.compile(format_input(args))

    api_key = os.getenv("OPENAI_API_KEY")
    adapter = OpenAIAdapter(api_key=api_key)
    pipeline = AsyncPipeline(adapter=adapter, max_concurrency=5)

    # Bulk CSV mode
    if args.csv:
        from .bulk import run_bulk

        async def run_bulk_wrapper():
            await run_bulk(csv_path=args.csv, pipeline=pipeline, template=master, out_path=args.csv_out)

        asyncio.run(run_bulk_wrapper())
        return

    # Single-run mode
    async def run():
        raw = await pipeline.generate(prompt, temperature=args.temperature)
        out = OutputSchema.parse_raw(raw)
        # apply platform filters
        from .validation import apply_platform_filters

        processed, truncated, reason = apply_platform_filters(args.platform, out.generated)
        # profanity sanitize
        from .validation import check_and_sanitize_profanity

        sanitized, unsafe = check_and_sanitize_profanity(processed)

        out.platform = args.platform
        out.processed = sanitized
        out.truncated = truncated

        # wrap into strict output model
        from .models import TextOutput

        text_out = TextOutput(
            product=args.product,
            name=args.name,
            tone=args.tone,
            platform=args.platform,
            generated=out.generated,
            processed=sanitized,
            truncated=truncated,
            filter_reason=reason,
            unsafe=unsafe,
        )

        print("--- Generated Output ---")
        print(text_out.json(indent=2))
        return

    asyncio.run(run())
