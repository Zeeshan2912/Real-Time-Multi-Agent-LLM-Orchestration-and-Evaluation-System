# Architecture Trade-offs

| Component | Chosen Approach | Omitted | Why |
|-----------|----------------|---------|-----|
| Worker Queue | `asyncio` + BackgroundTasks | Celery/Kafka | Overkill for <50 RPS. Async matches LLM latency profile. |
| Log Interface | FastAPI `/v1/trace` + structured JSON | Grafana/Loki | Reduces setup time from 30m → 0m. Queryable via API. |
| Context Compression | Prompt-based summarization | External compressors | LLM-native, avoids dependency bloat, preserves structured data. |
| DAG Routing | Topological sort on LLM plans | Rule-based chains | Dynamic routing required; rules break on ambiguous queries. |

**Pragmatism Principle:** Complexity added only where failure modes demand it (span critique, budget overflow, adversarial injection).