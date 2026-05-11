import asyncio, json
from pathlib import Path
from app.eval.scorer import Scorer
from app.utils.logging import log_event

class EvalHarness:
    def __init__(self):
        self.cases = json.loads(Path("app/eval/test_cases.json").read_text())["test_cases"]
        self.scorer = Scorer()

    async def run_all(self):
        results = []
        for c in self.cases:
            mock_run = {"tokens_used": 450, "token_budget": 8000}
            scores = self.scorer.score(mock_run)
            passed = scores["answer_correctness"]["score"] >= c["threshold"]
            results.append({"id": c["id"], "category": c["category"], "scores": scores, "passed": passed})
            log_event(c["id"], "eval_completed", {"category": c["category"], "passed": passed})
        return results