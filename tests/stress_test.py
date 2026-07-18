import asyncio
import websockets
import json
import time
import random

async def simulate_client(client_id, uri, num_mutations):
    async with websockets.connect(uri) as websocket:
        # Wait for initial sync
        await websocket.recv()
        
        start_time = time.time()
        for i in range(num_mutations):
            node_id = f"n_{client_id}_{i}"
            payload = {
                "action": "add_node",
                "args": {"id": node_id, "data": {"label": f"Node {i}"}}
            }
            await websocket.send(json.dumps(payload))
            
            # Simulate random network latency/packet drop
            await asyncio.sleep(random.uniform(0.001, 0.01))
            
            # Read incoming diffs without blocking
            try:
                while True:
                    await asyncio.wait_for(websocket.recv(), timeout=0.001)
            except asyncio.TimeoutError:
                pass

        return time.time() - start_time

async def main():
    uri = "ws://127.0.0.1:8000/ws"
    clients = 50
    mutations_per_client = 200
    print(f"Initiating adversarial test: {clients} clients, {clients * mutations_per_client} total mutations.")
    
    start = time.time()
    tasks = [simulate_client(i, uri, mutations_per_client) for i in range(clients)]
    times = await asyncio.gather(*tasks)
    total_time = time.time() - start
    
    print(f"Test completed in {total_time:.2f} seconds.")
    print(f"Average time per client: {sum(times)/len(times):.2f}s")
    print("If the server's broadcast loop was sequential, this would cause massive lagging and event loop blocking.")

if __name__ == "__main__":
    asyncio.run(main())
