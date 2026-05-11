# 🤖 Mega AI: Multi-Agent LLM Orchestration

## 🚀 Setup (5 Minutes)
```bash
cp .env.example .env && docker compose up --build -d
curl -N -X POST http://localhost:8000/v1/query/stream -H "Content-Type: application/json" -d '{"query":"test"}'