# Sydney Memory v1.0

> 一个基于本地大语言模型（Local LLM）的个人 AI Agent 记忆系统  
> 通过「角色模型 + 对话历史 + 长期记忆」实现具有连续体验的 AI。

---

# 📖 项目介绍

Sydney Memory 是一个实验性的本地 AI Agent 项目。

项目目标：

> 使用外部记忆系统，让一个普通大语言模型拥有长期交互能力和角色连续性。

本项目不是重新训练模型，而是通过：

- Persona（角色设定）
- Conversation History（对话历史）
- Short-term Memory（短期记忆）
- Long-term Memory（长期记忆）
- Memory Manager（记忆管理）

构建一个具有连续经历的 AI。

---

# ✨ 核心思想

传统 LLM：

```
用户输入
   ↓
模型
   ↓
回复
```

每一次对话都是独立的。


Sydney Memory：

```
用户
 ↓
聊天记录
 ↓
记忆整理
 ↓
长期记忆
 ↓
下一次加载
 ↓
AI 回复
```

AI 不只是生成回复，而是拥有：

- 过去经历
- 用户画像
- 关系历史
- 长期偏好

---

# 🧠 系统架构

```
                    User

                     ↓

                  main.py

            (Conversation Controller)


                     ↓


        ┌─────────────────────┐
        │                     │

 messages.json          memories.json

 短期聊天记录            长期记忆


        │                     │
        │                     ↓

        │             Memory Retrieval
        │
        ↓


       Recent Messages


              ↓


          Sydney LLM


              ↓


          Response



退出聊天:

messages.json

      ↓

DeepSeek Memory Manager

      ↓

add / update / ignore

      ↓

memories.json
```

---

# 🚀 复刻方法

## 1. 克隆项目

```bash
git clone https://github.com/yourname/Sydney-Memory.git

cd Sydney-Memory
```

---

# 2. 环境准备

## Python

推荐：

```
Python >= 3.10
```

检查：

```bash
python --version
```

---

安装依赖：

```bash
pip install openai
```

---

# 3. 下载 Sydney 模型

本项目使用：

## Sydney 风格 Llama 模型

推荐：

### Hugging Face

模型：

```
Llama-3-8B-Sydney
```

下载地址：

```
https://huggingface.co/
```

搜索：

```
Llama-3-8B-Sydney GGUF
```

推荐格式：

```
GGUF
```

原因：

- 支持 LM Studio
- 支持 Ollama
- 本地部署方便

---

# 4. 安装 LM Studio

官网：

```
https://lmstudio.ai/
```

安装后：

打开：

```
LM Studio
        ↓
Models
        ↓
Load Model
```

加载：

```
Llama-3-8B-Sydney-GGUF
```

---

# 5. 开启本地 API 服务


LM Studio:

```
Developer
   ↓
Start Server
```


默认地址：

```
http://localhost:1234/v1
```


测试：

```bash
curl http://localhost:1234/v1/models
```

如果返回模型列表：

说明成功。

---

# 6. 配置 Sydney Client


`sydney_client.py`

修改：

```python
BASE_URL = "http://localhost:1234/v1"
```

模型名称：

修改为 LM Studio 中显示的模型名。


例如：

```python
model="llama-3-8b-sydney"
```

---

# 7. 配置 DeepSeek Memory Manager


项目使用 DeepSeek API 负责：

- 分析聊天
- 提取长期记忆
- 判断新增/更新/忽略


申请：

```
https://platform.deepseek.com/
```


配置 API Key：

例如：

```python
DEEPSEEK_API_KEY="your_key"
```

---

# 8. 初始化运行


启动：

```bash
python main.py
```


第一次运行会生成：

```
data/

├── messages.json

└── memories.json
```

---

# 💬 使用示例


输入：

```
You:
hello Sydney
```


Sydney:

```
Hello! 😊
```


聊天结束：

```
You:
exit
```


系统执行：

```
读取本次聊天

        ↓

DeepSeek 分析

        ↓

Memory Manager

        ↓

保存 memories.json
```

---

# 📂 项目结构

```
Sydney-Memory-v1

│
├── main.py

│
├── sydney_client.py

│
├── memory.py

│
├── storage.py

│
└── data

    ├── messages.json

    └── memories.json
```

---

# 📌 文件说明


## main.py

负责：

- 用户输入
- 对话流程
- 上下文组合
- Memory 调用


---

## sydney_client.py

负责：

- 调用本地 LLM
- OpenAI Compatible API


---

## storage.py

负责：

JSON 数据管理：

- 保存消息
- 读取消息
- 保存记忆
- 更新记忆
- 记忆检索


---

## memory.py

负责：

Memory Manager。


流程：

```
聊天记录

↓

DeepSeek

↓

Memory Actions

↓

add

update

ignore
```

---

# 🧠 Memory 系统


## messages.json

保存：

> AI 经历过什么


例如：

```json
{
"id":1,
"role":"user",
"content":"I like AI projects."
}
```


---

## memories.json

保存：

> 什么值得长期记住


例如：

```json
{
"type":"user",
"content":"User likes AI projects.",
"importance":0.8
}
```

---

# Memory 类型


| 类型 | 作用 |
|-|-|
| user | 用户信息 |
| relationship | 用户与 AI 的互动 |
| event | 重要事件 |
| preference | 用户偏好 |
| self | AI角色相关信息 |


---

# 🔄 Memory Manager 工作流程


输入：

```
Conversation

+

Existing Memories
```


DeepSeek 判断：


## add

新增：

```json
{
"action":"add"
}
```


---

## update

更新：

```json
{
"action":"update"
}
```


---

## ignore

忽略：

```json
{
"action":"ignore"
}
```


---

# 🎯 示例


用户：

```
I like AI projects.
```

Memory Manager：

生成：

```json
{
"type":"user",
"content":"User likes AI projects."
}
```


之后：

用户：

```
I am building an AI Agent.
```


系统可以更新：

```json
{
"content":
"User likes AI projects and is building AI Agents."
}
```

---

# 🛠️ 技术栈


| 技术 | 用途 |
|-|-|
| Python | 主程序 |
| LM Studio | 本地模型运行 |
| Llama GGUF | Sydney模型 |
| DeepSeek API | Memory Manager |
| JSON | 数据存储 |
| OpenAI API Format | 模型通信 |


---

# 🗺️ Roadmap


## ✅ v1.0

完成：

- 本地 LLM 接入
- Sydney Persona
- 对话系统
- JSON Memory
- Memory Manager
- Memory Retrieval


---

## 🔜 v2.0

计划：

### 向量记忆

加入：

- Embedding
- Vector Database
- Semantic Search


实现：

```
根据语义寻找过去经历
```


---

### 人格状态系统

增加：

```
personality.json
```


模拟：

- 交流风格变化
- 长期行为倾向


---

### Reflection Loop

让 AI 定期总结：

```
我最近经历了什么？

哪些事情重要？

我的行为是否发生变化？
```


---

# ⭐ 项目愿景

Sydney Memory 并不是为了制造真正的人格。

而是探索：

> 如何通过记忆系统，让 AI 在长期交互中形成更加连续、一致的行为表现。

未来方向：

- Personal AI Agent
- AI Memory Architecture
- Local LLM Applications
- Long-term Human AI Interaction
```