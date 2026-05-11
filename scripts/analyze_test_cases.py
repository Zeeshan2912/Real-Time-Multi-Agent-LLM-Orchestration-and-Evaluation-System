import json, statistics
from pathlib import Path

cases = json.loads(Path("app/eval/test_cases.json").read_text())["test_cases"]
cats = {}
for c in cases:
    cats.setdefault(c["category"], []).append(len(c["input"]))

print("📊 Test Case Distribution")
for cat, lens in cats.items():
    print(f"{cat}: {len(lens)} cases | avg len: {statistics.mean(lens):.0f}")