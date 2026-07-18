import asyncio
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components
from typing import Dict, Any

class CycleDetectedError(Exception): pass

class GraphEngineV4:
    """
    V4 integrates C-Level Optimization via scipy.sparse and numpy.
    Bypasses native Python dict overhead for cycle detection during extreme scaling.
    """
    def __init__(self):
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.edges: Dict[str, Dict[str, str]] = {}
        
        # O(1) integer mappings for numpy matrix indexing
        self.node_to_idx: Dict[str, int] = {}
        self.idx_to_node: Dict[int, str] = {}
        self._next_idx = 0
        
        self.lock = asyncio.Lock()
        self.state_version = 0

    def _increment_version(self):
        self.state_version += 1
        return self.state_version

    def _has_cycle_c_level(self, edge_list, num_nodes) -> bool:
        """
        Executes Tarjan's Strongly Connected Components algorithm entirely in C.
        If any component has >1 node, a cycle exists.
        """
        if not edge_list: return False
        row = np.array([e[0] for e in edge_list], dtype=np.int32)
        col = np.array([e[1] for e in edge_list], dtype=np.int32)
        data = np.ones(len(edge_list), dtype=np.int8)
        
        # Construct Compressed Sparse Row matrix
        graph = csr_matrix((data, (row, col)), shape=(num_nodes, num_nodes))
        
        n_components, labels = connected_components(csgraph=graph, directed=True, return_labels=True)
        return n_components < num_nodes

    async def add_node(self, node_id: str, data: Dict[str, Any]) -> Dict:
        async with self.lock:
            if node_id in self.nodes: return {}
            self.nodes[node_id] = data
            
            # Map for C-level matrix
            idx = self._next_idx
            self.node_to_idx[node_id] = idx
            self.idx_to_node[idx] = node_id
            self._next_idx += 1
            
            return {"nodes": {"add": [{"id": node_id, **data}]}, "version": self._increment_version()}

    async def add_edge(self, edge_id: str, u: str, v: str) -> Dict:
        async with self.lock:
            if edge_id in self.edges: return {}
            if u not in self.nodes or v not in self.nodes:
                raise ValueError("Nodes must exist before adding an edge")
            
            # Extract pure integer edge list for C execution
            u_idx = self.node_to_idx[u]
            v_idx = self.node_to_idx[v]
            
            edge_list = [(self.node_to_idx[e['from']], self.node_to_idx[e['to']]) for e in self.edges.values()]
            edge_list.append((u_idx, v_idx))
            num_nodes = self._next_idx
            
        # Offload C-level matrix computation to thread
        has_cycle = await asyncio.to_thread(self._has_cycle_c_level, edge_list, num_nodes)
        
        async with self.lock:
            if has_cycle:
                raise CycleDetectedError(f"Edge {u}->{v} creates a cycle")
            if u not in self.nodes or v not in self.nodes:
                raise ValueError("Node removed during computation")

            self.edges[edge_id] = {"from": u, "to": v}
            return {"edges": {"add": [{"id": edge_id, "from": u, "to": v}]}, "version": self._increment_version()}

    async def remove_node(self, node_id: str) -> Dict:
        # Simplification for prototype: nodes removed from dicts, matrix idx remains sparse
        async with self.lock:
            if node_id not in self.nodes: return {}
            del self.nodes[node_id]
            edges_to_remove = [e for e, data in self.edges.items() if data['from'] == node_id or data['to'] == node_id]
            for e in edges_to_remove: del self.edges[e]
            diff = {"nodes": {"remove": [{"id": node_id}]}, "edges": {"remove": [{"id": e} for e in edges_to_remove]}, "version": self._increment_version()}
            return diff

    async def remove_edge(self, edge_id: str) -> Dict:
        async with self.lock:
            if edge_id not in self.edges: return {}
            del self.edges[edge_id]
            return {"edges": {"remove": [{"id": edge_id}]}, "version": self._increment_version()}
