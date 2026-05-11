import json
from pathlib import Path

test_text = json.loads(Path("app/eval/test_cases.json").read_text())["test_cases"]
prompts = [f.read_text() for f in Path("app").rglob("*.py")]
combined = " ".join(prompts).lower()

leaks = [c["input"] for c in test_text if c["input"].lower() in combined]
print("✅ No test case leakage detected" if not leaks else f"🚨 Leakage detected: {leaks}")