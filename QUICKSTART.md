# 🚀 Mega AI Quick Start

Get the system running in under 5 minutes.

## 1. Environment Setup
Create the `.env` file from the example:
```bash
cp .env.example .env
```
Open `.env` and add your LLM API Key:
```env
LLM_API_KEY=your-api-key-here
LLM_MODEL=gemini/gemini-2.5-pro  # Ensure this matches your provider
```

## 2. Start the Infrastructure
Use Docker Compose to build the FastAPI server, the Worker, and the PostgreSQL database:
```bash
docker compose up --build -d
```

## 3. Verify System Health
Check the container logs to ensure the database has migrated and the API is listening:
```bash
docker compose logs -f api
```

## 4. Run the Evaluation Suite
The system ships with 15 baseline, ambiguous, and adversarial test cases. Trigger the evaluation harness:
```bash
docker compose exec worker python -m app.eval.harness
```

## 5. Test Live Streaming
Send a query directly to the Orchestrator to see dynamic tool routing and SSE streaming in real-time:
```bash
curl -N -X POST http://localhost:8000/v1/query/stream \
-H "Content-Type: application/json" \
-d '{"query":"Calculate the 10th fibonacci number using python and then verify your answer."}'
```