import tracemalloc
import asyncio
from graph_engine_v3 import GraphEngineV3
from graph_engine_v4 import GraphEngineV4

async def profile_engine(engine_class, name, num_nodes=5000, num_edges=10000):
    engine = engine_class()
    tracemalloc.start()
    
    for i in range(num_nodes):
        await engine.add_node(f"n{i}", {"label": f"Node {i}"})
        
    for i in range(num_edges):
        try:
            # Create a sparse chain to test cycle detection
            await engine.add_edge(f"e{i}", f"n{i % num_nodes}", f"n{(i+1) % num_nodes}")
        except Exception:
            pass

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"[{name}] Current Memory: {current / 10**6:.2f} MB; Peak: {peak / 10**6:.2f} MB")

async def main():
    print("Initiating Phase 4 Memory Profiling...")
    await profile_engine(GraphEngineV3, "V3 Native Python DFS")
    await profile_engine(GraphEngineV4, "V4 C-Level SciPy Matrix")
    print("Profiling Complete.")

if __name__ == "__main__":
    asyncio.run(main())
