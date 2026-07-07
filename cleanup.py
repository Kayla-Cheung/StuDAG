import json
import os

path = r"C:\Users\Kayla\Desktop\Repos\StuDAG\state_machine.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

nodes = data.get("nodes", {})

def get_all_descendants(node_id):
    if node_id not in nodes: return []
    desc = [node_id]
    for child in nodes[node_id].get("children", []):
        desc.extend(get_all_descendants(child))
    return desc

# Target the reviewed Digital Circuit branches
to_remove = []
to_remove.extend(get_all_descendants("node_85924d92")) # 74LS151 branch
to_remove.extend(get_all_descendants("node_4ebbd9f9")) # Karnaugh map branch

# Remove from parent's children list
if "node_68f46638" in nodes:
    nodes["node_68f46638"]["children"] = [
        c for c in nodes["node_68f46638"]["children"] if c not in to_remove
    ]

# Delete nodes
for nid in to_remove:
    if nid in nodes:
        del nodes[nid]

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Removed {len(to_remove)} resolved nodes from the DAG.")
