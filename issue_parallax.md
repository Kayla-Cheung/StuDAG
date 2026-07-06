---
title: "Architecture: Parallax Cognitive Dimensions (视差认知空间)"
labels: ["enhancement", "architecture", "epistemology"]
assignees: ["Kayla-Cheung"]
---

## 1. 视差哲学 (The Parallax Philosophy)
当前的 DAG 物理引擎呈现的是一个**单线程、扁平化**的知识解构路径（父节点 -> 子节点）。
但在真实的深度认知（尤其对于 ADHD 发散性学习者）中，知识不是树状的，而是**全息的（Holographic）**。
同一个概念，必须通过多视角的“视差（Parallax）”对齐，才能形成真正的物理理解。

比如 `CPU`:
- **Parallax 1 (Physics)**: 晶体管与半导体掺杂
- **Parallax 2 (Architecture)**: 指令集与流水线
- **Parallax 3 (Sociology/History)**: 仙童半导体与摩尔定律

## 2. 核心痛点
目前大模型在 `push_node` 时，只能提供单调的 `topic`。如果它同时推入多个不同维度的视差，在现有的 2D 图谱上会显得混乱不堪，且无法体现“它们其实是同一个物体的不同侧面”这一空间关系。

## 3. 架构演进方案 (Proposed Architecture)

### 3.1 后端引擎层 (DAG Engine)
需要扩展 `Node` 的物理模型，引入 `parallax_layer` 维度。
```python
class Node(BaseModel):
    id: str
    topic: str
    parent_id: Optional[str]
    status: str = "pending"
    parallax_layer: str = "core"  # e.g., 'physics', 'math', 'philosophy'
```

### 3.2 大模型网关层 (MCP Membrane)
强制大模型在压栈时，不仅要进行概念分解，还要**进行空间视差映射**：
```python
class PushRequest(BaseModel):
    topic: str
    parent_id: Optional[str]
    parallax_layer: str 
```

### 3.3 前端物理渲染层 (Glassmorphism UI)
*   **空间折叠**：在网页端引入 2.5D 或 3D 分层概念（利用 `vis.js` 的 group 物理隔离，或引入 Three.js 驱动空间图谱）。
*   **视差切换**：用户可以通过快捷键（比如 `Tab` 或 `Space`），像切换滤镜一样，在一张图谱上快速切换不同的 Parallax 视角。

## 4. 交付验收标准 (PoW)
1.  [ ] `core.py` 支持 Parallax Meta-data。
2.  [ ] `server.py` MCP 协议更新，要求 LLM 生成多视差节点。
3.  [ ] `index.html` 支持基于视差的过滤与物理着色（不同 Parallax 使用不同的极客高亮色）。
