from typing import Dict


class MasterTemplate:
    """A simple master instruction template using Python f-strings.

    In production we'd sandbox compilation; here we use safe formatting.
    """

    TEMPLATE = (
        "Product: {product}\n"
        "Name: {name}\n"
        "Platform: {platform}\n"
        "Tone: {tone}\n"
        "\n"
        "Write a concise marketing blurb for the product above tailored to {platform} using a {tone} tone."
    )

    def compile(self, variables: Dict[str, str]) -> str:
        # Basic sanitization
        safe = {k: str(v).strip() for k, v in variables.items()}
        return self.TEMPLATE.format(**safe)
