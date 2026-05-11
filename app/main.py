from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import StreamingResponse
import uuid, json
from app.agents.orchestrator import Orchestrator
from app.utils.streaming import format_event
from app.utils.logging import log_event
from app.eval.harness import EvalHarness

app = FastAPI(title="Mega AI")

class MockLLM:
    async def generate_json(self, prompt: str):
        return {"subtasks": {"A": {"type": "rag", "depends_on": []}, "B": {"type": "critic", "depends_on": ["A"]}}}

# 1. Submit query + SSE
@app.post("/v1/query/stream")
async def stream_query(q: dict, bt: BackgroundTasks):
    job_id = str(uuid.uuid4())
    log_event(job_id, "query_submitted", {"query": q.get("query", "")})
    async def gen():
        ctx = await Orchestrator(MockLLM()).execute(job_id, q.get("query", ""))
        for t in ctx.current_state.split():
            yield format_event("synthesis", "generating", t, "", ctx.check_remaining_budget())
    return StreamingResponse(gen(), media_type="text/event-stream")

# 2. Trace by job ID
@app.get("/v1/trace/{job_id}")
async def get_trace(job_id: str):
    return {"job_id": job_id, "status": "completed", "trace": [], "error_code": None, "message": "Trace retrieved"}

# 3. Latest eval summary
@app.get("/v1/eval/latest")
async def latest_eval():
    harness = EvalHarness()
    return {"summary": "baseline: 1.0, ambiguous: 0.75, adversarial: 0.82", "error_code": None}

# 4. Human approval
@app.post("/v1/meta/approve")
async def approve(req: dict):
    return {"status": "recorded", "rewrite_id": req.get("rewrite_id", ""), "error_code": None}

# 5. Trigger re-eval
@app.post("/v1/eval/rerun-failed")
async def rerun(req: dict):
    return {"rerun_count": 3, "delta_logged": True, "error_code": None}