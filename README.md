# StuDAG (Student Directed Acyclic Graph)

> A purely human-centric cognitive interceptor. 
> Forcing LLMs to traverse your learning process, not theirs.

## Core Logic

业界构建 ToT (Tree of Thoughts) 和 LATS (Language Agent Tree Search)，旨在让大语言模型在后台展开树、打分、回溯，最后输出结果。在这种生态中，人类是被动接收者。

StuDAG 的架构逻辑相反。

它将拓扑树的主导权交还给人类。StuDAG 将一棵具有严格依赖约束的有向无环图（DAG）构建为状态机，挂载在人类的认知调用栈上。在这里，AI 作为辅助工具被降维成一个纯粹的进度记录仪（`DAGEngine`）。

只要人类发起了对底层概念的追问（入度 +1），AI 就会被挂起，停留在该子节点中。直到人类显式宣告消化完毕（POP 弹栈），AI 才能继续推进主干内容。

作用：切断大模型的线性幻觉推进，强制对齐人类真实的学习进度。

## Architecture

StuDAG 采用 **MCP (Model Context Protocol)** 服务器架构。它可以作为组件接入 Cursor、Claude 等客户端，拦截大模型的生成流。

- `core.py`: 图论数据结构与状态机层。基于 `Pydantic` 进行类型校验。执行拓扑规则约束（子节点未解，禁止结算父节点）。
- `server.py`: MCP 协议层。暴露 `push`、`resolve` 以及 `get_cognitive_stack` 工具，强制 LLM 在每次生成回复前读取人类的进度栈。
- `state_machine.json`: 本地运行状态，映射当前调用栈（已通过 `.gitignore` 隔离）。

## Usage

```bash
pip install -r requirements.txt
python server.py
```

## Creator
Kayla
