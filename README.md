# StuDAG (Student Directed Acyclic Graph)

[English](#english) | [简体中文](#简体中文)

---

<h2 id="english">English</h2>

An external working-memory prosthetic for ADHD learners.

### The Core Problem: Context Drift
When you use an LLM (like ChatGPT or Claude) to learn a complex topic, you usually fall into the **Context Drift Trap**:

- **Without StuDAG**: You ask "How does a CPU work?" The AI mentions "Transistors". You ask "What is a Transistor?" The AI explains it, then segues into semiconductor physics, then the history of Silicon Valley... 30 minutes later, your working memory is overloaded, and you've completely forgotten you were trying to learn about CPUs. The learning session is ruined.

LLMs are linear conversationalists. They blindly follow your ADHD hyperfocus down infinite rabbit holes.

### The Solution: A Physical Cognitive Graph
StuDAG fixes this by stripping the LLM of its conversational freedom and forcing it to act as a strict **Directed Acyclic Graph (DAG) State Machine**. 

It provides you with a physical, interactive visual dashboard that tracks your cognitive stack.

- **With StuDAG**: 
  1. You ask "How does a CPU work?" (Node A is created on your dashboard). 
  2. You ask about "Transistors". The AI is forced to `push` Node B. The AI's context is now physically restricted to ONLY explaining Node B.
  3. Once you understand Node B, you double-click it on your dashboard to `pop` it.
  4. The system physically forces the AI to drag your attention back to Node A. 

No more drifting. No more cognitive overload. You maintain absolute control over your learning topology.

### Architecture
StuDAG uses the Model Context Protocol (MCP) server architecture.

- `core.py`: The DAG state machine layer (Pydantic). Enforces topological constraints: a parent node cannot be resolved before its children.
- `server.py`: The MCP interface. Exposes `push`, `resolve`, and `get_state` tools to the LLM.
- `dashboard.py`: A FastAPI backend that streams real-time physical state to a Web UI.
- `index.html`: The interactive visual frontend (vis-network) for human-in-the-loop control.

### Usage
```bash
git clone https://github.com/Kayla-Cheung/StuDAG.git
cd StuDAG
pip install -r requirements.txt

# 1. Run the interactive web dashboard (Recommended)
python dashboard.py
# Then open http://localhost:8080 in your browser

# 2. Start the MCP server (for Claude/Cursor integration)
python server.py

# 3. Or run the local terminal tester
python cli_tester.py
```

### MCP Client Integration

To use StuDAG in an AI client (like Claude Desktop or Cursor), add it to your MCP configuration:

**Claude Desktop (`claude_desktop_config.json`):**
```json
{
  "mcpServers": {
    "StuDAG": {
      "command": "python",
      "args": [
        "/absolute/path/to/StuDAG/server.py"
      ]
    }
  }
}
```

**Cursor:**
Go to `Cursor Settings > Features > MCP` and add a new server:
- Type: `command`
- Name: `StuDAG`
- Command: `python /absolute/path/to/StuDAG/server.py`

---

<h2 id="简体中文">简体中文</h2>

专为 ADHD 学习者设计的外部“工作记忆”义肢。

### 核心痛点：认知漂移 (Context Drift)
当你使用大模型学习复杂知识时，通常会陷入致命的**发散陷阱**：

- **没有 StuDAG 时**：你问“CPU是怎么工作的？” AI 提到了“晶体管”。你顺口问“什么是晶体管？” AI 解释完后，开始顺着话头聊半导体物理、甚至硅谷的历史…… 半小时后，你的短时工作记忆彻底溢出，你完全忘了最初其实是在学 CPU。学习主线全面崩溃。

大模型会盲目迎合 ADHD 极易涣散的注意力，带着你一路走进死胡同。

### 解决方案：物理强制认知树
StuDAG 的做法是：剥夺大模型的自由对话权，把它降维成一个极度死板的 **有向无环图（DAG）状态机**。

它为你提供了一个动态生成的“可视化认知监控大屏”。

- **接入 StuDAG 后**：
  1. 你问“CPU工作原理”。（监控大屏上自动建立节点 A）。
  2. 你追问“晶体管”。AI 必须调用工具 `push` 节点 B。此时，AI 会被系统强行剥夺对节点 A 的记忆，**只准**解释节点 B。
  3. 当你彻底搞懂了，在屏幕上双击节点 B 宣告“已消化（Pop）”。
  4. 系统底层物理介入，发出强指令，强迫 AI 主动把你的注意力拽回遗忘的节点 A（CPU工作原理）。

彻底切断上下文漂移。让机器替你承担最耗费精力的“执行功能（Executive Function）”。

### 系统架构
StuDAG 采用 Model Context Protocol (MCP) 服务器架构，直接拦截 LLM 的生成流。

- `core.py`: DAG 状态机层 (基于 Pydantic)。执行物理拓扑约束：子节点未解决前，绝对禁止跨级结算父节点。
- `server.py`: MCP 协议接口层。暴露 `push`、`resolve` 和 `get_state`，强制大模型按图谱流转。
- `dashboard.py`: FastAPI 后端，负责向前端实时同步底层的拓扑状态机。
- `index.html`: 可视化交互大屏。把状态机变为人类可以直接双击操作的控制台。

### 启动指南
```bash
git clone https://github.com/Kayla-Cheung/StuDAG.git
cd StuDAG
pip install -r requirements.txt

# 1. 启动全栈可视化监控大屏（推荐）
python dashboard.py
# 然后用浏览器打开 http://localhost:8080

# 2. 启动 MCP 服务器拦截网 (用于接入 Claude/Cursor)
python server.py

# 3. 启动本地命令行交互测试台
python cli_tester.py
```

### MCP 客户端接入指南

要在真实的 AI 客户端（如 Claude Desktop 或 Cursor）中激活此拦截网，请将其配置为 MCP Server：

**Claude Desktop (`claude_desktop_config.json`):**
```json
{
  "mcpServers": {
    "StuDAG": {
      "command": "python",
      "args": [
        "绝对路径/StuDAG/server.py"
      ]
    }
  }
}
```

**Cursor:**
前往 `Cursor Settings > Features > MCP` 添加新服务器：
- Type: `command`
- Name: `StuDAG`
- Command: `python 绝对路径/StuDAG/server.py`

---

## Creator
Kayla
