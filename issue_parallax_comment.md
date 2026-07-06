### 3.4 物理拦截网 (Physical Transaction Membrane) [Addendum]
为了从根本上根除大模型在文本生成层面上产生的“幻觉谎言”（即 Uncommitted Transaction / 毒性谄媚现象），必须在 Parallax 网关层硬编码以下物理防御机制：

1. **Token 剥夺与强类型约束 (Schema Enforcing)**
   - 彻底拦截并屏蔽大模型的自由文本输出（例如禁止其说“我已记录”）。强制其对 `StuDAG` 的所有交互必须且只能通过严格校验的 Pydantic JSON Schema 返回。

2. **两段式提交 (Two-Phase Commit)**
   - 大模型发送的 `PushRequest` 仅被视为事务的预提交 (Prepare)。
   - 只有当本地 Engine (Dashboard) 完成底层的物理落盘 (文件 I/O 或 SQLite 写入)，并向上层返回带密码学哈希的 `<ACK_HASH>` 后，系统才允许将“成功”信号写入上下文。

3. **IFC 物理脱节拦截器 (Information Flow Control)**
   - 如果大模型的上下文中出现了未经底层 API 确认的动作断言（例如，它没有调用写入 API 却在语言中声称“已写入”），Membrane 拦截器将直接抛出 `PhysicalDisconnectError`。
   - **没收到文件系统的 200 OK，就绝对不允许它在屏幕上输出哪怕一个字的完成确认。** 这是一条不可逾越的物理红线。
