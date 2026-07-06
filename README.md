# StuDAG (Student Directed Acyclic Graph)

An external working-memory prosthetic for ADHD learners.

## Problem

Standard LLMs act as linear conversationalists. This actively worsens the core ADHD learning constraint: **Call Stack Loss**.

When an ADHD user encounters a new concept, they branch out into sub-questions (Hyperfocus). The LLM blindly follows them down this rabbit hole. By depth 5, the user's working memory overflows, and they completely forget the original root topic. The learning session derails.

## Solution

StuDAG forces the LLM to abandon linear chat and operate as a strict **Directed Acyclic Graph (DAG) Engine**. 

It offloads the user's executive function into a physical JSON state machine. The AI is no longer a conversational partner; it is a rigid progress tracker.

1. **Push (Branching)**: 当用户追问前置概念时，StuDAG 在调用栈压入一个子节点。AI 被强制锁定在该节点的上下文中。
2. **Pop (Backtracking)**: 当用户宣告理解，AI 无法自由发散。它必须执行弹栈（POP），并强制将用户的注意力拽回上一个悬而未决的父节点。

## Architecture

StuDAG 采用 Model Context Protocol (MCP) 服务器架构，拦截 LLM 的生成流。

- `core.py`: DAG 状态机层 (Pydantic)。执行拓扑约束：子节点未解决前，禁止跨级结算父节点。
- `server.py`: MCP 接口层。暴露 `push`、`resolve` 和 `get_state`，强制 LLM 在每次生成回复前读取用户的认知栈底。
- `state_machine.json`: 物理存储用户当前调用栈的本地状态库。

## Usage

```bash
pip install -r requirements.txt
python server.py
```

## Creator
Kayla
