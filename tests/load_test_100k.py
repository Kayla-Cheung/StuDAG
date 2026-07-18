import asyncio
import time
from graph_engine_v4 import GraphEngineV4

async def main():
    engine = GraphEngineV4()
    num_nodes = 100000
    num_edges = 150000

    print(f"Loading {num_nodes} nodes into memory...")
    start = time.time()
    for i in range(num_nodes):
        await engine.add_node(f"n{i}", {})
    print(f"Nodes loaded in {time.time() - start:.2f}s")

    print(f"Creating {num_edges} edges (DAG structure)...")
    start = time.time()
    
    # Create valid DAG edges
    for i in range(num_edges):
        u = f"n{i % (num_nodes - 1)}"
        v = f"n{(i % (num_nodes - 1)) + 1}"
        try:
            await engine.add_edge(f"e{i}", u, v)
        except Exception:
            pass # Ignore duplicate edges or cycles for load generation

    print(f"Edges created in {time.time() - start:.2f}s")
    
    # Extreme Cycle Check profiling
    print("Executing worst-case $O(V+E)$ C-level cycle trace...")
    start = time.time()
    try:
        await engine.add_edge("killer_edge", f"n{num_nodes-1}", "n0")
    except Exception as e:
        print(f"Cycle properly blocked: {e}")
    print(f"C-Level Cycle Detection execution time: {(time.time() - start) * 1000:.2f}ms")

if __name__ == "__main__":
    asyncio.run(main())
