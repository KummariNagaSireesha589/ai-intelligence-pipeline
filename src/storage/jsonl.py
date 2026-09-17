import json
from pathlib import Path

def write_jsonl(records, path):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record.model_dump(mode="json"), ensure_ascii=False) + "\n")
