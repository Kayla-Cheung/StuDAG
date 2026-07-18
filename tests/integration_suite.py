import unittest
import asyncio
from graph_engine_v4 import GraphEngineV4, CycleDetectedError

class TestGraphEngineV4(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.engine = GraphEngineV4()

    async def test_add_nodes(self):
        diff = await self.engine.add_node("n1", {"label": "Node 1"})
        self.assertIn("add", diff["nodes"])
        self.assertEqual(diff["nodes"]["add"][0]["id"], "n1")
        self.assertEqual(self.engine.state_version, 1)

    async def test_cycle_detection_c_level(self):
        await self.engine.add_node("A", {})
        await self.engine.add_node("B", {})
        await self.engine.add_node("C", {})
        
        await self.engine.add_edge("e1", "A", "B")
        await self.engine.add_edge("e2", "B", "C")
        
        with self.assertRaises(CycleDetectedError):
            await self.engine.add_edge("e3", "C", "A")

    async def test_concurrent_mutations(self):
        await self.engine.add_node("root", {})
        
        # Dispatch 500 concurrent additions to verify lock safety
        async def worker(i):
            await self.engine.add_node(f"n{i}", {})
            await self.engine.add_edge(f"e{i}", "root", f"n{i}")

        await asyncio.gather(*(worker(i) for i in range(500)))
        
        self.assertEqual(len(self.engine.nodes), 501)
        self.assertEqual(len(self.engine.edges), 500)
        # 1 root + 500 nodes + 500 edges = 1001 mutations
        self.assertEqual(self.engine.state_version, 1001)

    async def test_invalid_edge_nodes(self):
        with self.assertRaises(ValueError):
            await self.engine.add_edge("e1", "nonexistent1", "nonexistent2")

if __name__ == '__main__':
    unittest.main()
