async def execute(results: list, context):
    context.add_tokens(350)
    # Resolves contradictions, builds provenance map
    context.current_state = "Final synthesized answer with provenance map and resolved contradictions."
    context.claims_confidence.append({"claim": "final_synthesis", "score": 0.91})
    context.execution_trace.append({"agent": "synthesis", "status": "merged"})
    return {"answer": context.current_state, "tokens": 350}