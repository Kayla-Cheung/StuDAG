# StuDAG (Student Directed Acyclic Graph)

> A purely human-centric cognitive interceptor. 
> Forcing LLMs to traverse your learning process, not theirs.

## 哲学 (Philosophy)

整个 AI 工业界都在疯狂构建 ToT (Tree of Thoughts) 和 LATS (Language Agent Tree Search)，试图让大语言模型在后台自己展开树、自己打分、自己回溯，最后把“最优解”喂给人类。在那些生态里，人类是被动的接收者。

**StuDAG 是一次暴力的底层反叛。**

它不为了让 AI 变聪明，而是将树的开辟权完全移交给**人类**。StuDAG 将一棵具有严格依赖约束的有向无环图（DAG）硬编码成了物理状态机，强行套在了人类的认知调用栈上。
在这里，AI 被剥夺了主观能动性，降维成一个纯粹的进度记录仪（`DAG Engine`）。

只要人类发起了对底层概念的下钻追问（入度 +1），AI 就会被物理挂起，被强制困在这个子节点中。直到人类显式宣告消化完毕（POP 弹栈），AI 才能继续推进。

拒绝大模型的线性幻觉推进。夺回你的认知控制权。

## 架构层 (Architecture)

StuDAG 以 **MCP (Model Context Protocol)** 服务器的形式存在。这使得它可以作为终极寄生组件，无缝插入 Cursor、Claude 等任何主流客户端，直接接管大模型的生成流。

- `core.py`: 纯净的图论数据结构与物理约束层。基于 `Pydantic` 强类型校验。它无情地守护着拓扑真理（子节点未解，禁止结算父节点）。
- `server.py`: MCP 协议隔离层。向 LLM 暴露 `push`、`resolve` 以及 `get_cognitive_stack` 工具，强制 LLM 在每次张嘴前必须扫描人类的进度条。
- `state_machine.json`: 本地挥发性内存，实时映射人类当前的脑容量栈（已被严格 `.gitignore` 保护）。

## 启动指南

```bash
pip install -r requirements.txt
python server.py
```

## Creator
Architected by **Kayla**.
*Systems Architect & AI Sociologist*
