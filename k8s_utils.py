def config(key: str) -> str:
    with open(f"/configs/default/parameters/{key}", "r", encoding="utf-8") as f:
        return f.read()
