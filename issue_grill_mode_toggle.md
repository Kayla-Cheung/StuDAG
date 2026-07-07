# Feature Request: Mode Switch Toggle (Learning vs. Grill) in StuDAG UI

## Architectural Context
Currently, the DAG tracks cognitive progression but does not differentiate between the user's cognitive state modes. The user proposed separating "Learning State" (data ingestion, pushing new nodes, mapping architectures) from "Grill State" (garbage collection, aggressive node popping via hard questions).

## Proposed Implementation
1. **Frontend (View)**: 
   - Introduce a high-contrast toggle switch in `index.html` (e.g., using Glassmorphism aesthetics) to flip the system between `[ 📖 LEARNING ]` and `[ 🔥 GRILL ]` modes.
2. **Backend (Controller/Model)**:
   - When in Grill mode, the UI should visually highlight "Active" leaf nodes in red, signaling they are targets for the next Garbage Collection phase.
   - The MCP gateway should inject a system prompt prefix to the LLM when in Grill mode, enforcing the "No pleasantries, strict interrogation" persona.

## Value Proposition
This prevents cognitive overload by explicitly separating forward propagation (learning) from backward propagation (testing/verifying). It gives the Systems Architect precise control over their mental execution threads.
