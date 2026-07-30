from src.decode_lab.template import MasterTemplate


def test_compile_basic():
    tpl = MasterTemplate()
    prompt = tpl.compile({"product": "Shoe", "name": "Acme", "tone": "witty", "platform": "linkedin"})
    assert "Product: Shoe" in prompt
    assert "Platform: linkedin" in prompt
