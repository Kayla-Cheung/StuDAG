import os
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
import uuid

# ---------------------------------------------------------
# 数据传输对象 (DTO/信封)
# 运用了我们上午刚刚推演过的结构体思想，隔离数据与行为
# ---------------------------------------------------------
class Node(BaseModel):
    id: str
    topic: str
    status: str = "active" # "active" 或 "resolved"
    parent_id: Optional[str] = None
    children: List[str] = Field(default_factory=list)

class DAGState(BaseModel):
    nodes: Dict[str, Node] = Field(default_factory=dict)
    call_stack: List[str] = Field(default_factory=list) # 用户的认知压栈轨迹

# ---------------------------------------------------------
# 服务中枢 (Engine/Service)
# 拒绝使用语法糖，纯手工控制底层物理 JSON 的序列化和校验
# ---------------------------------------------------------
class CognitiveTracker:
    """人类认知拓扑跟踪引擎核心"""
    
    def __init__(self, storage_path: str = None):
        if storage_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            storage_path = os.path.join(base_dir, "state_machine.json")
        self.storage_path = storage_path
        self.state = self._load_state()

    def _load_state(self) -> DAGState:
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                return DAGState.model_validate_json(f.read())
        return DAGState()

    def _save_state(self):
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            f.write(self.state.model_dump_json(indent=2))

    def push_node(self, topic: str, parent_id: Optional[str] = None) -> str:
        """人类发起了深层追问，将新概念压入认知栈"""
        # 强制磁盘同步：防止多进程脑裂覆写
        self.state = self._load_state()

        node_id = f"node_{uuid.uuid4().hex[:8]}"
        
        # 寻址规则：如果没有指定父节点，自动挂载在当前栈顶节点之下
        if not parent_id and self.state.call_stack:
            parent_id = self.state.call_stack[-1]

        # 物理防御：绝对禁止在已经消灭的节点上节外生枝
        if parent_id and parent_id in self.state.nodes:
            if self.state.nodes[parent_id].status == "resolved":
                raise PermissionError(f"物理熔断被触发：父节点 [{self.state.nodes[parent_id].topic}] 已经结算完毕。系统禁止在已死节点上强行开辟新分支！")

        new_node = Node(id=node_id, topic=topic, parent_id=parent_id)
        self.state.nodes[node_id] = new_node
        
        if parent_id and parent_id in self.state.nodes:
            self.state.nodes[parent_id].children.append(node_id)
            
        self.state.call_stack.append(node_id)
        self._save_state()
        return node_id

    def resolve_node(self, node_id: str):
        """人类宣告理解，将节点弹栈 (POP)"""
        # 强制磁盘同步：防止多进程脑裂覆写
        self.state = self._load_state()

        if node_id not in self.state.nodes:
            raise ValueError(f"节点 {node_id} 不存在")
            
        node = self.state.nodes[node_id]
        if node.status == "resolved":
            return
            
        # 强制约束（物理防御机制）：只有子节点全懂了，才能结算父节点
        for child_id in node.children:
            if self.state.nodes[child_id].status != "resolved":
                # 直接通过 raise 抛出物理熔断！
                raise PermissionError(f"物理熔断被触发：子节点 [{self.state.nodes[child_id].topic}] 尚未被用户消化，系统绝对禁止越权解决父节点！")
                
        node.status = "resolved"
        
        if node_id in self.state.call_stack:
            self.state.call_stack.remove(node_id)
            
        self._save_state()

    def get_cognitive_stack(self) -> dict:
        """抛给 LLM 的冷酷指令视图"""
        active_nodes = [self.state.nodes[nid].model_dump() for nid in self.state.call_stack]
        return {
            "current_focus": active_nodes[-1] if active_nodes else None,
            "call_stack_depth": len(active_nodes),
            "system_instruction": "CRITICAL PROTOCOL: 如果 current_focus 不为空，你必须、且只能回答该焦点节点的问题。绝对禁止用任何引导语向用户推进父节点的内容！"
        }
