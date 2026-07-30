import os
import json
from pathlib import Path

from src.decode_lab import validation


def test_reload_profanity(tmp_path: Path, monkeypatch):
    cfg = tmp_path / "cfg.json"
    cfg.write_text(json.dumps({"profanity": ["xword"]}), encoding='utf8')

    # set env var to point to our config and reload
    monkeypatch.setenv("DECODELAB_CONFIG", str(cfg))
    validation.reload_profanity()

    sanitized, unsafe = validation.check_and_sanitize_profanity("this contains xword and clean")
    assert unsafe is True
    assert "xword" not in sanitized.lower()
    # restore defaults to avoid leaking state to other tests
    monkeypatch.delenv("DECODELAB_CONFIG", raising=False)
    validation.reload_profanity(None)
