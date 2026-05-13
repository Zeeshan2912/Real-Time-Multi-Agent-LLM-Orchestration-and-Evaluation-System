from fastapi import FastAPI, BackgroundTasks, Depends
from fastapi.responses import StreamingResponse
import uuid, json, asyncio
from app.agents.orchestrator import Orchestrator
from app.utils.streaming import format_event
from app.utils.logging import log_event
from app.eval.harness import EvalHarness
from app.db.database import init_db, AsyncSessionLocal
from sqlalchemy import select
from app.db.models import LogEvent, EvaluationRun, PromptRewrite

app = FastAPI(title="Mega AI")

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.post("/v1/query/stream")
async def stream_query(q: dict, bt: BackgroundTasks):
    job_id = str(uuid.uuid4())
    query = q.get("query", "")
    await log_event(job_id, "query_submitted", {"query": query})
    
    async def gen():
        orchestrator = Orchestrator()
        task = asyncio.create_task(orchestrator.execute(job_id, query))
        
        last_state = ""
        while not task.done():
            if orchestrator.context and orchestrator.context.current_state != last_state:
                yield format_event("orchestrator", "update", orchestrator.context.current_state[-100:], "", orchestrator.context.check_remaining_budget())
                last_state = orchestrator.context.current_state
            await asyncio.sleep(0.5)
            
        context = await task
        yield format_event("synthesis", "complete", context.current_state, "", context.check_remaining_budget())
        
    return StreamingResponse(gen(), media_type="text/event-stream")

@app.get("/v1/trace/{job_id}")
async def get_trace(job_id: str):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(LogEvent).where(LogEvent.job_id == job_id).order_by(LogEvent.timestamp))
        logs = [row[0] for row in result]
        
    return {
        "job_id": job_id, 
        "trace": [{"event": l.event_type, "timestamp": l.timestamp.isoformat(), "details": l.details} for l in logs]
    }

@app.get("/v1/eval/latest")
async def latest_eval():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(EvaluationRun).order_by(EvaluationRun.timestamp.desc()).limit(15))
        runs = [row[0] for row in result]
        
    return {"summary": f"Retrieved {len(runs)} latest runs.", "runs": [{"id": r.id, "scores": r.scores} for r in runs]}

@app.post("/v1/meta/approve")
async def approve(req: dict):
    rewrite_id = req.get("rewrite_id")
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(PromptRewrite).where(PromptRewrite.id == rewrite_id))
        rewrite = result.scalar_one_or_none()
        if rewrite:
            rewrite.status = "approved"
            await session.commit()
            return {"status": "approved", "rewrite_id": rewrite_id}
    return {"status": "not_found"}

@app.post("/v1/eval/rerun-failed")
async def rerun(req: dict):
    return {"status": "rerun_triggered"}

from fastapi.responses import HTMLResponse
@app.get("/logs/ui", response_class=HTMLResponse)
async def log_ui():
    html_content = """
    <!DOCTYPE html>
    <html><head><title>Mega AI Logs</title></head>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h2>Trace Viewer</h2>
        <input type="text" id="jobId" placeholder="Enter Job ID" style="width:300px; padding:5px;"/>
        <button onclick="fetchLogs()" style="padding:5px 15px;">Search</button>
        <pre id="output" style="background:#f4f4f4; padding:10px; margin-top:10px; border-radius:5px; white-space: pre-wrap;"></pre>
        <script>
            async function fetchLogs() {
                const jid = document.getElementById('jobId').value;
                if(!jid) return;
                const res = await fetch('/v1/trace/' + jid);
                const data = await res.json();
                document.getElementById('output').textContent = JSON.stringify(data, null, 2);
            }
        </script>
    </body></html>
    """
    return HTMLResponse(content=html_content)