# StuDAG

**A Graph-Based C-S Architecture for Dynamic Knowledge Representation**

StuDAG is designed around a strict Client-Server Single Source of Truth (SSoT) architecture. By decoupling state management from the rendering layer and embracing `vis.DataSet` for incremental updates, StuDAG delivers high-performance, deterministic graph synchronizations.

## Architecture: C-S Single Source of Truth
- **Server-Side State**: The backend maintains the absolute source of truth for all DAG structures.
- **Client-Side Sync**: The frontend syncs purely through incremental diffs.
- **`vis.DataSet` Integration**: Leveraging `vis.DataSet` allows the graph visualization to selectively update nodes and edges without full re-renders, dramatically reducing compute overhead on large DAGs.

## Features
- **Incremental Updates**: Only modified nodes/edges are dispatched to the client, mapped directly to vis.js methods.
- **Deterministic Rendering**: The server dictates graph topology; the client purely reflects the data structure.
- **High Performance**: Eliminates full DOM wipe-and-rebuild cycles and mitigates memory thrashing.
