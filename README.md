# StuDAG (Student Directed Acyclic Graph)

[English](#english) | [简体中文](#简体中文)

---

<h2 id="english">English</h2>

An external working-memory prosthetic for ADHD learners.

### Problem
Standard LLMs act as linear conversationalists. This actively worsens the core ADHD learning constraint: **Call Stack Loss**.

When an ADHD user encounters a new concept, they branch out into sub-questions (Hyperfocus). The LLM blindly follows them down this rabbit hole. By depth 5, the user's working memory overflows, and they completely forget the original root topic. The learning session derails.

### Solution
StuDAG forces the LLM to abandon linear chat and operate as a strict **Directed Acyclic Graph (DAG) Engine**. 

It offloads the user's executive function into a physical JSON state machine. The AI is no longer a conversational partner; it is a rigid progress tracker.

1. **Push (Branching)**: When the user asks a foundational question, StuDAG pushes a sub-node onto the call stack. The AI is forced to isolate its context to this specific node.
2. **Pop (Backtracking)**: When the user signals comprehension, the AI cannot randomly pivot. It must `POP` the stack and forcefully drag the user's attention back to the exact parent node they left behind.

### Architecture
StuDAG uses the Model Context Protocol (MCP) server architecture.

- `core.py`: The DAG state machine layer (Pydantic). Enforces topological constraints: a parent node cannot be resolved before its children.
- `server.py`: The MCP interface. Exposes `push`, `resolve`, and `get_state` tools to the LLM.
- `state_machine.json`: Physical local storage mapping the user's active call stack.

### Usage
```bash
git clone https://github.com/Kayla-Cheung/StuDAG.git
cd StuDAG
pip install -r requirements.txt

# Start the MCP server
python server.py

# Or run the local interactive tester
python cli_tester.py
```

---

<h2 id="简体中文">简体中文</h2>

专为 ADHD 学习者设计的外部“工作记忆”义肢。

### 核心痛点
主流大语言模型（LLM）的本质是线性对话。这恰恰加剧了 ADHD 人群在学习时的核心缺陷：**调用栈迷失（Call Stack Loss）**。

当 ADHD 用户遇到新概念时，往往会不受控地发散出无数子问题（Hyperfocus 状态）。LLM 会盲目地顺着这个发散分支聊下去。当嵌套深度达到 5 层时，用户的工作记忆早已溢出，彻底遗忘了最初的根问题。学习进程全面崩溃。

### 解决方案
StuDAG 强制剥夺了 LLM 的闲聊能力，将其降维成一个极度死板的 **有向无环图（DAG）引擎**。

它将用户的“执行功能”物理外包给了一个 JSON 状态机。AI 不再是对话伙伴，而是一个冷酷的进度追踪器：

1. **Push (压栈锁定)**: 当用户追问前置概念时，StuDAG 在调用栈压入一个子节点。AI 被强制锁定在该节点的上下文中，禁止提及主干。
2. **Pop (强制回溯)**: 当用户宣告理解，AI 无法自由发散。它必须执行弹栈（POP），并强制将用户的注意力拽回上一个悬而未决的父节点。

### 系统架构
StuDAG 采用 Model Context Protocol (MCP) 服务器架构，直接拦截 LLM 的生成流。

- `core.py`: DAG 状态机层 (基于 Pydantic)。执行物理拓扑约束：子节点未解决前，绝对禁止跨级结算父节点。
- `server.py`: MCP 协议接口层。暴露 `push`、`resolve` 和 `get_state`，强制 LLM 在每次生成回复前读取用户的认知栈底。
- `state_machine.json`: 物理存储用户当前调用栈的本地状态库（已在版本控制中隔离）。

### 启动指南
```bash
git clone https://github.com/Kayla-Cheung/StuDAG.git
cd StuDAG
pip install -r requirements.txt

# 启动 MCP 服务器拦截网
python server.py

# 或者启动本地交互测试台
python cli_tester.py
```

---

## Creator
Kayla
