from src.decode_lab.validation import check_and_sanitize_profanity


def test_profanity_sanitized():
    text = "This is foo and BAR in text"
    sanitized, unsafe = check_and_sanitize_profanity(text)
    assert unsafe is True
    assert "***" in sanitized or "****" in sanitized


def test_no_profanity():
    text = "Clean text here"
    sanitized, unsafe = check_and_sanitize_profanity(text)
    assert unsafe is False
    assert sanitized == text
