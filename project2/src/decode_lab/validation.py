from typing import Tuple
import os
import json

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

# Profanity configuration
_PROFANITY_LIST = set()


def _default_config_path():
    # default config path in repo `config/defaults.json` at repo root
    base = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    return os.path.normpath(os.path.join(base, "config", "defaults.json"))


def load_profanity_from_config(path: str = None):
    """Load profanity list from a JSON config file. If path is None, read
    environment variable `DECODELAB_CONFIG` or fallback to packaged defaults.
    The config JSON is expected to have a top-level `profanity` array.
    """
    global _PROFANITY_LIST
    cfg_path = path or os.getenv("DECODELAB_CONFIG") or _default_config_path()
    try:
        with open(cfg_path, "r", encoding="utf8") as fh:
            data = json.load(fh)
            profs = data.get("profanity", []) if isinstance(data, dict) else []
            _PROFANITY_LIST = set(str(x).lower() for x in profs)
    except Exception:
        # fallback to some defaults if loading fails
        _PROFANITY_LIST = {"foo", "bar", "badword"}


# load once at import
load_profanity_from_config()

# Ensure fallback defaults present
if not _PROFANITY_LIST:
    _PROFANITY_LIST = {"foo", "bar", "badword"}


def check_and_sanitize_profanity(text: str) -> Tuple[str, bool]:
    """Detects simple profane tokens and replaces them with asterisks.

    Returns (sanitized_text, unsafe_flag).
    """
    if not text:
        return text, False

    # ensure profanity list is loaded; fallback to defaults when empty
    if not _PROFANITY_LIST:
        load_profanity_from_config()

    words = text.split()
    unsafe = False
    for i, w in enumerate(words):
        wl = ''.join(ch.lower() for ch in w if ch.isalpha())
        if wl in _PROFANITY_LIST:
            words[i] = '*' * len(w)
            unsafe = True

    return ' '.join(words), unsafe


def reload_profanity(path: str = None):
    """Public helper to reload profanity config (used by tests or runtime).

    If `path` is provided, it will be used as the config file path.
    """
    load_profanity_from_config(path)
