import networkx as nx
from typing import Dict, List
from app.utils.llm import generate_json

async def generate_plan(query: str) -> dict:
    prompt = f"""
    Break down the following ambiguous query into a typed set of sub-tasks with explicit dependencies.
    Query: "{query}"
    
    Return a JSON object with a "subtasks" dictionary.
    Each subtask must have a key (e.g., "T1"), and an object with:
    - "type": either "rag" (for information retrieval and reasoning) or "critic" (to review findings).
    - "description": specific instructions.
    - "depends_on": list of keys of subtasks that must complete before this one.
    
    Example:
    {{
        "subtasks": {{
            "T1": {{"type": "rag", "description": "Find X", "depends_on": []}},
            "T2": {{"type": "critic", "description": "Review T1 output", "depends_on": ["T1"]}}
        }}
    }}
    """
    
    return await generate_json(prompt, system_prompt="You are a decomposition agent planning multi-step execution graphs.")

async def resolve_dependencies(subtasks: Dict[str, dict]) -> List[str]:
    if not subtasks: return []
    G = nx.DiGraph()
    for tid, t in subtasks.items():
        G.add_node(tid)
        for dep in t.get("depends_on", []):
            if dep in subtasks:
                G.add_edge(dep, tid)
    try:
        return list(nx.topological_sort(G))
    except nx.NetworkXUnfeasible:
        # Fallback if there is a cycle
        return list(subtasks.keys())