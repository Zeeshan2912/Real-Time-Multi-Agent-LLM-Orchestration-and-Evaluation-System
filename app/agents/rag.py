async def execute(prompt: str, context, task_id: str):
    # Simulates multi-hop retrieval with chunk-level provenance
    context.add_tokens(450)
    context.citations.append({
        "task_id": task_id,
        "chunk_id": "chunk_01",
        "url": "https://example.com/source1",
        "relevance": 0.92,
        "span_mapped_to": "sentence_1"
    })
    context.tool_calls_log.append({"task": task_id, "tool": "web_search", "status": "success"})
    return {"answer": "Retrieved chunk with citation.", "tokens": 450}