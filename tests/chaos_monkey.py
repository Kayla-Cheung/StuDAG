import asyncio
import websockets
import json
import random

async def chaos_client(client_id, uri):
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                # Wait for initial sync
                await websocket.recv()
                
                # Normal operations
                for i in range(5):
                    node_id = f"c_{client_id}_{random.randint(0, 1000)}"
                    payload = {"action": "add_node", "args": {"id": node_id, "data": {"label": "Chaos Node"}}}
                    await websocket.send(json.dumps(payload))
                    await asyncio.sleep(0.1)

                # Inject Chaos
                chaos_type = random.choice(["malformed_json", "abrupt_close", "corrupted_payload"])
                
                if chaos_type == "malformed_json":
                    await websocket.send("{invalid_json: true, action: 'add_node'")
                    
                elif chaos_type == "abrupt_close":
                    # Forcefully close the connection without closing handshake
                    websocket.transport.close()
                    
                elif chaos_type == "corrupted_payload":
                    # Send valid JSON but semantically corrupt
                    await websocket.send(json.dumps({"action": "add_edge", "args": {"from": None, "to": dict()}}))

                # If connection survives, forcefully kill it to simulate network partition
                await asyncio.sleep(0.5)
                
        except Exception:
            # Reconnect after chaos partition
            await asyncio.sleep(1)

async def main():
    uri = "ws://127.0.0.1:8000/ws"
    clients = 20
    print(f"Unleashing Chaos Monkey with {clients} rogue connections...")
    tasks = [chaos_client(i, uri) for i in range(clients)]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
