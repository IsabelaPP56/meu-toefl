import json, re
from pathlib import Path

OUT = Path("/workspace/site/data/parts")

def words(text):
    return re.findall(r"[A-Za-z0-9’']+", text)

def dump(name, data):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{name}.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(name, len(data), path.stat().st_size)

def mc(q, options, a, why):
    assert len(options) == 4 and 0 <= a < 4
    return {"q": q, "options": options, "a": a, "why": why}
