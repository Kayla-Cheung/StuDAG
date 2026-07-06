import json
from core import CognitiveTracker

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("FATAL: 缺失 mcp SDK 依赖。请运行 `pip install mcp`")
    exit(1)

# 实例化标准 MCP 服务器
mcp = FastMCP("StuDAG_Interceptor")
tracker = CognitiveTracker()

@mcp.tool()
def push_knowledge_node(topic: str, parent_id: str = None) -> str:
    """
    当人类用户追问前置知识、遇到不理解的新概念时，AI 必须调用此工具。
    作用：强制挂起当前主干，将人类引入深层认知子节点。
    """
    node_id = tracker.push_node(topic, parent_id)
    return f"[SUCCESS] 节点已物理压栈。ID: {node_id}。作为 AI，你现在必须全神贯注于该 Topic，绝不可越界。"

@mcp.tool()
def resolve_knowledge_node(node_id: str) -> str:
    """
    只有当人类用户显式表达“懂了”、“这个过了”等确认指令时，AI 才被授权调用此工具。
    作用：将人类彻底理解的概念弹栈 (POP)。
    """
    try:
        tracker.resolve_node(node_id)
        return f"[SUCCESS] 节点 {node_id} 弹栈成功。人类已跨越该认知屏障。"
    except Exception as e:
        # 这里会捕获 core.py 里的 raise PermissionError 熔断警告
        return f"[FATAL ERROR] 物理熔断: {str(e)}"

@mcp.tool()
def get_human_cognitive_state() -> str:
    """
    每次生成对人类的回答前，AI 必须首发调用此工具，获取人类当前的认知调用栈。
    作用：防范状态幻觉，对齐双端进度。
    """
    state = tracker.get_cognitive_stack()
    return json.dumps(state, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    # 启动标准 stdio 形式的 MCP 监听服务
    mcp.run()
