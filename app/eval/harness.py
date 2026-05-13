import asyncio, json, uuid
from pathlib import Path
from app.eval.scorer import Scorer
from app.utils.logging import log_event
from app.agents.orchestrator import Orchestrator
from app.db.database import AsyncSessionLocal
from app.db.models import EvaluationRun

class EvalHarness:
    def __init__(self):
        self.cases = json.loads(Path("app/eval/test_cases.json").read_text())["test_cases"]
        self.scorer = Scorer()

    async def run_all(self):
        run_id = str(uuid.uuid4())
        results = []
        
        for c in self.cases:
            job_id = str(uuid.uuid4())
            query = c["input"]
            
            orchestrator = Orchestrator()
            context = await orchestrator.execute(job_id, query)
            
            scores = await self.scorer.score(
                query=query, 
                context_state=context.current_state,
                tokens_used=context.tokens_used,
                budget=context.token_budget
            )
            
            passed = scores.get("answer_correctness", {}).get("score", 0.0) >= c["threshold"]
            
            async with AsyncSessionLocal() as session:
                eval_run = EvaluationRun(
                    test_case_id=c["id"],
                    run_id=run_id,
                    scores={k: v.get("score", 0.0) for k, v in scores.items()},
                    justification={k: v.get("justification", "") for k, v in scores.items()}
                )
                session.add(eval_run)
                await session.commit()
            
            results.append({"id": c["id"], "category": c["category"], "scores": scores, "passed": passed})
            await log_event(job_id, "eval_completed", {"category": c["category"], "passed": passed})
            
        return results

if __name__ == "__main__":
    harness = EvalHarness()
    asyncio.run(harness.run_all())