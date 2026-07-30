from src.decode_lab.validation import apply_platform_filters


def test_twitter_truncation():
    text = "x" * 500
    processed, truncated, reason = apply_platform_filters("twitter", text)
    assert truncated is True
    assert len(processed) <= 280


def test_linkedin_no_truncation():
    text = "hello world"
    processed, truncated, reason = apply_platform_filters("linkedin", text)
    assert truncated is False
    assert processed == "hello world"
