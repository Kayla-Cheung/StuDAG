import httpx
import time
import sys
import os

BASE_URL = "http://127.0.0.1:8080/api"
client = httpx.Client(trust_env=False)

def test_api():
    print("========================================")
    print("StuDAG Autonomous CI/CD Integrity Test")
    print("========================================")
    
    # 1. Clean up
    state_file = os.path.join(os.path.dirname(__file__), "state_machine.json")
    if os.path.exists(state_file):
        os.remove(state_file)
        print("[*] Cleaned up legacy state_machine.json")

    # 2. Push Root Node
    print("\n[+] Pushing root node: CPU Principles")
    r = client.post(f"{BASE_URL}/push", params={"topic": "CPU Principles"})
    assert r.status_code == 200, r.text
    root_id = r.json()["node_id"]
    print(f"    -> Root ID: {root_id}")

    # 3. Push Sub Node 1
    print("\n[+] Pushing sub node: Transistors")
    r = client.post(f"{BASE_URL}/push", params={"topic": "Transistors"})
    sub1_id = r.json()["node_id"]
    print(f"    -> Sub1 ID: {sub1_id}")

    # 4. Push Sub Node 2 under Sub 1
    print("\n[+] Pushing sub node: Semiconductors")
    r = client.post(f"{BASE_URL}/push", params={"topic": "Semiconductors"})
    sub2_id = r.json()["node_id"]
    print(f"    -> Sub2 ID: {sub2_id}")

    # 5. TEST: Hard Constraint Violation (Resolve Sub 1 BEFORE Sub 2)
    print("\n[!] TEST: Attempting to resolve Transistors before Semiconductors")
    r = client.post(f"{BASE_URL}/resolve", json={"node_id": sub1_id})
    res = r.json()
    assert res["status"] == "error", "Constraint Failed: Engine allowed illegal POP!"
    print(f"    -> Blocked successfully. Engine returned: {res['detail']}")

    # 6. Resolve Sub 2
    print("\n[+] Resolving Semiconductors")
    r = client.post(f"{BASE_URL}/resolve", json={"node_id": sub2_id})
    assert r.json()["status"] == "success"

    # 7. Resolve Sub 1
    print("\n[+] Resolving Transistors")
    r = client.post(f"{BASE_URL}/resolve", json={"node_id": sub1_id})
    assert r.json()["status"] == "success"

    # 8. Check Final State
    print("\n[*] Fetching final DAG state...")
    r = client.get(f"{BASE_URL}/state")
    state = r.json()
    active_stack = state["call_stack"]
    print(f"    -> Current Call Stack Depth: {len(active_stack)}")
    assert active_stack == [root_id], "Stack mismatch!"
    
    print("\n✅ ALL TESTS PASSED. The topological engine physical constraints hold perfectly.")
    print("========================================")

if __name__ == "__main__":
    try:
        test_api()
    except Exception as e:
        print(f"❌ TEST FAILED: {e}")
        sys.exit(1)
