import networkx as nx
from typing import Dict, List

async def resolve_dependencies(subtasks: Dict[str, dict]) -> List[str]:
    if not subtasks: return []
    G = nx.DiGraph()
    for tid, t in subtasks.items():
        G.add_node(tid)
        for dep in t.get("depends_on", []):
            G.add_edge(dep, tid)
    return list(nx.topological_sort(G))