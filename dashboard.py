import os
import json
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from core import CognitiveTracker
import uvicorn

app = FastAPI()
tracker = CognitiveTracker()

class ResolveRequest(BaseModel):
    node_id: str

@app.post("/api/push")
def push_node(topic: str, parent_id: str = None):
    try:
        nid = tracker.push_node(topic, parent_id)
        return {"status": "success", "node_id": nid}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

@app.get("/api/state")
def get_state():
    # Force reload from physical disk to ensure sync with MCP server
    tracker.state = tracker._load_state()
    return {
        "nodes": [
            {
                "id": n.id,
                "topic": n.topic,
                "status": n.status,
                "parent_id": n.parent_id,
            }
            for n in tracker.state.nodes.values()
        ],
        "call_stack": tracker.state.call_stack
    }

@app.post("/api/resolve")
def resolve_node(req: ResolveRequest):
    try:
        tracker.resolve_node(req.node_id)
        return {"status": "success"}
    except Exception as e:
        # Pass the PermissionError up to the frontend UI
        return {"status": "error", "detail": str(e)}

@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    print("🔥 StuDAG Cognitive Dashboard is running at: http://localhost:8080")
    uvicorn.run(app, host="0.0.0.0", port=8080)
