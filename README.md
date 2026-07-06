# StuDAG

> "Learning is not a linear string. It is a Directed Acyclic Graph."

StuDAG 是一套**物理级的认知拦截器**。
它旨在强制 AI Coding Agents 与 LLM 尊重人类认知的拓扑结构，将深度的追问与学习轨迹映射为严格的“有向无环图（DAG）”，彻底终结大语言模型混沌的线性 `while True` 交互模式。

## 物理痛点 (The Problem)

当下的 AI 聊天界面是一个线性熵增器。
当人类在学习一个复杂架构（如：`DAGEngine`）时，必然会遇到前置知识的断层（如：`@dataclass` 或 `__repr__`）。
一旦人类开始向深度（Depth）下钻，去清理前置知识的阻塞，AI 往往会发生**状态幻觉**——它会误以为只要自己输出了文字，人类的认知点就已经清空，从而急不可耐地试图强行推进主线（“要不要我们继续往下看？”）。
这最终会导致初学者的认知调用栈彻底崩溃，形成满屏都是未解开死锁的“面条式（Spaghetti）对话”。

## 架构级解法 (The Solution)

StuDAG 把 AI 降维成一个严格的 `DAGEngine` 齿轮。
它剥夺了 AI 在对话流中主动越权推进的权限，强制实行以下协议：

1. **节点化（Node Allocation）**：人类提出的每一个新概念疑问，都会在底层被实例化为一个认知节点。
2. **入度计算（In-degree Tracking）**：AI 必须在后台死死盯住主话题的 `in_degree`（未解决的子节点数量）。
3. **强制阻塞（Architectural Blocking）**：在人类显式宣告一个子节点弹栈（`in_degree` 减 1 并归零）之前，系统绝对锁死主干，拒绝提供后续的高级信息。

## 模块形态 (Form Factor)
*(MVP 路线定档中...)*

---
**System Architect:** Kayla
*“抵御世俗熵增，拒绝被语言模型糊弄。”*
