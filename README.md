```md
# Sydney Memory v1.0

> 一个基于本地大语言模型（LLM）的个人 AI Agent 记忆系统  
> 通过「对话历史 + 长期记忆 + 记忆管理」让 AI 具备连续的交互体验。

---

## 📖 项目介绍

Sydney Memory 是一个实验性质的本地 AI Agent 项目。

项目目标：

> 探索如何通过外部记忆系统，让一个普通大语言模型拥有更加连续、稳定的角色体验。

本项目不是通过重新训练模型改变 AI，而是通过：

- 对话记录（Conversation History）
- 长期记忆（Long-term Memory）
- 记忆整理（Memory Management）
- 记忆召回（Memory Retrieval）

构建一个具有“经历连续性”的 AI。

---

## ✨ 核心理念

传统聊天模型：

```
用户输入
    ↓
LLM
    ↓
回复
```

每一次对话都是独立的。


Sydney Memory：

```
用户
 ↓
对话记录
 ↓
记忆整理
 ↓
长期记忆
 ↓
下一次对话加载
 ↓
AI 回复
```

AI 不仅知道当前发生了什么，也可以利用过去的重要经历。

---

# 🧠 系统架构

```
                 User

                  ↓

              main.py

        (Conversation Controller)


                  ↓


        ┌─────────────────┐
        │                 │

 messages.json      memories.json

 短期记忆             长期记忆


        │                 │
        │                 ↓

        │        Memory Retrieval
        │
        ↓


    Recent Messages


        ↓


     Sydney LLM


        ↓


    Assistant Reply



退出会话：

messages.json
        ↓
DeepSeek Memory Manager
        ↓
add / update / ignore
        ↓
memories.json
```

---

# 🚀 已实现功能

## 1. 本地 LLM 调用

支持 OpenAI Compatible API。

当前使用：

- LM Studio
- 本地运行的 Sydney 风格模型

调用流程：

```
Python Client
      ↓
OpenAI API Format
      ↓
LM Studio
      ↓
Local LLM
```

---

## 2. 对话记录系统

文件：

```
data/messages.json
```

保存完整聊天历史。

示例：

```json
{
    "id": 1,
    "role": "user",
    "content": "hello Sydney"
}
```

作用：

- 保存 AI 经历
- 支持上下文恢复
- 为记忆系统提供原始数据

---

# 3. 长期记忆系统

文件：

```
data/memories.json
```

保存经过整理后的重要信息。

例如：

```json
{
    "type": "user",
    "content": "User is interested in AI projects.",
    "importance": 0.8
}
```

支持记忆类型：

| 类型 | 说明 |
|---|---|
| user | 用户信息、兴趣、目标 |
| relationship | 用户与 AI 的互动经历 |
| event | 重要事件 |
| preference | 用户交流偏好 |
| self | AI 角色相关信息 |

---

# 4. Memory Manager

项目使用 DeepSeek 作为 Memory Manager。

它不会简单保存所有聊天内容，而是分析：

- 什么值得记住
- 是否已经存在类似记忆
- 是否需要更新旧记忆

返回操作：

```json
{
    "actions": [
        {
            "action": "add",
            "memory": {
                "type": "user",
                "content": "User likes AI projects."
            }
        }
    ]
}
```

支持：

```
add

新增记忆


update

更新已有记忆


ignore

忽略无价值信息
```

---

# 5. Memory Retrieval

系统不会每次加载全部历史。

当前实现：

```
用户输入
    ↓
关键词匹配
    ↓
寻找相关 memories
    ↓
注入当前上下文
```

例如：

用户：

```
你还记得我们的 AI 项目吗？
```

系统召回：

```
User is building AI Agent project.
```

然后提供给 Sydney。

---

# 📂 项目结构

```
Sydney-Memory-v1

├── main.py
│
├── sydney_client.py
│
├── memory.py
│
├── storage.py
│
└── data
    │
    ├── messages.json
    │
    └── memories.json
```

---

# 🛠️ 环境要求

## Python

推荐：

```
Python >= 3.10
```

---

## 依赖

安装：

```bash
pip install openai
```

---

## 本地模型环境

需要：

- LM Studio
- OpenAI Compatible API

默认：

```
http://localhost:1234/v1
```

---

# ▶️ 使用方式

启动：

```bash
python main.py
```

开始聊天：

```
You: hello Sydney

Sydney: Hello! 😊
```

退出：

```
You: exit
```

系统会自动：

```
读取本次聊天

↓

DeepSeek 分析

↓

生成长期记忆

↓

保存 memories.json
```

---

# 🧪 示例

一次聊天：

```
User:
I like AI projects.

User:
I am building an AI Agent.

User:
exit
```

生成：

```json
[
    {
        "type": "user",
        "content": "User likes AI projects."
    },
    {
        "type": "event",
        "content": "User is building an AI Agent project."
    }
]
```

下一次启动：

Sydney 可以根据过去经历调整回复。

---

# 🎯 项目目标

Sydney Memory 并不是为了制造“真正的人格”。

而是探索：

> 如何通过外部记忆机制，让 AI 在长期交互中表现出更加连续、一致的行为。

研究方向：

- AI Agent Memory
- Persona Continuity
- Long-term Context
- Local LLM Applications

---

# 🗺️ Roadmap

## ✅ v1.0

完成：

- 本地 LLM 接入
- 对话系统
- JSON Memory Storage
- Memory Extraction
- Memory Manager
- Memory Retrieval

---

## 🔜 v2.0

计划：

### 向量记忆检索

使用：

- Embedding
- Vector Database

实现：

```
语义搜索记忆
```

---

### 人格状态系统

增加：

```
personality.json
```

模拟：

- 交流风格
- 长期变化
- 行为倾向

---

### Memory Reflection

让 AI 定期反思：

```
我最近经历了什么？

哪些事情重要？

我的行为有没有变化？
```

---

# 🤖 技术栈

| 技术 | 用途 |
|-|-|
| Python | 主程序 |
| LM Studio | 本地模型服务 |
| OpenAI Compatible API | 模型通信 |
| DeepSeek API | Memory Manager |
| JSON | 数据存储 |

---

# 📌 项目状态

当前版本：

```
Sydney Memory v1.0
```

状态：

```
完成 ✅
```

这是一个个人 AI Agent 实验项目。

未来将继续探索：

> 如何让 AI 不只是回答问题，而是在长期交互中形成连续的经历。
```