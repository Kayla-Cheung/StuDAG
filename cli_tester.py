import sys
import json
from core import CognitiveTracker

tracker = CognitiveTracker()

print("="*50)
print("StuDAG 物理引擎本地测试控制台 (MVP)")
print("在这里你可以模拟 AI，亲自尝试操作调用栈。")
print("命令列表:")
print("  push <topic>   - 将一个新概念压栈 (例如: push 什么是面向对象)")
print("  pop [node_id]  - 宣告节点已消化并尝试弹栈 (默认弹栈顶节点)")
print("  state          - 查看暴露给 AI 的只读栈底试图")
print("  exit           - 退出测试台")
print("="*50)

while True:
    try:
        raw = input("\nStuDAG> ").strip()
        if not raw: continue
        
        cmd = raw.split(" ", 1)
        action = cmd[0].lower()
        arg = cmd[1] if len(cmd) > 1 else ""

        if action == "exit" or action == "quit":
            print("测试结束。")
            break
            
        elif action == "push":
            if not arg:
                print("⚠️ 请输入要压栈的概念 (topic)")
                continue
            nid = tracker.push_node(arg)
            print(f"✅ [SUCCESS] 已物理压栈！")
            print(f"   分配 ID: {nid}")
            print(f"   当前深度: {len(tracker.state.call_stack)}")
            
        elif action == "pop":
            stack = tracker.state.call_stack
            if not arg:
                if not stack:
                    print("⚠️ 调用栈当前为空，无可弹出的节点。")
                    continue
                arg = stack[-1] # 默认尝试 pop 栈顶
            
            try:
                tracker.resolve_node(arg)
                print(f"✅ [SUCCESS] 节点 {arg} 弹栈成功！人类已消化。")
            except Exception as e:
                print(f"💥 [FATAL] 物理熔断被触发！\n   报错原因: {str(e)}")
                
        elif action == "state":
            state = tracker.get_cognitive_stack()
            print("--- 暴露给大模型的物理视图 ---")
            print(json.dumps(state, indent=2, ensure_ascii=False))
            print("------------------------------")
            
        else:
            print("⚠️ 未知命令。请使用 push, pop, state, exit")
            
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"系统异常: {e}")
