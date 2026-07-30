import argparse
import os
import asyncio

from .template import MasterTemplate
from .llm import OpenAIAdapter
from .models import OutputSchema


def build_parser():
    p = argparse.ArgumentParser(description="Automated Copywriting & Tone Transformer CLI")
    p.add_argument("--product", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--tone", required=True)
    p.add_argument("--platform", required=True, choices=["linkedin", "twitter", "instagram", "email"]) 
    p.add_argument("--temperature", type=float, default=0.7)
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

    async def run():
        raw = await adapter.generate(prompt, temperature=args.temperature)
        out = OutputSchema.parse_raw(raw)
        print("--- Generated Output ---")
        print(out.json(indent=2))

    asyncio.run(run())
