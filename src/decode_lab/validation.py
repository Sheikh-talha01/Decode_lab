from typing import Tuple

# Platform character limits (sane defaults)
PLATFORM_LIMITS = {
    "twitter": 280,
    "linkedin": 1300,
    "instagram": 2200,
    "email": 10000,
}


def apply_platform_filters(platform: str, text: str) -> Tuple[str, bool, str]:
    """Apply simple platform-specific filters.

    Returns (processed_text, truncated_flag, reason).
    """
    if not text:
        return text, False, "empty"

    key = (platform or "").lower()
    max_len = PLATFORM_LIMITS.get(key)
    processed = text.strip()
    truncated = False
    reason = "ok"

    if max_len is not None and len(processed) > max_len:
        # simple truncation preserving words
        cutoff = processed[: max_len]
        # try to cut at last space
        last_space = cutoff.rfind(" ")
        if last_space > int(max_len * 0.6):
            cutoff = cutoff[:last_space]
        processed = cutoff.rstrip()
        truncated = True
        reason = f"truncated to {max_len} chars"

    return processed, truncated, reason
