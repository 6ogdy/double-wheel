import json
rows = [json.loads(l) for l in open("out/rec.jsonl", encoding="utf-8") if l.strip()]
print(len(rows), "rows")
for i, r in enumerate(rows):
    d = r["d"]
    try:
        j = json.loads(d)
        if isinstance(j, dict) and "1" in j and isinstance(j["1"], dict):
            j["1"].pop("history", None)
        d = json.dumps(j, ensure_ascii=False)
    except Exception:
        pass
    print(i, round(r.get("ts", 0) - rows[0].get("ts", 0), 1), r["dir"], d[:200])
