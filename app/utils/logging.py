import json, datetime
from app.db.database import AsyncSessionLocal
from app.db.models import LogEvent

async def log_event(job_id: str, event: str, data: dict = None, agent_id: str = None, token_count: int = None, latency_ms: float = None):
    async with AsyncSessionLocal() as session:
        log_entry = LogEvent(
            job_id=job_id,
            event_type=event,
            agent_id=agent_id,
            token_count=token_count,
            latency_ms=latency_ms,
            details=data or {}
        )
        session.add(log_entry)
        await session.commit()
    
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "job_id": job_id,
        "event": event,
        **(data or {})
    }
    print(json.dumps(entry))