import json, datetime

def log_event(job_id: str, event: str, data: dict = None):
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "job_id": job_id,
        "event": event,
        **(data or {})
    }
    # In production: pipe to structured log sink
    print(json.dumps(entry))