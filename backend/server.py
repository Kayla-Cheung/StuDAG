import json
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Set
from graph_engine import GraphEngineV4, CycleDetectedError

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

graph_engine = GraphEngineV4()

class AsyncClientQueue:
    def __init__(self, websocket: WebSocket):
        self.websocket = websocket
        self.queue = asyncio.Queue(maxsize=100)
        self.task = asyncio.create_task(self._send_loop())

    async def _send_loop(self):
        try:
            while True:
                msg = await self.queue.get()
                await self.websocket.send_text(msg)
                self.queue.task_done()
        except Exception:
            pass 

    def enqueue(self, msg: str):
        try:
            self.queue.put_nowait(msg)
        except asyncio.QueueFull:
            pass 

class ConnectionManagerV3:
    def __init__(self):
        self.active_clients: Set[AsyncClientQueue] = set()

    async def connect(self, websocket: WebSocket) -> AsyncClientQueue:
        await websocket.accept()
        client = AsyncClientQueue(websocket)
        self.active_clients.add(client)
        
        async with graph_engine.lock:
            initial_payload = {
                "type": "sync",
                "version": graph_engine.state_version,
                "payload": {
                    "nodes": {"add": [{"id": k, **v} for k, v in graph_engine.nodes.items()]},
                    "edges": {"add": [{"id": k, **v} for k, v in graph_engine.edges.items()]}
                }
            }
        client.enqueue(json.dumps(initial_payload))
        return client

    def disconnect(self, client: AsyncClientQueue):
        if client in self.active_clients:
            client.task.cancel()
            self.active_clients.remove(client)

    def broadcast(self, diff: Dict):
        version = diff.pop("version", None)
        clean_diff = {}
        for category, ops in diff.items():
            clean_ops = {op: items for op, items in ops.items() if items}
            if clean_ops:
                clean_diff[category] = clean_ops
                
        if not clean_diff: return

        message = json.dumps({"type": "diff", "version": version, "payload": clean_diff})
        for client in self.active_clients:
            client.enqueue(message)

manager = ConnectionManagerV3()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    client = await manager.connect(websocket)
    try:
        while True:
            try:
                data = await websocket.receive_text()
                req = json.loads(data)
            except json.JSONDecodeError:
                # Chaos Monkey malformed JSON resistance
                continue
            
            # Chaos Monkey semantic corruption resistance
            if not isinstance(req, dict): continue
            
            action = req.get("action")
            args = req.get("args", {})
            if not isinstance(args, dict): continue
            
            diff = {}
            try:
                if action == "add_node" and "id" in args:
                    diff = await graph_engine.add_node(str(args["id"]), args.get("data", {}))
                elif action == "update_node" and "id" in args:
                    diff = await graph_engine.update_node(str(args["id"]), args.get("data", {}))
                elif action == "remove_node" and "id" in args:
                    diff = await graph_engine.remove_node(str(args["id"]))
                elif action == "add_edge" and "id" in args and "from" in args and "to" in args:
                    if args["from"] is not None and args["to"] is not None:
                        diff = await graph_engine.add_edge(str(args["id"]), str(args["from"]), str(args["to"]))
                elif action == "remove_edge" and "id" in args:
                    diff = await graph_engine.remove_edge(str(args["id"]))
                
                if diff:
                    manager.broadcast(diff)
            except CycleDetectedError as e:
                client.enqueue(json.dumps({"type": "error", "message": str(e)}))
            except Exception as e:
                # Catch internal dictionary exceptions, e.g., missing node errors
                client.enqueue(json.dumps({"type": "error", "message": f"Server Validation Error: {str(e)}"}))
                
    except WebSocketDisconnect:
        manager.disconnect(client)
