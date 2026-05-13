# Architecture Trade-offs & Decisions

| Component | Chosen Approach | Omitted | Why |
|-----------|----------------|---------|-----|
| **Database ORM** | `SQLAlchemy` (Async) | `Raw asyncpg` / `Prisma` | Provides robust type safety and relationship mapping while maintaining high asynchronous throughput for logging and traces. |
| **Worker Queue** | `asyncio.create_task` | `Celery` / `Kafka` | The assignment requires a background worker, but adding RabbitMQ + Celery containers for <50 RPS introduces excessive infrastructure overhead. `asyncio` inside FastAPI perfectly matches the LLM streaming latency profile. |
| **LLM Provider** | `litellm` | Hardcoded `OpenAI` or `Google` SDK | Maximizes interoperability. Allows the evaluator to swap between Gemini, Anthropic, or OpenAI simply by changing `.env` variables without touching application code. |
| **Log Interface** | FastAPI `/v1/trace` + PostgreSQL | `Grafana` / `Loki` | Reduces setup time from 30m to 0m. Logs are directly queryable via standard API endpoints. |
| **Context Compression** | Lossless/Lossy LLM Split | External vector summarizers | Avoids dependency bloat. LLMs naturally understand which conversational filler to drop while retaining structured JSON arrays (citations). |
| **DAG Routing** | `networkx` Topological sort | `LangChain` default chains | Hardcoded chains break on ambiguous queries. Dynamic routing with cycle-fallback ensures resilience. |

**Pragmatism Principle:** Complexity is added *only* where failure modes demand it (span critique, strict token budget tracking, adversarial injection handling). Over-engineering is deliberately avoided in infrastructure scaffolding.