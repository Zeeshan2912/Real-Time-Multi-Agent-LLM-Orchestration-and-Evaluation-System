from app.utils.llm import generate_text
from app.tools.web_search import WebSearchTool

async def execute(instruction: str, context, task_id: str):
    search_tool = WebSearchTool()
    
    current_query = instruction
    retries = 0
    chunks = []
    
    while retries <= 2:
        search_res = await search_tool.run(query=current_query)
        status = search_res.get("result", {}).get("status")
        
        context.tool_calls_log.append({
            "task": task_id, 
            "tool": "web_search", 
            "query": current_query,
            "status": status,
            "attempt": retries + 1,
            "decision": "accepted" if status == "success" and search_res.get("result", {}).get("data") else "rejected"
        })
        
        if status == "success":
            chunks = search_res["result"]["data"]
            if chunks:
                break # Agent accepted result
                
        # Agent decides it's insufficient and modifies input
        retries += 1
        if retries <= 2:
            prompt = f"The web search for '{current_query}' failed or returned empty results. Generate a single modified search query string to try again."
            current_query = await generate_text(prompt, system_prompt="You are an expert search modifier.")
            current_query = current_query.strip('"\' \n')
    
    if not chunks:
        chunks = search_tool.get_fallback()
        
    chunks_text = "\n".join([f"[{i+1}] {c['snippet']} (Source: {c['url']})" for i, c in enumerate(chunks)])
    
    prompt = f"""
    Perform multi-hop reasoning on the following retrieved chunks to answer the instruction.
    You MUST cite which chunk contributed to which part of the answer using [1], [2], etc.
    
    Instruction: {instruction}
    Retrieved Chunks:
    {chunks_text}
    """
    
    answer = await generate_text(prompt, system_prompt="You are a RAG reasoning agent.")
    
    context.add_text_to_state(f"RAG Agent (Task {task_id}): {answer}")
    
    for i, c in enumerate(chunks):
        context.citations.append({
            "task_id": task_id,
            "chunk_id": f"chunk_{i+1}",
            "url": c.get('url', ''),
            "relevance": c.get('score', 0.0),
            "span_mapped_to": f"[{i+1}]"
        })
        
    return {"answer": answer}