import os


def require_token(authorization: str | None) -> bool:
    token = os.environ.get("PROJECT1_API_TOKEN")
    if not token:
        return True
    if not authorization:
        return False
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return False
    return parts[1] == token


def get_token():
    return os.environ.get("PROJECT1_API_TOKEN")
