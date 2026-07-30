import csv
import json
import asyncio
from typing import Any


async def run_bulk(csv_path: str, pipeline, template, out_path: str = "outputs.jsonl") -> None:
    """Read CSV rows, compile prompts, call pipeline, and write JSONL outputs.

    Expected CSV columns: id (optional), product, name, tone, platform, context (optional)
    """
    loop = asyncio.get_event_loop()

    with open(csv_path, newline='', encoding='utf8') as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)

    tasks = []
    mapping = {}
    for idx, row in enumerate(rows):
        vars = {
            "product": row.get("product") or row.get("Product") or "",
            "name": row.get("name") or row.get("Name") or "",
            "tone": row.get("tone") or row.get("Tone") or "",
            "platform": row.get("platform") or row.get("Platform") or "",
        }
        prompt = template.compile(vars)
        task = asyncio.create_task(pipeline.generate(prompt))
        tasks.append(task)
        mapping[task] = row

    # write outputs as they complete using asyncio.wait for robust Task identity
    with open(out_path, "w", encoding="utf8") as out_fh:
        pending = set(tasks)
        while pending:
            done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)
            for task in done:
                try:
                    res = task.result()
                except Exception as exc:
                    res = json.dumps({"error": str(exc)})
                row = mapping[task]
                try:
                    data = json.loads(res)
                except Exception:
                    data = {"generated": str(res)}

                # apply platform filters
                from .validation import apply_platform_filters

                platform = (row.get("platform") or row.get("Platform") or "").lower()
                processed, truncated, reason = apply_platform_filters(platform, data.get("generated", ""))

                out_record = {**row, **data, "processed": processed, "truncated": truncated, "filter_reason": reason}
                out_fh.write(json.dumps(out_record, ensure_ascii=False) + "\n")
