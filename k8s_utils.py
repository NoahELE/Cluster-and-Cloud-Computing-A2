def secret(key: str) -> str:
    with open(f"/secrets/default/secrets/{key}", "r", encoding="utf-8") as f:
        return f.read()
